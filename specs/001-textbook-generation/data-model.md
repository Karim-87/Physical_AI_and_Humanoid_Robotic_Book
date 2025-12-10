# Data Model for AI-Native Textbook with RAG Chatbot

## Entities

### TextbookChapter
- **id**: string (unique identifier)
- **title**: string (chapter title)
- **content**: string (chapter content in markdown format)
- **order**: integer (sequence number for navigation)
- **language**: string (language code, e.g., 'en', 'ur')
- **metadata**: object (additional information like word count, reading time)

### EmbeddingVector
- **id**: string (unique identifier)
- **chapter_id**: string (foreign key to TextbookChapter)
- **content**: string (the text that was embedded)
- **embedding**: array<float> (vector representation of content)
- **section_ref**: string (reference to specific section in chapter)
- **created_at**: datetime (timestamp of embedding creation)

### User
- **id**: string (unique identifier)
- **username**: string (unique username)
- **email**: string (email address, optional)
- **password_hash**: string (hashed password)
- **preferences**: object (user preferences for personalization)
- **created_at**: datetime (account creation timestamp)

### UserQuery
- **id**: string (unique identifier)
- **user_id**: string (foreign key to User, null for anonymous)
- **query_text**: string (the original query)
- **query_embedding**: array<float> (vector representation of query)
- **timestamp**: datetime (when query was made)
- **ip_address**: string (hashed IP for rate limiting)

### ChatResponse
- **id**: string (unique identifier)
- **query_id**: string (foreign key to UserQuery)
- **response_text**: string (AI-generated response)
- **source_chapters**: array<string> (IDs of chapters used for response)
- **confidence_score**: float (confidence level of response)
- **timestamp**: datetime (when response was generated)

### UserSession
- **id**: string (unique identifier)
- **user_id**: string (foreign key to User)
- **session_token**: string (session identifier)
- **created_at**: datetime (session start time)
- **expires_at**: datetime (session expiration time)

### RateLimitRecord
- **id**: string (unique identifier)
- **ip_address**: string (IP address being rate limited)
- **request_count**: integer (number of requests in current window)
- **window_start**: datetime (start of current rate limit window)
- **expires_at**: datetime (when rate limit expires)

## Relationships

- TextbookChapter → EmbeddingVector (1 to many): Each chapter has multiple embedding vectors
- User → UserQuery (1 to many): Each user can make multiple queries
- User → UserSession (1 to many): Each user can have multiple sessions
- UserQuery → ChatResponse (1 to 1): Each query generates one response
- UserQuery → EmbeddingVector (many to many through similarity): Queries match with relevant embeddings

## Validation Rules

- TextbookChapter.title must be 1-200 characters
- TextbookChapter.order must be positive integer
- User.username must be 3-50 characters and unique
- UserQuery.query_text must be 1-1000 characters
- RateLimitRecord.request_count must not exceed 60 per hour per IP
- ChatResponse.response_text must be sourced only from textbook content