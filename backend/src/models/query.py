from sqlalchemy import Column, String, Text, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY
from ..config.database import Base
from datetime import datetime
import uuid


class UserQuery(Base):
    __tablename__ = "user_queries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True, nullable=True)  # Foreign key to User, null for anonymous
    query_text = Column(Text)  # The original query
    query_embedding = Column(ARRAY(Float), nullable=True)  # Vector representation of query (using PostgreSQL ARRAY)
    timestamp = Column(DateTime, default=datetime.utcnow)  # When query was made
    ip_address = Column(String, index=True)  # IP address for rate limiting
    language = Column(String, default="en")  # Language of the query