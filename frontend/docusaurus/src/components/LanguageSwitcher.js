import React, { useState, useEffect } from 'react';
import './LanguageSwitcher.css';

const LanguageSwitcher = ({ currentLanguage = 'en', onLanguageChange = () => {} }) => {
  const [selectedLanguage, setSelectedLanguage] = useState(currentLanguage);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'ur', name: 'اردو' }
  ];

  const handleLanguageChange = (langCode) => {
    setSelectedLanguage(langCode);
    onLanguageChange(langCode);
  };

  return (
    <div className="language-switcher">
      <select
        value={selectedLanguage}
        onChange={(e) => handleLanguageChange(e.target.value)}
        className="language-select"
      >
        {languages.map(lang => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSwitcher;