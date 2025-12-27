# Implementation Tasks: Backend RAG Chatbot for Physical AI and Humanoid Robotics Textbook

**Feature**: 005-backend-rag-chatbot | **Date**: 2025-12-26 | **Spec**: [specs/005-backend-rag-chatbot/spec.md](spec.md)

## Implementation Strategy

**MVP Scope**: User Story 1 (P1) - Basic RAG functionality allowing students to ask questions about textbook content and receive AI-generated responses.

**Delivery Approach**: Incremental delivery with each user story building on the previous. Each phase delivers independently testable functionality.

## Dependencies

User Story 2 (P2) depends on User Story 1 (P1) for the core RAG functionality. User Story 3 (P3) can be developed in parallel with User Story 1 after foundational setup is complete.

## Parallel Execution Examples

- **User Story 1**: T010-T030 (content ingestion) can run in parallel with T031-T050 (database setup)
- **User Story 1**: T051-T070 (agent and tools) can run in parallel with T071-T090 (API endpoints)
- **User Story 2**: T091-T100 (frontend integration) can run after User Story 1 is complete

---

## Phase 1: Setup

### Goal
Initialize project structure and install dependencies per implementation plan.

### Independent Test
Project structure matches plan with all required dependencies installed and environment variables configured.

### Tasks

- [X] T001 Create backend directory structure per implementation plan
- [X] T002 Initialize uv project in backend directory
- [X] T003 [P] Create .gitignore with appropriate entries for backend
- [X] T004 [P] Create .env file with placeholder credentials
- [X] T005 [P] Create .env.example with template for required environment variables
- [X] T006 Install required dependencies via uv per implementation plan
- [X] T007 [P] Create project directory structure (src/api, src/models, src/services, src/tools, src/config, scripts, tests)

---

## Phase 2: Foundational Components

### Goal
Set up foundational services (Qdrant, Postgres) and core utilities that all user stories depend on.

### Independent Test
Both Qdrant and Postgres connections are established and ready for use by other components.

### Tasks

- [X] T008 [P] Set up Qdrant client configuration and test connection
- [X] T009 [P] Create Qdrant collection for textbook content with appropriate dimensions and cosine distance
- [X] T010 Set up Neon Postgres async SQLAlchemy configuration
- [X] T011 Define ChatSession model based on data model specification
- [X] T012 Define ChatMessage model based on data model specification
- [X] T013 Create database initialization script to create tables
- [X] T014 Create utility functions for token counting and text chunking
- [X] T015 [P] Set up Cohere client configuration and test embedding functionality
- [X] T016 [P] Set up AsyncOpenAI client with Gemini endpoint configuration
- [X] T017 Create configuration module to manage environment variables

---

## Phase 3: User Story 1 - Ask Questions About Textbook Content (P1)

### Goal
Enable students to ask questions about textbook content and receive AI-generated responses based on textbook material.

### Independent Test
System can independently answer textbook-related questions by retrieving relevant content from the vector database and generating responses, delivering immediate educational value to students.

### Tests
- [X] T018 [US1] Create test for "What is Physical AI?" query returning relevant textbook content
- [X] T019 [US1] Create test for selected text mode returning focused responses
- [X] T020 [US1] Create test for out-of-scope queries with appropriate fallback responses

### Implementation Tasks

- [X] T021 [US1] Implement sitemap parsing and URL extraction from textbook site
- [X] T022 [US1] Create web scraping function to extract clean text content from textbook pages
- [X] T023 [US1] Implement text cleaning to remove navigation, headers, footers from scraped content
- [X] T024 [US1] Create text chunking function with 800-1000 token chunks and 200-token overlap
- [X] T025 [US1] Implement embedding generation for text chunks using Cohere
- [X] T026 [US1] Create ingestion pipeline to upload embeddings to Qdrant with metadata
- [X] T027 [US1] Implement retrieval function to search Qdrant for relevant chunks
- [X] T028 [US1] Create selected-text-only mode with in-memory similarity search
- [X] T029 [US1] Implement dual-mode handling (full-book RAG vs selected-text-only)
- [X] T030 [US1] Run full content ingestion pipeline and verify coverage
- [X] T031 [US1] Create retrieval tool for OpenAI Agents SDK with dual-mode support
- [X] T032 [US1] Configure RAG agent with Gemini and retrieval tool
- [X] T033 [US1] Implement system prompt emphasizing textbook context usage
- [X] T034 [US1] Add source citation capability to agent responses
- [ ] T035 [US1] Implement streaming response support in agent
- [X] T036 [US1] Create chat session management with Neon Postgres
- [X] T037 [US1] Implement chat history persistence in database
- [X] T038 [US1] Add query logging with mode tracking and response time metrics
- [X] T039 [US1] Create error handling for external API failures (Cohere, Qdrant, Gemini)
- [X] T040 [US1] Implement rate limiting for external API calls
- [X] T041 [US1] Add validation for user inputs and selected text
- [X] T042 [US1] Create test retrieval script to verify pipeline functionality
- [X] T043 [US1] Run sample queries ("What is Physical AI?", "Explain VLA models", "ROS2 fundamentals") to verify relevance
- [X] T044 [US1] Create acceptance test for scenario 1: accurate response to Physical AI concepts
- [X] T045 [US1] Create acceptance test for scenario 2: focused response on selected text
- [X] T046 [US1] Create acceptance test for scenario 3: appropriate response for out-of-scope queries

---

## Phase 4: User Story 2 - Access RAG Chatbot Through Frontend Integration (P2)

### Goal
Enable seamless integration between the frontend textbook interface and the backend RAG service for a cohesive learning experience.

### Independent Test
Frontend can independently connect to the backend RAG service and display responses to user queries, providing a complete user experience without requiring separate tools.

### Tests
- [X] T047 [US2] Create test for frontend calling /chat endpoint and receiving formatted response
- [X] T048 [US2] Create test for CORS middleware allowing frontend domain access
- [X] T049 [US2] Create test for frontend integration with session management

### Implementation Tasks

- [X] T050 [US2] Implement FastAPI with CORS middleware allowing Vercel frontend origin
- [X] T051 [US2] Create /chat POST endpoint per API contract specification
- [X] T052 [US2] Implement request validation for /chat endpoint (message, selected_text, session_id)
- [X] T053 [US2] Create response formatting for /chat endpoint per API contract
- [X] T054 [US2] Add error response handling for /chat endpoint
- [X] T055 [US2] Implement /health GET endpoint per API contract specification
- [X] T056 [US2] Add dependency health checks to health endpoint (Cohere, Qdrant, Postgres)
- [X] T057 [US2] Create /ingest GET endpoint for content ingestion triggering
- [X] T058 [US2] Implement request processing in /chat endpoint with session management
- [X] T059 [US2] Add response time tracking to API endpoints
- [ ] T060 [US2] Implement streaming response support for /chat endpoint
- [X] T061 [US2] Create API documentation with OpenAPI/Swagger
- [X] T062 [US2] Add request logging for monitoring and debugging
- [X] T063 [US2] Create acceptance test for scenario 1: chatbot responds without separate page navigation
- [X] T064 [US2] Create acceptance test for scenario 2: responses returned in frontend-compatible format

---

## Phase 5: User Story 3 - System Maintains Reliable Content Indexing (P3)

### Goal
Ensure the system reliably crawls, processes, and indexes textbook content from the deployed site for up-to-date knowledge base.

### Independent Test
System can independently crawl the textbook site, extract content, generate embeddings, and store them in the vector database, creating a complete knowledge base without manual intervention.

### Tests
- [X] T065 [US3] Create test for automatic content update when textbook site changes
- [X] T066 [US3] Create test for processing all textbook pages from sitemap
- [X] T067 [US3] Create test for handling malformed HTML gracefully

### Implementation Tasks

- [X] T068 [US3] Create scheduled content update mechanism or webhook integration
- [X] T069 [US3] Implement content change detection to identify updated pages
- [X] T070 [US3] Add incremental update capability to ingestion pipeline
- [X] T071 [US3] Create content validation to handle malformed HTML or content
- [X] T072 [US3] Implement retry logic for failed page extractions
- [X] T073 [US3] Add progress tracking and reporting for ingestion process
- [X] T074 [US3] Create content indexing metrics and monitoring
- [ ] T075 [US3] Implement backup/recovery for vector database content
- [X] T076 [US3] Create acceptance test for scenario 1: updated content reflected in vector database
- [X] T077 [US3] Create acceptance test for scenario 2: all relevant textbook pages processed and indexed

---

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Address cross-cutting concerns, edge cases, and performance optimizations to complete the implementation.

### Independent Test
All edge cases are handled gracefully and system meets performance requirements.

### Tasks

- [X] T078 Handle Qdrant vector database temporary unavailability with graceful degradation
- [X] T079 Implement handling for extremely long user queries or selected text
- [X] T080 Add handling for questions about content not in textbook with helpful suggestions
- [X] T081 Create concurrent user handling to support multiple simultaneous requests
- [X] T082 Handle invalid or expired API keys with appropriate error messages
- [X] T083 Add malformed HTML handling in content extraction
- [X] T084 Implement performance monitoring and metrics collection
- [X] T085 Add structured logging for debugging and monitoring
- [X] T086 Create caching layer for frequently accessed embeddings
- [X] T087 Optimize response times to meet <5s requirement
- [X] T088 Add comprehensive error handling throughout the application
- [X] T089 Create health monitoring and alerting for dependencies
- [X] T090 Write comprehensive README with setup and usage instructions
- [X] T091 Create deployment configuration for cloud hosting
- [X] T092 Run full pipeline test: ingest → test retrieval → start FastAPI → test /chat endpoint
- [X] T093 Verify chat history persistence in Neon Postgres
- [X] T094 Confirm agent cites sources and stays grounded in context
- [X] T095 Performance test: verify <5s response time for queries
- [X] T096 Performance test: verify 99% uptime capability
- [X] T097 Performance test: verify handling of 100+ concurrent users
- [X] T098 Run content indexing test: verify 95%+ content coverage
- [X] T099 Create final verification checklist for hackathon demo
- [X] T100 Document any remaining issues or future enhancements