# Pandit Ji - AI-Powered Pooja Recommendation Platform

A full-stack web application that provides AI-powered spiritual guidance and pooja recommendations for users seeking Hindu spiritual services. The platform features an intelligent chatbot interface that helps users find appropriate poojas based on their needs.

## Features

- 🤖 **AI Chatbot Interface** - Interactive chat with Pandit Ji for personalized recommendations
- 🕉️ **Pooja Recommendations** - Smart matching of poojas based on user intents and needs
- 📚 **General Q&A** - Answer questions about Hindu rituals, practices, and spiritual concepts
- 🛡️ **Safety Guardrails** - Content filtering and appropriate response handling
- 🌐 **Web Frontend** - Clean, responsive chat interface with pooja catalog
- 🔌 **Dual Backend Support** - Flask (simple) and FastAPI (advanced) implementations

## Project Structure

```
POOJAI/
├── app.py                      # Flask backend server (simple implementation)
├── backend/
│   └── main.py                 # FastAPI backend server (advanced implementation)
├── frontend/
│   ├── index.html              # Chat interface
│   └── catalog.html            # Pooja catalog view
├── ai/
│   ├── chat.py                 # Main chat orchestration
│   ├── chat_handler.py         # Casual conversation handling
│   ├── config.py               # Configuration and settings
│   ├── context.py              # Conversation context management
│   ├── demo.py                 # CLI demo for testing
│   ├── general_qa.py           # General question answering
│   ├── guardrails.py           # Safety and content filtering
│   ├── llm.py                  # LLM client integration
│   ├── models.py               # Data models
│   ├── pandit_ji_chatbot.py    # Core chatbot logic
│   ├── prompting.py            # Prompt templates
│   ├── rag.py                  # RAG-based recommendation engine
│   └── sample_data/
│       ├── poojas.json         # Pooja catalog data
│       └── general_qa.json     # Q&A knowledge base
└── tests/
    └── test_recommender.py     # Unit tests
```

## Installation

1) **Clone the repository**
```bash
git clone <your-repo-url>
cd POOJAI
```

2) **Create and activate virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3) **Install dependencies**
```bash
pip install --upgrade pip
pip install flask flask-cors
# For FastAPI backend:
pip install fastapi uvicorn pydantic
# Optional for enhanced features:
pip install sentence-transformers
```

## Running the Application

### Option 1: Flask Backend (Simple)
```bash
python app.py
```
Then open `index.html` in your browser (update API endpoint to `http://localhost:5000`)

### Option 2: FastAPI Backend (Advanced)
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Then open `frontend/index.html` in your browser (update API endpoint to `http://localhost:8000`)

### Option 3: CLI Demo
```bash
python -m ai.demo "I need a puja for health and peace"
```

## API Endpoints

### Flask Backend (app.py)
- `GET /greeting` - Get initial greeting message
- `POST /chat` - Send message and get recommendations
- `GET /poojas` - Get all poojas from catalog
- `GET /health` - Health check

### FastAPI Backend (backend/main.py)
- `GET /` - API info
- `GET /greeting` - Get initial greeting message
- `POST /chat` - Send message and get recommendations
- `GET /poojas` - Get all poojas from catalog
- `GET /health` - Health check

## Configuration

Edit `ai/config.py` to configure:
- LLM provider (OpenAI, Groq, or fallback)
- API keys
- Model selection
- Temperature and other parameters
- Data file paths

## Adding LLM Integration

By default, the system uses a fallback keyword-based matcher. To enable AI-powered responses:

1) Set your API key in environment variables:
```bash
set OPENAI_API_KEY=your-key-here
# or
set GROQ_API_KEY=your-key-here
```

2) Update `ai/config.py` with your preferred LLM provider and model

3) The system will automatically use the LLM for enhanced recommendations and responses

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Poojas
Edit `ai/sample_data/poojas.json` with the following structure:
```json
{
  "id": "unique-id",
  "name": "Pooja Name",
  "intents": ["intent1", "intent2"],
  "tags": ["tag1", "tag2"],
  "description": "Description",
  "benefits": ["benefit1"],
  "materials": ["material1"],
  "steps": ["step1"],
  "duration_minutes": 60,
  "price_inr": 1000,
  "cities": ["city1"],
  "scriptural_refs": ["reference"]
}
```

## Future Enhancements

- WhatsApp integration via webhook
- Database integration (PostgreSQL/MongoDB)
- Vector store for semantic search (Qdrant/Chroma)
- Hindi language support
- Payment gateway integration
- Booking and scheduling system
- Pandit availability management
- User authentication and profiles
