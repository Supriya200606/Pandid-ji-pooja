from __future__ import annotations

from ai.models import Pooja


def build_recommendation_prompt(user_issue: str, pooja: Pooja, language: str = "en") -> str:
    # English-only prompt; language parameter retained for interface compatibility.
    return (
        "You are a respectful Pandit Ji assistant.\n"
        f"User need: {user_issue}\n"
        f"Suggested pooja: {pooja.name}\n"
        f"Benefits: {', '.join(pooja.benefits)}\n"
        f"Duration: {pooja.duration_minutes} minutes\n"
        f"Required items: {', '.join(pooja.materials)}\n"
        "Respond briefly and empathetically."
    )
