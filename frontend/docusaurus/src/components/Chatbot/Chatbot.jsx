import React, { useState, useRef, useEffect } from 'react';
import { useThemeContext } from '@docusaurus/theme-common';
import { getApiBaseUrl, API_ENDPOINTS, buildApiUrl } from '../../utils/apiConfig';
import apiService from '../../utils/ApiService';
import sessionManager from '../../utils/SessionManager';
import TextSelectionUtil from '../../utils/TextSelectionUtil';
import { ErrorHandler } from '../../utils/ErrorHandler';
import ValidationUtil from '../../utils/ValidationUtil';
import chatContext from '../../utils/StateManagement';

import './Chatbot.css';

const Chatbot = ({ pageText = "" }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(sessionManager.getCurrentSessionId());
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Initialize with a welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{
        id: 'welcome-' + Date.now(),
        sender: 'assistant',
        content: 'Hello! I\'m your AI assistant for this textbook. Ask me any questions about the content on this page or select text to ask specific questions about it.',
        timestamp: new Date()
      }]);
    }
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = TextSelectionUtil.getSelectedText();
      if (selectedText && selectedText.length > 0 && selectedText.length <= 5000) {
        // Optionally show a visual indicator that text is selected
        chatContext.setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();

    // Check for extremely long user queries
    const longContentCheck = ErrorHandler.handleLongContent(userMessage, 10000, 'user query');
    if (!longContentCheck.isValid) {
      const errorMsgObj = {
        id: 'error-' + Date.now(),
        sender: 'assistant',
        content: longContentCheck.message,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMsgObj]);
      return;
    }

    setInputValue('');
    setIsLoading(true);

    // Add user message to UI immediately
    const userMsgObj = {
      id: 'user-' + Date.now(),
      sender: 'user',
      content: userMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsgObj]);

    try {
      // Get selected text if any
      const selectedText = TextSelectionUtil.getSelectedText();

      // Validate selected text length to ensure it meets API constraints
      if (selectedText && selectedText.length > 0) {
        // Check for extremely long selected text
        const longSelectedTextCheck = ErrorHandler.handleLongContent(selectedText, 5000, 'selected text');
        if (!longSelectedTextCheck.isValid) {
          throw new Error(longSelectedTextCheck.message);
        }

        const isValidLength = TextSelectionUtil.validateSelectionLength(selectedText, 5000);

        if (!isValidLength) {
          throw new Error('Selected text is too long. Please select a shorter portion of text.');
        }
      }

      // Check if we have selected text to determine the mode
      const hasSelectedText = selectedText && selectedText.length > 0;

      // Optionally show a message about which mode is being used
      if (hasSelectedText) {
        // Add a system message to indicate selected text mode
        const modeMsgObj = {
          id: 'system-' + Date.now(),
          sender: 'system',
          content: `Querying about selected text: "${selectedText.substring(0, 100)}${selectedText.length > 100 ? '...' : ''}"`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, modeMsgObj]);
      }

      // Validate the request payload
      const validation = ValidationUtil.validateChatRequest({
        message: userMessage,
        selected_text: selectedText || null,
        session_id: sessionId
      });

      if (!validation.isValid) {
        throw new Error(`Invalid request: ${validation.errors.map(e => e.message).join('; ')}`);
      }

      // Use the API service to make the request
      const response = await apiService.chat(userMessage, selectedText || null, sessionId);

      // Validate the response
      const responseValidation = ValidationUtil.validateChatResponse(response);
      if (!responseValidation.isValid) {
        throw new Error(`Invalid response: ${responseValidation.errors.map(e => e.message).join('; ')}`);
      }

      // Update session ID if new one was returned
      if (response.session_id && response.session_id !== sessionId) {
        setSessionId(response.session_id);
        sessionManager.updateSessionId(response.session_id);
      }

      const botMsgObj = {
        id: 'assistant-' + Date.now(),
        sender: 'assistant',
        content: response.response,
        timestamp: new Date(),
        sources: response.sources || [],
        mode: response.mode, // Include mode information for display purposes
        retrieved_chunks_count: response.retrieved_chunks_count
      };

      setMessages(prev => [...prev, botMsgObj]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Use the error handler to get a user-friendly error message
      let errorInfo;

      // Check if it's a content not found error from the backend
      if (error.message && error.message.toLowerCase().includes('content not found')) {
        errorInfo = {
          type: 'content_not_found',
          message: 'The topic you asked about doesn\'t appear to be covered in the textbook. Try asking about a different topic or be more specific.',
          severity: 'medium'
        };
      } else {
        errorInfo = ErrorHandler.handleApiError(error, 'chat');
      }

      const errorMsgObj = {
        id: 'error-' + Date.now(),
        sender: 'assistant',
        content: errorInfo.message,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMsgObj]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([{
      id: 'welcome-' + Date.now(),
      sender: 'assistant',
      content: 'Chat history cleared. How can I help you with this textbook content?',
      timestamp: new Date()
    }]);
    // Optionally create a new session
    sessionManager.clearSession();
    setSessionId(sessionManager.getCurrentSessionId());
  };

  return (
    <div className="chatbot-container" ref={chatContainerRef}>
      <div className="chat-header">
        <h3>Textbook AI Assistant</h3>
        <button
          onClick={handleClearChat}
          className="clear-chat-button"
          title="Clear chat history"
        >
          Clear Chat
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender}`}>
            <div className="message-content">{msg.content}</div>
            {msg.mode && msg.sender === 'assistant' && (
              <div className="message-mode">
                <small>Mode: {msg.mode}</small>
              </div>
            )}
            {msg.retrieved_chunks_count !== undefined && msg.sender === 'assistant' && (
              <div className="message-chunks">
                <small>Retrieved {msg.retrieved_chunks_count} chunks</small>
              </div>
            )}
            {msg.sources && msg.sources.length > 0 && (
              <div className="message-sources">
                <strong>Sources:</strong> {msg.sources.join(', ')}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          ref={inputRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the textbook content..."
          disabled={isLoading}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="chat-send-button"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default Chatbot;