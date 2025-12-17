from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application settings
    APP_ENV: str = "development"
    APP_NAME: str = "physical-ai-textbook"
    APP_BASE_URL: str = "http://localhost:8000"

    # Database settings
    DATABASE_URL: str = "sqlite:///./textbook.db"  # Use SQLite as default for local development
    NEON_DATABASE_URL: Optional[str] = None

    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_EN: str = "book_embeddings_en"
    QDRANT_COLLECTION_UR: str = "book_embeddings_ur"

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # JWT settings (mapped from .env.example)
    JWT_SECRET: Optional[str] = None
    JWT_EXPIRE_MINUTES: int = 1440

    # Rate limiting settings
    RATE_LIMIT_REQUESTS: int = 60  # requests per window
    RATE_LIMIT_WINDOW: int = 3600  # window in seconds (1 hour)

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Physical AI & Humanoid Robotics Textbook API"

    # RAG settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # LLM Provider settings
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # OAuth Provider settings
    FACEBOOK_CLIENT_ID: Optional[str] = None
    FACEBOOK_CLIENT_SECRET: Optional[str] = None
    FACEBOOK_REDIRECT_URI: str = "http://localhost:3000/auth/facebook/callback"

    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/auth/google/callback"

    # Frontend settings
    FRONTEND_OAUTH_CALLBACK_URL: str = "http://localhost:3000"

    # RAG Constraints
    RAG_MODE: str = "book_only"
    RAG_ALLOW_SELECTED_TEXT_ONLY: bool = True
    MAX_CONTEXT_CHUNKS: int = 4

    # Language Settings
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: str = "en,ur"

    class Config:
        env_file = ".env"


settings = Settings()