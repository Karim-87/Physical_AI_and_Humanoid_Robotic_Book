# Data Model: Frontend Backend Integration for RAG Chatbot

## Entity: Chat Message
**Description**: Represents a single message in the conversation between user and AI assistant
**Fields**:
- `id` (string): Unique identifier for the message
- `sender` (string): Either "user" or "assistant"
- `content` (string): The text content of the message
- `timestamp` (datetime): When the message was created
- `sources` (array): List of source citations (for assistant messages)
- `sessionId` (string): Reference to the chat session

## Entity: Chat Session
**Description**: Represents a conversation context that persists across page views
**Fields**:
- `id` (string): Unique session identifier
- `messages` (array): Array of ChatMessage objects
- `createdAt` (datetime): When the session was created
- `lastActiveAt` (datetime): When the session was last used
- `isActive` (boolean): Whether the session is currently active

## Entity: API Request Payload
**Description**: Structure of the request sent from frontend to backend
**Fields**:
- `message` (string): The user's query message
- `selectedText` (string, optional): Text selected by user from the page
- `sessionId` (string, optional): Existing session identifier (creates new if not provided)

## Entity: API Response Payload
**Description**: Structure of the response received from backend
**Fields**:
- `response` (string): AI-generated response to the user query
- `sessionId` (string): Session identifier for continued conversation
- `mode` (string): Either "full-book" or "selected-text-only"
- `retrievedChunksCount` (integer): Number of text chunks used to generate response
- `responseTime` (float): Time taken to generate response in seconds
- `sources` (array): Source citations for the response

## Entity: Selected Text
**Description**: Represents user-selected content from textbook pages that provides focused context for queries
**Fields**:
- `id` (string): Unique identifier for the selection
- `content` (string): The actual selected text
- `position` (object): Position information (start/end indices, page location)
- `timestamp` (datetime): When the text was selected

## Entity: API Response
**Description**: Represents the structured response from the backend RAG service
**Fields**:
- `aiResponse` (string): The AI-generated answer to the user's question
- `citations` (array): List of source citations referenced in the response
- `metadata` (object): Additional metadata (confidence scores, processing time, etc.)
- `sessionId` (string): Session identifier for conversation continuity

## Relationships
- Chat Session 1 → * Chat Message (one session contains multiple messages)
- Chat Message 1 → 1 Selected Text (when user provides selected text context)
- Chat Message 1 → 1 API Response (each user message generates one response)

## Validation Rules
1. **Chat Message**: Content must be between 1-2000 characters to prevent overly long messages
2. **Chat Session**: Must have a valid session ID format and maintain message order
3. **API Request**: Message field is required, selectedText is optional but limited to 5000 characters
4. **Selected Text**: Must be contiguous text from the current page, not exceed 5000 characters
5. **API Response**: Must contain either a response or an error message, never both empty

## State Transitions
- Chat Session: `isActive` (true) ↔ `inactive` (false) based on user activity
- Chat Message: `pending` (being sent) → `sent` (delivered) → `received` (response processed)
- API Request: `initialized` → `in-progress` → `success` or `error`