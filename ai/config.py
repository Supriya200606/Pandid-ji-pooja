from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    data_path: Path = Path(__file__).resolve().parent / "sample_data" / "poojas.json"
    top_k: int = 2
    llm_provider: str = os.getenv("LLM_PROVIDER", "")
    llm_model: str = os.getenv("LLM_MODEL", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    min_relevance_score: float = 0.1  # Lowered for more lenient matching


def load_settings() -> Settings:
    return Settings()
