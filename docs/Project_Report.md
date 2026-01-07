# Pandit Ji Conversational Agent – Project Report

## Executive Summary
Pandit Ji is a WhatsApp-first AI agent that recommends culturally authentic Hindu poojas, answers general spiritual questions, and supports a guided chat experience. This project implements the AI layer (retrieval + Q&A), a REST backend (FastAPI), and a simple web frontend to demonstrate the E2E flow. Future phases add WhatsApp integration, booking, and payments.

## Goals & Success Criteria
- Natural chat in English; recommends suitable poojas with reasons.
- General spiritual Q&A (mantras, rituals, concepts) from curated content.
- End-to-end demo: user query → AI recommendations/Q&A → web UI display.
- Success: Finish a typical journey in under 5 minutes with coherent answers.

## Scope & Constraints
- In-scope: AI recommender, general Q&A, REST API, web UI demo.
- Out-of-scope (current phase): Payments, priest scheduling, WhatsApp official integration.
- Constraints: Respectful tone, safety guardrails, test-mode only for payments (future).

## Architecture Overview
```
[User (Web UI/WhatsApp)]
        │
        ▼
[Frontend (index.html)]  →  calls  →  [Backend FastAPI]
                                      │
                                      │  uses
                                      ▼
                              [AI Layer (Python)]
                              ├─ Recommender (RAG-lite)
                              ├─ General Q&A (curated)
                              ├─ Guardrails (safety)
                              └─ Config/Prompts/Models

Data: ai/sample_data/poojas.json, ai/sample_data/general_qa.json
Optional: sentence-transformers embeddings for better ranking
```

## Components
- AI Layer (Python, `ai/`)
  - `rag.py`: In-memory retrieval with optional embeddings; ranks poojas.
  - `general_qa.py`: Keyword-based general Q&A engine (English only).
  - `guardrails.py`: Safety checks (word boundary matching; respectful tone).
  - `prompting.py`: English-only prompt builders.
  - `models.py`: `Pooja`, `Recommendation`, `QueryContext`, conversation turns.
  - `config.py`: Paths, ranking thresholds; embedding defaults.
- Backend (FastAPI, `backend/main.py`)
  - Endpoints: `/chat`, `/poojas`, `/poojas/{id}`, `/health`, `/greeting`.
  - Session management: `ConversationManager` to track chat history.
- Frontend (`frontend/index.html`)
  - Minimal chat UI: greeting, send message, show recommendations/Q&A.
  - Calls REST API directly; shows relevance, benefits, price, cities.

## Data Models (simplified)
- `pooja(id, name, intents[], tags[], description, benefits[], materials[], steps[], duration_minutes, price_inr, cities[], scriptural_refs[])`
- `recommendation(pooja, score, reason, language)`
- `query_context(user_issue, city?, language, budget_inr?, preferred_deity?, conversation_history[])`

## Conversation & AI Flow
1. User sends a message from web UI.
2. Backend `/chat` runs safety checks.
3. If general Q&A: use curated KB; return answer.
4. Else: use recommender to retrieve and rank poojas.
5. Return structured payload with top options.

## Safety & Cultural Accuracy
- Guardrails refuse harmful or inappropriate requests using exact-word matching.
- Disclaimers suggested for health/career where appropriate (extensible).
- Catalog curated from commonly known poojas; scriptural references included where relevant.

## Setup & Run
```powershell
# From repo root, create venv
python -m venv .venv
.venv\Scripts\activate

# Install dependencies for backend
pip install fastapi uvicorn
# Optional for better ranking
pip install sentence-transformers

# Start backend
python backend/main.py
# or
python -m backend.main

# Open frontend
start .\frontend\index.html
```

## Demo Scenarios
- Recommendation: "wealth for business in Mumbai" → Lakshmi Kubera / Business Launch.
- Health: "health and peace in Delhi" → Maha Mrityunjaya / Rudrabhishek.
- Marriage: "marriage harmony" → Vivah Puja.
- General Q&A: "What is a mantra?", "How to prepare for pooja?".

## API Endpoints
- `GET /greeting` → Initial assistant greeting text.
- `POST /chat { user_id, message, city? }` →
  - Returns `{status, message | recommendations[], intents[], is_general_qa}`
- `GET /poojas?intent=&city=` → Filtered list.
- `GET /poojas/{pooja_id}` → Detailed pooja info.
- `GET /health` → Service status.

## Testing
- Unit tests: `tests/test_recommender.py` checks query mapping, sorting, catalog size, JSON export.
- Manual: Try multiple queries via CLI and UI.
```powershell
pytest tests/ -v
python -m ai.demo "wealth for business" --city Mumbai --lang en
python -m ai.chat
```

## Deployment (suggested)
- Free-tier hosting: Render/Railway for FastAPI; static hosting for frontend.
- Env vars: `EMBEDDING_MODEL=all-MiniLM-L6-v2` for embeddings.
- Logging & monitoring: simple access logs; expand with OpenTelemetry later.

## Roadmap & Future Work
- WhatsApp integration (Meta Cloud API/Twilio sandbox): `/webhook/whatsapp`.
- Booking & payments (Razorpay/Stripe test mode) with webhooks.
- DB (Postgres/Supabase) for catalog, users, bookings, slots.
- Vector store (Qdrant/Chroma) for scalable retrieval.
- Admin dashboard (React/Vite) for catalog & schedules.
- Hindi & regional language support if needed later.

## Team Roles (suggested)
1. AI/NLP: RAG, prompts, embeddings, guardrails.
2. Backend: FastAPI, WhatsApp webhook, APIs.
3. Payments/Booking: slots, payment links, webhooks.
4. Content Research: curate & validate pooja data.
5. Frontend/UX: chat flows, admin UI.
6. DevOps: deploy, observability.

## Appendix – File Map
- AI: `ai/models.py`, `ai/rag.py`, `ai/general_qa.py`, `ai/guardrails.py`, `ai/prompting.py`, `ai/config.py`
- Data: `ai/sample_data/poojas.json`, `ai/sample_data/general_qa.json`
- Backend: `backend/main.py`
- Frontend: `frontend/index.html`
- Demos: `ai/demo.py`, `ai/chat.py`
- Tests: `tests/test_recommender.py`
