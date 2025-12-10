from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..services.auth_service import AuthService
from ..config.database import get_db
from ..config.settings import settings
from pydantic import BaseModel
import json


class RegisterRequest(BaseModel):
    username: str
    email: Optional[str] = None
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UpdatePreferencesRequest(BaseModel):
    preferences: Optional[dict] = None
    language: Optional[str] = None
    personalization_enabled: Optional[bool] = None


router = APIRouter()
auth_service = AuthService()
security = HTTPBearer()


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    try:
        user = auth_service.create_user(
            db=db,
            username=request.username,
            email=request.email or "",
            password=request.password
        )

        return {
            "user_id": user.id,
            "username": user.username,
            "message": "Registration successful"
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during registration: {str(e)}"
        )


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user."""
    try:
        user = auth_service.authenticate_user(
            db=db,
            username=request.username,
            password=request.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = auth_service.create_access_token(
            data={"sub": user.username}
        )

        return {
            "token": access_token,
            "user_id": user.id,
            "username": user.username
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user."""
    # In a real implementation, you might want to invalidate the token
    # For now, we just return a success message
    return {"message": "Successfully logged out"}


@router.get("/preferences")
def get_preferences(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get user preferences."""
    try:
        token = credentials.credentials
        user = auth_service.get_current_user(db, token)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        preferences = json.loads(user.preferences) if user.preferences else {}

        return {
            "preferences": preferences,
            "language": preferences.get("language", "en"),
            "personalization_enabled": preferences.get("personalization_enabled", True)
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving preferences: {str(e)}"
        )


@router.put("/preferences")
def update_preferences(
    request: UpdatePreferencesRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update user preferences."""
    try:
        token = credentials.credentials
        user = auth_service.get_current_user(db, token)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get current preferences and update with new values
        current_preferences = json.loads(user.preferences) if user.preferences else {}

        if request.preferences is not None:
            current_preferences.update(request.preferences)
        if request.language is not None:
            current_preferences["language"] = request.language
        if request.personalization_enabled is not None:
            current_preferences["personalization_enabled"] = request.personalization_enabled

        # Update the user's preferences
        user.preferences = json.dumps(current_preferences)
        db.commit()

        return {"message": "Preferences updated successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating preferences: {str(e)}"
        )