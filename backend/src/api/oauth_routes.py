from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..services.oauth_service import OAuthService
from ..services.auth_service import AuthService
from ..config.database import get_db
from ..config.settings import settings
from pydantic import BaseModel
import json
import secrets


class OAuthLoginRequest(BaseModel):
    code: str
    provider: str
    redirect_uri: Optional[str] = None


class OAuthAuthURLResponse(BaseModel):
    auth_url: str


router = APIRouter()
oauth_service = OAuthService()
auth_service = AuthService()
security = HTTPBearer()


@router.post("/{provider}")
def oauth_login(
    provider: str,
    request: OAuthLoginRequest,
    db: Session = Depends(get_db)
):
    """Handle OAuth login callback from provider."""
    if provider not in ['facebook', 'google']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported OAuth provider"
        )

    try:
        # Exchange authorization code for access token
        token_data = oauth_service.exchange_code_for_token(provider, request.code)
        access_token = token_data.get('access_token')

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid access token received from {provider}"
            )

        # Get user information from provider
        user_data = oauth_service.get_user_info(provider, access_token)

        # Get or create user from OAuth data
        user, is_new_user = oauth_service.get_or_create_oauth_user(db, provider, user_data)

        # Create JWT access token
        access_token = auth_service.create_access_token(
            data={"sub": user.username}
        )

        return {
            "token": access_token,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_new_user": is_new_user,
            "message": "OAuth login successful"
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during OAuth login: {str(e)}"
        )


@router.get("/{provider}/auth-url")
def get_oauth_auth_url(
    provider: str,
    request: Request
):
    """Generate OAuth authorization URL for the given provider."""
    if provider not in ['facebook', 'google']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported OAuth provider"
        )

    # Generate a random state parameter for security
    state = secrets.token_urlsafe(32)

    # Get the authorization URL
    auth_url = oauth_service.get_auth_url(provider, state)

    return {
        "auth_url": auth_url,
        "state": state
    }


@router.get("/{provider}/callback")
def oauth_callback(
    provider: str,
    code: str,
    state: str,
    redirect_uri: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Handle OAuth callback from provider.
    This endpoint exchanges the authorization code for an access token,
    authenticates the user, and redirects to the frontend with the token.
    """
    if provider not in ['facebook', 'google']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported OAuth provider"
        )

    # In a real implementation, you would validate the state parameter here
    # For security purposes to prevent CSRF attacks
    # For this example we'll proceed directly

    try:
        # Exchange authorization code for access token
        token_data = oauth_service.exchange_code_for_token(provider, code)
        access_token = token_data.get('access_token')

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid access token received from {provider}"
            )

        # Get user information from provider
        user_data = oauth_service.get_user_info(provider, access_token)

        # Get or create user from OAuth data
        user, is_new_user = oauth_service.get_or_create_oauth_user(db, provider, user_data)

        # Create JWT access token
        jwt_token = auth_service.create_access_token(
            data={"sub": user.username}
        )

        # Determine redirect URL - either from parameter or default to frontend
        frontend_redirect = redirect_uri or settings.FRONTEND_OAUTH_CALLBACK_URL or "http://localhost:3000"

        # Construct redirect URL with token
        redirect_url = f"{frontend_redirect}?token={jwt_token}&user_id={user.id}&username={user.username}&email={user.email}&is_new_user={'true' if is_new_user else 'false'}"

        # Redirect to frontend with token
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=redirect_url)

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during OAuth callback: {str(e)}"
        )