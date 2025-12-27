from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional
import logging
from .settings import settings

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        self.client: Optional[QdrantClient] = None
        self.collection_name = settings.qdrant_collection_name
        self.embedding_size = 1024  # Cohere embed-english-v3.0 returns 1024-dimensional vectors

    async def initialize(self):
        """Initialize Qdrant client and create collection if it doesn't exist"""
        try:
            # Initialize the Qdrant client
            if settings.qdrant_url.startswith("http"):
                # Cloud instance
                self.client = QdrantClient(
                    url=settings.qdrant_url,
                    api_key=settings.qdrant_api_key,
                    timeout=10
                )
            else:
                # Local instance
                self.client = QdrantClient(
                    host=settings.qdrant_url,
                    api_key=settings.qdrant_api_key,
                    timeout=10
                )

            # Use collection name from settings
            self.collection_name = settings.collection_name

            # Check if collection exists, if not create it
            try:
                collections = self.client.get_collections()
                collection_exists = any(col.name == self.collection_name for col in collections.collections)
            except Exception:
                collection_exists = False

            if not collection_exists:
                await self.create_collection()
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")

        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise

    async def create_collection(self):
        """Create the collection for storing textbook content embeddings"""
        if not self.client:
            raise RuntimeError("Qdrant client not initialized")

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.embedding_size,
                distance=models.Distance.COSINE
            )
        )

    async def test_connection(self) -> bool:
        """Test if Qdrant connection is working"""
        try:
            if not self.client:
                return False
            # Try to get collection info as a simple test
            collection_info = self.client.get_collection(self.collection_name)
            return True
        except Exception:
            return False

# Global instance
qdrant_service = QdrantService()