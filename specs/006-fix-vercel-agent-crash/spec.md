# Feature Specification: Fix Vercel 500 INTERNAL_SERVER_ERROR Crash

**Feature Branch**: `006-fix-vercel-agent-crash`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "ONLY make these SPECIFIC changes to my existing FastAPI backend in the backend/ folder to fix the Vercel 500 INTERNAL_SERVER_ERROR crash. Do NOT change frontend code, do NOT add new features, do NOT modify database schema, do NOT change any existing endpoints or logic. Keep ALL existing functionality exactly the same.

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
4. Generate new requirements.txt: uv export"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - RAG Chatbot Query Processing (Priority: P1)

As a user of the Physical AI textbook RAG chatbot, I want to submit queries that are processed without server crashes so that I can get responses to my questions about the textbook content.

**Why this priority**: This is the core functionality that is currently broken in the production environment (Vercel), preventing users from using the chatbot.

**Independent Test**: Can be fully tested by sending a query to the /api/v1/chat endpoint and receiving a response without the server crashing with a 500 error.

**Acceptance Scenarios**:

1. **Given** the RAG chatbot service is running on Vercel, **When** a user submits a query about textbook content, **Then** the service returns a relevant response without crashing
2. **Given** the RAG chatbot service is running on Vercel, **When** a user submits a query with selected text context, **Then** the service returns a relevant response incorporating the selected text without crashing

---

### User Story 2 - Dual-Mode Query Support (Priority: P2)

As a user of the Physical AI textbook RAG chatbot, I want to be able to ask questions in both full-book RAG mode and selected-text-only mode so that I can get contextually appropriate responses for different types of queries.

**Why this priority**: This maintains the existing functionality that users depend on while fixing the crash issue.

**Independent Test**: Can be tested by submitting queries both with and without selected text and verifying both modes work without crashes.

**Acceptance Scenarios**:

1. **Given** the RAG chatbot service is running, **When** a user submits a query without selected text, **Then** the service performs full-book RAG and returns a response
2. **Given** the RAG chatbot service is running, **When** a user submits a query with selected text, **Then** the service performs selected-text RAG and returns a response

---

### User Story 3 - Error Handling (Priority: P3)

As a user of the Physical AI textbook RAG chatbot, I want to receive meaningful error messages when the service encounters issues so that I understand what went wrong instead of seeing server crashes.

**Why this priority**: This improves the user experience by providing clear feedback when problems occur instead of server crashes.

**Independent Test**: Can be tested by simulating conditions that cause agent failures and verifying that the service returns appropriate error messages instead of crashing.

**Acceptance Scenarios**:

1. **Given** the RAG chatbot service is running but encounters an agent processing error, **When** a user submits a query, **Then** the service returns an error message in the expected format instead of crashing

---

### Edge Cases

- What happens when the Gemini API is temporarily unavailable?
- How does the system handle malformed queries that cause agent processing failures?
- What happens when the retrieval tool returns no results for a query?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST replace the current OpenAI chat.completions implementation with OpenAI Agents SDK and Runner
- **FR-002**: System MUST use Gemini API via OpenAI-compatible endpoint with base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
- **FR-003**: System MUST create a global TextbookRAGAgent that is initialized once at startup for serverless performance
- **FR-004**: System MUST attach the existing retrieval_tool from src.tools.retrieval_tool to the agent
- **FR-005**: System MUST support dual-mode queries: full-book RAG (Qdrant) and selected-text-only mode
- **FR-006**: System MUST maintain identical response format to current implementation: {"response": str, "session_id": str, "mode": str, "retrieved_chunks_count": int, "response_time": float, "retrieved_chunks": list}
- **FR-007**: System MUST handle errors gracefully by returning error messages in the response format instead of crashing
- **FR-008**: System MUST update FastAPI endpoints to use the new agent.process_query() method
- **FR-009**: System MUST add openai-agents dependency to both pyproject.toml and requirements.txt
- **FR-010**: System MUST be compatible with Vercel serverless deployment (no blocking startup, lazy init clients)
- **FR-011**: System MUST inject selected_text into queries when provided by users
- **FR-012**: System MUST preserve all existing functionality including imports, error handling, logging, response_time calculation, and session management

### Key Entities *(include if feature involves data)*

- **RAGAgent**: The OpenAI Agents SDK-based agent that processes textbook queries using retrieval-augmented generation
- **RetrievalTool**: The existing tool that fetches relevant textbook content from Qdrant vector database
- **QueryProcessor**: The async function that handles incoming queries and coordinates with the agent
- **Response**: The structured output containing the response text, session information, mode, and retrieved chunks

## Success Criteria

- 95% of RAG chatbot queries return successfully without server crashes on Vercel
- Average response time for queries remains under 5 seconds
- All existing API endpoints continue to function with identical response formats
- The service handles both full-book RAG and selected-text queries without crashes
- Error conditions result in appropriate error responses instead of server crashes
- Deployment to Vercel completes successfully without runtime errors
- All existing functionality is preserved while fixing the crash issue