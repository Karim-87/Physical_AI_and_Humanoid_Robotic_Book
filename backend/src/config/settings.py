from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./textbook.db"

    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None

    # Neon database settings (if needed)
    NEON_DATABASE_URL: Optional[str] = None

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate limiting settings
    RATE_LIMIT_REQUESTS: int = 60  # requests per window
    RATE_LIMIT_WINDOW: int = 3600  # window in seconds (1 hour)

    # Application settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Textbook RAG API"

    # RAG settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"


settings = Settings()