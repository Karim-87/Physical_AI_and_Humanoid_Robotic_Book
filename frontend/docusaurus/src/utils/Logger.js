// Comprehensive logging utility for debugging connectivity issues
class Logger {
  constructor() {
    this.level = this.getLogLevel();
    this.isEnabled = true;
  }

  // Get log level from environment or default to 'info'
  getLogLevel() {
    const envLevel = process.env.REACT_APP_LOG_LEVEL || 'info';
    const levels = {
      'debug': 0,
      'info': 1,
      'warn': 2,
      'error': 3
    };
    return levels[envLevel] !== undefined ? envLevel : 'info';
  }

  // Check if a log level should be printed
  shouldLog(level) {
    const levels = {
      'debug': 0,
      'info': 1,
      'warn': 2,
      'error': 3
    };
    return levels[level] >= levels[this.level];
  }

  // Format log message with timestamp and metadata
  formatMessage(level, message, metadata = {}) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      message,
      ...metadata
    };

    // Include additional context if available
    if (typeof window !== 'undefined') {
      logEntry.url = window.location.href;
      logEntry.userAgent = navigator.userAgent;
    }

    return logEntry;
  }

  // Log debug messages
  debug(message, metadata = {}) {
    if (this.shouldLog('debug') && this.isEnabled) {
      const logEntry = this.formatMessage('debug', message, metadata);
      console.debug('[DEBUG]', logEntry);
    }
  }

  // Log info messages
  info(message, metadata = {}) {
    if (this.shouldLog('info') && this.isEnabled) {
      const logEntry = this.formatMessage('info', message, metadata);
      console.info('[INFO]', logEntry);
    }
  }

  // Log warning messages
  warn(message, metadata = {}) {
    if (this.shouldLog('warn') && this.isEnabled) {
      const logEntry = this.formatMessage('warn', message, metadata);
      console.warn('[WARN]', logEntry);
    }
  }

  // Log error messages
  error(message, metadata = {}) {
    if (this.shouldLog('error') && this.isEnabled) {
      const logEntry = this.formatMessage('error', message, metadata);
      console.error('[ERROR]', logEntry);
    }
  }

  // Log API request details
  logApiRequest(url, method, startTime, response, error = null) {
    const duration = Date.now() - startTime;
    const logData = {
      url,
      method,
      duration,
      status: error ? 'error' : response?.status || 'unknown',
      responseTime: duration,
      ...error ? { error: error.message } : { responseSize: JSON.stringify(response).length }
    };

    if (error) {
      this.error(`API request failed: ${method} ${url}`, logData);
    } else {
      this.info(`API request completed: ${method} ${url}`, logData);
    }
  }

  // Log connectivity issues specifically
  logConnectivityIssue(url, error, context = {}) {
    const logData = {
      url,
      error: error.message,
      type: error.name,
      context,
      timestamp: new Date().toISOString()
    };

    this.error(`Connectivity issue detected: ${url}`, logData);
  }

  // Log rate limiting events
  logRateLimit(url, retryAfter, context = {}) {
    const logData = {
      url,
      retryAfter,
      context,
      timestamp: new Date().toISOString()
    };

    this.warn(`Rate limit hit: ${url}`, logData);
  }

  // Log session events
  logSessionEvent(eventType, sessionId, details = {}) {
    const logData = {
      eventType,
      sessionId,
      details,
      timestamp: new Date().toISOString()
    };

    this.info(`Session event: ${eventType}`, logData);
  }

  // Log text selection events
  logTextSelection(selectionLength, context = {}) {
    const logData = {
      selectionLength,
      context,
      timestamp: new Date().toISOString()
    };

    this.info(`Text selection event`, logData);
  }

  // Set logging level
  setLevel(level) {
    this.level = level;
  }

  // Enable/disable logging
  setEnabled(enabled) {
    this.isEnabled = enabled;
  }
}

// Create singleton instance
const logger = new Logger();

export default logger;

// Export the class for cases where multiple instances might be needed
export { Logger };