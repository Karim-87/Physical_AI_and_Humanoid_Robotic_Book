# Data Model: Backend RAG Chatbot for Physical AI and Humanoid Robotics Textbook

## Entity: Textbook Content
**Description**: Represents the educational material from the Physical AI and Humanoid Robotics textbook
**Fields**:
- `id` (string): Unique identifier for the content page
- `url` (string): Source URL of the textbook page
- `title` (string): Title of the textbook page
- `content` (text): Raw text content extracted from the page
- `created_at` (datetime): Timestamp when content was indexed
- `updated_at` (datetime): Timestamp when content was last updated

## Entity: Text Chunk
**Description**: Represents segments of textbook content that have been processed and prepared for embedding
**Fields**:
- `id` (string): Unique identifier for the chunk
- `content_id` (string): Reference to the parent textbook content
- `text` (text): The actual text content of the chunk
- `metadata` (json): Additional metadata (source URL, page title, etc.)
- `embedding_vector` (array): Vector representation of the text chunk
- `created_at` (datetime): Timestamp when chunk was created

## Entity: Embedding
**Description**: Vector representations of text chunks that enable semantic similarity search
**Fields**:
- `id` (string): Unique identifier for the embedding
- `chunk_id` (string): Reference to the text chunk
- `vector` (array): High-dimensional vector representation
- `model` (string): Embedding model used (e.g., "embed-english-v3.0")
- `created_at` (datetime): Timestamp when embedding was generated

## Entity: Chat Session
**Description**: Represents a conversation between a user and the RAG chatbot
**Fields**:
- `id` (string): Unique session identifier
- `user_id` (string, optional): Identifier for the user (if available)
- `created_at` (datetime): Timestamp when session started
- `updated_at` (datetime): Timestamp when session was last updated
- `active` (boolean): Whether the session is currently active

## Entity: Query Log
**Description**: Records of user questions and system responses for analytics
**Fields**:
- `id` (string): Unique identifier for the log entry
- `session_id` (string): Reference to the chat session
- `query` (text): The user's original question
- `response` (text): The system's response
- `retrieved_chunks` (array): IDs of chunks used in the response
- `mode` (string): Either "full-book" or "selected-text-only"
- `timestamp` (datetime): When the query was made
- `response_time` (float): Time taken to generate response in seconds

## Entity: Selected Text
**Description**: User-selected content from textbook pages for focused Q&A sessions
**Fields**:
- `id` (string): Unique identifier for the selected text
- `session_id` (string): Reference to the chat session
- `text` (text): The user-selected text content
- `embedding_vector` (array): Vector representation of the selected text
- `created_at` (datetime): Timestamp when text was selected

## Relationships
- Textbook Content 1 → * Text Chunk (one content page can have multiple chunks)
- Text Chunk 1 → 1 Embedding (one chunk has one embedding vector)
- Chat Session 1 → * Query Log (one session can have multiple queries)
- Chat Session 1 → * Selected Text (one session can have multiple selected text entries)

## Validation Rules
1. **Text Chunk**: Text must be between 100-1500 tokens to ensure meaningful semantic units
2. **Embedding**: Vector dimensions must match the expected embedding model output
3. **Query Log**: Mode must be either "full-book" or "selected-text-only"
4. **Chat Session**: Must have a valid session ID format and active state
5. **Textbook Content**: URL must be a valid URL from the textbook domain

## State Transitions
- Chat Session: `active` (true) ↔ `inactive` (false) based on user activity
- Query Log: Created when user submits query, response populated when generated