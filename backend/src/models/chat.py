from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: str = Column(String, primary_key=True, default=generate_uuid)
    user_id: str = Column(String, nullable=True)  # Optional user identifier
    created_at: datetime = Column(DateTime, default=func.now())
    updated_at: datetime = Column(DateTime, default=func.now(), onupdate=func.now())
    active: bool = Column(Boolean, default=True)

    # Relationship to chat messages
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: str = Column(String, primary_key=True, default=generate_uuid)
    session_id: str = Column(String, ForeignKey("chat_sessions.id"))
    role: str = Column(String, nullable=False)  # 'user' or 'assistant'
    content: str = Column(Text, nullable=False)
    timestamp: datetime = Column(DateTime, default=func.now())
    retrieved_chunks: list = Column(ARRAY(String), nullable=True)  # IDs of chunks used in response
    mode: str = Column(String, nullable=True)  # 'full-book' or 'selected-text-only'
    response_time: float = Column(Float, nullable=True)  # Time taken to generate response in seconds

    # Relationship back to session
    session = relationship("ChatSession", back_populates="messages")