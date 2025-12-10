from sqlalchemy import Column, Integer, String, DateTime, Text
from ..config.database import Base
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String, unique=True, index=True)  # Unique username
    email = Column(String, unique=True, index=True, nullable=True)  # Email address (optional)
    password_hash = Column(String)  # Hashed password
    preferences = Column(Text)  # User preferences for personalization as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)  # Account creation timestamp