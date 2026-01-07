from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Pooja:
    id: str
    name: str
    intents: List[str]
    tags: List[str]
    description: str
    benefits: List[str]
    materials: List[str]
    steps: List[str]
    duration_minutes: int
    price_inr: int
    cities: List[str]
    scriptural_refs: List[str] = field(default_factory=list)
    language: str = "en"


@dataclass
class Recommendation:
    pooja: Pooja
    score: float
    reason: str
    language: str


@dataclass
class ConversationTurn:
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None


@dataclass
class QueryContext:
    user_issue: str
    city: Optional[str] = None
    language: str = "en"
    budget_inr: Optional[int] = None
    preferred_deity: Optional[str] = None
    conversation_history: List[ConversationTurn] = field(default_factory=list)
    user_id: Optional[str] = None  # For multi-turn tracking
