---
id: 006
title: Backend RAG Chatbot Planning
stage: plan
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-rag-chatbot
branch: 005-backend-rag-chatbot
user: Claude Sonnet 4.5
command: /sp.plan
labels: [plan,rag,chatbot,backend,education,architecture]
links:
  spec: specs/005-backend-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-backend-rag-chatbot/plan.md
 - specs/005-backend-rag-chatbot/research.md
 - specs/005-backend-rag-chatbot/data-model.md
 - specs/005-backend-rag-chatbot/contracts/api-contracts.md
 - specs/005-backend-rag-chatbot/quickstart.md
 - CLAUDE.md
tests:
 - specs/005-backend-rag-chatbot/contracts/api-contracts.md
---

## Prompt

Create a detailed, step-by-step plan to implement the backend for the integrated RAG chatbot in my hackathon project "Physical AI and Humanoid Robotics" textbook.
The frontend (Docusaurus site) is already built and deployed at: https://physical-ai-and-humanoid-robotic-bo-three.vercel.app (sitemap: https://physical-ai-and-humanoid-robotic-bo-three.vercel.app/sitemap.xml lists pages like intro-to-physical-ai, basics-humanoid-robotics, ros2-fundamentals, vision-language-action, digital-twin-simulation, capstone-pipeline, etc.).
The backend must follow these mandatory requirements:

Use Cohere embedding model (recommend embed-english-v3.0 or the latest suitable like embed-v4.0 if available in 2025 for technical content; prefer multilingual if needed but English-focused is fine).
Use Qdrant Cloud Free Tier as vector store.
Use GEMINI_API_KEY with OpenAI Agents SDK (via OpenAI-compatible endpoint: base_url="https://generativelanguage.googleapis.com/v1beta/openai/", model e.g. "gemini-2.0-flash" or "gemini-1.5-flash" or latest stable Gemini model that supports tool/function calling well).
Use FastAPI for the API layer.
Use Neon Serverless Postgres for relational storage (e.g., chat history, sessions, or query logs).
Support two modes: 1) Full book RAG (retrieve from Qdrant), 2) Only user-selected text (embed on-the-fly and generate without Qdrant or use simple similarity if multiple chunks).
All credentials from .env file.

Plan structure:

Overall folder structure and setup commands (using uv).
Environment & dependency installation steps.
Content ingestion pipeline: sitemap crawling → text extraction → chunking → Cohere embedding → Qdrant upload.
Retrieval & test script.
Agent definition with retrieval tool + selected-text handling.
FastAPI app setup with endpoints (e.g. /chat, /ingest if needed).
Frontend integration approach (CORS, how frontend calls backend locally or via proxy).
Testing steps and verification checklist.
Potential gotchas & best practices (e.g. handling rate limits, async usage, error handli

## Response snapshot

## Implementation Plan Complete: Backend RAG Chatbot for Physical AI and Humanoid Robotics Textbook

I have successfully created the complete implementation plan for the backend RAG chatbot. Here's a summary of what was accomplished:

### **Branch**: `005-backend-rag-chatbot`

### **Completed Artifacts**:
1. **Implementation Plan**: `specs/005-backend-rag-chatbot/plan.md` - Complete technical architecture and project structure
2. **Research Summary**: `specs/005-backend-rag-chatbot/research.md` - Technology decisions and best practices
3. **Data Model**: `specs/005-backend-rag-chatbot/data-model.md` - Complete entity definitions with relationships
4. **API Contracts**: `specs/005-backend-rag-chatbot/contracts/api-contracts.md` - Complete API specification
5. **Quickstart Guide**: `specs/005-backend-rag-chatbot/quickstart.md` - Step-by-step setup instructions
6. **Agent Context Updated**: Technology stack added to Claude Code context file

### **Key Architecture Decisions**:
- **Backend Structure**: Python 3.12 with FastAPI, organized in clean architecture layers
- **External Services**: Cohere for embeddings, Qdrant for vector storage, Gemini via OpenAI-compatible endpoint
- **Database**: Neon Serverless Postgres for relational data, Qdrant for vector storage
- **Dual Modes**: Full-book RAG and selected-text-only modes both supported
- **Security**: Environment variable-based credential management

### **Ready for Next Phase**:
The implementation plan is complete and ready for the next phase. You can now proceed with `/sp.tasks` to generate detailed implementation tasks.

## Outcome

- ✅ Impact: Created comprehensive implementation plan for backend RAG chatbot
- 🧪 Tests: Defined API contracts that can be used for contract testing
- 📁 Files: Generated plan.md, research.md, data-model.md, contracts, and quickstart.md
- 🔁 Next prompts: Ready for task generation with `/sp.tasks`
- 🧠 Reflection: Plan addresses all requirements with proper architecture decisions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All planning artifacts completed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate implementation tasks with /sp.tasks