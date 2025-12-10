from sqlalchemy import Column, String, DateTime
from ..config.database import Base
from datetime import datetime
import uuid


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True)  # Foreign key to User
    session_token = Column(String, unique=True, index=True)  # Session identifier
    created_at = Column(DateTime, default=datetime.utcnow)  # Session start time
    expires_at = Column(DateTime)  # Session expiration time