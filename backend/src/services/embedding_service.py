from typing import List, Optional
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from ..config.settings import settings
import logging
import uuid


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        # Use configured collection names from settings
        self.collection_name_en = settings.QDRANT_COLLECTION_EN
        self.collection_name_ur = settings.QDRANT_COLLECTION_UR
        self.default_collection = self.collection_name_en
        self._initialize_collections()

    def _get_collection_name(self, language: str = None) -> str:
        """Get the appropriate collection name based on language."""
        if language == "ur":
            return self.collection_name_ur
        else:
            return self.collection_name_en

    def _initialize_collections(self):
        """Initialize both English and Urdu Qdrant collections for storing embeddings."""
        for collection_name in [self.collection_name_en, self.collection_name_ur]:
            try:
                # Check if collection exists
                self.client.get_collection(collection_name)
            except:
                # Create collection if it doesn't exist
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
                )
                logging.info(f"Created Qdrant collection: {collection_name}")

    def _initialize_collection(self):
        """Deprecated: Use _initialize_collections instead."""
        self._initialize_collections()

    def create_embedding(self, text: str) -> List[float]:
        """Create an embedding for the given text."""
        embedding = self.model.encode([text])
        return embedding[0].tolist()

    def store_embedding(self, chapter_id: str, content: str, language: str, section_ref: str = "") -> str:
        """Store an embedding in Qdrant and return the ID."""
        embedding = self.create_embedding(content)
        point_id = str(uuid.uuid4())
        collection_name = self._get_collection_name(language)

        self.client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "chapter_id": chapter_id,
                        "content": content,
                        "language": language,
                        "section_ref": section_ref
                    }
                )
            ]
        )

        return point_id

    def search_similar(self, query: str, limit: int = 5, language: str = None) -> List[dict]:
        """Search for similar content based on the query."""
        query_embedding = self.create_embedding(query)

        # Determine which collection to search based on language
        collection_name = self._get_collection_name(language)

        # Prepare search filter based on language (for consistency, though collection name already specifies language)
        search_filter = None
        if language:
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="language",
                        match=models.MatchValue(value=language)
                    )
                ]
            )

        search_results = self.client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit,
            query_filter=search_filter
        )

        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "payload": result.payload,
                "score": result.score
            })

        return results

    def batch_store_embeddings(self, chapter_id: str, language: str, contents: List[str], section_refs: List[str] = None) -> List[str]:
        """Store multiple embeddings at once."""
        if section_refs is None:
            section_refs = [""] * len(contents)

        embeddings = self.model.encode(contents)
        point_ids = []

        points = []
        for i, content in enumerate(contents):
            point_id = str(uuid.uuid4())
            point_ids.append(point_id)

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embeddings[i].tolist(),
                    payload={
                        "chapter_id": chapter_id,
                        "content": content,
                        "language": language,
                        "section_ref": section_refs[i] if i < len(section_refs) else ""
                    }
                )
            )

        collection_name = self._get_collection_name(language)
        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

        return point_ids