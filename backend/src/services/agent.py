from openai import AsyncOpenAI
from typing import Dict, Any, Optional
import logging
from src.config.gemini_config import gemini_service
from src.tools.retrieval_tool import retrieval_tool
from src.config.settings import settings
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGAgent:
    def __init__(self):
        self.client = None
        self.model = settings.gemini_model

    def get_client(self):
        if self.client is None:
            self.client = gemini_service.get_client()
        return self.client

    async def process_query(
        self,
        query: str,
        selected_text: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user query using the RAG agent.

        Args:
            query: The user's query
            selected_text: Optional selected text for focused search
            session_id: Optional session ID for conversation context

        Returns:
            Dictionary containing the response and metadata
        """
        start_time = datetime.now()

        try:
            # Use the retrieval tool to get relevant context
            retrieval_result = await retrieval_tool(query, selected_text)

            # Prepare the context for the LLM
            if retrieval_result.get("error"):
                context = "No relevant content found in the textbook."
                mode = "error"
            else:
                context = retrieval_result.get("context", "")
                mode = retrieval_result.get("mode", "unknown")

            # Create the system message
            system_message = {
                "role": "system",
                "content": (
                    "You are an AI assistant for the Physical AI and Humanoid Robotics textbook. "
                    "Answer questions based only on the provided context from the textbook. "
                    "If the context doesn't contain relevant information, say so clearly. "
                    "Be helpful, accurate, and cite sources when possible."
                )
            }

            # Create the user message with context
            user_message_content = (
                f"Context from textbook:\n{context}\n\n"
                f"User question: {query}\n\n"
                f"Please provide an answer based on the context provided. "
                f"If the context doesn't contain relevant information, say so clearly."
            )

            user_message = {
                "role": "user",
                "content": user_message_content
            }

            # Prepare messages for the API call
            messages = [system_message, user_message]

            # Get the client (initialize if needed)
            client = self.get_client()

            # Make the API call to Gemini
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1000,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": retrieval_tool.name,
                        "description": retrieval_tool.description,
                        "parameters": retrieval_tool.parameters
                    }
                }] if retrieval_result.get("retrieved_chunks_count", 0) > 0 else None,
                tool_choice="none"  # For now, don't let the model call tools itself
            )

            # Extract the response
            llm_response = response.choices[0].message.content

            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds()

            return {
                "response": llm_response,
                "session_id": session_id or f"session_{int(datetime.now().timestamp())}",
                "mode": mode,
                "retrieved_chunks_count": retrieval_result.get("retrieved_chunks_count", 0),
                "response_time": response_time,
                "retrieved_chunks": retrieval_result.get("retrieved_chunks", [])
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            response_time = (datetime.now() - start_time).total_seconds()
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "session_id": session_id or f"session_{int(datetime.now().timestamp())}",
                "mode": "error",
                "retrieved_chunks_count": 0,
                "response_time": response_time,
                "retrieved_chunks": []
            }

# Global instance
rag_agent = RAGAgent()