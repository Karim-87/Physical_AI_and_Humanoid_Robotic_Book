# Feature Specification: Backend RAG Chatbot for Physical AI and Humanoid Robotics Textbook

**Feature Branch**: `005-backend-rag-chatbot`
**Created**: 2025-12-26
**Status**: Draft
**Input**: User description: "/sp.specify I have already completed the frontend (Docusaurus-based textbook on Physical AI and Humanoid Robotics) deployed at https://physical-ai-and-humanoid-robotic-bo-three.vercel.app/sitemap.xml. Now, continue building the backend for Part 2: the integrated RAG chatbot.

Follow these exact steps in sequence:

1. In the root directory, create a new folder named 'backend' if it doesn't already exist.

2. Inside the 'backend' folder, initialize a new Python project using uv: run the command `uv init` (this sets up pyproject.toml, .gitattributes, etc.).

3. Use the deployed site's sitemap URL (https://physical-ai-and-humanoid-robotic-bo-three.vercel.app/sitemap.xml) to crawl and extract the main content/pages of the book. Parse the sitemap, fetch each linked page, clean the text (remove navigation, footers, scripts, etc.), and chunk it into suitable pieces for embedding (e.g., 500-1000 tokens per chunk with overlap).

4. Generate embeddings for these text chunks using the Cohere embedding model (use Cohere's embed-english-v3.0 or similar multilingual/English model suitable for technical content). Install necessary packages via uv (e.g., cohere, requests, beautifulsoup4 for scraping). Store the embeddings + metadata (source URL, chunk text, page title) in Qdrant Cloud Free Tier. Create a collection in Qdrant, upload the vectors, and use appropriate distance metric (e.g., Cosine).

5. After ingestion, implement a simple retrieval test pipeline: write a Python script or function that takes a sample query (e.g., \"What is Physical AI?\"), embeds it with Cohere, searches Qdrant for top-k similar chunks, and prints the retrieved texts to verify the pipeline works correctly.

6. Build a RAG-capable agent using the OpenAI Agents SDK (https://openai.github.io/openai-agents-python/). Since we need to use GEMINI_API_KEY, configure the agent to use Gemini via its OpenAI-compatible endpoint: create an AsyncOpenAI client with base_url=\"https://generativelanguage.googleapis.com/v1beta/openai/\" and your GEMINI_API_KEY. Then use OpenAIChatCompletionsModel(model=\"gemini-1.5-flash\" or latest available like \"gemini-2.0-flash\", openai_client=your_client). Integrate retrieval as a tool: create a @function_tool that takes a user query (and optionally selected text), embeds it with Cohere, queries Qdrant, and returns top relevant chunks as context. The agent should use this tool for book-related questions. For questions based only on user-selected text, add logic to embed and retrieve only from that provided text (bypass Qdrant or use a separate in-memory index). Also integrate Neon Serverless Postgres (using asyncpg or SQLAlchemy) to store e.g. chat sessions, query logs, or user-selected text history. Use uv to add dependencies (openai-agents, litellm if needed for extra compatibility, qdrant-client, cohere, python-dotenv, fastapi, uvicorn, etc.).

7. Build a FastAPI application in the backend folder that exposes endpoints like /chat (POST) to receive user messages (and optional selected_text), runs the agent with retrieval, and returns the response (support streaming if possible). Include CORS middleware to allow requests from the frontend (Vercel URL). For local integration/testing, the frontend can call http://localhost:8000/chat (or wherever FastAPI runs). Provide instructions on how to run the FastAPI server (uv run uvicorn main:app --reload).

8. Create a .env file in the backend folder (and add to .gitignore) to securely load all credentials: GEMINI_API_KEY, COHERE_API_KEY, QDRANT_API_KEY and QDRANT_URL (from Qdrant Cloud dashboard), NEON_DATABASE_URL (connection string from Neon dashboard). Use python-dotenv to load them in code. Never hardcode keys.

Generate the necessary folder structure, key code files (e.g., ingestion.py for steps 3-5, app.py for FastAPI + agent, tools.py for retrieval tool, models.py if needed, .env.example), and detailed step-by-step terminal commands to set everything up and test. Ensure the system supports both full-book RAG and selected-text-only mode. Use best practices for error handling, async where appropr"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions About Textbook Content (Priority: P1)

A student reading the Physical AI and Humanoid Robotics textbook wants to ask questions about the content to get immediate, accurate answers based on the textbook material. The student selects text on a page or types a question about the textbook content, and the RAG chatbot retrieves relevant information from the textbook and generates a helpful response.

**Why this priority**: This is the core value proposition of the feature - enabling students to get answers to their questions directly from the textbook content, enhancing their learning experience.

**Independent Test**: The system can independently answer textbook-related questions by retrieving relevant content from the vector database and generating responses, delivering immediate educational value to students.

**Acceptance Scenarios**:

1. **Given** the RAG chatbot is integrated with the textbook content, **When** a student asks a question about Physical AI concepts, **Then** the system returns an accurate response based on the textbook material with proper context.
2. **Given** a student has selected specific text on the textbook page, **When** they ask a question about that selected text, **Then** the system focuses its response on the selected content rather than the full textbook.
3. **Given** the student asks a question that doesn't match textbook content, **When** the system processes the query, **Then** it provides a helpful response indicating the limitation and suggesting related topics from the textbook.

---

### User Story 2 - Access RAG Chatbot Through Frontend Integration (Priority: P2)

A student browsing the Physical AI and Humanoid Robotics textbook on the frontend website wants to interact with the RAG chatbot without leaving the textbook interface. The frontend seamlessly integrates with the backend RAG service to provide a cohesive learning experience.

**Why this priority**: Essential for user adoption - the chatbot must be easily accessible from within the textbook interface to provide a seamless learning experience.

**Independent Test**: The frontend can independently connect to the backend RAG service and display responses to user queries, providing a complete user experience without requiring separate tools.

**Acceptance Scenarios**:

1. **Given** the student is viewing a textbook page, **When** they interact with the chatbot interface, **Then** the system responds without requiring navigation to a separate page or application.
2. **Given** the frontend makes requests to the backend RAG service, **When** the backend processes these requests, **Then** responses are returned in a format that can be properly displayed in the frontend.

---

### User Story 3 - System Maintains Reliable Content Indexing (Priority: P3)

An administrator or content manager needs to ensure that the RAG chatbot has access to the most current textbook content. The system must reliably crawl, process, and index the textbook content from the deployed site.

**Why this priority**: Ensures the chatbot remains accurate and up-to-date as the textbook content evolves, maintaining long-term educational value.

**Independent Test**: The system can independently crawl the textbook site, extract content, generate embeddings, and store them in the vector database, creating a complete knowledge base without manual intervention.

**Acceptance Scenarios**:

1. **Given** the textbook content has been updated on the deployed site, **When** the content crawling process runs, **Then** the vector database is updated with the new content.
2. **Given** the system has access to the sitemap, **When** the crawling process begins, **Then** all relevant textbook pages are processed and indexed.

---

### Edge Cases

- What happens when the Qdrant vector database is temporarily unavailable?
- How does the system handle extremely long user queries or selected text?
- What happens when the student asks about content that isn't in the textbook?
- How does the system handle concurrent users accessing the chatbot simultaneously?
- What happens when the API keys for Cohere, Gemini, or Qdrant are invalid or expired?
- How does the system handle malformed HTML or content that can't be properly extracted from the textbook pages?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST crawl and extract content from the deployed textbook site using the provided sitemap URL (https://physical-ai-and-humanoid-robotic-bo-three.vercel.app/sitemap.xml)
- **FR-002**: System MUST parse the sitemap and fetch each linked page to extract textbook content
- **FR-003**: System MUST clean the extracted text by removing navigation, footers, scripts, and other non-content elements
- **FR-004**: System MUST chunk the cleaned text into suitable pieces for embedding (500-1000 tokens per chunk with overlap)
- **FR-005**: System MUST generate embeddings for text chunks using the Cohere embedding model (embed-english-v3.0 or similar)
- **FR-006**: System MUST store embeddings and metadata (source URL, chunk text, page title) in Qdrant Cloud with appropriate distance metric (Cosine)
- **FR-007**: System MUST provide a retrieval test pipeline that can take sample queries, embed them, search Qdrant, and return relevant chunks
- **FR-008**: System MUST build a RAG-capable agent using the OpenAI Agents SDK that integrates with Gemini via OpenAI-compatible endpoint
- **FR-009**: System MUST implement a retrieval tool that takes user queries, embeds them with Cohere, queries Qdrant, and returns top relevant chunks as context
- **FR-010**: System MUST support both full-book RAG mode and selected-text-only mode for different query contexts
- **FR-011**: System MUST store chat sessions, query logs, and user-selected text history in Neon Serverless Postgres database
- **FR-012**: System MUST expose a FastAPI endpoint at /chat (POST) to receive user messages and optional selected text
- **FR-013**: System MUST support streaming responses for improved user experience when possible
- **FR-014**: System MUST include CORS middleware to allow requests from the frontend Vercel URL
- **FR-015**: System MUST securely load credentials from environment variables without hardcoding them
- **FR-016**: System MUST handle errors gracefully and provide appropriate error responses to users

### Key Entities

- **Textbook Content**: Represents the educational material from the Physical AI and Humanoid Robotics textbook, including pages, sections, and their textual content
- **Text Chunks**: Represents segments of textbook content that have been processed and prepared for embedding, with associated metadata (source URL, chunk text, page title)
- **Embeddings**: Represents vector representations of text chunks that enable semantic similarity search in the vector database
- **Chat Session**: Represents a conversation between a user and the RAG chatbot, including query history and context
- **Query Log**: Represents records of user questions and system responses for analytics and improvement purposes
- **Selected Text**: Represents user-selected content from textbook pages that can be used for focused Q&A sessions

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can receive relevant answers to textbook-related questions within 5 seconds of submitting their query
- **SC-002**: The system successfully indexes at least 95% of the textbook content available in the sitemap without manual intervention
- **SC-003**: 90% of user queries receive contextually appropriate responses based on the textbook content
- **SC-004**: The RAG chatbot maintains a 99% uptime during peak usage hours (8 AM - 10 PM)
- **SC-005**: Students report a 70% improvement in their ability to find answers to textbook questions compared to manual searching
- **SC-006**: The system can handle at least 100 concurrent users without degradation in response time
- **SC-007**: Content extraction and indexing process completes within 30 minutes for the entire textbook
- **SC-008**: The system achieves at least 80% accuracy in retrieving relevant textbook content for sample questions during testing