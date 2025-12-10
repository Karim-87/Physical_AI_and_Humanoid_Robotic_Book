import React, { useState, useEffect } from 'react';
import './RagChatbot.css';
import ApiClient from './ApiClient';

const RagChatbot = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?', sender: 'bot' }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const toggleChat = () => {
    // In the textbook context, we might want to close the chatbot differently
    // For now, we'll just clear the messages to "close" it conceptually
    setMessages([
      { id: 1, text: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?', sender: 'bot' }
    ]);
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
      // Call the backend API for RAG query
      const response = await ApiClient.queryRag(inputText);

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
      <div className="rag-chatbot-window textbook-chatbot">
        <div className="rag-chatbot-header">
          <span>Textbook AI Assistant</span>
          <button className="chatbot-close-button" onClick={toggleChat}>
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
            <div className="message bot-message">
              Thinking...
            </div>
          )}
        </div>
        <div className="rag-chatbot-input">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about the textbook content..."
            rows="2"
          />
          <button onClick={sendMessage} disabled={isLoading}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default RagChatbot;