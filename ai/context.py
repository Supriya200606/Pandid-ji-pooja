from __future__ import annotations

from typing import Dict, List, Optional
from datetime import datetime

from ai.models import ConversationTurn, QueryContext


class ConversationManager:
    """Manages multi-turn conversation context and state."""

    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.sessions: Dict[str, List[ConversationTurn]] = {}

    def add_turn(self, user_id: str, role: str, content: str) -> None:
        """Add a turn to the conversation history."""
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        turn = ConversationTurn(
            role=role,
            content=content,
            timestamp=datetime.utcnow().isoformat(),
        )
        self.sessions[user_id].append(turn)
        # Keep history size under control
        if len(self.sessions[user_id]) > self.max_history:
            self.sessions[user_id] = self.sessions[user_id][-self.max_history:]

    def get_history(self, user_id: str) -> List[ConversationTurn]:
        """Retrieve conversation history for a user."""
        return self.sessions.get(user_id, [])

    def summarize_history(self, user_id: str) -> str:
        """Create a brief text summary of conversation history for context."""
        history = self.get_history(user_id)
        if not history:
            return ""
        summary_lines = []
        for turn in history[-5:]:  # Last 5 turns
            prefix = "User:" if turn.role == "user" else "Assistant:"
            summary_lines.append(f"{prefix} {turn.content[:100]}")
        return "\n".join(summary_lines)

    def enrich_context(self, ctx: QueryContext, user_id: str) -> QueryContext:
        """Enrich context with conversation history."""
        ctx.user_id = user_id
        ctx.conversation_history = self.get_history(user_id)
        return ctx

    def clear_session(self, user_id: str) -> None:
        """Clear a user's session."""
        if user_id in self.sessions:
            del self.sessions[user_id]


class IntentExtractor:
    """Extract structured intent and parameters from free-text queries."""

    # Map of intent keywords to standard intent names
    INTENT_KEYWORDS = {
        "health": ["health", "healing", "wellness", "disease", "pain", "sick"],
        "wealth": ["wealth", "money", "business", "trade", "profit", "commerce"],
        "marriage": ["marriage", "wedding", "relationship", "love", "harmony"],
        "career": ["career", "job", "promotion", "work", "success", "business"],
        "education": ["education", "exam", "study", "learning", "knowledge"],
        "protection": ["protection", "safety", "shield", "harm", "negative"],
        "family": ["family", "children", "kid", "daughter", "son"],
        "prosperity": ["prosperity", "abundance", "fortune", "luck"],
        "graha dosha": ["graha", "planet", "planetary", "doshas", "astrology"],
    }

    @staticmethod
    def extract(user_issue: str) -> List[str]:
        """Extract intents from user query."""
        query_lower = user_issue.lower()
        extracted = []
        for intent, keywords in IntentExtractor.INTENT_KEYWORDS.items():
            if any(kw in query_lower for kw in keywords):
                if intent not in extracted:
                    extracted.append(intent)
        return extracted if extracted else ["general"]

    @staticmethod
    def extract_city(user_issue: str) -> Optional[str]:
        """Simple city extraction (can be enhanced with NER)."""
        cities = ["delhi", "mumbai", "bengaluru", "pune", "hyderabad", "jaipur",
                  "kolkata", "chennai", "indore", "nagpur", "lucknow", "varanasi",
                  "ujjain", "ayodhya", "tirupati", "surat", "assam", "nashik"]
        query_lower = user_issue.lower()
        for city in cities:
            if city in query_lower:
                return city.capitalize()
        return None
