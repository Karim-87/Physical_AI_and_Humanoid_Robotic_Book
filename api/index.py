from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
import logging
import datetime
import os
import sys

# Add backend directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

# Import backend services - adjust import paths for Vercel
from src.services.agent import rag_agent
from src.services.session import session_service
from src.config.qdrant_config import qdrant_service
from src.config.cohere_config import cohere_service
from src.config.gemini_config import gemini_service
from src.config.database import init_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    mode: str
    retrieved_chunks_count: int
    response_time: float

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    dependencies: Dict[str, bool]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    logger.info("Initializing services...")

    # Initialize Qdrant
    await qdrant_service.initialize()

    # Initialize Cohere
    cohere_service.initialize()

    # Initialize Gemini
    gemini_service.initialize()

    # Initialize database
    await init_db()

    logger.info("All services initialized successfully!")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Physical AI and Humanoid Robotics RAG Chatbot",
    description="Backend service for RAG-powered textbook Q&A",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://physical-ai-and-humanoid-robotic-bo-three.vercel.app",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Test dependencies
    qdrant_ok = await qdrant_service.test_connection()
    cohere_ok = cohere_service.client is not None
    gemini_ok = gemini_service.client is not None

    all_ok = qdrant_ok and cohere_ok and gemini_ok

    return HealthResponse(
        status="healthy" if all_ok else "unhealthy",
        timestamp=datetime.datetime.now().isoformat(),
        dependencies={
            "qdrant": qdrant_ok,
            "cohere": cohere_ok,
            "gemini": gemini_ok
        }
    )

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint that processes user queries using RAG"""
    try:
        # Get or create session
        session = await session_service.get_or_create_session(request.session_id)

        # Process the query with the RAG agent
        result = await rag_agent.process_query(
            query=request.message,
            selected_text=request.selected_text,
            session_id=session.id
        )

        # Save user message to history
        await session_service.save_message(
            session_id=session.id,
            role="user",
            content=request.message,
            mode=result.get("mode", "unknown"),
            response_time=result.get("response_time", 0)
        )

        # Save AI response to history
        await session_service.save_message(
            session_id=session.id,
            role="assistant",
            content=result.get("response", ""),
            retrieved_chunks=[chunk.get("text", "")[:100] for chunk in result.get("retrieved_chunks", [])],  # Store chunk previews
            mode=result.get("mode", "unknown"),
            response_time=result.get("response_time", 0)
        )

        return ChatResponse(
            response=result["response"],
            session_id=result["session_id"],
            mode=result["mode"],
            retrieved_chunks_count=result["retrieved_chunks_count"],
            response_time=result["response_time"]
        )

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/api/v1/ingest")
async def trigger_ingestion(force: bool = False):
    """Trigger content ingestion from textbook sitemap"""
    from scripts.ingestion import TextbookIngestion

    try:
        ingestion = TextbookIngestion()
        await ingestion.ingest_all_pages()

        return {
            "status": "started",
            "pages_processed": ingestion.processed_pages,
            "chunks_created": ingestion.created_chunks,
            "message": f"Ingestion completed: {ingestion.processed_pages} pages processed, {ingestion.created_chunks} chunks created"
        }
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")