from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from ..services.rag_service import RAGService
from ..services.rate_limit_service import RateLimitService
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
rate_limit_service = RateLimitService()


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

        # Check rate limit
        if not rate_limit_service.is_allowed(db, client_ip):
            remaining_requests = rate_limit_service.get_remaining_requests(db, client_ip)
            reset_time = rate_limit_service.get_reset_time(db, client_ip)

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests from this IP. Limit is {rate_limit_service.requests_limit} requests per hour.",
                    "retry_after": reset_time.isoformat()
                }
            )

        # Process the query
        result = rag_service.process_query(
            db=db,
            query_text=request.query,
            ip_address=client_ip
        )

        # Add rate limit headers to response
        remaining_requests = rate_limit_service.get_remaining_requests(db, client_ip)
        reset_time = rate_limit_service.get_reset_time(db, client_ip)

        # Note: FastAPI doesn't easily allow adding headers in path operations
        # In a real implementation, we'd use a middleware or response_class
        # For now, we'll return rate limit info in the response
        return {
            "result": result,
            "rate_limit_info": {
                "remaining": remaining_requests,
                "reset_time": reset_time.isoformat()
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
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

        # Check rate limit
        if not rate_limit_service.is_allowed(db, client_ip):
            remaining_requests = rate_limit_service.get_remaining_requests(db, client_ip)
            reset_time = rate_limit_service.get_reset_time(db, client_ip)

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests from this IP. Limit is {rate_limit_service.requests_limit} requests per hour.",
                    "retry_after": reset_time.isoformat()
                }
            )

        # Process the selection query
        result = rag_service.process_selection_query(
            db=db,
            selected_text=request.selected_text,
            question=request.question,
            ip_address=client_ip
        )

        # Add rate limit headers to response
        remaining_requests = rate_limit_service.get_remaining_requests(db, client_ip)
        reset_time = rate_limit_service.get_reset_time(db, client_ip)

        # Note: FastAPI doesn't easily allow adding headers in path operations
        # In a real implementation, we'd use a middleware or response_class
        # For now, we'll return rate limit info in the response
        return {
            "result": result,
            "rate_limit_info": {
                "remaining": remaining_requests,
                "reset_time": reset_time.isoformat()
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing selection query: {str(e)}"
        )