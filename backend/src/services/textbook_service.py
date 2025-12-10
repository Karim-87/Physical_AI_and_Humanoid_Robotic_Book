from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.textbook import TextbookChapter
import uuid
import json


class TextbookService:
    def __init__(self):
        pass

    def get_all_chapters(self, db: Session, language: str = "en") -> List[dict]:
        """Get all textbook chapters."""
        chapters = db.query(TextbookChapter).filter(
            TextbookChapter.language == language
        ).order_by(TextbookChapter.order).all()

        result = []
        for chapter in chapters:
            metadata = json.loads(chapter.metadata_json) if chapter.metadata_json else {}
            result.append({
                "id": chapter.id,
                "title": chapter.title,
                "order": chapter.order,
                "language": chapter.language,
                "metadata": metadata
            })

        return result

    def get_chapter_by_id(self, db: Session, chapter_id: str) -> Optional[dict]:
        """Get a specific textbook chapter by ID."""
        chapter = db.query(TextbookChapter).filter(
            TextbookChapter.id == chapter_id
        ).first()

        if not chapter:
            return None

        metadata = json.loads(chapter.metadata_json) if chapter.metadata_json else {}

        return {
            "id": chapter.id,
            "title": chapter.title,
            "content": chapter.content,
            "order": chapter.order,
            "language": chapter.language,
            "metadata": metadata
        }

    def create_chapter(self, db: Session, title: str, content: str, order: int, language: str = "en", metadata: dict = None) -> TextbookChapter:
        """Create a new textbook chapter."""
        chapter = TextbookChapter(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            order=order,
            language=language,
            metadata_json=json.dumps(metadata) if metadata else "{}"
        )

        db.add(chapter)
        db.commit()
        db.refresh(chapter)

        return chapter

    def update_chapter(self, db: Session, chapter_id: str, title: str = None, content: str = None, order: int = None, metadata: dict = None) -> Optional[TextbookChapter]:
        """Update an existing textbook chapter."""
        chapter = db.query(TextbookChapter).filter(
            TextbookChapter.id == chapter_id
        ).first()

        if not chapter:
            return None

        if title is not None:
            chapter.title = title
        if content is not None:
            chapter.content = content
        if order is not None:
            chapter.order = order
        if metadata is not None:
            chapter.metadata_json = json.dumps(metadata)

        db.commit()
        db.refresh(chapter)

        return chapter

    def delete_chapter(self, db: Session, chapter_id: str) -> bool:
        """Delete a textbook chapter."""
        chapter = db.query(TextbookChapter).filter(
            TextbookChapter.id == chapter_id
        ).first()

        if not chapter:
            return False

        db.delete(chapter)
        db.commit()

        return True