---
id: 1
title: "Fix Vercel Agent Crash Spec"
stage: "spec"
date: "2025-12-28"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "fix-vercel-agent-crash"
branch: "006-fix-vercel-agent-crash"
user: "user"
command: "/sp.specify"
labels: ["specification", "vercel", "agent", "crash"]
spec: "specs/006-fix-vercel-agent-crash/spec.md"
ticket: null
adr: null
pr: null
files:
  - "specs/006-fix-vercel-agent-crash/spec.md"
  - "specs/006-fix-vercel-agent-crash/checklists/requirements.md"
tests: []
prompt: |
  /sp.specify

  ONLY make these SPECIFIC changes to my existing FastAPI backend in the backend/ folder to fix the Vercel 500 INTERNAL_SERVER_ERROR crash. Do NOT change frontend code, do NOT add new features, do NOT modify database schema, do NOT change any existing endpoints or logic. Keep ALL existing functionality exactly the same.

  PROBLEM: Current src/services/agent.py uses raw OpenAI chat.completions (NOT agents SDK) which crashes on Vercel serverless. Need to replace with OpenAI Agents SDK + Runner using Gemini API key via OpenAI-compatible endpoint.

  EXACT CHANGES REQUIRED (minimal only):

  1. REPLACE src/services/agent.py completely with production-ready OpenAI Agents SDK version:
     - Use from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
     - Create AsyncOpenAI client with GEMINI_API_KEY and base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
     - Use model="gemini-2.0-flash-exp" (or gemini-1.5-flash-exp if 2.0 not available)
     - Create global Agent named "TextbookRAGAgent" with instructions for Physical AI textbook
     - Attach existing retrieval_tool from src.tools.retrieval_tool
     - Create async function process_query(query: str, selected_text: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]
     - Inside process_query: use Runner.run() with agent + tool, inject selected_text into query if provided
     - Return SAME response format as current agent: {"response": str, "session_id": str, "mode": str, "retrieved_chunks_count": int, "response_time": float, "retrieved_chunks": list}
     - Handle errors gracefully (return error message in response dict, no crashes)
     - Global instance: rag_agent = RAGAgent()

  2. UPDATE FastAPI endpoints that use agent (in api/routers/chat.py or main.py) to call the NEW agent.process_query() - NO OTHER CHANGES TO ENDPOINTS

  3. ADD missing dependency to pyproject.toml and requirements.txt:
     uv add openai-agents[all]
     OR manually add "openai-agents>=0.3.0" to dependencies

  4. Do NOT use Chainlit decorators (@cl.on_chat_start, @cl.on_message) - this is API only, NOT chat UI
  5. Do NOT change retrieval_tool, database, Qdrant, Cohere embedding, CORS, sessions, ANY other files
  6. Keep ALL existing imports, error handling, logging, response_time calculation, session management
  7. Ensure 100% Vercel serverless compatible (no blocking startup, lazy init clients, no file I/O)

  CONSTRAINTS:
  - Support dual-mode: full-book RAG (Qdrant) AND selected-text-only (pass selected_text to retrieval_tool)
  - Keep response format IDENTICAL to current working local version
  - Global agent instance (no recreation per request for serverless performance)
  - Error handling: if agent fails, return {"response": "Error message", ...} NEVER raise/crash
  - Use existing settings.gemini_model from src.config.settings

  After changes:
  1. Test locally: uv run fastapi dev api/index.py --port 8000
  2. Test /health and /api/v1/chat with curl (both full query and selected_text)
  3. Confirm /docs Swagger works
  4. Generate new requirements.txt: uv export
response: |
  Created feature specification for fixing the Vercel 500 INTERNAL_SERVER_ERROR crash by replacing the current OpenAI chat.completions implementation with OpenAI Agents SDK using Gemini API. The specification includes user scenarios, functional requirements, and success criteria for the agent replacement while maintaining all existing functionality.
outcome: "Specification created successfully for the Vercel agent crash fix feature"
evaluation: "The specification clearly defines the requirements for replacing the OpenAI chat.completions with OpenAI Agents SDK to fix Vercel crashes while preserving all existing functionality."
---
