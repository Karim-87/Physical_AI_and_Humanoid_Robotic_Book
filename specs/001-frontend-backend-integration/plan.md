# Implementation Plan: Frontend Backend Integration for RAG Chatbot

**Branch**: `001-frontend-backend-integration` | **Date**: 2025-12-27 | **Spec**: [specs/001-frontend-backend-integration/spec.md](spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of frontend-backend integration for the RAG chatbot in the Physical AI and Humanoid Robotics textbook project. This involves connecting the Docusaurus frontend to the FastAPI backend, enabling students to ask questions about textbook content directly on book pages. The system will support both full-book RAG and selected-text-only modes with proper CORS configuration, local proxy setup for development, and deployment to Vercel.

## Technical Context

**Language/Version**: JavaScript (ECMAScript 2020+), Python 3.12
**Primary Dependencies**: Docusaurus v3.x, React 18+, FastAPI 0.104+, Node.js 18+
**Storage**: Qdrant Cloud (vector store), Neon Serverless Postgres (relational), Local files (frontend)
**Testing**: Jest for frontend unit tests, pytest for backend tests, manual E2E testing
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge) - modern versions
**Project Type**: Web application (frontend + backend integration)
**Performance Goals**: <5s response time for queries, 99% uptime during peak hours, handle 100+ concurrent users, <2s UI load time
**Constraints**: <200ms p95 for internal API calls, CORS compliance for cross-origin requests, secure credential handling, rate limits for external APIs (Cohere, Qdrant, Gemini)
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
specs/001-frontend-backend-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure for frontend-backend integration
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

frontend/ (root directory)
├── src/
│   ├── components/      # React components (Chatbot, etc.)
│   ├── pages/           # Docusaurus pages
│   ├── theme/           # Docusaurus theme overrides
│   └── utils/           # Utility functions
├── static/              # Static assets
├── docusaurus.config.js # Docusaurus configuration
├── package.json         # Node.js dependencies
├── babel.config.js      # Babel configuration
└── .env                 # Environment variables (gitignored)
```

**Structure Decision**: Option 2: Web application structure selected as this involves frontend-backend integration. The frontend (Docusaurus) is in the root directory and the backend is in the ./backend subdirectory with clear separation of concerns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Cross-origin communication | Required for frontend-backend integration | Single service approach impossible when services run on different ports |
| Multiple external services | Need to integrate Cohere, Qdrant, and Gemini APIs | Single-service approach insufficient for RAG functionality |
| Dual-mode processing | Support both full-book RAG and selected-text-only modes | Single mode would limit user experience |

## Phase 1 Completion Summary

### ✅ Completed Artifacts
- **Research Summary** (`research.md`): CORS configuration, component architecture, text selection, state management decisions
- **Data Model** (`data-model.md`): Complete entity definitions with relationships and validation rules for chat messages, sessions, API payloads
- **API Contracts** (`contracts/api-contracts.md`): Complete API specification with request/response schemas for chat, health, and ingestion endpoints
- **Quickstart Guide** (`quickstart.md`): Step-by-step setup and integration instructions
- **Agent Context Updated**: Technology stack added to Claude Code context file

### 🎯 Next Steps
1. **Phase 2**: Generate detailed implementation tasks with `/sp.tasks` command
2. **Implementation**: Execute tasks to build the frontend-backend integration
3. **Testing**: Validate all components against specification requirements
4. **Deployment**: Deploy frontend to Vercel and backend to serverless provider

### 🔧 Implementation Notes
- Frontend-backend integration architecture finalized with clear separation of concerns
- All external service integrations planned (Cohere, Qdrant, Gemini, Neon Postgres)
- Both RAG modes (full-book and selected-text-only) architecturally supported
- CORS and proxy configurations planned for seamless development and production
