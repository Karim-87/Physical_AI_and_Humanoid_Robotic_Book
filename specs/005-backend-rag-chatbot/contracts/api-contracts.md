# API Contracts: Backend RAG Chatbot

## Contract: /chat POST
**Purpose**: Process user queries and return AI-generated responses using RAG
**Endpoint**: `POST /chat`

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
    "cohere": "boolean - Status of Cohere API connection",
    "qdrant": "boolean - Status of Qdrant vector database connection",
    "postgres": "boolean - Status of Neon Postgres connection"
  }
}
```

---

## Contract: /ingest GET
**Purpose**: Trigger content ingestion from textbook sitemap
**Endpoint**: `GET /ingest`

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