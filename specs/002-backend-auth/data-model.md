# Data Model for Backend Environment & Authentication

## Entities

### User
- **id**: string (unique identifier)
- **username**: string (unique username, 3-50 characters)
- **email**: string (email address, optional, unique if provided)
- **password_hash**: string (hashed password, null for OAuth users)
- **oauth_provider**: string (provider name for OAuth users: 'facebook', 'google', null for email users)
- **oauth_id**: string (provider's user ID for OAuth users, null for email users)
- **preferences**: JSON object (user preferences for personalization)
- **language_preference**: string (default language: 'en', 'ur', default: 'en')
- **personalization_enabled**: boolean (whether to show personalized content, default: true)
- **is_active**: boolean (whether account is active, default: true)
- **created_at**: datetime (account creation timestamp)
- **updated_at**: datetime (last update timestamp)
- **last_login_at**: datetime (last login timestamp, optional)

### UserSession
- **id**: string (unique identifier)
- **user_id**: string (foreign key to User)
- **session_token**: string (JWT token identifier, hashed)
- **created_at**: datetime (session start time)
- **expires_at**: datetime (session expiration time)
- **ip_address**: string (IP address of the session)
- **user_agent**: string (browser/device information)
- **is_active**: boolean (whether session is still valid, default: true)

### OAuthState
- **id**: string (unique identifier)
- **state**: string (random state parameter for OAuth security)
- **provider**: string ('facebook', 'google')
- **redirect_uri**: string (where to redirect after OAuth)
- **created_at**: datetime (timestamp of state creation)
- **expires_at**: datetime (when state expires, typically 5 minutes)

### RateLimitRecord
- **id**: string (unique identifier)
- **identifier**: string (IP address or user_id for rate limiting)
- **endpoint**: string (API endpoint being rate limited)
- **request_count**: integer (number of requests in current window)
- **window_start**: datetime (start of current rate limit window)
- **expires_at**: datetime (when rate limit expires)

### UserQuery (Enhanced)
- **id**: string (unique identifier)
- **user_id**: string (foreign key to User, null for anonymous)
- **query_text**: string (the original query, 1-1000 characters)
- **query_embedding**: array<float> (vector representation of query)
- **timestamp**: datetime (when query was made)
- **ip_address**: string (IP address for rate limiting)
- **language**: string (language of the query: 'en', 'ur')

### ChatResponse (Enhanced)
- **id**: string (unique identifier)
- **query_id**: string (foreign key to UserQuery)
- **response_text**: string (AI-generated response)
- **source_chapters**: array<string> (IDs of chapters used for response)
- **confidence_score**: float (confidence level of response, 0.0-1.0)
- **timestamp**: datetime (when response was generated)
- **language**: string (language of the response: 'en', 'ur')

## Relationships

- User → UserSession (1 to many): Each user can have multiple active sessions
- User → UserQuery (1 to many): Each user can make multiple queries
- UserQuery → ChatResponse (1 to 1): Each query generates one response
- UserQuery → EmbeddingVector (many to many through similarity): Queries match with relevant embeddings

## Validation Rules

- User.username must be 3-50 characters and unique
- User.email must be valid email format if provided and unique
- User.password_hash is required for email-based users
- User.oauth_provider and User.oauth_id must both be present or both null
- User.language_preference must be in SUPPORTED_LANGUAGES
- UserSession.session_token must be unique and properly hashed
- UserSession.expires_at must be in the future
- RateLimitRecord.request_count must not exceed configured limits per window
- ChatResponse.response_text must be sourced only from textbook content
- OAuthState.expires_at must be within 10 minutes of creation
- UserQuery.query_text must be 1-1000 characters
- UserQuery.language must be in SUPPORTED_LANGUAGES

## Indexes

- User: [username] (unique), [email] (unique, partial), [oauth_provider, oauth_id] (unique, partial)
- UserSession: [session_token] (unique), [user_id], [expires_at]
- RateLimitRecord: [identifier, endpoint, expires_at]
- UserQuery: [user_id], [timestamp], [ip_address]
- ChatResponse: [query_id]