from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from ..config.database import Base


class TextbookChapter(Base):
    __tablename__ = "textbook_chapters"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)  # Chapter content in markdown format
    order = Column(Integer)  # Sequence number for navigation
    language = Column(String, default="en")  # Language code (e.g., 'en', 'ur')
    metadata_json = Column(Text)  # Additional information like word count, reading time as JSON string