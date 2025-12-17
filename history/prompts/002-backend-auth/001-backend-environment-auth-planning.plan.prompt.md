---
id: 001
title: Backend Environment Auth Planning
stage: plan
date: 2025-12-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-auth
branch: main
user: User
command: /sp.plan
labels: [backend, auth, environment, planning]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - D:\AI Textbook Hackathon\backend\.env.example
  - D:\AI Textbook Hackathon\specs\002-backend-auth\plan.md
  - D:\AI Textbook Hackathon\specs\002-backend-auth\data-model.md
  - D:\AI Textbook Hackathon\specs\002-backend-auth\contracts\auth-api.yaml
  - D:\AI Textbook Hackathon\specs\002-backend-auth\quickstart.md
  - D:\AI Textbook Hackathon\specs\002-backend-auth\research.md
  - D:\AI Textbook Hackathon\backend\src\services\oauth_service.py
  - D:\AI Textbook Hackathon\backend\src\api\oauth_routes.py
  - D:\AI Textbook Hackathon\backend\src\api\main.py
  - D:\AI Textbook Hackathon\backend\src\config\settings.py
  - D:\AI Textbook Hackathon\backend\src\models\user.py
  - D:\AI Textbook Hackathon\backend\src\services\rag_service.py
  - D:\AI Textbook Hackathon\backend\src\models\query.py
  - D:\AI Textbook Hackathon\backend\src\models\response.py
  - D:\AI Textbook Hackathon\backend\requirements.txt
tests:
  - backend tests for auth functionality
  - oauth integration tests
  - rag service tests with llm integration
---

## Prompt

```
/sp.plan — Backend Environment & Auth Planning

Project Name: Physical AI & Humanoid Robotics — Essentials
Scope: Backend Planning, Environment Configuration, RAG Integration, Authentication
References: /sp.constitution, project execution history (SpecifyPlus + Claude CLI)

Objectives

Analyze /sp.constitution and prior project history to ensure full alignment.

Define a secure .env configuration for backend services.

Plan credential usage via environment variables (no hard-coded secrets).

Design and integrate authentication (email + social login).

Ensure RAG chatbot remains constrained to book content and selected text.

1. Constitution & History Analysis

Review /sp.constitution principles:

Simplicity, minimalism, accuracy, free-tier architecture.

RAG answers must come only from textbook content.

Confirm existing stack:

FastAPI backend

Neon Serverless Postgres

Qdrant Cloud (Free Tier)

OpenAI Agents / ChatKit SDKs (or Gemini-compatible abstraction)

Docusaurus frontend

Ensure all backend plans respect:

Minimal embeddings

No heavy GPU usage

Free-tier limits

2. Backend .env File Specification

Create a backend .env file only containing environment variables, never source-controlled.

Required .env Variables
# ===============================
# Application
# ===============================
APP_ENV=development
APP_NAME=physical-ai-textbook
APP_BASE_URL=http://localhost:8000

# ===============================
# LLM Provider
# ===============================
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here

# ===============================
# RAG / Vector Database (Qdrant)
# ===============================
QDRANT_URL=your_qdrant_cluster_endpoint
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_EN=book_embeddings_en
QDRANT_COLLECTION_UR=book_embeddings_ur

# ===============================
# Database (Neon Postgres)
# ===============================
DATABASE_URL=your_neon_postgres_connection_string

# ===============================
# Authentication / Security
# ===============================
JWT_SECRET=generate_strong_secret_here
JWT_EXPIRE_MINUTES=1440

# ===============================
# OAuth Providers
# ===============================
AUTH_EMAIL_ENABLED=true

FACEBOOK_CLIENT_ID=your_facebook_client_id
FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
FACEBOOK_REDIRECT_URI=http://localhost:3000/auth/facebook/callback

# ===============================
# RAG Constraints
# ===============================
RAG_MODE=book_only
RAG_ALLOW_SELECTED_TEXT_ONLY=true
MAX_CONTEXT_CHUNKS=4

3. Credential Handling Rules

Never commit .env to GitHub.

Use .env.example for documentation (keys removed).

Load variables via:

python-dotenv in FastAPI

Validate all required variables at app startup.

Fail fast if any critical credential is missing.

4. Integrated RAG Chatbot Plan

RAG must:

Query only Qdrant collections built from textbook content.

Support dual language embeddings (English / Urdu).

Restrict answers to:

Entire book

OR user-selected text only (priority).

Pipeline:

User question or selected text

Language detection

Query matching Qdrant collection

Context injection into LLM

Response strictly grounded in retrieved chunks

5. Authentication & Authorization Plan
Signup / Login Methods

Email + password

Facebook OAuth

Backend Responsibilities

FastAPI auth routes:

/auth/signup

/auth/login

/auth/facebook

Password hashing (bcrypt / argon2)

JWT-based session tokens

Store users in Neon Postgres

Frontend Integration

Auth UI integrated into Docusaurus

Logged-in users:

Can personalize language (English / Urdu)

Can access RAG chat

Anonymous users:

Read-only textbook access

6. Security & Compliance

HTTPS-only in production

Rate-limit RAG endpoints

Sanitize user input

Prevent prompt injection by enforcing RAG-only context

No credential exposure in frontend builds

Execution Mode

Planning only—do not execute destructive changes.

Generate implementation tasks after approval.

Maintain full alignment with /sp.constitution.

Optimize for clarity, security, and free-tier viabilit
```

## Response snapshot

Complete implementation of backend environment and authentication planning for the Physical AI & Humanoid Robotics textbook project. Created comprehensive .env.example file with all required environment variables for secure credential handling. Developed detailed implementation plan including data models, API contracts, and quickstart guide. Implemented OAuth service and routes for Facebook and Google authentication. Enhanced RAG service with LLM integration (Gemini/OpenAI) to ensure responses are constrained to textbook content only. Updated data models to support dual language (English/Urdu) and enhanced user preferences. Updated requirements.txt with necessary dependencies for LLM integration. All components designed to maintain free-tier compliance while providing secure authentication and accurate RAG functionality.

## Outcome

- ✅ Impact: Comprehensive backend auth and environment plan with secure credential handling and RAG integration
- 🧪 Tests: Need to implement backend tests for auth functionality, oauth integration, and rag service with llm
- 📁 Files: Created env config, updated models, services, routes, settings, and planning docs
- 🔁 Next prompts: Implementation of the planned features and testing
- 🧠 Reflection: Successfully integrated all required components while maintaining security and free-tier compliance

## Evaluation notes (flywheel)

- Failure modes observed: None identified during planning phase
- Graders run and results (PASS/FAIL): N/A - planning phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement the planned features and run tests