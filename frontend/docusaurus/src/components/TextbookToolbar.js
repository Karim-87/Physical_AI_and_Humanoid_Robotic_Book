import React, { useState, useEffect } from 'react';
import './TextbookToolbar.css';
import LanguageSwitcher from './LanguageSwitcher';
import AuthenticatedRagChatbot from './AuthenticatedRagChatbot';

const TextbookToolbar = ({ content, chapterTitle }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const handleLanguageChange = (langCode) => {
    setCurrentLanguage(langCode);
    // In a real implementation, this would trigger content translation
    console.log(`Language changed to: ${langCode}`);
  };

  return (
    <div className="textbook-toolbar">
      <div className="toolbar-section translation-tools">
        <h4>Translation</h4>
        <LanguageSwitcher
          currentLanguage={currentLanguage}
          onLanguageChange={handleLanguageChange}
        />
      </div>
      <div className="toolbar-section chatbot-tools">
        <h4>AI Assistant</h4>
        <div className="inline-chatbot">
          <AuthenticatedRagChatbot />
        </div>
      </div>
    </div>
  );
};

export default TextbookToolbar;