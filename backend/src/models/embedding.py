from sqlalchemy import Column, String, Text, DateTime, Float, Index
from sqlalchemy.dialects.postgresql import ARRAY
from ..config.database import Base
from datetime import datetime


class EmbeddingVector(Base):
    __tablename__ = "embedding_vectors"

    id = Column(String, primary_key=True, index=True)
    chapter_id = Column(String, index=True)  # Foreign key to TextbookChapter
    content = Column(Text)  # The text that was embedded
    embedding = Column(ARRAY(Float))  # Vector representation of content (using PostgreSQL ARRAY)
    section_ref = Column(String)  # Reference to specific section in chapter
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of embedding creation

    # Create index on chapter_id for faster lookups
    __table_args__ = (Index('idx_chapter_id', 'chapter_id'),)