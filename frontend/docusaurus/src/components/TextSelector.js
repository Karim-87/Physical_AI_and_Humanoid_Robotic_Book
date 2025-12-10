import React, { useEffect } from 'react';

const TextSelector = () => {
  useEffect(() => {
    const handleMouseUp = () => {
      const selectedText = window.getSelection().toString().trim();

      if (selectedText && selectedText.length > 0) {
        // Show a floating button or tooltip to ask about the selected text
        showAskButton(selectedText);
      } else {
        // Hide the button if no text is selected
        hideAskButton();
      }
    };

    const showAskButton = (selectedText) => {
      // Remove any existing button
      hideAskButton();

      // Create a new button
      const button = document.createElement('div');
      button.id = 'text-selector-ask-button';
      button.innerHTML = 'Ask AI';
      button.style.position = 'fixed';
      button.style.zIndex = '9999';
      button.style.backgroundColor = '#25c2a0';
      button.style.color = 'white';
      button.style.padding = '8px 12px';
      button.style.borderRadius = '4px';
      button.style.cursor = 'pointer';
      button.style.fontSize = '14px';
      button.style.boxShadow = '0 2px 4px rgba(0,0,0,0.2)';
      button.style.userSelect = 'none';

      // Position the button near the selection
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        button.style.top = (rect.top - 40) + 'px';
        button.style.left = (rect.left + rect.width/2 - 30) + 'px';
      }

      // Add click handler
      button.onclick = () => {
        // In a real implementation, this would trigger the RAG query
        // For now, we'll just log the selected text
        console.log('Selected text:', selectedText);

        // Send the selected text to the chatbot
        window.dispatchEvent(new CustomEvent('selectedTextQuery', {
          detail: { text: selectedText }
        }));

        hideAskButton();
      };

      document.body.appendChild(button);
    };

    const hideAskButton = () => {
      const existingButton = document.getElementById('text-selector-ask-button');
      if (existingButton) {
        existingButton.remove();
      }
    };

    // Add event listeners
    document.addEventListener('mouseup', handleMouseUp);

    // Clean up event listeners
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      hideAskButton();
    };
  }, []);

  return null; // This component doesn't render anything itself
};

export default TextSelector;