import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import TextbookTranslator from './TextbookTranslator';
import RagChatbot from './RagChatbot';

const TextbookLayout = ({ children, title, description, currentContent }) => {
  const [translatedContent, setTranslatedContent] = useState(null);
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [processedChildren, setProcessedChildren] = useState(children);

  useEffect(() => {
    // When content is translated, we would update the children
    // For now, we'll just pass through the original children
    setProcessedChildren(children);
  }, [translatedContent]);

  const handleTranslationChange = (translated) => {
    setTranslatedContent(translated);
  };

  return (
    <Layout title={title} description={description}>
      <div className="textbook-container">
        <div className="textbook-header">
          <TextbookTranslator
            content={currentContent}
            onTranslationChange={handleTranslationChange}
            currentLanguage={currentLanguage}
          />
        </div>
        <main className="textbook-content">
          {processedChildren}
        </main>
        <div className="textbook-footer">
          <RagChatbot />
        </div>
      </div>
    </Layout>
  );
};

export default TextbookLayout;