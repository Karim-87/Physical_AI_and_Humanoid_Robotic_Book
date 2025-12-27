import cohere
from typing import List
import logging
from .settings import settings

logger = logging.getLogger(__name__)

class CohereService:
    def __init__(self):
        self.client = None
        self.model = settings.embedding_model

    def initialize(self):
        """Initialize Cohere client with API key"""
        try:
            self.client = cohere.Client(settings.cohere_api_key)
            logger.info("Cohere client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {e}")
            raise

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        if not self.client:
            raise RuntimeError("Cohere client not initialized")

        try:
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"  # Best for document search use cases
            )
            return response.embeddings
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

    async def embed_text_async(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts (async version)"""
        return self.embed_text(texts)

# Global instance
cohere_service = CohereService()