from openai import AssistantEventHandler
from typing_extensions import override
from openai.types.beta.threads import Text, TextDelta
from typing import Dict, Any, List
import json
from src.services.retrieval import retrieval_service
from src.config.settings import settings

# Import the function_tool decorator from the appropriate library
# Since we're using OpenAI Agents SDK, we'll create a function-based tool
def create_retrieval_tool():
    """
    Creates a retrieval tool for the OpenAI Agents SDK that can retrieve
    relevant content from the textbook based on the query and selected text.
    """

    async def retrieval_function(query: str, selected_text: str = None) -> str:
        """
        Retrieve relevant content from the textbook based on the query.

        Args:
            query: The user's query
            selected_text: Optional selected text for focused search

        Returns:
            JSON string containing retrieved chunks and metadata
        """
        try:
            # Use the retrieval service to get relevant chunks
            results = await retrieval_service.retrieve(
                query=query,
                selected_text=selected_text,
                top_k=5
            )

            # Format results as context for the agent
            context_chunks = []
            for result in results:
                context_chunks.append({
                    "text": result["text"],
                    "source": result["source"],
                    "title": result["title"],
                    "relevance_score": result["score"]
                })

            # Create context string
            context_text = "\n\n".join([chunk["text"] for chunk in context_chunks])

            return json.dumps({
                "context": context_text,
                "retrieved_chunks": context_chunks,
                "mode": "selected-text-only" if selected_text else "full-book"
            })

        except Exception as e:
            return json.dumps({
                "error": f"Retrieval failed: {str(e)}",
                "context": "",
                "retrieved_chunks": []
            })

    # Return the function with metadata for the tool
    return {
        "type": "function",
        "function": {
            "name": "retrieve_textbook_content",
            "description": "Retrieve relevant content from the Physical AI and Humanoid Robotics textbook based on a query. Can work in two modes: full-book RAG (when no selected_text provided) or selected-text-only mode (when selected_text is provided).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for in the textbook content"
                    },
                    "selected_text": {
                        "type": "string",
                        "description": "Optional text selected by the user for focused search"
                    }
                },
                "required": ["query"]
            }
        },
        "function_impl": retrieval_function
    }

# Alternative implementation using a class-based approach
class RetrievalTool:
    """
    A class-based implementation of the retrieval tool for the OpenAI Agents SDK.
    """

    def __init__(self):
        self.name = "retrieve_textbook_content"
        self.description = "Retrieve relevant content from the Physical AI and Humanoid Robotics textbook based on a query. Can work in two modes: full-book RAG (when no selected_text provided) or selected-text-only mode (when selected_text is provided)."

        self.parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for in the textbook content"
                },
                "selected_text": {
                    "type": "string",
                    "description": "Optional text selected by the user for focused search"
                }
            },
            "required": ["query"]
        }

    async def __call__(self, query: str, selected_text: str = None) -> Dict[str, Any]:
        """
        Execute the retrieval tool.

        Args:
            query: The user's query
            selected_text: Optional selected text for focused search

        Returns:
            Dictionary containing retrieved context and metadata
        """
        try:
            # Use the retrieval service to get relevant chunks
            results = await retrieval_service.retrieve(
                query=query,
                selected_text=selected_text,
                top_k=5
            )

            # Format results as context for the agent
            context_chunks = []
            for result in results:
                context_chunks.append({
                    "text": result["text"],
                    "source": result["source"],
                    "title": result["title"],
                    "relevance_score": result["score"]
                })

            # Create context string
            context_text = "\n\n".join([chunk["text"] for chunk in context_chunks])

            return {
                "context": context_text,
                "retrieved_chunks": context_chunks,
                "mode": "selected-text-only" if selected_text else "full-book",
                "retrieved_chunks_count": len(context_chunks)
            }

        except Exception as e:
            return {
                "error": f"Retrieval failed: {str(e)}",
                "context": "",
                "retrieved_chunks": [],
                "mode": "error",
                "retrieved_chunks_count": 0
            }

# Create the global tool instance
retrieval_tool = RetrievalTool()