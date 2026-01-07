from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Tuple


class GeneralQAEngine:
    """Handles general spiritual Q&A beyond pooja recommendations."""

    def __init__(self, qa_path: Optional[Path] = None):
        self.qa_data = []
        if qa_path is None:
            qa_path = Path(__file__).resolve().parent / "sample_data" / "general_qa.json"
        self.load_qa(qa_path)

    def load_qa(self, path: Path) -> None:
        """Load Q&A knowledge base."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.qa_data = data.get("general_qa", [])

    def is_general_question(self, query: str) -> bool:
        """Check if query is a general (non-pooja) question."""
        general_keywords = [
            "what is", "how to", "when", "why", "explain",
            "tell me", "define", "meaning", "difference",
            "can", "should", "prepare", "best way",
            "mantra", "yoga", "meditation", "tantra",
            "karma", "dharma", "bhakti", "dosha",
        ]
        query_lower = query.lower()
        return any(kw in query_lower for kw in general_keywords)

    def search_qa(self, query: str) -> Optional[Tuple[str, str]]:
        """Search Q&A database for matching answer."""
        query_lower = query.lower()
        best_match = None
        match_score = 0

        for qa in self.qa_data:
            keywords = qa.get("keywords", [])
            score = sum(1 for kw in keywords if kw in query_lower)

            if score > match_score:
                match_score = score
                best_match = qa

        if best_match and match_score > 0:
            return best_match.get("question"), best_match.get("answer")

        return None

    def answer(self, query: str) -> Optional[str]:
        """Get answer for a general question."""
        if not self.is_general_question(query):
            return None

        result = self.search_qa(query)
        if result:
            _, answer = result
            return answer

        # Fallback for unmatched but general questions
        return (
            "That's a great spiritual question! While I don't have a specific answer in my "
            "knowledge base, I recommend:\n\n"
            "1. Consulting with an experienced spiritual teacher or guru\n"
            "2. Reading authentic Hindu scriptures (Bhagavad Gita, Upanishads, Puranas)\n"
            "3. Visiting a local temple and speaking with the priest\n\n"
            "In the meantime, would you like pooja recommendations for any specific intent?"
        )

    def get_related_qa(self, keyword: str, limit: int = 3) -> list:
        """Get related Q&A entries for a keyword."""
        keyword_lower = keyword.lower()
        matches = [
            qa for qa in self.qa_data
            if keyword_lower in [kw.lower() for kw in qa.get("keywords", [])]
        ]
        return matches[:limit]
