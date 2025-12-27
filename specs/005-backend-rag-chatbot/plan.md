# Implementation Plan: Backend RAG Chatbot for Physical AI and Humanoid Robotics Textbook

**Branch**: `005-backend-rag-chatbot` | **Date**: 2025-12-26 | **Spec**: [specs/005-backend-rag-chatbot/spec.md](../005-backend-rag-chatbot/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a backend RAG chatbot system that integrates with the Physical AI and Humanoid Robotics textbook frontend. The system will crawl and index textbook content using Cohere embeddings, store in Qdrant vector database, and provide AI-powered responses via Gemini through OpenAI-compatible endpoint. The backend will support both full-book RAG and selected-text-only modes with FastAPI endpoints and Neon Postgres for session management.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Cohere, Qdrant Client, Neon Postgres, uv
**Storage**: Qdrant Cloud (vector store), Neon Serverless Postgres (relational), Local files (ingestion pipeline)
**Testing**: pytest for unit/integration tests
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Web application (backend service)
**Performance Goals**: <5s response time for queries, 99% uptime during peak hours, handle 100+ concurrent users
**Constraints**: <200ms p95 for internal API calls, rate limits for external APIs (Cohere, Qdrant, Gemini), secure credential handling
**Scale/Scope**: Support entire textbook content (~50+ pages), handle 10k+ user queries per day, maintain 95%+ content indexing coverage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution (though not fully defined), the following checks apply:
- ✅ Test-first approach: Unit and integration tests will be written for all core components
- ✅ Observability: Structured logging will be implemented for debugging and monitoring
- ✅ Simplicity: Architecture will follow YAGNI principles, starting with minimal viable implementation
- ✅ Security: Credentials will be handled through environment variables, not hardcoded

## Project Structure

### Documentation (this feature)

```text
specs/005-backend-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/             # FastAPI endpoints
│   ├── models/          # Pydantic models and data structures
│   ├── services/        # Business logic (embedding, retrieval, agent)
│   ├── tools/           # Agent tools (retrieval, selected-text processing)
│   └── config/          # Configuration and settings
├── scripts/             # Ingestion and utility scripts
├── tests/               # Test suite
│   ├── unit/
│   ├── integration/
│   └── contract/
├── pyproject.toml       # Project dependencies and metadata
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── main.py             # FastAPI application entry point
```

**Structure Decision**: Option 2: Web application structure selected as this is a backend service that will integrate with an existing frontend. The backend will be in the `backend/` directory with a clear separation of concerns following FastAPI best practices.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple external services | Need to integrate Cohere, Qdrant, and Gemini APIs | Single-service approach insufficient for RAG functionality |
| Vector database integration | Required for semantic search capabilities | Keyword search inadequate for textbook content |
| Dual-mode processing | Support both full-book RAG and selected-text modes | Single mode would limit user experience |

## Phase 1 Completion Summary

### ✅ Completed Artifacts
- **Research Summary** (`research.md`): Cohere/Gemini model selection, architecture decisions, best practices
- **Data Model** (`data-model.md`): Complete entity definitions with relationships and validation rules
- **API Contracts** (`contracts/api-contracts.md`): Complete API specification with request/response schemas
- **Quickstart Guide** (`quickstart.md`): Step-by-step setup and deployment instructions
- **Agent Context Updated**: Technology stack added to Claude Code context file

### 🎯 Next Steps
1. **Phase 2**: Generate detailed tasks with `/sp.tasks` command
2. **Implementation**: Execute tasks to build the backend RAG system
3. **Testing**: Validate all components against specification requirements
4. **Integration**: Connect with frontend textbook application

### 🔧 Implementation Notes
- Backend directory structure ready for development
- All external service integrations planned (Cohere, Qdrant, Gemini, Neon Postgres)
- Both RAG modes (full-book and selected-text-only) architecturally supported
- Security and performance requirements addressed in design
