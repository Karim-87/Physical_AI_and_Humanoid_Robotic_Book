# Quickstart Guide for AI-Native Textbook with RAG Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for Qdrant container)
- Git

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
DATABASE_URL=sqlite:///./textbook.db
QDRANT_URL=http://localhost:6333
NEON_DATABASE_URL=your_neon_db_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW=3600  # 1 hour in seconds
```

**Frontend (.env):**
```
REACT_APP_API_URL=http://localhost:8000
```

### 5. Start Qdrant Vector Database
```bash
docker run -d --name qdrant-container -p 6333:6333 qdrant/qdrant
```

### 6. Initialize Backend
```bash
cd backend
python -m src.models.database  # Initialize database
python -m src.services.embedding_service  # Initialize embeddings for textbook content
uvicorn src.api.main:app --reload --port 8000
```

### 7. Start Frontend
```bash
cd frontend/docusaurus
npm start
```

## Development Workflow

### Adding New Textbook Content
1. Create a new markdown file in `frontend/docusaurus/docs/`
2. Add the file to the sidebar configuration in `frontend/docusaurus/docusaurus.config.js`
3. Run the embedding service to process the new content:
   ```bash
   python -m src.services.embedding_service --add-new-content
   ```

### Testing the RAG Functionality
1. Access the frontend at `http://localhost:3000`
2. Navigate to any textbook chapter
3. Select text and use the "Ask AI" feature or use the chat interface
4. Verify responses are sourced from textbook content

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend/docusaurus
npm test
```

## Deployment

### Production Build
```bash
# Frontend
cd frontend/docusaurus
npm run build

# Serve the build
npx serve -s build
```

### Environment Variables for Production
- Set `NODE_ENV=production` for frontend
- Use proper secret keys and database URLs
- Configure reverse proxy for both frontend and backend

## Troubleshooting

### Common Issues
1. **Qdrant Connection Error**: Ensure Qdrant container is running and accessible at the configured URL
2. **Embedding Processing Error**: Check that all textbook content is properly formatted
3. **Rate Limiting**: Verify that rate limit settings match your requirements
4. **Authentication**: Ensure tokens are properly configured and not expired

### Performance Tips
- Monitor embedding size to stay within free-tier limits
- Use caching for frequently accessed textbook content
- Optimize database queries for user sessions