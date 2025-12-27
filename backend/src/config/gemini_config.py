from openai import AsyncOpenAI
import logging
from .settings import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.client = None
        self.model = settings.gemini_model

    def initialize(self):
        """Initialize AsyncOpenAI client with Gemini endpoint configuration"""
        try:
            self.client = AsyncOpenAI(
                api_key=settings.gemini_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise

    def get_client(self):
        """Get the initialized client"""
        if not self.client:
            raise RuntimeError("Gemini client not initialized")
        return self.client

# Global instance
gemini_service = GeminiService()