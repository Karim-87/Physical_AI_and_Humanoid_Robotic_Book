// Text selection utility using window.getSelection() API
class TextSelectionUtil {
  // Get currently selected text
  static getSelectedText() {
    if (typeof window !== 'undefined') {
      const selection = window.getSelection();
      return selection.toString().trim();
    }
    return '';
  }

  // Get detailed selection information
  static getSelectionInfo() {
    if (typeof window !== 'undefined') {
      const selection = window.getSelection();

      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const selectedText = selection.toString().trim();

        return {
          text: selectedText,
          range: range,
          rect: range.getBoundingClientRect(),
          startOffset: range.startOffset,
          endOffset: range.endOffset,
          startContainer: range.startContainer,
          endContainer: range.endContainer,
          isValid: selectedText.length > 0,
          startContainerNodeName: range.startContainer.nodeName,
          endContainerNodeName: range.endContainer.nodeName,
          startContainerParentTag: range.startContainer.parentElement ? range.startContainer.parentElement.tagName : null,
          endContainerParentTag: range.endContainer.parentElement ? range.endContainer.parentElement.tagName : null,
          selectionDirection: this.getSelectionDirection(range),
          wordCount: selectedText.split(/\s+/).filter(word => word.length > 0).length
        };
      }
    }

    return {
      text: '',
      range: null,
      rect: null,
      startOffset: null,
      endOffset: null,
      startContainer: null,
      endContainer: null,
      isValid: false,
      startContainerNodeName: null,
      endContainerNodeName: null,
      startContainerParentTag: null,
      endContainerParentTag: null,
      selectionDirection: null,
      wordCount: 0
    };
  }

  // Determine the direction of selection (left-to-right or right-to-left)
  static getSelectionDirection(range) {
    if (!range || !window.getSelection) {
      return null;
    }

    const selection = window.getSelection();
    if (selection.rangeCount === 0) {
      return null;
    }

    // Create a temporary range to compare positions
    const tempRange = document.createRange();
    tempRange.selectNodeContents(range.commonAncestorContainer);
    tempRange.setStart(range.startContainer, range.startOffset);

    const direction = tempRange.compareBoundaryPoints(Range.START_TO_END, range) === -1 ? 'left-to-right' : 'right-to-left';
    tempRange.detach(); // Clean up
    return direction;
  }

  // Check if there's any text currently selected
  static hasSelection() {
    const selectedText = this.getSelectedText();
    return selectedText.length > 0;
  }

  // Clear the current text selection
  static clearSelection() {
    if (typeof window !== 'undefined') {
      const selection = window.getSelection();
      if (selection) {
        selection.removeAllRanges();
      }
    }
  }

  // Get the element that contains the selection
  static getSelectionContainer() {
    if (typeof window !== 'undefined') {
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        return range.commonAncestorContainer;
      }
    }
    return null;
  }

  // Check if the selection is within a specific element
  static isSelectionInElement(element) {
    if (!element || typeof window === 'undefined') {
      return false;
    }

    const selectionInfo = this.getSelectionInfo();
    if (!selectionInfo.isValid) {
      return false;
    }

    // Check if the selection is within the specified element
    return element.contains(selectionInfo.startContainer) ||
           element.contains(selectionInfo.endContainer);
  }

  // Validate text selection length
  static validateSelectionLength(text, maxLength = 5000) {
    return text.length <= maxLength;
  }

  // Get contextual information around the selection
  static getSelectionContext(maxContextLength = 100) {
    const selectionInfo = this.getSelectionInfo();
    if (!selectionInfo.isValid) {
      return {
        before: '',
        selected: selectionInfo.text,
        after: ''
      };
    }

    // Get text content from the selection container
    let containerText = '';
    if (selectionInfo.startContainer.nodeType === Node.TEXT_NODE) {
      containerText = selectionInfo.startContainer.textContent;
    } else if (selectionInfo.startContainer.textContent) {
      containerText = selectionInfo.startContainer.textContent;
    }

    if (containerText) {
      const start = Math.max(0, selectionInfo.startOffset - maxContextLength);
      const end = Math.min(containerText.length, selectionInfo.endOffset + maxContextLength);

      return {
        before: containerText.substring(start, selectionInfo.startOffset),
        selected: selectionInfo.text,
        after: containerText.substring(selectionInfo.endOffset, end)
      };
    }

    return {
      before: '',
      selected: selectionInfo.text,
      after: ''
    };
  }

  // Get more detailed context information about the selection
  static getDetailedContext() {
    const selectionInfo = this.getSelectionInfo();
    if (!selectionInfo.isValid) {
      return {
        selectionInfo,
        context: {
          elementId: null,
          elementClass: null,
          elementTag: null,
          elementPath: [],
          documentTitle: typeof document !== 'undefined' ? document.title : null,
          documentUrl: typeof window !== 'undefined' ? window.location.href : null,
          selectionPosition: null
        }
      };
    }

    const element = selectionInfo.startContainer.parentElement || selectionInfo.startContainer;
    const context = {
      elementId: element.id || null,
      elementClass: element.className || null,
      elementTag: element.tagName ? element.tagName.toLowerCase() : null,
      elementPath: this.getElementPath(element),
      documentTitle: typeof document !== 'undefined' ? document.title : null,
      documentUrl: typeof window !== 'undefined' ? window.location.href : null,
      selectionPosition: {
        top: selectionInfo.rect.top,
        left: selectionInfo.rect.left,
        bottom: selectionInfo.rect.bottom,
        right: selectionInfo.rect.right,
        width: selectionInfo.rect.width,
        height: selectionInfo.rect.height
      }
    };

    return {
      selectionInfo,
      context
    };
  }

  // Get the DOM path of an element
  static getElementPath(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return [];
    }

    const path = [];
    let current = element;

    while (current && current.nodeType === Node.ELEMENT_NODE) {
      let selector = current.tagName.toLowerCase();

      if (current.id) {
        selector += `#${current.id}`;
        path.unshift(selector);
        break; // Stop at ID since it should be unique
      } else {
        let sibling = current.previousElementSibling;
        let nth = 1;

        while (sibling) {
          if (sibling.tagName === current.tagName) nth++;
          sibling = sibling.previousElementSibling;
        }

        if (nth !== 1) selector += `:nth-of-type(${nth})`;
        path.unshift(selector);
      }

      current = current.parentElement;
    }

    return path;
  }

  // Get the semantic context of the selected text (heading, paragraph, etc.)
  static getSemanticContext() {
    const selectionInfo = this.getSelectionInfo();
    if (!selectionInfo.isValid) {
      return null;
    }

    const element = selectionInfo.startContainer.parentElement || selectionInfo.startContainer;
    if (!element) return null;

    // Find the closest semantic elements
    const semanticContext = {
      heading: this.findClosestHeading(element),
      parentElementTag: element.tagName.toLowerCase(),
      parentElementClass: element.className,
      allParentTags: this.getParentTags(element)
    };

    return semanticContext;
  }

  // Find the closest heading element
  static findClosestHeading(element) {
    let current = element.parentElement;
    while (current) {
      const tag = current.tagName.toLowerCase();
      if (tag.startsWith('h') && /[1-6]/.test(tag[1])) {
        return {
          tag: tag,
          text: current.textContent.trim(),
          id: current.id || null
        };
      }
      current = current.parentElement;
    }
    return null;
  }

  // Get all parent tags
  static getParentTags(element) {
    const tags = [];
    let current = element.parentElement;
    while (current) {
      tags.push(current.tagName.toLowerCase());
      current = current.parentElement;
    }
    return tags;
  }

  // Store selected text in localStorage to preserve across page refreshes
  static storeSelectedText(selectedText, context = {}) {
    if (typeof window !== 'undefined' && selectedText) {
      const selectionData = {
        text: selectedText,
        timestamp: Date.now(),
        context: context,
        url: typeof window !== 'undefined' ? window.location.href : null
      };
      try {
        localStorage.setItem('chatbot_selected_text', JSON.stringify(selectionData));
      } catch (error) {
        console.error('Failed to store selected text in localStorage:', error);
      }
    }
  }

  // Retrieve selected text from localStorage
  static retrieveSelectedText() {
    if (typeof window !== 'undefined') {
      try {
        const storedData = localStorage.getItem('chatbot_selected_text');
        if (storedData) {
          const parsedData = JSON.parse(storedData);
          // Check if the data is still fresh (less than 1 hour old)
          if (Date.now() - parsedData.timestamp < 3600000) {
            return parsedData;
          } else {
            // Remove expired data
            localStorage.removeItem('chatbot_selected_text');
          }
        }
      } catch (error) {
        console.error('Failed to retrieve selected text from localStorage:', error);
      }
    }
    return null;
  }

  // Clear stored selected text
  static clearStoredSelectedText() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('chatbot_selected_text');
    }
  }
}

export default TextSelectionUtil;