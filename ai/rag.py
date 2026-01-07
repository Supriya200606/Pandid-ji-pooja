from __future__ import annotations

import json
import math
import re
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from ai.config import Settings
from ai.context import IntentExtractor
from ai.guardrails import SafetyChecker
from ai.llm import LLMClient
from ai.models import Pooja, QueryContext, Recommendation
from ai.prompting import build_recommendation_prompt

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover
    SentenceTransformer = None  # type: ignore


WORD_RE = re.compile(r"[a-zA-Z]+")


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in WORD_RE.findall(text)]


def _jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    set_a = set(a)
    set_b = set(b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


class PoojaRecommender:
    def __init__(self, settings: Settings, llm: Optional[LLMClient] = None):
        self.settings = settings
        self.llm = llm
        self._poojas: List[Pooja] = []
        self._embeddings: List[List[float]] = []
        self._embedder = None
        if SentenceTransformer and settings.embedding_model:
            self._embedder = SentenceTransformer(settings.embedding_model)

    def load_data(self, path: Optional[Path] = None) -> None:
        data_path = path or self.settings.data_path
        with open(data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._poojas = [Pooja(**item) for item in raw]
        self._build_index()

    def _build_index(self) -> None:
        self._embeddings.clear()
        if self._embedder:
            texts = [self._pooja_text(p) for p in self._poojas]
            self._embeddings = self._embedder.encode(texts, convert_to_numpy=False)
        else:
            # Fallback: store token lists for Jaccard scoring
            self._embeddings = [_tokenize(self._pooja_text(p)) for p in self._poojas]

    def _pooja_text(self, pooja: Pooja) -> str:
        return " ".join([
            pooja.name,
            " ".join(pooja.tags),
            " ".join(pooja.intents),
            pooja.description,
            " ".join(pooja.benefits),
        ])

    def _encode(self, text: str):
        if self._embedder:
            return self._embedder.encode([text], convert_to_numpy=False)[0]
        return _tokenize(text)

    def _similarity(self, a, b) -> float:
        if self._embedder:
            # Cosine similarity
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(x * x for x in b))
            if norm_a == 0 or norm_b == 0:
                return 0.0
            score = dot / (norm_a * norm_b)
            # Convert Tensor to float if needed
            return float(score) if hasattr(score, 'item') else float(score)
        return _jaccard(a, b)

    def search(self, query: str, top_k: Optional[int] = None) -> List[Tuple[Pooja, float]]:
        if not self._poojas:
            raise ValueError("Pooja catalog is empty. Call load_data() first.")
        q_emb = self._encode(query)
        scores: List[Tuple[Pooja, float]] = []
        for pooja, emb in zip(self._poojas, self._embeddings):
            score = self._similarity(q_emb, emb)
            scores.append((pooja, score))
        # Filter by minimum relevance threshold
        filtered = [(p, s) for p, s in scores if s >= self.settings.min_relevance_score]
        top_n = top_k or self.settings.top_k
        return sorted(filtered, key=lambda x: x[1], reverse=True)[:top_n]

    def recommend(self, ctx: QueryContext) -> List[Recommendation]:
        # Safety check
        is_safe, safety_msg = SafetyChecker.check_query(ctx.user_issue)
        if not is_safe:
            return []  # Return empty to signal unsafe query; caller should use safety_msg
        
        ranked = self.search(ctx.user_issue)
        recs: List[Recommendation] = []
        for pooja, score in ranked:
            reason = self._build_reason(pooja, ctx)
            recs.append(
                Recommendation(
                    pooja=pooja,
                    score=round(score, 3),
                    reason=reason,
                    language=ctx.language,
                )
            )
        return recs

    def _build_reason(self, pooja: Pooja, ctx: QueryContext) -> str:
        base = f"Aligned with intents {pooja.intents} and tags {pooja.tags}."
        if ctx.city and ctx.city.lower() in [c.lower() for c in pooja.cities]:
            base += f" Available in {ctx.city}."
        if ctx.budget_inr and pooja.price_inr <= ctx.budget_inr:
            base += f" Within your budget (₹{pooja.price_inr})."
        if ctx.preferred_deity:
            deity_match = any(d.lower() in pooja.description.lower() or d.lower() in pooja.name.lower() 
                            for d in ctx.preferred_deity.split(","))
            if deity_match:
                base += f" Invokes {ctx.preferred_deity}."
        if self.llm:
            prompt = build_recommendation_prompt(ctx.user_issue, pooja, ctx.language)
            try:
                return self.llm.generate(prompt)
            except Exception:
                return base
        return base

    def to_jsonable(self, recs: List[Recommendation]) -> List[Dict]:
        return [
            {
                "pooja": asdict(r.pooja),
                "score": r.score,
                "reason": r.reason,
                "language": r.language,
            }
            for r in recs
        ]
