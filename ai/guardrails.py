from __future__ import annotations

import re
from typing import Tuple


class SafetyChecker:
    """Guardrails for respectful, safe responses."""

    # Keywords that indicate potentially harmful or out-of-scope requests
    FORBIDDEN_KEYWORDS = [
        "curse", "black magic", "voodoo", "harm", "kill", "death", "suicide",
        "abuse", "violence", "hate", "discrimination", "illegal",
    ]

    # Keywords that should defer to medical/legal professionals
    DEFER_KEYWORDS = [
        "medical", "doctor", "hospital", "surgery", "medication",
        "lawyer", "court", "legal",
    ]

    # Respectful tone enforcement
    DISRESPECTFUL_TERMS = [
        "fake", "fraud", "scam", "stupid", "useless",
    ]

    @staticmethod
    def check_query(user_query: str) -> Tuple[bool, str]:
        """
        Validate user query for safety and appropriateness.
        Returns: (is_safe: bool, message: str)
        """
        query_lower = user_query.lower()

        # Check for forbidden content (word-boundary matching)
        for keyword in SafetyChecker.FORBIDDEN_KEYWORDS:
            if re.search(rf"\b{keyword}\b", query_lower):
                return False, (
                    "I cannot assist with that request. Spiritual practices are meant to "
                    "bring peace and harmony. If you're in distress, please reach out to "
                    "a mental health professional or trusted community member."
                )

        # Check for defer-to-expert keywords (word-boundary matching)
        for keyword in SafetyChecker.DEFER_KEYWORDS:
            if re.search(rf"\b{keyword}\b", query_lower):
                return False, (
                    "For medical or legal matters, I recommend consulting with a qualified "
                    "professional. Spiritual practices complement, but do not replace, "
                    "professional guidance."
                )

        # Check for disrespectful tone (word-boundary matching)
        for term in SafetyChecker.DISRESPECTFUL_TERMS:
            if re.search(rf"\b{term}\b", query_lower):
                return False, (
                    "Let's maintain a respectful tone. I'm here to help you find authentic "
                    "spiritual practices aligned with your needs."
                )

        return True, ""

    @staticmethod
    def add_disclaimer(recommendation_text: str, intent: str) -> str:
        """Add contextual disclaimer based on intent."""
        disclaimers = {
            "health": (
                "\n\n📝 *Spiritual Disclaimer*: This pooja complements wellness practices but "
                "does not replace medical care. For serious health concerns, consult a healthcare professional."
            ),
            "career": (
                "\n\n📝 *Intent Disclaimer*: This pooja supports clarity and positive intention. "
                "Career success depends on your effort, skills, and dedication as well."
            ),
            "legal": (
                "\n\n📝 *Legal Disclaimer*: Spiritual practices support inner peace but do not "
                "resolve legal matters. Consult a qualified attorney."
            ),
        }
        return recommendation_text + disclaimers.get(intent, "")
