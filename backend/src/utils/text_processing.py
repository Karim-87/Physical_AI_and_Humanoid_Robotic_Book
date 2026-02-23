import re
from typing import List, Tuple
from bs4 import BeautifulSoup
from src.config.settings import settings

def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """
    Estimate the number of tokens in a text.
    Uses a word-based approximation (~1.3 tokens per word).
    """
    words = text.split()
    return int(len(words) * 1.3)

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 200) -> List[str]:
    """
    Split text into chunks of specified size with overlap.

    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk (in tokens)
        overlap: Number of tokens to overlap between chunks

    Returns:
        List of text chunks
    """
    # First, we'll split by sentences to try to maintain semantic coherence
    sentences = re.split(r'[.!?]+\s+', text)

    chunks = []
    current_chunk = ""
    current_token_count = 0

    for sentence in sentences:
        # Estimate token count for this sentence
        sentence_token_count = count_tokens(sentence)

        # If adding this sentence would exceed chunk size
        if current_token_count + sentence_token_count > chunk_size:
            # If current chunk is not empty, add it to chunks
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # Start a new chunk with this sentence
            # If sentence is too long by itself, we'll need to split it further
            if sentence_token_count > chunk_size:
                # Split the long sentence into smaller pieces
                sub_chunks = split_long_text(sentence, chunk_size, overlap)
                chunks.extend(sub_chunks[:-1])  # Add all but the last chunk
                # The last chunk becomes our current chunk
                current_chunk = sub_chunks[-1] if sub_chunks else ""
                current_token_count = count_tokens(current_chunk) if current_chunk else 0
            else:
                current_chunk = sentence
                current_token_count = sentence_token_count
        else:
            # Add sentence to current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
            current_token_count += sentence_token_count

    # Add the final chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Add overlap by including some content from previous chunk
    if overlap > 0 and len(chunks) > 1:
        chunks_with_overlap = [chunks[0]]  # First chunk has no previous

        for i in range(1, len(chunks)):
            prev_chunk = chunks[i-1]
            curr_chunk = chunks[i]

            # Get the end portion of the previous chunk for overlap
            prev_end = get_token_subset(prev_chunk, overlap // 2)
            curr_start = get_token_subset(curr_chunk, overlap // 2)

            # Combine with overlap
            overlap_chunk = prev_end + " " + curr_chunk
            chunks_with_overlap.append(overlap_chunk.strip())

        return chunks_with_overlap

    return chunks

def get_token_subset(text: str, token_count: int) -> str:
    """
    Get a subset of text containing approximately token_count tokens.
    Uses word-based approximation.
    """
    words = text.split()
    # Approximate: ~1.3 tokens per word, so word_count ~ token_count / 1.3
    word_count = max(1, int(token_count / 1.3))
    subset_words = words[:word_count]
    return " ".join(subset_words)

def split_long_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Split a long text into smaller chunks when it exceeds chunk_size.
    """
    if count_tokens(text) <= chunk_size:
        return [text]

    # Split by characters as a fallback
    words = text.split()
    chunks = []
    current_chunk = []
    current_token_count = 0

    for word in words:
        word_token_count = count_tokens(word)

        if current_token_count + word_token_count > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                # Add overlap with the beginning of the next chunk
                if len(chunks) > 0 and overlap > 0:
                    # Use the last part of the current chunk as overlap
                    overlap_text = " ".join(current_chunk[-max(overlap//2, 1):])
                    current_chunk = [overlap_text, word]
                    current_token_count = count_tokens(" ".join(current_chunk))
                else:
                    current_chunk = [word]
                    current_token_count = word_token_count
            else:
                current_chunk = [word]
                current_token_count = word_token_count
        else:
            current_chunk.append(word)
            current_token_count += word_token_count

    # Add the final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def extract_text_from_html(html_content: str) -> str:
    """
    Extract clean text content from HTML, removing navigation, headers, footers, etc.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove common navigation and structural elements
    for element in soup(['nav', 'header', 'footer', 'aside', 'script', 'style']):
        element.decompose()

    # Remove elements with common class names for navigation, ads, etc.
    for element in soup.find_all(class_=re.compile(r'nav|menu|sidebar|footer|header|ads|advertisement')):
        element.decompose()

    # Get the cleaned text
    text = soup.get_text()

    # Clean up the text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    return text

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra whitespace and normalizing.
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters that might be artifacts from HTML parsing
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

    return text.strip()