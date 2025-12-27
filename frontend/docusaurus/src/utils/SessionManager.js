// Session management utility using localStorage
const SESSION_STORAGE_KEY = 'chatbot-session';

class SessionManager {
  constructor() {
    this.sessionId = this.getSessionId();
  }

  // Get session ID from localStorage or generate a new one
  getSessionId() {
    if (typeof window !== 'undefined') {
      let sessionId = localStorage.getItem(SESSION_STORAGE_KEY);

      if (!sessionId) {
        sessionId = this.generateSessionId();
        localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
      }

      return sessionId;
    }

    // Return a temporary ID if running server-side (SSR)
    return null;
  }

  // Generate a new session ID
  generateSessionId() {
    // Create a unique session ID using timestamp and random component
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substr(2, 5);
    return `session_${timestamp}_${random}`;
  }

  // Update the session ID
  updateSessionId(newSessionId) {
    if (typeof window !== 'undefined' && newSessionId) {
      this.sessionId = newSessionId;
      localStorage.setItem(SESSION_STORAGE_KEY, newSessionId);
    }
  }

  // Clear the current session
  clearSession() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(SESSION_STORAGE_KEY);
      this.sessionId = this.generateSessionId(); // Generate a new session
      localStorage.setItem(SESSION_STORAGE_KEY, this.sessionId);
    }
  }

  // Get session data (for future use if we need to store more than just the ID)
  getSessionData() {
    if (typeof window !== 'undefined') {
      const sessionData = localStorage.getItem(`${SESSION_STORAGE_KEY}_data`);
      return sessionData ? JSON.parse(sessionData) : {};
    }
    return {};
  }

  // Set session data (for future use if we need to store more than just the ID)
  setSessionData(data) {
    if (typeof window !== 'undefined') {
      const currentData = this.getSessionData();
      const updatedData = { ...currentData, ...data };
      localStorage.setItem(`${SESSION_STORAGE_KEY}_data`, JSON.stringify(updatedData));
    }
  }

  // Get the current session ID
  getCurrentSessionId() {
    if (!this.sessionId) {
      this.sessionId = this.getSessionId();
    }
    return this.sessionId;
  }
}

// Create a singleton instance
const sessionManager = new SessionManager();
export default sessionManager;

// Also export the class for cases where multiple instances might be needed
export { SessionManager };