from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from ..config.database import Base
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String, unique=True, index=True)  # Unique username
    email = Column(String, unique=True, index=True, nullable=True)  # Email address (optional)
    password_hash = Column(String, nullable=True)  # Hashed password, nullable for OAuth users
    oauth_provider = Column(String, nullable=True)  # OAuth provider name (e.g., 'facebook', 'google')
    oauth_id = Column(String, nullable=True)  # Provider's user ID for OAuth users
    preferences = Column(Text)  # User preferences for personalization as JSON string
    language_preference = Column(String, default="en")  # Default language preference
    personalization_enabled = Column(Boolean, default=True)  # Whether to show personalized content
    is_active = Column(Boolean, default=True)  # Whether account is active
    created_at = Column(DateTime, default=datetime.utcnow)  # Account creation timestamp
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update timestamp
    last_login_at = Column(DateTime, nullable=True)  # Last login timestamp