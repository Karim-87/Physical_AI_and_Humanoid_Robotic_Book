# Quickstart Guide: Frontend Backend Integration for RAG Chatbot

## Prerequisites
- Node.js 18+ installed
- Python 3.12+ installed
- Git installed
- Access to the existing backend running on http://localhost:8000
- Docusaurus project already set up in the root directory

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
# If not already in the project directory
cd /path/to/AI-Textbook-Hackathon
```

### 2. Ensure Backend is Running
```bash
# Navigate to backend directory
cd backend

# Make sure the backend is running on port 8000
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Configure Frontend for Local Development
```bash
# In the root directory (frontend), add proxy to package.json
cat >> package.json << 'EOF'
,
  "proxy": "http://localhost:8000"
EOF
```

### 4. Create Chatbot Component Directory
```bash
mkdir -p src/components/Chatbot
```

### 5. Create the Chatbot Component
```bash
# Create Chatbot.jsx in src/components/Chatbot
cat > src/components/Chatbot/Chatbot.jsx << 'EOF'
import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

const Chatbot = ({ pageText = "" }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getSelectedText = () => {
    const selection = window.getSelection();
    return selection.toString().trim();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue;
    setInputValue('');
    setIsLoading(true);

    // Add user message to UI immediately
    const userMsgObj = {
      id: Date.now(),
      sender: 'user',
      content: userMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsgObj]);

    try {
      // Get selected text if any
      const selectedText = getSelectedText();

      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          selected_text: selectedText || null,
          session_id: sessionId || null
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update session ID if new one was created
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
      }

      const botMsgObj = {
        id: Date.now() + 1,
        sender: 'assistant',
        content: data.response,
        timestamp: new Date(),
        sources: data.sources || []
      };

      setMessages(prev => [...prev, botMsgObj]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMsgObj = {
        id: Date.now() + 1,
        sender: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMsgObj]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender}`}>
            <div className="message-content">{msg.content}</div>
            {msg.sources && msg.sources.length > 0 && (
              <div className="message-sources">
                Sources: {msg.sources.join(', ')}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the textbook content..."
          disabled={isLoading}
          className="chat-input"
        />
        <button type="submit" disabled={isLoading} className="chat-send-button">
          Send
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
EOF
```

### 6. Create Chatbot Styles
```bash
# Create Chatbot.css in src/components/Chatbot
cat > src/components/Chatbot/Chatbot.css << 'EOF'
.chatbot-container {
  display: flex;
  flex-direction: column;
  height: 400px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  margin: 20px 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #fafafa;
}

.message {
  margin-bottom: 16px;
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background-color: #e3f2fd;
  align-self: flex-end;
  margin-left: auto;
}

.message.assistant {
  background-color: #ffffff;
  border: 1px solid #eee;
}

.message-sources {
  font-size: 0.8em;
  color: #666;
  margin-top: 4px;
}

.chat-input-form {
  display: flex;
  padding: 16px;
  background-color: white;
  border-top: 1px solid #eee;
}

.chat-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 8px;
}

.chat-send-button {
  padding: 8px 16px;
  background-color: #007cba;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-send-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
EOF
```

### 7. Update Docusaurus Configuration
```bash
# Add the chatbot component import to docusaurus.config.js
# This assumes you want to add it globally to all pages
# You may want to customize this based on your specific needs
```

### 8. Run the Frontend Development Server
```bash
# In the root directory
npm run start
# or
yarn start
```

## Testing the Integration
```bash
# With both backend (port 8000) and frontend (port 3000) running:

# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint via proxy
curl -X POST http://localhost:3000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Physical AI?",
    "selected_text": null,
    "session_id": null
  }'
```

## Environment Variables for Production
- `REACT_APP_API_BASE_URL`: Set to your deployed backend URL for production builds
- `NODE_ENV`: Used to determine whether to use proxy or direct API calls

## Deployment Configuration
1. For Vercel deployment, ensure the frontend environment variables are configured
2. Set the backend API URL in production builds
3. Update CORS settings in the backend to allow your deployed frontend domain
4. Test the integration after deployment

## Troubleshooting
- If CORS errors occur in development, ensure the proxy is configured in package.json
- If API calls fail in production, check that the backend URL is correctly set
- Verify that the backend is running and accessible from the frontend
- Check browser console for any JavaScript errors