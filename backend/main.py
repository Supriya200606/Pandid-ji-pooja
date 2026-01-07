from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

from ai.config import load_settings
from ai.chat_handler import CasualChatHandler
from ai.context import ConversationManager, IntentExtractor
from ai.general_qa import GeneralQAEngine
from ai.guardrails import SafetyChecker
from ai.llm import build_llm
from ai.models import QueryContext
from ai.rag import PoojaRecommender

app = FastAPI(
    title="Pandit Ji API",
    description="WhatsApp Pooja Recommendation & Booking Agent",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
settings = load_settings()
llm = build_llm(settings.llm_provider, settings.llm_model)
recommender = PoojaRecommender(settings, llm=llm)
recommender.load_data()
conversation_manager = ConversationManager(max_history=10)
qa_engine = GeneralQAEngine()


# Request/Response models
class ChatRequest(BaseModel):
    user_id: str
    message: str
    city: Optional[str] = None


class PoojaInfo(BaseModel):
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
    scriptural_refs: List[str]


class RecommendationResponse(BaseModel):
    pooja: PoojaInfo
    score: float
    reason: str


class ChatResponse(BaseModel):
    status: str
    message: str
    recommendations: List[RecommendationResponse] = []
    intents: List[str] = []
    is_general_qa: bool = False


@app.get("/")
def root():
    return {
        "service": "Pandit Ji AI",
        "status": "online",
        "endpoints": [
            "POST /chat",
            "GET /poojas",
            "GET /health"
        ]
    }


@app.get("/greeting")
def get_greeting():
    """Get initial greeting message."""
    return {
        "status": "success",
        "message": "🙏 Namaste! Welcome to Pandit Ji.\n\n"
                   "I'm here to help you find the perfect pooja for your spiritual needs, "
                   "answer questions about Hindu rituals and practices, or guide you on your spiritual journey.\n\n"
                   "You can ask me:\n"
                   "• 'Health and peace' - for wellness poojas\n"
                   "• 'Business success' - for prosperity\n"
                   "• 'What is a mantra?' - for spiritual knowledge\n"
                   "• 'How to prepare for pooja?' - for guidance\n\n"
                   "What brings you here today?"
    }


@app.get("/health")
def health():
    return {"status": "healthy", "poojas_loaded": len(recommender._poojas)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Chat endpoint for pooja recommendations or general Q&A."""
    
    # Safety check
    is_safe, safety_msg = SafetyChecker.check_query(req.message)
    if not is_safe:
        return ChatResponse(
            status="unsafe",
            message=safety_msg,
            recommendations=[],
            intents=[],
            is_general_qa=False
        )
    
    # Check if it's a casual greeting/chat
    if CasualChatHandler.is_casual_chat(req.message):
        response = CasualChatHandler.respond(req.message)
        if response:
            conversation_manager.add_turn(req.user_id, "user", req.message)
            conversation_manager.add_turn(req.user_id, "assistant", response)
            return ChatResponse(
                status="success",
                message=response,
                recommendations=[],
                intents=[],
                is_general_qa=False
            )
    
    # Check if it's a general Q&A question
    if qa_engine.is_general_question(req.message):
        answer = qa_engine.answer(req.message)
        if answer:
            conversation_manager.add_turn(req.user_id, "user", req.message)
            conversation_manager.add_turn(req.user_id, "assistant", answer)
            return ChatResponse(
                status="success",
                message=answer,
                recommendations=[],
                intents=[],
                is_general_qa=True
            )
    
    # Otherwise, proceed with pooja recommendation
    intents = IntentExtractor.extract(req.message)
    city = req.city or IntentExtractor.extract_city(req.message)
    
    # Build context
    ctx = QueryContext(
        user_issue=req.message,
        city=city,
        language="en",
    )
    ctx = conversation_manager.enrich_context(ctx, req.user_id)
    
    # Get recommendations
    recs = recommender.recommend(ctx)
    
    if not recs:
        return ChatResponse(
            status="no_match",
            message="No matching poojas found. Try a more specific query or ask a general question about poojas.",
            recommendations=[],
            intents=intents,
            is_general_qa=False
        )
    
    # Convert to response format
    rec_list = [
        RecommendationResponse(
            pooja=PoojaInfo(**{
                "id": r.pooja.id,
                "name": r.pooja.name,
                "intents": r.pooja.intents,
                "tags": r.pooja.tags,
                "description": r.pooja.description,
                "benefits": r.pooja.benefits,
                "materials": r.pooja.materials,
                "steps": r.pooja.steps,
                "duration_minutes": r.pooja.duration_minutes,
                "price_inr": r.pooja.price_inr,
                "cities": r.pooja.cities,
                "scriptural_refs": r.pooja.scriptural_refs,
            }),
            score=r.score,
            reason=r.reason
        )
        for r in recs
    ]
    
    # Add to conversation history
    conversation_manager.add_turn(req.user_id, "user", req.message)
    response_summary = f"Recommended {len(recs)} pooja(s)"
    conversation_manager.add_turn(req.user_id, "assistant", response_summary)
    
    return ChatResponse(
        status="success",
        message=f"Found {len(recs)} recommendation(s)",
        recommendations=rec_list,
        intents=intents,
        is_general_qa=False
    )


@app.get("/poojas")
def list_poojas(intent: Optional[str] = None, city: Optional[str] = None):
    """List all poojas with optional filtering."""
    poojas = recommender._poojas
    
    if intent:
        poojas = [p for p in poojas if intent.lower() in [i.lower() for i in p.intents]]
    
    if city:
        poojas = [p for p in poojas if city.lower() in [c.lower() for c in p.cities]]
    
    return {
        "total": len(poojas),
        "poojas": [
            {
                "id": p.id,
                "name": p.name,
                "intents": p.intents,
                "tags": p.tags,
                "description": p.description,
                "benefits": p.benefits,
                "materials": p.materials,
                "steps": p.steps,
                "duration_minutes": p.duration_minutes,
                "price_inr": p.price_inr,
                "cities": p.cities,
                "scriptural_refs": p.scriptural_refs,
            }
            for p in poojas
        ]
    }


@app.get("/poojas/{pooja_id}")
def get_pooja(pooja_id: str):
    """Get detailed info for a specific pooja."""
    for pooja in recommender._poojas:
        if pooja.id == pooja_id:
            return {
                "id": pooja.id,
                "name": pooja.name,
                "intents": pooja.intents,
                "tags": pooja.tags,
                "description": pooja.description,
                "benefits": pooja.benefits,
                "materials": pooja.materials,
                "steps": pooja.steps,
                "duration_minutes": pooja.duration_minutes,
                "price_inr": pooja.price_inr,
                "cities": pooja.cities,
                "scriptural_refs": pooja.scriptural_refs,
            }
    raise HTTPException(status_code=404, detail="Pooja not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
