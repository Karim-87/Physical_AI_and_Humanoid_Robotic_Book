---
id: 005
title: Backend RAG Chatbot Specification
stage: spec
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-rag-chatbot
branch: 005-backend-rag-chatbot
user: Claude Sonnet 4.5
command: /sp.specify
labels: [spec,rag,chatbot,backend,education]
links:
  spec: specs/005-backend-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-backend-rag-chatbot/spec.md
 - specs/005-backend-rag-chatbot/checklists/requirements.md
tests:
 - specs/005-backend-rag-chatbot/checklists/requirements.md
---

## Prompt

/sp.specify I have already completed the frontend (Docusaurus-based textbook on Physical AI and Humanoid Robotics) deployed at https://physical-ai-and-humanoid-robotic-bo-three.vercel.app/sitemap.xml. Now, continue building the backend for Part 2: the integrated RAG chatbot.

Follow these exact steps in sequence:

1. In the root directory, create a new folder named 'backend' if it doesn't already exist.

2. Inside the 'backend' folder, initialize a new Python project using uv: run the command `uv init` (this sets up pyproject.toml, .gitattributes, etc.).

3. Use the deployed site's sitemap URL (https://physical-ai-and-humanoid-robotic-bo-three.vercel.app/sitemap.xml) to crawl and extract the main content/pages of the book. Parse the sitemap, fetch each linked page, clean the text (remove navigation, footers, scripts, etc.), and chunk it into suitable pieces for embedding (e.g., 500-1000 tokens per chunk with overlap).

4. Generate embeddings for these text chunks using the Cohere embedding model (use Cohere's embed-english-v3.0 or similar multilingual/English model suitable for technical content). Install necessary packages via uv (e.g., cohere, requests, beautifulsoup4 for scraping). Store the embeddings + metadata (source URL, chunk text, page title) in Qdrant Cloud Free Tier. Create a collection in Qdrant, upload the vectors, and use appropriate distance metric (e.g., Cosine).

5. After ingestion, implement a simple retrieval test pipeline: write a Python script or function that takes a sample query (e.g., "What is Physical AI?"), embeds it with Cohere, searches Qdrant for top-k similar chunks, and prints the retrieved texts to verify the pipeline works correctly.

6. Build a RAG-capable agent using the OpenAI Agents SDK (https://openai.github.io/openai-agents-python/). Since we need to use GEMINI_API_KEY, configure the agent to use Gemini via its OpenAI-compatible endpoint: create an AsyncOpenAI client with base_url="https://generativelanguage.googleapis.com/v1beta/openai/" and your GEMINI_API_KEY. Then use OpenAIChatCompletionsModel(model="gemini-1.5-flash" or latest available like "gemini-2.0-flash", openai_client=your_client). Integrate retrieval as a tool: create a @function_tool that takes a user query (and optionally selected text), embeds it with Cohere, queries Qdrant, and returns top relevant chunks as context. The agent should use this tool for book-related questions. For questions based only on user-selected text, add logic to embed and retrieve only from that provided text (bypass Qdrant or use a separate in-memory index). Also integrate Neon Serverless Postgres (using asyncpg or SQLAlchemy) to store e.g. chat sessions, query logs, or user-selected text history. Use uv to add dependencies (openai-agents, litellm if needed for extra compatibility, qdrant-client, cohere, python-dotenv, fastapi, uvicorn, etc.).

7. Build a FastAPI application in the backend folder that exposes endpoints like /chat (POST) to receive user messages (and optional selected_text), runs the agent with retrieval, and returns the response (support streaming if possible). Include CORS middleware to allow requests from the frontend (Vercel URL). For local integration/testing, the frontend can call http://localhost:8000/chat (or wherever FastAPI runs). Provide instructions on how to run the FastAPI server (uv run uvicorn main:app --reload).

8. Create a .env file in the backend folder (and add to .gitignore) to securely load all credentials: GEMINI_API_KEY, COHERE_API_KEY, QDRANT_API_KEY and QDRANT_URL (from Qdrant Cloud dashboard), NEON_DATABASE_URL (connection string from Neon dashboard). Use python-dotenv to load them in code. Never hardcode keys.

Generate the necessary folder structure, key code files (e.g., ingestion.py for steps 3-5, app.py for FastAPI + agent, tools.py for retrieval tool, models.py if needed, .env.example), and detailed step-by-step terminal commands to set everything up and test. Ensure the system supports both full-book RAG and selected-text-only mode. Use best practices for error handling, async where appropr

## Response snapshot

## Specification Complete: Backend RAG Chatbot for Physical AI and Humanoid Robotics Textbook

I have successfully created the feature specification for the backend RAG chatbot. Here's a summary of what was accomplished:

### **Branch Created**
- `005-backend-rag-chatbot` - New feature branch for the RAG chatbot implementation

### **Specification Created**
- **File**: `specs/005-backend-rag-chatbot/spec.md`
- **Content**: Comprehensive feature specification with:
  - User Scenarios & Testing (3 prioritized user stories)
  - Functional Requirements (16 specific requirements)
  - Key Entities (6 data entities defined)
  - Success Criteria (8 measurable outcomes)

### **Quality Validation**
- **Checklist File**: `specs/005-backend-rag-chatbot/checklists/requirements.md`
- **Validation**: All quality criteria met and verified
- **Ready for**: Planning phase (`/sp.plan`)

### **Key Features Specified**
1. **RAG Chatbot Integration**: Students can ask questions about textbook content
2. **Dual Mode Support**: Full-book RAG and selected-text-only modes
3. **Frontend Integration**: Seamless integration with the existing textbook interface
4. **Content Indexing**: Automated crawling and indexing of textbook content
5. **Backend Services**: FastAPI endpoints with streaming support

The specification is complete, validated, and ready for the planning phase. The feature is well-defined with clear user value, measurable success criteria, and comprehensive requirements that will guide the implementation process.

## Outcome

- ✅ Impact: Created comprehensive specification for backend RAG chatbot feature
- 🧪 Tests: Created validation checklist to ensure spec quality
- 📁 Files: Generated spec.md and requirements checklist in feature directory
- 🔁 Next prompts: Ready for planning phase with `/sp.plan`
- 🧠 Reflection: Specification successfully abstracts implementation details while maintaining clear requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All quality criteria met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with planning phase