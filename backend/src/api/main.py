from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .textbook_routes import router as textbook_router
from .rag_routes import router as rag_router
from .auth_routes import router as auth_router
from ..config.settings import settings


app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(textbook_router, prefix=settings.API_V1_STR, tags=["textbook"])
app.include_router(rag_router, prefix=settings.API_V1_STR, tags=["rag"])
app.include_router(auth_router, prefix=settings.API_V1_STR, tags=["auth"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Textbook RAG API"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "textbook-rag-api"}