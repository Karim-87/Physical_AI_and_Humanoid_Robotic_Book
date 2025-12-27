import re
from typing import Optional
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

class QueryValidationResult(BaseModel):
    is_valid: bool
    error_message: Optional[str] = None
    sanitized_query: str = ""

class InputValidator:
    """
    Utility class for validating user inputs and selected text.
    """

    @staticmethod
    def validate_query(query: str) -> QueryValidationResult:
        """
        Validate the user's query input.
        """
        if not query or not query.strip():
            return QueryValidationResult(
                is_valid=False,
                error_message="Query cannot be empty"
            )

        # Check length
        if len(query.strip()) < 3:
            return QueryValidationResult(
                is_valid=False,
                error_message="Query must be at least 3 characters long"
            )

        if len(query) > 1000:  # Arbitrary limit
            return QueryValidationResult(
                is_valid=False,
                error_message="Query is too long (max 1000 characters)"
            )

        # Sanitize the query (remove potential injection characters)
        sanitized_query = InputValidator._sanitize_text(query)

        return QueryValidationResult(
            is_valid=True,
            sanitized_query=sanitized_query
        )

    @staticmethod
    def validate_selected_text(selected_text: str) -> QueryValidationResult:
        """
        Validate the user's selected text input.
        """
        if not selected_text or not selected_text.strip():
            return QueryValidationResult(
                is_valid=False,
                error_message="Selected text cannot be empty"
            )

        # Check length
        if len(selected_text) > 10000:  # Arbitrary limit
            return QueryValidationResult(
                is_valid=False,
                error_message="Selected text is too long (max 10000 characters)"
            )

        # Sanitize the selected text
        sanitized_text = InputValidator._sanitize_text(selected_text)

        return QueryValidationResult(
            is_valid=True,
            sanitized_query=sanitized_text
        )

    @staticmethod
    def _sanitize_text(text: str) -> str:
        """
        Sanitize text by removing potentially harmful characters.
        """
        # Remove potential SQL injection characters (basic)
        # In a real application, you'd want more sophisticated sanitization
        sanitized = re.sub(r'[<>"\']', '', text)
        return sanitized.strip()

# Global instance
validator = InputValidator()