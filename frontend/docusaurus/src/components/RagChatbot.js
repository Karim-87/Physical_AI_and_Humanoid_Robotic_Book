import React, { useState, useEffect, useRef } from 'react';
import './RagChatbot.css';
import ApiClient from './ApiClient';
import { useAuth } from './AuthProvider';

const RagChatbot = ({ defaultLanguage = 'en' }) => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?', sender: 'bot' }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState(defaultLanguage);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef(null);

  // Get auth context to access user preferences
  const { user, isAuthenticated } = useAuth();

  // Update language based on user preferences when user changes
  useEffect(() => {
    const loadUserPreferences = async () => {
      if (user && isAuthenticated) {
        try {
          const response = await fetch('/api/v1/auth/preferences', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('textbook_token')}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const data = await response.json();
            setLanguage(data.language || defaultLanguage);
          }
        } catch (error) {
          console.error('Error loading user preferences:', error);
        }
      }
    };

    loadUserPreferences();
  }, [user, isAuthenticated, defaultLanguage]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading]);

  const toggleChat = () => {
    setIsOpen(prev => !prev);
  };

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Call the backend API for RAG query with user's language preference
      const response = await ApiClient.queryRag(inputText, language);

      const botResponse = {
        id: Date.now() + 1,
        text: response.answer || 'I found relevant information in the textbook but could not generate a specific answer. Please try rephrasing your question.',
        sender: 'bot',
        sources: response.sources || []
      };

      setMessages(prev => [...prev, botResponse]);
      setIsLoading(false);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please make sure the backend server is running.',
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="rag-chatbot">
      {/* Floating toggle button */}
      <button
        className={`chatbot-toggle-button ${isOpen ? 'chatbot-toggle-open' : ''}`}
        onClick={toggleChat}
        aria-label={isOpen ? 'Close chatbot' : 'Open chatbot'}
      >
        {isOpen ? '×' : '💬'}
      </button>

      {/* Chat window */}
      {isOpen && (
        <div className="rag-chatbot-window">
          <div className="rag-chatbot-header">
            <span>Textbook AI Assistant</span>
            <button className="chatbot-close-button" onClick={toggleChat} aria-label="Close chatbot">
              ×
            </button>
          </div>
          <div className="rag-chatbot-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender}-message`}
              >
                {message.text}
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <small>Sources: {message.sources.join(', ')}</small>
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="message bot-message typing-indicator-message">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="rag-chatbot-input">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask about the textbook content..."
              rows="2"
              maxLength={5000}
              aria-label="Type your question"
            />
            <button onClick={sendMessage} disabled={isLoading} aria-label="Send message">
              Send
            </button>
          </div>
          {user && (
            <div className="chatbot-footer">
              <small>Current language: {language === 'en' ? 'English' : 'Urdu'}</small>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RagChatbot;
