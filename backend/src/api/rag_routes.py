from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from ..services.rag_service import RAGService
from ..config.database import get_db
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    language: Optional[str] = "en"
    context: Optional[str] = None


class SelectionQueryRequest(BaseModel):
    selected_text: str
    question: Optional[str] = None


router = APIRouter()
rag_service = RAGService()


@router.post("/query")
def query_rag(
    request: QueryRequest,
    db: Session = Depends(get_db),
    req: Request = None
):
    """Submit a query to the RAG system."""
    try:
        # Get the client IP for rate limiting
        client_ip = req.client.host if req else "127.0.0.1"

        # Process the query
        result = rag_service.process_query(
            db=db,
            query_text=request.query,
            ip_address=client_ip
        )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.post("/query-by-selection")
def query_by_selection(
    request: SelectionQueryRequest,
    db: Session = Depends(get_db),
    req: Request = None
):
    """Submit a query based on selected text."""
    try:
        # Get the client IP for rate limiting
        client_ip = req.client.host if req else "127.0.0.1"

        # Process the selection query
        result = rag_service.process_selection_query(
            db=db,
            selected_text=request.selected_text,
            question=request.question,
            ip_address=client_ip
        )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing selection query: {str(e)}"
        )