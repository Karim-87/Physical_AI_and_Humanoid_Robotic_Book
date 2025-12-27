// Loading and state management utilities for chat interface
class LoadingState {
  constructor() {
    this.loadingStates = new Map();
  }

  // Set loading state for a specific component/task
  setLoading(key, isLoading, message = null) {
    this.loadingStates.set(key, {
      isLoading,
      message,
      timestamp: Date.now()
    });
  }

  // Get loading state for a specific component/task
  getLoading(key) {
    return this.loadingStates.get(key) || { isLoading: false, message: null };
  }

  // Check if any loading state is active
  isAnyLoading() {
    for (const [key, state] of this.loadingStates) {
      if (state.isLoading) {
        return true;
      }
    }
    return false;
  }

  // Get all loading states
  getAllLoadingStates() {
    const states = {};
    for (const [key, state] of this.loadingStates) {
      states[key] = state;
    }
    return states;
  }

  // Clear loading state for a specific key
  clearLoading(key) {
    this.loadingStates.delete(key);
  }

  // Clear all loading states
  clearAllLoading() {
    this.loadingStates.clear();
  }
}

// Message state management
class MessageState {
  constructor() {
    this.messages = [];
    this.sessionId = null;
  }

  // Add a message to the state
  addMessage(message) {
    this.messages.push({
      id: message.id || Date.now(),
      sender: message.sender,
      content: message.content,
      timestamp: message.timestamp || new Date(),
      sources: message.sources || [],
      status: message.status || 'sent' // 'sent', 'delivered', 'read', 'error'
    });
  }

  // Update a message in the state
  updateMessage(id, updates) {
    const messageIndex = this.messages.findIndex(msg => msg.id === id);
    if (messageIndex !== -1) {
      this.messages[messageIndex] = {
        ...this.messages[messageIndex],
        ...updates
      };
    }
  }

  // Remove a message from the state
  removeMessage(id) {
    this.messages = this.messages.filter(msg => msg.id !== id);
  }

  // Clear all messages
  clearMessages() {
    this.messages = [];
  }

  // Get all messages
  getMessages() {
    return [...this.messages];
  }

  // Get messages by sender
  getMessagesBySender(sender) {
    return this.messages.filter(msg => msg.sender === sender);
  }

  // Set session ID
  setSessionId(sessionId) {
    this.sessionId = sessionId;
  }

  // Get session ID
  getSessionId() {
    return this.sessionId;
  }

  // Get message count
  getMessageCount() {
    return this.messages.length;
  }

  // Get the last message
  getLastMessage() {
    if (this.messages.length > 0) {
      return this.messages[this.messages.length - 1];
    }
    return null;
  }
}

// Chat context state management
class ChatContext {
  constructor() {
    this.loadingState = new LoadingState();
    this.messageState = new MessageState();
    this.context = {
      selectedText: null,
      currentPage: null,
      userInput: '',
      isInitialized: false
    };
  }

  // Initialize the chat context
  initialize() {
    this.context.isInitialized = true;
  }

  // Set current page context
  setCurrentPage(page) {
    this.context.currentPage = page;
  }

  // Get current page context
  getCurrentPage() {
    return this.context.currentPage;
  }

  // Set selected text context
  setSelectedText(text) {
    this.context.selectedText = text;
  }

  // Get selected text context
  getSelectedText() {
    return this.context.selectedText;
  }

  // Set user input
  setUserInput(input) {
    this.context.userInput = input;
  }

  // Get user input
  getUserInput() {
    return this.context.userInput;
  }

  // Get loading state instance
  getLoadingState() {
    return this.loadingState;
  }

  // Get message state instance
  getMessageState() {
    return this.messageState;
  }

  // Reset the entire context
  reset() {
    this.loadingState.clearAllLoading();
    this.messageState.clearMessages();
    this.context = {
      selectedText: null,
      currentPage: null,
      userInput: '',
      isInitialized: false
    };
  }

  // Get context summary
  getSummary() {
    return {
      isInitialized: this.context.isInitialized,
      messageCount: this.messageState.getMessageCount(),
      loadingStates: this.loadingState.getAllLoadingStates(),
      hasSelectedText: !!this.context.selectedText,
      currentPage: this.context.currentPage
    };
  }
}

// Singleton instance for global state management
const chatContext = new ChatContext();

export {
  LoadingState,
  MessageState,
  ChatContext
};

export default chatContext;