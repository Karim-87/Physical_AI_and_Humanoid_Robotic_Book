from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # Application settings
    app_name: str = "Physical AI and Humanoid Robotics RAG Chatbot"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Qdrant settings
    qdrant_collection_name: str = "textbook_content"

    # Model settings
    embedding_model: str = "embed-english-v3.0"
    gemini_model: str = "gemini-2.0-flash"

    # Text processing
    chunk_size: int = 800
    chunk_overlap: int = 200

    # URLs and Collection
    sitemap_url: str = os.getenv("SITEMAP_URL", "https://physical-ai-and-humanoid-robotic-bo-three.vercel.app/sitemap.xml")
    collection_name: str = os.getenv("COLLECTION_NAME", "textbook_content")

    # Additional settings from .env
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    embed_model: str = os.getenv("EMBED_MODEL", "embed-english-v3.0")

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env that are not defined in the model

settings = Settings()