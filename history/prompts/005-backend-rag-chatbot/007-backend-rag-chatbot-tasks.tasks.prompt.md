---
id: 007
title: Backend RAG Chatbot Tasks
stage: tasks
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-rag-chatbot
branch: 005-backend-rag-chatbot
user: Claude Sonnet 4.5
command: /sp.tasks
labels: [tasks,rag,chatbot,backend,education,implementation]
links:
  spec: specs/005-backend-rag-chatbot/spec.md
  plan: specs/005-backend-rag-chatbot/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-backend-rag-chatbot/tasks.md
tests:
 - specs/005-backend-rag-chatbot/tasks.md
---

## Prompt

Implement the backend for the integrated RAG chatbot in the "Physical AI and Humanoid Robotics" hackathon project. The frontend Docusaurus site is already deployed at https://physical-ai-and-humanoid-robotic-bo-three.vercel.app (sitemap: https://physical-ai-and-humanoid-robotic-bo-three.vercel.app/sitemap.xml).

Break this into clear, sequential, actionable tasks that can be completed one by one. Each task should be self-contained with a description, expected output/files created or modified, and any necessary terminal commands or code outlines.

**Task 1: Set up the backend folder and uv project**
- Create a folder named `backend` in the root directory.
- Navigate into `backend` and initialize a uv project: `uv init`.
- Create a `.gitignore` inside `backend` (if not auto-created) and add `/venv`, `__pycache__`, `.env`.
- Create a `.env` file with placeholders for: GEMINI_API_KEY, COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY, NEON_DATABASE_URL.
- Create an empty `.env` file (do not commit real keys).
- Output: Folder structure with `backend/pyproject.toml`, `backend/.env`, `backend/.gitignore`.

**Task 2: Install required dependencies via uv**
- Inside `backend`, add the following packages using `uv add`:
  - fastapi, uvicorn[standard], python-dotenv, requests, beautifulsoup4, lxml, tqdm
  - cohere
  - qdrant-client
  - openai-agents (or openai-agents-python if that's the package name)
  - asyncpg, sqlalchemy[asyncio], pydantic
  - httpx (for async requests if needed)
- Also add any optional but helpful: langchain-text-splitters (for better chunking), tiktoken (for token counting).
- Output: Updated `pyproject.toml` with all dependencies listed.

**Task 3: Implement content ingestion pipeline**
- Create `ingestion.py` inside `backend`.
- Write code to:
  - Fetch and parse the sitemap.xml.
  - Extract all <loc> URLs (filter only book content pages, exclude /blog, /docs if needed).
  - For each URL, fetch HTML, extract main text content using BeautifulSoup (focus on <article>, <main>, or Docusaurus-specific classes like .markdown).
  - Clean text: remove navigation, headers, footers, code blocks if too noisy, scripts.
  - Chunk text into 800-1000 token pieces with 200-token overlap (use RecursiveCharacterTextSplitter or similar).
  - Generate embeddings using Cohere (model="embed-english-v3.0" or latest available in Dec 2025).
  - Upload to Qdrant Cloud: create collection if not exists (dimension from Cohere model, cosine distance), upsert points with payload { "text": chunk, "source": url, "title": page title }.
- Add progress bars with tqdm and error handling/retry for rate limits.
- Load credentials from .env.
- Output: Fully working `ingestion.py` that can be run with `uv run ingestion.py`.

**Task 4: Test retrieval pipeline**
- Create `test_retrieval.py` inside `backend`.
- Implement a function that:
  - Takes a query string.
  - Embeds it with Cohere.
  - Searches Qdrant for top 5-10 results.
  - Prints the retrieved texts and sources.
- Run several test queries like "What is Physical AI?", "Explain VLA models", "ROS2 fundamentals" to verify relevance.
- Output: `test_retrieval.py` and sample output showing good retrieval.

**Task 5: Set up Neon Postgres and basic DB models**
- Create `database.py` with async SQLAlchemy setup using NEON_DATABASE_URL.
- Define at least one model: ChatSession (id, user_id optional, created_at) and ChatMessage (id, session_id, role, content, timestamp).
- Create `init_db.py` to create tables asynchronously.
- Output: `database.py`, models file, and `init_db.py`.

**Task 6: Implement retrieval tool and selected-text handling**
- Create `tools.py`.
- Define an async retrieval function that:
  - If selected_text is provided, chunk and embed only that text, perform in-memory similarity search (or create temporary Qdrant collection).
  - Else, query main Qdrant collection.
  - Return concatenated relevant chunks as context.
- Wrap it as a @function_tool for OpenAI Agents SDK.
- Output: `tools.py` with clearly defined tool(s).

**Task 7: Build the RAG agent using OpenAI Agents SDK with Gemini**
- Create `agent.py`.
- Configure AsyncOpenAI client with base_url="https://generativelanguage.googleapis.com/v1beta/openai/" and api_key=GEMINI_API_KEY.
- Use OpenAIChatCompletionsModel with model="gemini-1.5-flash" or "gemini-2.0-flash" (or latest stable in Dec 2025 that supports tools).
- Create an Agent with the retrieval tool from Task 6.
- Add system prompt emphasizing: answer only based on provided context or selected text, be helpful for book content, cite sources when possible.
- Support streaming responses.
- Output: Working `agent.py` that can process a query and return response.

**Task 8: Build FastAPI application**
- Create `main.py` (or `app.py`).
- Set up FastAPI app with CORS middleware allowing the Vercel frontend origin and localhost.
- Define POST /chat endpoint that accepts JSON: { "message": str, "session_id": optional str, "selected_text": optional str }.
- Inside endpoint: load or create session from Neon, run agent with retrieval (pass selected_text if provided), save messages to DB, stream or return response.
- Add health check endpoint /health.
- Output: `main.py` ready to run with `uv run uvicorn main:app --reload`.

**Task 9: Frontend integration instructions**
- Create `README.md` inside `backend` explaining:
  - How to run locally: `uv sync`, `uv run uvicorn main:app --reload`.
  - How frontend should call the API (use relative /api/chat or proxy in Vercel).
  - For local testing: run backend on port 8000, point frontend to http://localhost:8000/chat.
  - For production: deploy backend (e.g., to Render/Vercel) and update frontend base URL.
- Output: Clear integration guide.

**Task 10: Final testing and verification**
- Run full pipeline: ingest → test retrieval → start FastAPI → test /chat endpoint with curl or Postman (both normal query and with selected_text).
- Verify chat history persists in Neon.
- Confirm agent cites sources or stays grounded in context.
- Output: Checklist confirming all features work for hackathon demo.

## Response snapshot

## Task Generation Complete: Backend RAG Chatbot for Physical AI and Humanoid Robotics Textbook

I have successfully generated the complete implementation tasks for the backend RAG chatbot. Here's a summary of what was accomplished:

### **Feature**: `005-backend-rag-chatbot`

### **Generated Artifacts**:
- **Tasks File**: `specs/005-backend-rag-chatbot/tasks.md` - Complete implementation tasks organized by user stories

### **Task Organization**:
1. **Phase 1**: Setup tasks (project initialization and dependencies)
2. **Phase 2**: Foundational components (Qdrant, Postgres, core utilities)
3. **Phase 3**: User Story 1 (P1) - Ask Questions About Textbook Content
4. **Phase 4**: User Story 2 (P2) - Frontend Integration
5. **Phase 5**: User Story 3 (P3) - Content Indexing
6. **Phase 6**: Polish & Cross-Cutting Concerns

### **Task Statistics**:
- **Total Tasks**: 100 tasks (T001-T100)
- **User Story 1 (P1)**: 26 implementation tasks + 3 tests
- **User Story 2 (P2)**: 14 implementation tasks + 3 tests
- **User Story 3 (P3)**: 9 implementation tasks + 3 tests
- **Cross-cutting**: 24 tasks for polish, testing, and deployment

### **Key Features Covered**:
- Content ingestion pipeline from sitemap
- Text chunking and Cohere embeddings
- Qdrant vector storage
- Dual-mode RAG (full-book and selected-text)
- OpenAI Agents SDK with Gemini integration
- FastAPI endpoints with CORS
- Neon Postgres session management
- Error handling and performance optimization

### **Ready for Implementation**:
The tasks are organized for incremental delivery with User Story 1 (P1) as the MVP scope. Each task follows the required format with proper dependencies and parallel execution opportunities identified.

## Outcome

- ✅ Impact: Created comprehensive task breakdown for backend RAG chatbot implementation
- 🧪 Tests: Defined test tasks for each user story with acceptance criteria
- 📁 Files: Generated tasks.md with 100 sequential tasks organized by user stories
- 🔁 Next prompts: Ready for implementation following the task sequence
- 🧠 Reflection: Tasks organized for incremental delivery with MVP scope identified

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All tasks follow required format with proper organization
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with Phase 1 tasks