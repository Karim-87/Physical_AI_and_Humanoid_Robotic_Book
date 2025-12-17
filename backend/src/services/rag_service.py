from typing import List, Dict, Any
from ..services.embedding_service import EmbeddingService
from ..models.query import UserQuery
from ..models.response import ChatResponse
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from ..config.settings import settings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json


class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self._initialize_llm_client()

    def _initialize_llm_client(self):
        """Initialize the LLM client based on the configured provider."""
        if settings.LLM_PROVIDER == "gemini":
            if settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.llm_client = ChatGoogleGenerativeAI(
                    model="gemini-pro",
                    google_api_key=settings.GEMINI_API_KEY,
                    temperature=0.3
                )
            else:
                raise ValueError("GEMINI_API_KEY not configured in settings")
        elif settings.LLM_PROVIDER == "openai":
            if settings.OPENAI_API_KEY:
                self.llm_client = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    openai_api_key=settings.OPENAI_API_KEY,
                    temperature=0.3
                )
            else:
                raise ValueError("OPENAI_API_KEY not configured in settings")
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

    def _generate_response_with_llm(self, query: str, context: str) -> str:
        """Generate a response using the configured LLM with the provided context."""
        try:
            # Create a system message to constrain the response to textbook content
            system_message = SystemMessage(
                content="You are an AI assistant for a Physical AI & Humanoid Robotics textbook. "
                        "Answer questions based ONLY on the provided textbook content. "
                        "If the answer is not in the provided context, say so explicitly. "
                        "Do not make up information or use external knowledge. "
                        "Always be accurate and cite the source material when possible."
            )

            human_message = HumanMessage(
                content=f"Context:\n{context}\n\nQuestion: {query}\n\n"
                        f"Please provide an answer based only on the context provided above. "
                        f"If the answer is not in the context, please state this clearly."
            )

            response = self.llm_client.invoke([system_message, human_message])
            return response.content
        except Exception as e:
            # Fallback response if LLM call fails
            return f"Based on the textbook content:\n\n{context[:500]}... [Note: Response generated without LLM due to error: {str(e)}]"

    def process_query(self, db: Session, query_text: str, user_id: str = None, ip_address: str = None, language: str = None) -> Dict[str, Any]:
        """Process a user query and return a response based on textbook content."""
        # Create a query record
        query_record = UserQuery(
            id=str(uuid.uuid4()),
            user_id=user_id,
            query_text=query_text,
            ip_address=ip_address,
            language=language or settings.DEFAULT_LANGUAGE
        )
        db.add(query_record)
        db.commit()

        # Search for similar content in the textbook based on the specified language
        search_results = self.embedding_service.search_similar(query_text, limit=5, language=language)

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
                    "content_snippet": payload["content"][:200] + "..." if len(payload["content"]) > 200 else payload["content"],
                    "language": payload.get("language", "unknown")
                })

            # Combine context and generate response
            context = "\n\n".join(context_parts)

            # Generate response using LLM with the context
            response_text = self._generate_response_with_llm(query_text, context)

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

    def process_selection_query(self, db: Session, selected_text: str, question: str = None, user_id: str = None, ip_address: str = None, language: str = None) -> Dict[str, Any]:
        """Process a query based on selected text."""
        if question:
            # Combine selected text with question
            full_query = f"Regarding this text: '{selected_text}', {question}"
        else:
            # Use selected text as the query
            full_query = selected_text

        return self.process_query(db, full_query, user_id, ip_address, language)