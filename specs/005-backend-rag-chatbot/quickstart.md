# Quickstart Guide: Backend RAG Chatbot

## Prerequisites
- Python 3.12 or higher
- `uv` package manager installed
- Access to Cohere API (embed-english-v3.0 or newer)
- Qdrant Cloud account (Free Tier)
- Google AI Studio account for Gemini access
- Neon Serverless Postgres account

## Setup Instructions

### 1. Clone and Navigate to Backend
```bash
# If not already in the project directory
cd /path/to/AI-Textbook-Hackathon

# Create backend directory if it doesn't exist
mkdir -p backend
cd backend
```

### 2. Initialize Python Project
```bash
# Initialize new Python project with uv
uv init
```

### 3. Install Dependencies
```bash
# Navigate to backend directory
cd backend

# Add required dependencies
uv add fastapi uvicorn python-dotenv cohere qdrant-client openai-agents psycopg[binary] sqlalchemy python-multipart requests beautifulsoup4
```

### 4. Create Environment File
```bash
# Create .env file with required credentials
cat > .env << 'EOF'
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
NEON_DATABASE_URL=your_neon_postgres_connection_string_here
EOF
```

### 5. Create Project Structure
```bash
mkdir -p src/{api,models,services,tools,config}
mkdir -p scripts
mkdir -p tests/{unit,integration,contract}
```

### 6. Create the Main Application File
```bash
# Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI
from src.api.rag_routes import router as rag_router
from src.config.settings import settings
from contextlib import asynccontextmanager
from src.services.embedding_service import initialize_qdrant
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize services on startup
    logger.info("Initializing Qdrant connection...")
    await initialize_qdrant()
    logger.info("Qdrant connection established")
    yield
    # Cleanup on shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="Physical AI and Humanoid Robotics RAG Chatbot",
    description="Backend service for RAG-powered textbook Q&A",
    version="1.0.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(rag_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-12-26T00:00:00Z",
        "dependencies": {
            "cohere": True,
            "qdrant": True,
            "postgres": True
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
EOF
```

### 7. Run the Application
```bash
# Run the FastAPI application
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the API
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint (with sample query)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Physical AI?",
    "selected_text": null,
    "session_id": null
  }'
```

## Environment Variables Required
- `GEMINI_API_KEY`: Your Google AI Studio API key for Gemini access
- `COHERE_API_KEY`: Your Cohere API key for embeddings
- `QDRANT_API_KEY`: Your Qdrant Cloud API key
- `QDRANT_URL`: Your Qdrant Cloud cluster URL
- `NEON_DATABASE_URL`: Your Neon Postgres connection string

## Next Steps
1. Implement the ingestion script to crawl the textbook sitemap
2. Create the embedding and storage pipeline for textbook content
3. Build the RAG agent with retrieval tools
4. Implement the database models and session management
5. Add comprehensive error handling and logging