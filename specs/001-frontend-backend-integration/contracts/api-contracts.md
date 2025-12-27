# API Contracts: Frontend Backend Integration for RAG Chatbot

## Contract: /api/v1/chat POST
**Purpose**: Process user queries and return AI-generated responses using RAG
**Endpoint**: `POST /api/v1/chat`

### Request
```json
{
  "message": "string (required) - The user's query message",
  "selected_text": "string (optional) - Text selected by user from textbook",
  "session_id": "string (optional) - Existing session identifier, creates new if not provided"
}
```

### Response
```json
{
  "response": "string - AI-generated response to the user query",
  "session_id": "string - Session identifier for continued conversation",
  "mode": "string - Either 'full-book' or 'selected-text-only'",
  "retrieved_chunks_count": "integer - Number of text chunks used to generate response",
  "response_time": "float - Time taken to generate response in seconds"
}
```

### Error Responses
- `400 Bad Request`: Invalid request format or missing required fields
- `429 Too Many Requests`: Rate limit exceeded for external APIs
- `500 Internal Server Error`: Unexpected error during processing

---

## Contract: /health GET
**Purpose**: Check the health status of the backend service
**Endpoint**: `GET /health`

### Response
```json
{
  "status": "string - 'healthy' if service is operational",
  "timestamp": "string - ISO 8601 formatted timestamp",
  "dependencies": {
    "qdrant": "boolean - Status of Qdrant vector database connection",
    "cohere": "boolean - Status of Cohere API connection",
    "gemini": "boolean - Status of Gemini API connection",
    "postgres": "boolean - Status of Neon Postgres connection"
  }
}
```

---

## Contract: /api/v1/ingest GET
**Purpose**: Trigger content ingestion from textbook sitemap
**Endpoint**: `GET /api/v1/ingest`

### Query Parameters
- `force` (optional, boolean): If true, re-ingest all content even if already present

### Response
```json
{
  "status": "string - 'started' if ingestion process initiated",
  "pages_processed": "integer - Number of pages processed",
  "chunks_created": "integer - Number of text chunks created",
  "message": "string - Human-readable status message"
}
```

### Error Responses
- `423 Locked`: Ingestion already in progress
- `500 Internal Server Error`: Error during content ingestion

---

## Frontend Integration Contract

### Package.json Proxy Configuration
**Purpose**: Enable local development without CORS issues
**Configuration**:
```json
{
  "name": "docusaurus-frontend",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "start": "docusaurus start",
    "build": "docusaurus build",
    "swizzle": "docusaurus swizzle",
    "deploy": "docusaurus deploy",
    "clear": "docusaurus clear",
    "serve": "docusaurus serve",
    "write-translations": "docusaurus write-translations",
    "write-heading-ids": "docusaurus write-heading-ids"
  },
  "proxy": "http://localhost:8000",
  "browserslist": {
    "production": [
      ">0.5%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

### Environment Configuration
**Purpose**: Manage API base URLs for different environments
**Configuration**:
```javascript
// For development
const API_BASE_URL = process.env.NODE_ENV === 'development'
  ? ''  // Empty string to use proxy
  : 'https://your-deployed-backend-url.com';  // Production backend URL

// Example usage in Chatbot component
const sendMessage = async (message, selectedText, sessionId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      selectedText,
      sessionId
    })
  });

  return response.json();
};
```