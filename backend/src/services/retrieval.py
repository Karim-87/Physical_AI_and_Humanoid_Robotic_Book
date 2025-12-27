from typing import List, Dict, Any
import logging
from src.config.qdrant_config import qdrant_service
from src.config.cohere_config import cohere_service
from src.utils.text_processing import chunk_text
from src.config.settings import settings

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        pass

    async def retrieve_from_qdrant(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks from Qdrant based on the query"""
        if not qdrant_service.client:
            raise RuntimeError("Qdrant client not initialized")

        try:
            # Generate embedding for the query
            embeddings = cohere_service.embed_text([query])
            query_embedding = embeddings[0]

            # Search in Qdrant
            search_results = qdrant_service.client.search(
                collection_name=qdrant_service.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True
            )

            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "text": hit.payload.get("text", ""),
                    "source": hit.payload.get("source", ""),
                    "title": hit.payload.get("title", ""),
                    "score": hit.score
                })

            return results
        except Exception as e:
            logger.error(f"Failed to retrieve from Qdrant: {e}")
            return []

    async def retrieve_from_selected_text(self, query: str, selected_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks from the selected text using in-memory similarity"""
        try:
            # Chunk the selected text
            chunks = chunk_text(selected_text, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap)

            # Generate embeddings for chunks
            chunk_embeddings = cohere_service.embed_text(chunks)

            # Generate embedding for query
            query_embedding = cohere_service.embed_text([query])[0]

            # Calculate similarity scores (cosine similarity)
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np

            # Convert to numpy arrays for calculation
            chunk_embeddings_array = np.array(chunk_embeddings)
            query_embedding_array = np.array([query_embedding])

            # Calculate cosine similarities
            similarities = cosine_similarity(query_embedding_array, chunk_embeddings_array)[0]

            # Create list of (chunk, similarity_score) pairs
            chunk_score_pairs = list(zip(chunks, similarities))

            # Sort by similarity score in descending order
            chunk_score_pairs.sort(key=lambda x: x[1], reverse=True)

            # Return top_k results
            results = []
            for chunk, score in chunk_score_pairs[:top_k]:
                results.append({
                    "text": chunk,
                    "source": "selected_text",
                    "title": "Selected Text",
                    "score": float(score)
                })

            return results
        except Exception as e:
            logger.error(f"Failed to retrieve from selected text: {e}")
            return []

    async def retrieve(self, query: str, selected_text: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """Main retrieval method that handles both modes"""
        if selected_text:
            # Use selected-text-only mode
            return await self.retrieve_from_selected_text(query, selected_text, top_k)
        else:
            # Use full-book RAG mode
            return await self.retrieve_from_qdrant(query, top_k)

# Global instance
retrieval_service = RetrievalService()