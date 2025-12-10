#!/usr/bin/env python3
"""
Script to load textbook content into the database and create embeddings for both English and Urdu.
This script reads the markdown files from the frontend docs directory, creates database entries,
and generates embeddings for the RAG system.
"""

import os
import sys
import uuid
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import json

# Add backend src to path to import modules
backend_src_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_src_path)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import get_db
from src.config.settings import settings
from src.models.textbook import TextbookChapter
from src.services.textbook_service import TextbookService
from src.services.embedding_service import EmbeddingService


def extract_content_from_markdown(file_path):
    """Extract plain text content from markdown file, removing frontmatter and formatting."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove frontmatter (content between ---)
    lines = content.split('\n')
    if lines[0].strip() == '---':
        # Find the end of frontmatter
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                content = '\n'.join(lines[i+1:])
                break

    # Convert markdown to plain text to get content without formatting
    html = markdown.markdown(content)
    soup = BeautifulSoup(html, 'html.parser')
    plain_text = soup.get_text()

    return plain_text.strip()


def split_content_into_chunks(content, max_chunk_size=1000):
    """Split content into smaller chunks for better embedding."""
    chunks = []
    paragraphs = content.split('\n\n')

    current_chunk = ""
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) < max_chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def load_textbook_content():
    """Load textbook content from markdown files into database and create embeddings."""

    # Create database engine and session
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Initialize services
    textbook_service = TextbookService()
    embedding_service = EmbeddingService()

    # Define chapter order and file mapping
    chapters = [
        {"order": 1, "file": "intro-to-physical-ai.md", "title": "Introduction to Physical AI"},
        {"order": 2, "file": "basics-humanoid-robotics.md", "title": "Basics of Humanoid Robotics"},
        {"order": 3, "file": "ros2-fundamentals.md", "title": "ROS 2 Fundamentals"},
        {"order": 4, "file": "digital-twin-simulation.md", "title": "Digital Twin Simulation (Gazebo + Isaac)"},
        {"order": 5, "file": "vision-language-action.md", "title": "Vision-Language-Action Systems"},
        {"order": 6, "file": "capstone-pipeline.md", "title": "Capstone: Simple AI-Robot Pipeline"}
    ]

    # Define the path to the frontend docs directory
    docs_path = Path(__file__).parent.parent.parent / "frontend" / "docusaurus" / "docs"

    print("Loading textbook content into database...")

    with SessionLocal() as db:
        # Clear existing chapters to avoid duplicates
        db.query(TextbookChapter).delete()
        db.commit()

        for chapter_info in chapters:
            file_path = docs_path / chapter_info["file"]

            if not file_path.exists():
                print(f"Warning: File {file_path} does not exist, skipping...")
                continue

            print(f"Processing {chapter_info['file']}...")

            # Load English content
            english_content = extract_content_from_markdown(file_path)

            # Create English chapter
            english_chapter = textbook_service.create_chapter(
                db=db,
                title=chapter_info["title"],
                content=english_content,
                order=chapter_info["order"],
                language="en",
                metadata={"original_file": chapter_info["file"]}
            )

            # Create embeddings for English content
            english_chunks = split_content_into_chunks(english_content)
            print(f"  Creating {len(english_chunks)} embeddings for English content...")
            embedding_service.batch_store_embeddings(
                chapter_id=english_chapter.id,
                language="en",
                contents=english_chunks,
                section_refs=[f"{chapter_info['title']}_chunk_{i}" for i in range(len(english_chunks))]
            )

            # Load actual Urdu content from file
            urdu_content = load_urdu_content_from_file(chapter_info["file"])

            # Create Urdu chapter
            urdu_chapter = textbook_service.create_chapter(
                db=db,
                title=chapter_info["title"],  # Title will be translated in the frontend
                content=urdu_content,
                order=chapter_info["order"],
                language="ur",
                metadata={"original_file": chapter_info["file"], "translated": True}
            )

            # Create embeddings for Urdu content
            urdu_chunks = split_content_into_chunks(urdu_content)
            print(f"  Creating {len(urdu_chunks)} embeddings for Urdu content...")
            embedding_service.batch_store_embeddings(
                chapter_id=urdu_chapter.id,
                language="ur",
                contents=urdu_chunks,
                section_refs=[f"{chapter_info['title']}_urdu_chunk_{i}" for i in range(len(urdu_chunks))]
            )

            print(f"  Created chapters: English ID {english_chapter.id}, Urdu ID {urdu_chapter.id}")

    print("Textbook content loaded successfully!")


def create_urdu_translation(english_content):
    """Create a placeholder Urdu translation of the English content.

    In a real implementation, this would call a translation API like Google Translate.
    For now, we'll return a simple placeholder with the original content marked as translated.
    """
    # This is a placeholder - in a real implementation, you would use a translation API
    # For now, we'll create some basic Urdu text that explains this is a placeholder
    placeholder_urdu = f"""
**یہ ایک مقامی ترجمہ ہے:**\n
This is a placeholder translation for the content below. In the full implementation,
this would contain the actual Urdu translation of the textbook content.\n
\n
اصل انگریزی مواد:\n
{english_content[:500]}...  # First 500 chars of original content as reference
"""
    return placeholder_urdu


def load_urdu_content_from_file(chapter_file):
    """Load actual Urdu content from the corresponding Urdu file."""
    urdu_docs_path = Path(__file__).parent.parent.parent / "frontend" / "docusaurus" / "docs" / "ur"

    # Map English file names to Urdu file names
    urdu_file_path = urdu_docs_path / chapter_file

    if urdu_file_path.exists():
        with open(urdu_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove frontmatter (content between ---)
        lines = content.split('\n')
        if lines[0].strip() == '---':
            # Find the end of frontmatter
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    content = '\n'.join(lines[i+1:])
                    break

        return content.strip()
    else:
        # If Urdu file doesn't exist, return the placeholder
        return create_urdu_translation("Placeholder for " + chapter_file)


def load_actual_urdu_content():
    """Load actual Urdu content if available in a separate directory."""
    # Check if there's a urdu content directory
    urdu_docs_path = Path(__file__).parent.parent.parent / "frontend" / "docusaurus" / "i18n" / "ur" / "docusaurus-plugin-content-docs" / "current"

    if not urdu_docs_path.exists():
        # Try alternative location
        urdu_docs_path = Path(__file__).parent.parent.parent / "frontend" / "docusaurus" / "docs" / "ur"

    if urdu_docs_path.exists():
        print(f"Found Urdu content at {urdu_docs_path}")
        # Process Urdu content files here
        return True
    else:
        print("No dedicated Urdu content found, using placeholder translations")
        return False


if __name__ == "__main__":
    print("Starting textbook content loader...")

    # Check for actual Urdu content
    has_urdu_content = load_actual_urdu_content()

    # Load the content
    load_textbook_content()

    print("Content loading complete!")