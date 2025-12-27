# Physical AI and Humanoid Robotics RAG Chatbot Backend

This backend service provides RAG (Retrieval-Augmented Generation) capabilities for the Physical AI and Humanoid Robotics textbook, allowing students to ask questions and receive AI-generated responses based on textbook content.

## Features

- **RAG-powered Q&A**: Students can ask questions about the textbook content
- **Dual-mode support**: Full-book RAG or selected-text-only mode
- **Session management**: Persistent conversation history
- **Content ingestion**: Automated crawling and indexing of textbook content
- **API endpoints**: RESTful API for frontend integration

## Prerequisites

- Python 3.12+
- uv package manager
- Access to the following APIs:
  - Google AI Studio (for Gemini access)
  - Cohere API (for embeddings)
  - Qdrant Cloud (vector database)
  - Neon Serverless Postgres (relational database)

## Setup

### 1. Clone and navigate to the project

```bash
cd backend
```

### 2. Install dependencies

```bash
uv sync
# Or if using pip:
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
NEON_DATABASE_URL=your_neon_postgres_connection_string_here
```

### 4. Run the application

```bash
# Install dependencies
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Chat Endpoint
- **POST** `/api/v1/chat`
- Process user queries and return AI-generated responses
- Request body:
  ```json
  {
    "message": "string (required) - The user's query message",
    "selected_text": "string (optional) - Text selected by user from textbook",
    "session_id": "string (optional) - Existing session identifier, creates new if not provided"
  }
  ```
- Response:
  ```json
  {
    "response": "string - AI-generated response to the user query",
    "session_id": "string - Session identifier for continued conversation",
    "mode": "string - Either 'full-book' or 'selected-text-only'",
    "retrieved_chunks_count": "integer - Number of text chunks used to generate response",
    "response_time": "float - Time taken to generate response in seconds"
  }
  ```

### Health Check
- **GET** `/health`
- Check the health status of the backend service

### Content Ingestion
- **GET** `/api/v1/ingest`
- Trigger content ingestion from textbook sitemap

## Frontend Integration

### Local Development
- Run backend on port 8000: `http://localhost:8000`
- Frontend can call the API at `http://localhost:8000/api/v1/chat`

### Production
- Deploy backend (e.g., to Render/Vercel)
- Update frontend base URL to point to deployed backend

## Architecture

The backend follows a clean architecture pattern with:

- **API Layer**: FastAPI endpoints
- **Service Layer**: Business logic (retrieval, agent, session management)
- **Config Layer**: Service configuration and initialization
- **Model Layer**: Database models
- **Utility Layer**: Helper functions

## Development

### Running Tests

```bash
# Run the acceptance tests
uv run python -m tests.acceptance_tests
```

### Content Ingestion

To ingest the textbook content:

1. Ensure your API keys are properly configured
2. Run the ingestion script:
   ```bash
   uv run python scripts/ingestion.py
   ```

### Testing the RAG Pipeline

To test the retrieval functionality:

```bash
uv run python scripts/test_retrieval.py
```

## Deployment

The application can be deployed to any platform that supports Python applications (e.g., Render, Vercel, Heroku, AWS, etc.).

### Environment Variables for Production

Ensure all required environment variables are set in your deployment environment:

- `GEMINI_API_KEY`
- `COHERE_API_KEY`
- `QDRANT_API_KEY`
- `QDRANT_URL`
- `NEON_DATABASE_URL`
- `DEBUG` (set to "False" for production)

## Troubleshooting

- **API Rate Limits**: The system includes rate limiting to prevent exceeding API quotas
- **Qdrant Connection**: Ensure your Qdrant URL and API key are correct
- **Database Connection**: Verify your Neon Postgres connection string is valid
- **CORS Issues**: Check that your frontend domain is included in the CORS middleware

## License

This project is part of the Physical AI and Humanoid Robotics educational platform.