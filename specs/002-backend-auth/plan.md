# Implementation Plan: Backend Environment & Authentication with RAG Integration

**Branch**: `002-backend-auth` | **Date**: 2025-12-17 | **Spec**: [link to spec]
**Input**: Feature specification from `/specs/002-backend-auth/spec.md`

## Summary

Complete implementation of a secure backend environment with authentication, authorization, and RAG functionality for the Physical AI & Humanoid Robotics textbook project. The system integrates FastAPI with JWT-based authentication, OAuth providers (Facebook, Google), secure credential handling via environment variables, and a RAG chatbot constrained to textbook content only. The architecture maintains free-tier compliance while supporting dual language (English/Urdu) embeddings and personalized learning experiences.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript/TypeScript (frontend)
**Primary Dependencies**: Docusaurus (frontend), FastAPI (backend), Qdrant (vector database), Neon PostgreSQL (for user data), LangChain (RAG functionality), python-jose (JWT), passlib (password hashing), Google Generative AI/ChatOpenAI (LLM integration)
**Storage**: Qdrant vector database (for embeddings), Neon PostgreSQL (for user data), SQLite (fallback for development)
**Testing**: pytest (backend), Jest (frontend), integration tests for auth and RAG functionality
**Target Platform**: Web application (Linux server deployment)
**Performance Goals**: <10 second response time for RAG queries, <3 second page load time, 50+ concurrent users support
**Constraints**: Free-tier resource limits (minimal GPU usage, lightweight embeddings), 60 requests/hour/IP rate limit, secure credential handling, RAG-only knowledge source
**Scale/Scope**: 6 textbook chapters, 50+ concurrent users, multi-language support (English/Urdu), authenticated personalization

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Simplicity
✅ PASS: Architecture uses minimal authentication components (JWT, OAuth) without unnecessary complexity.

### Gate 2: Accuracy
✅ PASS: RAG system will provide responses exclusively from textbook content with proper source attribution.

### Gate 3: Minimalism
✅ PASS: Technology stack is lightweight with minimal dependencies to support fast builds and deployment.

### Gate 4: Fast Builds
✅ PASS: FastAPI provides quick startup times and efficient authentication middleware.

### Gate 5: Free-tier Architecture
✅ PASS: All components support free-tier usage with minimal resource requirements.

### Gate 6: RAG-Only Knowledge Source
✅ PASS: System design ensures responses are generated exclusively from textbook content embeddings.

### Gate 7: Technical Constraints Compliance
✅ PASS: No heavy GPU usage, minimal embeddings, secure credential handling, OAuth integration, free-tier friendly.

### Gate 8: Credential Security
✅ PASS: Environment variables for secrets, no hard-coded credentials, secure token handling.

### Gate 9: Authentication Requirements
✅ PASS: Supports both email/password and OAuth (Facebook, Google) authentication methods.

### Gate 10: Language Support
✅ PASS: Dual language support (English/Urdu) with content-based language detection.

### Post-Design Review
✅ PASS: All design decisions align with constitution principles after Phase 1 implementation design.

## Project Structure

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py              # User entity with preferences and OAuth support
│   │   ├── session.py           # Session management
│   │   ├── textbook.py          # TextbookChapter entity
│   │   ├── embedding.py         # EmbeddingVector entity
│   │   ├── query.py             # UserQuery entity with language support
│   │   └── response.py          # ChatResponse entity with language support
│   ├── services/
│   │   ├── auth_service.py      # Authentication service (enhanced)
│   │   ├── oauth_service.py     # OAuth integration service
│   │   ├── rag_service.py       # Enhanced RAG functionality with LLM integration
│   │   ├── embedding_service.py # Embedding management
│   │   └── rate_limit_service.py # Rate limiting
│   ├── api/
│   │   ├── main.py              # Main FastAPI app with all routes
│   │   ├── auth_routes.py       # Authentication endpoints
│   │   ├── oauth_routes.py      # OAuth endpoints
│   │   ├── textbook_routes.py   # Textbook content endpoints
│   │   └── rag_routes.py        # Enhanced RAG chatbot endpoints
│   └── config/
│       ├── database.py          # Database configuration
│       └── settings.py          # Application settings with env vars
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── docusaurus/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RagChatbot.js    # RAG chatbot component
│   │   │   ├── TextSelector.js  # Text selection feature
│   │   │   ├── AuthProvider.js  # Authentication context
│   │   │   ├── LoginModal.js    # Login modal component
│   │   │   └── UserProfile.js   # User profile component
│   │   ├── pages/
│   │   └── css/
│   ├── static/
│   └── docusaurus.config.js     # Docusaurus configuration
└── tests/
    ├── unit/
    └── integration/
```

## Security & Compliance Implementation

### 1. Credential Management
- All sensitive credentials stored in environment variables via python-dotenv
- .env.example provided with placeholder values for documentation
- Settings validation at application startup with fail-fast behavior
- Secure defaults for all configuration values
- No hard-coded secrets in source code

### 2. Authentication Security
- JWT tokens with 24-hour expiration for session management
- Secure password hashing with bcrypt for email-based users
- OAuth state parameter validation for CSRF protection
- Rate limiting on authentication endpoints to prevent abuse
- Input validation and sanitization on all endpoints

### 3. RAG Content Constraints
- LLM responses constrained to textbook content only via system prompt
- Dual language embeddings (English/Urdu) in Qdrant vector database
- Content-based language detection for accurate retrieval
- Source attribution for all generated responses
- Strict validation that responses come only from textbook content

### 4. Data Protection
- User data stored in Neon PostgreSQL with proper indexing
- IP address hashing for privacy in rate limiting
- No personal data stored in RAG logs
- Secure session management with proper token validation

## Implementation Tasks Summary

### Phase 1: Core Infrastructure
1. Update User model with OAuth and preference fields
2. Enhance auth_service with JWT and OAuth functionality
3. Create oauth_service for provider integration
4. Add OAuth routes and callback handlers
5. Update settings to include all environment variables
6. Implement authentication middleware

### Phase 2: RAG Enhancement
7. Integrate LLM provider (Gemini/OpenAI) with RAG service
8. Implement content-constrained responses with system prompts
9. Add dual language support (English/Urdu) to RAG pipeline
10. Enhance embedding service with language filtering
11. Update data models with language fields

### Phase 3: Security & Compliance
12. Implement rate limiting on all endpoints
13. Add input validation and sanitization
14. Set up secure credential handling
15. Test authentication flows and security measures
16. Verify RAG content constraints and language support

### Phase 4: Frontend Integration
17. Create frontend auth components
18. Implement OAuth login buttons and flows
19. Add language preference UI
20. Integrate RAG chatbot with authentication context
21. Test complete user flows

## Risk Analysis & Mitigation

### Top 3 Risks:
1. **LLM API Costs**: Monitor usage and implement strict rate limiting
2. **OAuth Provider Changes**: Build flexible architecture to accommodate API changes
3. **Content Hallucination**: Strict system prompts and validation to ensure textbook-only responses

### Mitigation Strategies:
- Comprehensive monitoring and alerting for API usage
- Regular testing of OAuth flows and provider documentation review
- Content validation and source attribution for all responses
- Fallback mechanisms for LLM failures
- Regular security audits of credential handling

## Success Criteria

- ✅ Authentication works with both email/password and OAuth providers
- ✅ RAG responses are constrained to textbook content only
- ✅ Dual language support (English/Urdu) functions correctly
- ✅ Rate limiting prevents abuse while allowing reasonable access
- ✅ All credentials are handled securely via environment variables
- ✅ System operates within free-tier resource limits
- ✅ 95% of chatbot responses are accurately sourced from textbook content
- ✅ Users can personalize their learning experience with preferences
- ✅ Anonymous users can access core textbook content and RAG chatbot