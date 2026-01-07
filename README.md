# Pandit Ji AI (WhatsApp Pooja Recommender)

This repo starts with the AI layer for a WhatsApp-first Pandit Ji agent. It focuses on:
- Pooja knowledge base (sample data included)
- Lightweight retrieval + recommendation logic
- Prompt templates and stubs for LLM integration

A minimal CLI demo is provided so you can test retrieval locally without external services.

## Structure
- `ai/models.py` – Data models for pooja entries and recommendations
- `ai/rag.py` – Retrieval and rule-based recommendation logic with an LLM hook
- `ai/prompting.py` – Prompt templates for English/Hindi
- `ai/llm.py` – LLM client stub; plug in OpenAI/Groq later
- `ai/config.py` – Settings and defaults
- `ai/sample_data/poojas.json` – Seed pooja catalog (8 examples)
- `ai/demo.py` – CLI to try the recommender locally

## Quickstart
1) Create a virtual env and install optional deps (only standard library required for the fallback scorer):
```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
# Optional, for better embeddings:
# pip install sentence-transformers
```

2) Run a quick recommendation (no API keys needed for the fallback path):
```bash
python -m ai.demo "I need a puja for health and peace"
```

3) (Optional) Configure an LLM in `ai/llm.py` and wire it in `PoojaRecommender` to get richer, personalized responses.

## Next steps
- Hook the recommender into a WhatsApp webhook (FastAPI/Express)
- Swap the in-memory catalog for a DB + vector store (Qdrant/Chroma)
- Add Hindi transliteration + stricter guardrails
- Integrate payment + slot booking flows
