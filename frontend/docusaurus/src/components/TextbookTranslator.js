import React, { useState, useEffect } from 'react';
import ApiClient from '../components/ApiClient';

const TextbookTranslator = ({ content, onTranslationChange, currentLanguage }) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [translatedContent, setTranslatedContent] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState(currentLanguage || 'en');

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'ur', name: 'اردو' }
  ];

  const translateContent = async () => {
    if (selectedLanguage === 'en' || !content) {
      // If English is selected, show original content
      onTranslationChange(content);
      return;
    }

    setIsTranslating(true);
    try {
      // In a real implementation, this would call the backend translation API
      // For now, we'll simulate the translation process
      const response = await ApiClient.request('/textbook/translate', {
        method: 'POST',
        body: JSON.stringify({
          content: content,
          target_language: selectedLanguage
        })
      });

      setTranslatedContent(response.translated_content);
      onTranslationChange(response.translated_content);
    } catch (error) {
      console.error('Translation error:', error);
      // Fallback to original content if translation fails
      onTranslationChange(content);
    } finally {
      setIsTranslating(false);
    }
  };

  useEffect(() => {
    if (selectedLanguage) {
      translateContent();
    }
  }, [selectedLanguage]);

  const handleLanguageChange = (langCode) => {
    setSelectedLanguage(langCode);
  };

  return (
    <div className="textbook-translator">
      <div className="translator-controls">
        <select
          value={selectedLanguage}
          onChange={(e) => handleLanguageChange(e.target.value)}
          disabled={isTranslating}
          className="translator-select"
        >
          {languages.map(lang => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
        {isTranslating && <span className="translating-indicator">Translating...</span>}
      </div>
    </div>
  );
};

export default TextbookTranslator;