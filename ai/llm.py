from __future__ import annotations

from typing import Optional


class LLMClient:
    """Stub LLM client. Plug in OpenAI/Groq/HF here."""

    def __init__(self, provider: str | None = None, model: str | None = None):
        self.provider = provider or ""
        self.model = model or ""

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        # TODO: Implement real LLM call. For now, return the prompt tail as a placeholder.
        return prompt[-max_tokens:]


def build_llm(provider: Optional[str], model: Optional[str]) -> Optional[LLMClient]:
    if not provider:
        return None
    return LLMClient(provider=provider, model=model)
