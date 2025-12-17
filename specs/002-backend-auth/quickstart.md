# Quickstart Guide for Backend Environment & Authentication

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for Qdrant container)
- Git
- Access to OAuth provider developer consoles (Facebook, Google)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend/docusaurus
npm install
```

### 4. Environment Configuration

Create `.env` files in both backend and frontend:

**Backend (.env):**
```
# Application
APP_ENV=development
APP_NAME=physical-ai-textbook
APP_BASE_URL=http://localhost:8000

# LLM Provider
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here

# For OpenAI as fallback (optional)
OPENAI_API_KEY=your_openai_api_key_here

# RAG / Vector Database (Qdrant)
QDRANT_URL=your_qdrant_cluster_endpoint
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_EN=book_embeddings_en
QDRANT_COLLECTION_UR=book_embeddings_ur

# Database (Neon Postgres)
DATABASE_URL=your_neon_postgres_connection_string

# Authentication / Security
JWT_SECRET=generate_strong_secret_here
JWT_EXPIRE_MINUTES=1440

# OAuth Providers (Optional)
FACEBOOK_CLIENT_ID=your_facebook_client_id
FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
FACEBOOK_REDIRECT_URI=http://localhost:3000/auth/facebook/callback

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

# RAG Constraints
RAG_MODE=book_only
RAG_ALLOW_SELECTED_TEXT_ONLY=true
MAX_CONTEXT_CHUNKS=4

# Rate Limiting
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW=3600

# Language Settings
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,ur
```

**Frontend (.env):**
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_FACEBOOK_APP_ID=your_facebook_app_id
REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
```

### 5. OAuth Provider Setup

#### Facebook OAuth Setup:
1. Go to [Facebook Developers Console](https://developers.facebook.com/)
2. Create a new app or select an existing one
3. Add "Facebook Login" product
4. Set valid OAuth redirect URIs to: `http://localhost:3000/auth/facebook/callback`
5. Note your App ID and App Secret

#### Google OAuth Setup:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google+ API
4. Go to Credentials > Create Credentials > OAuth 2.0 Client IDs
5. Set authorized redirect URIs to: `http://localhost:3000/auth/google/callback`
6. Note your Client ID and Client Secret

### 6. Start Qdrant Vector Database
```bash
docker run -d --name qdrant-container -p 6333:6333 qdrant/qdrant
```

### 7. Initialize Backend
```bash
cd backend
python -m src.models.database  # Initialize database
python -m src.services.embedding_service  # Initialize embeddings for textbook content
uvicorn src.api.main:app --reload --port 8000
```

### 8. Start Frontend
```bash
cd frontend/docusaurus
npm start
```

## Authentication Workflow

### Email/Password Registration
1. User visits `/auth/register` page
2. User provides username, email, and password
3. Backend validates input and creates hashed password
4. JWT token is returned and stored in frontend
5. User is logged in and can access personalized features

### OAuth Registration/Login
1. User clicks "Login with Facebook" or "Login with Google"
2. User is redirected to OAuth provider
3. User authenticates with provider and grants permissions
4. Provider redirects back with authorization code
5. Frontend sends code to backend `/auth/facebook` or `/auth/google`
6. Backend exchanges code for user info and creates/updates user account
7. JWT token is returned and stored in frontend
8. User is logged in and can access personalized features

### Personalization Features
1. Authenticated users can set language preference (English/Urdu)
2. Users can enable/disable personalization
3. Personalized chapter recommendations are shown based on preferences
4. User query history is stored for improved recommendations

## Development Workflow

### Adding New OAuth Providers
1. Update `src/services/oauth_service.py` with new provider implementation
2. Add new routes in `src/api/oauth_routes.py`
3. Update User model to support new provider
4. Add environment variables for new provider credentials

### Testing Authentication
```bash
# Backend tests
cd backend
python -m pytest tests/auth/

# Frontend tests
cd frontend/docusaurus
npm test
```

### Running Integration Tests
```bash
# Test authentication flows
python -m pytest tests/integration/test_auth.py

# Test RAG with authentication
python -m pytest tests/integration/test_rag_auth.py
```

## Security Best Practices

### Credential Management
- Never commit `.env` files to version control
- Use `.env.example` for documentation of required variables
- Rotate secrets regularly
- Use strong, randomly generated secrets

### Token Security
- JWT tokens have 24-hour expiration by default
- Refresh tokens are not implemented for simplicity
- Tokens are validated on each protected endpoint
- Session management is stateless (no server-side session storage)

### Rate Limiting
- 60 requests per hour per IP/user for RAG endpoints
- Rate limit headers are returned with responses
- Rate limit state is stored in database

## Troubleshooting

### Common Issues
1. **OAuth Redirect Error**: Ensure redirect URIs match exactly between OAuth provider and application
2. **JWT Validation Error**: Check that JWT_SECRET matches between frontend and backend
3. **Database Connection Error**: Verify DATABASE_URL is properly configured
4. **Qdrant Connection Error**: Ensure Qdrant container is running and accessible

### Debugging Authentication
1. Enable debug logging in settings
2. Check database for user records
3. Verify OAuth provider credentials and permissions
4. Test JWT token validation independently

### Performance Tips
- Monitor embedding size to stay within free-tier limits
- Use connection pooling for database connections
- Implement caching for frequently accessed user preferences
- Optimize OAuth token exchange for performance