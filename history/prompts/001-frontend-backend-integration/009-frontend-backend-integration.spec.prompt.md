---
id: 009
title: Frontend Backend Integration
stage: spec
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: frontend-backend-integration
branch: 001-frontend-backend-integration
user: Claude Sonnet 4.5
command: /sp.specify
labels: [integration,rag,chatbot,frontend,backend]
links:
  spec: specs/001-frontend-backend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-frontend-backend-integration/spec.md
 - specs/001-frontend-backend-integration/checklists/requirements.md
tests:
 - specs/001-frontend-backend-integration/checklists/requirements.md
---

## Prompt

I have already completed the backend for the integrated RAG chatbot in my hackathon project "Physical AI and Humanoid Robotics" textbook. The frontend Docusaurus site is deployed at https://physical-ai-and-humanoid-robotic-bo-three.vercel.app, and the backend is running locally on http://localhost:8000 with endpoints like /api/v1/chat, /health, and /api/v1/ingest.
Now, integrate the frontend with the backend to enable the embedded RAG chatbot. The chatbot should be able to handle user questions about the book's content via the backend, supporting both full-book RAG and selected-text-only modes.
Follow these exact steps:

In the frontend Docusaurus project (root directory), add or update the chatbot component (e.g., in src/components/Chatbot.js or a similar file) to make API calls to the backend using fetch or axios.
Configure CORS in the backend if not already done, to allow requests from localhost:3000 (Docusaurus dev server) and the production Vercel URL.
For local testing: Use a proxy in package.json to forward API calls to http://localhost:8000, so frontend can call relative paths like /api/v1/chat without CORS issues.
Implement the chatbot UI in Docusaurus: Add a chat interface (e.g., using React state for messages) that appears on book pages, allows text selection (use window.getSelection() to capture selected text), and sends POST requests to /api/v1/chat with { "message": userQuery, "selected_text": selectedText }.
Handle responses: Display the agent's reply in the chat UI, including any source citations if implemented.
For production: Update the API base URL to the deployed backend URL (after pushing backend to GitHub and deploying to Vercel or another host).
Test locally: Run backend on port 8000, start Docusaurus on port 3000, open a book page, select text or ask a question, and verify the chatbot responds correctly using RAG.
After local integration works, push changes to GitHub (frontend updates) and deploy to Vercel. For backend, create a separate repo if needed, push, and deploy as a serverless API

## Response snapshot

# Feature Specification: Frontend Backend Integration for RAG Chatbot

**Feature Branch**: `001-frontend-backend-integration`
**Created**: 2025-12-27
**Status**: Draft
**Input**: User description: "I have already completed the backend for the integrated RAG chatbot in my hackathon project \"Physical AI and Humanoid Robotics\" textbook. The frontend Docusaurus site is deployed at https://physical-ai-and-humanoid-robotic-bo-three.vercel.app, and the backend is running locally on http://localhost:8000 with endpoints like /api/v1/chat, /health, and /api/v1/ingest.
Now, integrate the frontend with the backend to enable the embedded RAG chatbot. The chatbot should be able to handle user questions about the book's content via the backend, supporting both full-book RAG and selected-text-only modes.
Follow these exact steps:

In the frontend Docusaurus project (root directory), add or update the chatbot component (e.g., in src/components/Chatbot.js or a similar file) to make API calls to the backend using fetch or axios.
Configure CORS in the backend if not already done, to allow requests from localhost:3000 (Docusaurus dev server) and the production Vercel URL.
For local testing: Use a proxy in package.json to forward API calls to http://localhost:8000, so frontend can call relative paths like /api/v1/chat without CORS issues.
Implement the chatbot UI in Docusaurus: Add a chat interface (e.g., using React state for messages) that appears on book pages, allows text selection (use window.getSelection() to capture selected text), and sends POST requests to /api/v1/chat with { \"message\": userQuery, \"selected_text\": selectedText }.
Handle responses: Display the agent's reply in the chat UI, including any source citations if implemented.
For production: Update the API base URL to the deployed backend URL (after pushing backend to GitHub and deploying to Vercel or another host).
Test locally: Run backend on port 8000, start Docusaurus on port 3000, open a book page, select text or ask a question, and verify the chatbot responds correctly using RAG.
After local integration works, push changes to GitHub (frontend updates) and deploy to Vercel. For backend, create a separate repo if needed, push, and deploy as a serverless API"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access RAG Chatbot on Book Pages (Priority: P1)

A student reading the Physical AI and Humanoid Robotics textbook wants to ask questions about the content directly on the book page they're viewing. The student sees a chat interface embedded on the page, types a question, and receives an AI-generated response based on the textbook content.

**Why this priority**: This is the core value proposition of the feature - enabling students to get immediate answers to their questions without leaving the textbook context, enhancing their learning experience.

**Independent Test**: The system can independently process user queries through the chat interface, communicate with the backend RAG service, and display AI-generated responses, delivering immediate educational value to students.

**Acceptance Scenarios**:

1. **Given** the student is viewing a textbook page with the embedded chat interface, **When** they type a question about the content and submit it, **Then** the system returns a relevant response based on the textbook material.
2. **Given** the student has selected specific text on the page, **When** they ask a question about that selected text, **Then** the system focuses its response on the selected content rather than the full textbook.
3. **Given** the student asks a question that doesn't match textbook content, **When** the system processes the query, **Then** it provides a helpful response indicating the limitation and suggesting related topics from the textbook.

---

### User Story 2 - Seamless Frontend-Backend Communication (Priority: P2)

A developer or student using the deployed textbook website wants to interact with the RAG chatbot without experiencing CORS issues or connectivity problems. The frontend seamlessly communicates with the backend RAG service to provide a cohesive learning experience.

**Why this priority**: Essential for user adoption - the chatbot must communicate reliably with the backend service to provide a seamless learning experience without technical barriers.

**Independent Test**: The frontend can independently connect to the backend RAG service and exchange data without CORS errors, providing a complete user experience without requiring separate tools.

**Acceptance Scenarios**:

1. **Given** the student is using the frontend from the deployed Vercel URL, **When** they interact with the chatbot interface, **Then** the system communicates with the backend without CORS errors.
2. **Given** the student is using the frontend from localhost during development, **When** they interact with the chatbot interface, **Then** the system communicates with the local backend via proxy without CORS issues.

---

### User Story 3 - Text Selection and Contextual Q&A (Priority: P3)

A student reading the textbook wants to select specific text on a page and ask questions about only that selected text. The system captures the selected text and uses it as context for the RAG query, providing focused answers.

**Why this priority**: Enhances the learning experience by allowing students to get specific answers about particular passages they're studying, rather than searching the entire textbook.

**Independent Test**: The system can independently capture selected text from the page, send it to the backend with the query, and return responses focused on that specific content.

**Acceptance Scenarios**:

1. **Given** the student has selected text on a textbook page, **When** they ask a question while text is selected, **Then** the system sends both the query and selected text to the backend for contextual processing.
2. **Given** the student has selected text and submitted a query, **When** the response returns, **Then** the response is focused on the selected text rather than the broader textbook content.

---

### Edge Cases

- What happens when the backend API is temporarily unavailable?
- How does the system handle extremely long user queries or selected text?
- What happens when the student asks about content that isn't in the textbook?
- How does the system handle concurrent users accessing the chatbot simultaneously?
- What happens when the API keys for Cohere, Gemini, or Qdrant are invalid or expired?
- How does the system handle network timeouts during API requests?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a chat interface component embedded in Docusaurus book pages that allows users to submit questions about textbook content
- **FR-002**: System MUST capture selected text on the page using browser APIs (window.getSelection()) and include it in the query context
- **FR-003**: System MUST send POST requests to /api/v1/chat endpoint with { "message": userQuery, "selected_text": selectedText, "session_id": sessionId } format
- **FR-004**: System MUST display AI-generated responses in the chat interface with proper formatting and source citations
- **FR-005**: System MUST handle CORS configuration to allow requests from both localhost:3000 (development) and production Vercel URL
- **FR-006**: System MUST implement local proxy configuration in package.json to forward API calls to http://localhost:8000 during development
- **FR-007**: System MUST maintain conversation history in the UI using React state management
- **FR-008**: System MUST handle API errors gracefully and display appropriate error messages to users
- **FR-009**: System MUST support both full-book RAG mode (when no selected text) and selected-text-only mode (when text is selected)
- **FR-010**: System MUST manage session IDs to maintain conversation continuity across page navigations
- **FR-011**: System MUST update the API base URL for production deployment to the deployed backend service
- **FR-012**: System MUST implement proper loading states and indicators during API requests
- **FR-013**: System MUST provide a clear way for users to clear chat history and start a new conversation
- **FR-014**: System MUST handle network timeouts and retry failed requests appropriately

### Key Entities

- **Chat Message**: Represents a single message in the conversation between user and AI assistant, including sender (user/assistant), content, timestamp, and source citations
- **Chat Session**: Represents a conversation context that persists across page views, identified by a unique session ID
- **Selected Text**: Represents user-selected content from textbook pages that provides focused context for queries
- **API Response**: Represents the structured response from the backend RAG service, including the AI-generated answer, source citations, and metadata

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can receive relevant answers to textbook-related questions within 5 seconds of submitting their query
- **SC-002**: The system successfully handles 100% of text selection operations and includes selected text in contextual queries
- **SC-003**: 95% of user queries receive contextually appropriate responses based on the textbook content or selected text context
- **SC-004**: The RAG chatbot maintains a 99% uptime during peak usage hours (8 AM - 10 PM)
- **SC-005**: Students report a 70% improvement in their ability to find answers to textbook questions compared to manual searching
- **SC-006**: The system can handle at least 100 concurrent users without degradation in response time
- **SC-007**: Chat interface loads and becomes responsive within 2 seconds on all supported textbook pages
- **SC-008**: The system achieves 99% success rate in API communication with zero CORS errors in both development and production environments

## Outcome

- ✅ Impact: Created comprehensive specification for frontend-backend integration of RAG chatbot
- 🧪 Tests: Defined acceptance scenarios for all user stories with measurable criteria
- 📁 Files: Generated spec.md and requirements checklist in feature directory
- 🔁 Next prompts: Ready for planning phase with `/sp.plan`
- 🧠 Reflection: Specification captures all integration requirements while maintaining user focus

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All quality criteria met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with planning phase