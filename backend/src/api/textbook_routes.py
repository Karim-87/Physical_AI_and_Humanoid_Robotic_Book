from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from ..services.textbook_service import TextbookService
from ..config.database import get_db
from ..models.textbook import TextbookChapter


router = APIRouter()
textbook_service = TextbookService()


@router.get("/chapters", response_model=List[dict])
def get_all_chapters(
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Get list of all textbook chapters."""
    try:
        chapters = textbook_service.get_all_chapters(db, language)
        return chapters
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving chapters: {str(e)}"
        )


@router.get("/chapters/{chapter_id}", response_model=dict)
def get_chapter_by_id(
    chapter_id: str,
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Get specific chapter content."""
    try:
        # First try to get the chapter in the requested language
        chapter = db.query(TextbookChapter).filter(
            TextbookChapter.id == chapter_id,
            TextbookChapter.language == language
        ).first()

        # If not found in requested language, fall back to English
        if not chapter and language != "en":
            chapter = db.query(TextbookChapter).filter(
                TextbookChapter.id == chapter_id,
                TextbookChapter.language == "en"
            ).first()

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )

        chapter_dict = {
            "id": chapter.id,
            "title": chapter.title,
            "content": chapter.content,
            "order": chapter.order,
            "language": chapter.language,
            "metadata": json.loads(chapter.metadata_json) if chapter.metadata_json else {}
        }
        return chapter_dict
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving chapter: {str(e)}"
        )


@router.post("/translate", response_model=dict)
def translate_chapter_content(
    content: str,
    target_language: str,
    source_language: str = "en",
    db: Session = Depends(get_db)
):
    """Translate chapter content to target language."""
    try:
        # In a real implementation, this would use a translation API
        # For now, we'll return the original content as placeholder
        # In the actual implementation, you'd integrate with Google Translate API,
        # Azure Translator, or similar service
        translated_content = f"**Translated to {target_language}:**\n\n{content}"
        return {
            "original_content": content,
            "translated_content": translated_content,
            "source_language": source_language,
            "target_language": target_language
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error translating content: {str(e)}"
        )