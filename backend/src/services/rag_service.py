from typing import List, Dict, Any
from ..services.embedding_service import EmbeddingService
from ..models.query import UserQuery
from ..models.response import ChatResponse
from sqlalchemy.orm import Session
import uuid
from datetime import datetime


class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def process_query(self, db: Session, query_text: str, user_id: str = None, ip_address: str = None) -> Dict[str, Any]:
        """Process a user query and return a response based on textbook content."""
        # Create a query record
        query_record = UserQuery(
            id=str(uuid.uuid4()),
            user_id=user_id,
            query_text=query_text,
            ip_address=ip_address
        )
        db.add(query_record)
        db.commit()

        # Search for similar content in the textbook
        # For now, we'll search across all languages, but in a full implementation
        # we might want to pass the user's selected language
        search_results = self.embedding_service.search_similar(query_text, limit=5)

        if not search_results:
            # No relevant content found
            response_text = "I couldn't find relevant information in the textbook to answer your question. Please check the textbook content for more information."
            source_chapters = []
        else:
            # Build context from the most relevant results
            context_parts = []
            source_chapters = []
            for result in search_results:
                payload = result["payload"]
                context_parts.append(payload["content"])
                source_chapters.append({
                    "chapter_id": payload["chapter_id"],
                    "content_snippet": payload["content"][:200] + "..." if len(payload["content"]) > 200 else payload["content"]
                })

            # Combine context and generate response
            context = "\n\n".join(context_parts)

            # For now, we'll return the context as the response
            # In a real implementation, we would use a language model to generate a proper response
            response_text = f"Based on the textbook content:\n\n{context[:500]}..."

        # Create a response record
        response_record = ChatResponse(
            id=str(uuid.uuid4()),
            query_id=query_record.id,
            response_text=response_text,
            source_chapters=[source["chapter_id"] for source in source_chapters],
            confidence_score=0.8  # Placeholder confidence score
        )
        db.add(response_record)
        db.commit()

        return {
            "response": response_text,
            "sources": source_chapters,
            "confidence": 0.8
        }

    def process_selection_query(self, db: Session, selected_text: str, question: str = None, user_id: str = None, ip_address: str = None) -> Dict[str, Any]:
        """Process a query based on selected text."""
        if question:
            # Combine selected text with question
            full_query = f"Regarding this text: '{selected_text}', {question}"
        else:
            # Use selected text as the query
            full_query = selected_text

        return self.process_query(db, full_query, user_id, ip_address)