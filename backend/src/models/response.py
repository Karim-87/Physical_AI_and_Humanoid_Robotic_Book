from sqlalchemy import Column, String, Text, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY
from ..config.database import Base
from datetime import datetime
import uuid


class ChatResponse(Base):
    __tablename__ = "chat_responses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    query_id = Column(String, index=True)  # Foreign key to UserQuery
    response_text = Column(Text)  # AI-generated response
    source_chapters = Column(ARRAY(String))  # IDs of chapters used for response
    confidence_score = Column(Float)  # Confidence level of response
    timestamp = Column(DateTime, default=datetime.utcnow)  # When response was generated
    language = Column(String, default="en")  # Language of the response