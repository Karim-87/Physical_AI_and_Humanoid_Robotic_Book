import asyncio
import requests
import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Any
import logging
from tqdm.asyncio import tqdm
import time
from src.config.qdrant_config import qdrant_service
from src.config.cohere_config import cohere_service
from src.utils.text_processing import extract_text_from_html, clean_text, chunk_text
from src.config.settings import settings

logger = logging.getLogger(__name__)

class TextbookIngestion:
    def __init__(self):
        self.sitemap_url = settings.sitemap_url
        self.processed_pages = 0
        self.created_chunks = 0

    async def initialize_services(self):
        """Initialize all required services"""
        # Initialize Qdrant
        await qdrant_service.initialize()
        logger.info("Qdrant service initialized")

        # Initialize Cohere
        cohere_service.initialize()
        logger.info("Cohere service initialized")

    def fetch_sitemap(self) -> List[str]:
        """Fetch and parse the sitemap to get all page URLs"""
        try:
            response = requests.get(self.sitemap_url)
            response.raise_for_status()

            root = ET.fromstring(response.content)

            # Find all URLs in the sitemap
            urls = []
            for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                page_url = url.text.strip()

                # Filter for textbook content pages, exclude non-content pages
                if (not any(exclude in page_url for exclude in ['/blog', '/docs', '/api']) and
                    'physical-ai-and-humanoid-robotic-bo-three.vercel.app' in page_url):
                    urls.append(page_url)

            logger.info(f"Found {len(urls)} URLs in sitemap")
            return urls
        except Exception as e:
            logger.error(f"Failed to fetch sitemap: {e}")
            return []

    def fetch_page_content(self, url: str) -> Dict[str, Any]:
        """Fetch and extract content from a single page"""
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Extract title from HTML
            title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
            title = title_match.group(1) if title_match else "Untitled"

            # Extract clean text content
            clean_content = extract_text_from_html(response.text)
            clean_content = clean_text(clean_content)

            return {
                "url": url,
                "title": title,
                "content": clean_content
            }
        except Exception as e:
            logger.error(f"Failed to fetch content from {url}: {e}")
            return None

    async def process_page(self, url: str) -> List[Dict[str, Any]]:
        """Process a single page: fetch content, chunk, embed, and store"""
        page_data = self.fetch_page_content(url)
        if not page_data or not page_data["content"]:
            return []

        # Chunk the content
        chunks = chunk_text(
            page_data["content"],
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap
        )

        processed_chunks = []
        for i, chunk_text in enumerate(chunks):
            chunk_id = f"{page_data['url']}_chunk_{i}"

            # Create payload for Qdrant
            payload = {
                "text": chunk_text,
                "source": page_data["url"],
                "title": page_data["title"],
                "chunk_index": i
            }

            processed_chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "payload": payload
            })

        return processed_chunks

    async def embed_and_store_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Generate embeddings for chunks and store in Qdrant"""
        if not chunks:
            return 0

        # Extract texts for embedding
        texts = [chunk["text"] for chunk in chunks]

        # Generate embeddings
        try:
            embeddings = cohere_service.embed_text(texts)
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return 0

        # Prepare points for Qdrant
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            points.append({
                "id": chunk["id"],
                "vector": embedding,
                "payload": chunk["payload"]
            })

        # Upload to Qdrant
        try:
            qdrant_service.client.upsert(
                collection_name=qdrant_service.collection_name,
                points=points
            )
            return len(points)
        except Exception as e:
            logger.error(f"Failed to upload to Qdrant: {e}")
            return 0

    async def ingest_all_pages(self, max_pages: int = None):
        """Main ingestion pipeline"""
        logger.info("Starting ingestion pipeline...")

        # Initialize services
        await self.initialize_services()

        # Fetch URLs from sitemap
        urls = self.fetch_sitemap()
        if max_pages:
            urls = urls[:max_pages]

        logger.info(f"Processing {len(urls)} pages...")

        # Process pages with progress bar
        tasks = []
        for url in urls:
            task = self.process_page(url)
            tasks.append(task)

        all_chunks = []
        for coro in tqdm.as_completed(tasks, desc="Processing pages"):
            page_chunks = await coro
            all_chunks.extend(page_chunks)
            self.processed_pages += 1

            # Batch upload to Qdrant every 100 chunks to avoid memory issues
            if len(all_chunks) >= 100:
                uploaded_count = await self.embed_and_store_chunks(all_chunks[:100])
                self.created_chunks += uploaded_count
                all_chunks = all_chunks[100:]

        # Upload remaining chunks
        if all_chunks:
            uploaded_count = await self.embed_and_store_chunks(all_chunks)
            self.created_chunks += uploaded_count

        logger.info(f"Ingestion completed: {self.processed_pages} pages processed, {self.created_chunks} chunks created")

async def main():
    ingestion = TextbookIngestion()
    await ingestion.ingest_all_pages()

if __name__ == "__main__":
    asyncio.run(main())