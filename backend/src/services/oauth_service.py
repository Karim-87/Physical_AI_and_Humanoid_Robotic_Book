from typing import Optional, Dict, Any
import requests
import uuid
from datetime import datetime
from fastapi import HTTPException, status
from ..config.settings import settings
from ..models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import or_
import json


class OAuthService:
    def __init__(self):
        self.providers = {
            'facebook': {
                'client_id': settings.FACEBOOK_CLIENT_ID,
                'client_secret': settings.FACEBOOK_CLIENT_SECRET,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'auth_url': 'https://www.facebook.com/v18.0/dialog/oauth',
                'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token',
                'user_info_url': 'https://graph.facebook.com/v18.0/me?fields=id,name,email'
            },
            'google': {
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': settings.GOOGLE_REDIRECT_URI,
                'auth_url': 'https://accounts.google.com/oauth/authorize',
                'token_url': 'https://oauth2.googleapis.com/token',
                'user_info_url': 'https://www.googleapis.com/oauth2/v2/userinfo'
            }
        }

    def get_auth_url(self, provider: str, state: str) -> str:
        """Generate OAuth authorization URL for the given provider."""
        if provider not in self.providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported OAuth provider: {provider}"
            )

        provider_config = self.providers[provider]
        auth_url = (
            f"{provider_config['auth_url']}?"
            f"client_id={provider_config['client_id']}&"
            f"redirect_uri={provider_config['redirect_uri']}&"
            f"response_type=code&"
            f"scope=email&"
            f"state={state}"
        )
        return auth_url

    def exchange_code_for_token(self, provider: str, code: str) -> Dict[str, Any]:
        """Exchange OAuth authorization code for access token."""
        if provider not in self.providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported OAuth provider: {provider}"
            )

        provider_config = self.providers[provider]

        # Exchange authorization code for access token
        token_response = requests.post(
            provider_config['token_url'],
            data={
                'client_id': provider_config['client_id'],
                'client_secret': provider_config['client_secret'],
                'redirect_uri': provider_config['redirect_uri'],
                'code': code,
                'grant_type': 'authorization_code'
            }
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to exchange code for token with {provider}"
            )

        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid access token received from {provider}"
            )

        return token_data

    def get_user_info(self, provider: str, access_token: str) -> Dict[str, Any]:
        """Get user information from OAuth provider using access token."""
        if provider not in self.providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported OAuth provider: {provider}"
            )

        provider_config = self.providers[provider]

        # Get user information
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(provider_config['user_info_url'], headers=headers)

        if user_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to get user info from {provider}"
            )

        user_data = user_response.json()
        return user_data

    def get_or_create_oauth_user(self, db: Session, provider: str, oauth_data: Dict[str, Any]) -> tuple[User, bool]:
        """Get existing user or create new user from OAuth data."""
        # Extract user information from OAuth provider
        oauth_id = str(oauth_data.get('id'))
        email = oauth_data.get('email', '')
        name = oauth_data.get('name', oauth_data.get('email', f'user_{uuid.uuid4()}'))

        # Check if user already exists with this OAuth provider
        existing_user = db.query(User).filter(
            User.oauth_provider == provider,
            User.oauth_id == oauth_id
        ).first()

        if existing_user:
            # Update last login time
            existing_user.last_login_at = datetime.utcnow()
            db.commit()
            return existing_user, False  # Not a new user

        # Check if user exists with the same email but different provider
        existing_user_by_email = db.query(User).filter(
            User.email == email
        ).first()

        if existing_user_by_email:
            # Link the OAuth account to the existing email-based account
            existing_user_by_email.oauth_provider = provider
            existing_user_by_email.oauth_id = oauth_id
            existing_user_by_email.last_login_at = datetime.utcnow()
            db.commit()
            return existing_user_by_email, False  # Not a new user

        # Create a new user
        user = User(
            id=str(uuid.uuid4()),
            username=name[:50],  # Limit username length
            email=email,
            oauth_provider=provider,
            oauth_id=oauth_id,
            preferences=json.dumps({
                "language": "en",
                "personalization_enabled": True
            }),
            last_login_at=datetime.utcnow()
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user, True  # New user created