// Error handling utilities for API failures and network issues
class ApiError extends Error {
  constructor(message, status, response = null, headers = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.response = response;
    this.headers = headers; // Include headers for rate limiting info
  }
}

class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NetworkError';
  }
}

class ValidationError extends Error {
  constructor(message, field = null) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

class RateLimitError extends Error {
  constructor(message, retryAfter = null, limit = null) {
    super(message);
    this.name = 'RateLimitError';
    this.retryAfter = retryAfter;
    this.limit = limit;
  }
}

class ContentNotFoundError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ContentNotFoundError';
  }
}

class ErrorHandler {
  // Handle API errors with appropriate user feedback
  static handleApiError(error, context = '') {
    console.error(`API Error in ${context}:`, error);

    // Determine error type and return appropriate user message
    if (error instanceof NetworkError) {
      return {
        type: 'network',
        message: 'Network error: Unable to connect to the server. Please check your internet connection and try again.',
        severity: 'high'
      };
    } else if (error instanceof RateLimitError) {
      // Handle rate limit errors specifically
      const retryAfter = error.retryAfter ? Math.ceil(error.retryAfter / 1000) : 60;
      return {
        type: 'rate_limit',
        message: `Rate limit exceeded. Please wait ${retryAfter} seconds before trying again.`,
        severity: 'medium',
        retryAfter: error.retryAfter
      };
    } else if (error instanceof ApiError) {
      switch (error.status) {
        case 400:
          return {
            type: 'validation',
            message: 'Invalid request: Please check your input and try again.',
            severity: 'medium'
          };
        case 401:
          return {
            type: 'auth',
            message: 'Authentication required: Please log in to continue.',
            severity: 'high'
          };
        case 403:
          return {
            type: 'forbidden',
            message: 'Access denied: You do not have permission to perform this action.',
            severity: 'high'
          };
        case 404:
          return {
            type: 'not_found',
            message: 'Service unavailable: The requested resource was not found.',
            severity: 'high'
          };
        case 429:
          // Extract rate limit information from headers if available
          const retryAfter = error.headers?.get('Retry-After') ||
                            error.headers?.get('X-RateLimit-Reset') ||
                            60;
          return {
            type: 'rate_limit',
            message: `Too many requests: Please wait before trying again.`,
            severity: 'medium',
            retryAfter: parseInt(retryAfter) * 1000 // Convert to milliseconds
          };
        case 500:
        case 502:
        case 503:
          return {
            type: 'server',
            message: 'Service temporarily unavailable: Our servers are experiencing issues. Please try again later.',
            severity: 'high'
          };
        default:
          return {
            type: 'unknown',
            message: `Server error: ${error.message || 'An unknown error occurred'}`,
            severity: 'high'
          };
      }
    } else {
      // Generic error
      return {
        type: 'unknown',
        message: error.message || 'An unexpected error occurred. Please try again.',
        severity: 'high'
      };
    }
  }

  // Check if an error is a rate limit error
  static isRateLimitError(error) {
    return error instanceof RateLimitError ||
           (error instanceof ApiError && error.status === 429);
  }

  // Check if an error is a network error
  static isNetworkError(error) {
    // Check for common network error indicators
    return error instanceof NetworkError ||
           error.name === 'TypeError' ||
           error.message.includes('Failed to fetch') ||
           error.message.includes('NetworkError') ||
           error.message.includes('network') ||
           error.message.includes('fetch') ||
           error.message.includes('CORS') ||
           error.message.includes('origin') ||
           error.message.includes('cross-origin');
  }

  // Handle network errors specifically
  static handleNetworkError(error, context = '') {
    console.error(`Network Error in ${context}:`, error);

    return {
      type: 'network',
      message: 'Network error: Unable to connect to the server. Please check your internet connection and try again.',
      severity: 'high'
    };
  }

  // Validate response format
  static validateResponse(response, expectedFormat = null) {
    if (!response) {
      throw new ValidationError('Response is null or undefined');
    }

    // If expected format is provided, validate against it
    if (expectedFormat) {
      // Basic validation for common expected formats
      if (expectedFormat === 'json') {
        if (typeof response !== 'object') {
          throw new ValidationError('Expected JSON response but got different format');
        }
      }
    }

    return true;
  }

  // Retry mechanism for failed requests, with special handling for rate limits
  static async retryRequest(requestFn, maxRetries = 3, delay = 1000) {
    let lastError;

    for (let i = 0; i < maxRetries; i++) {
      try {
        return await requestFn();
      } catch (error) {
        lastError = error;

        // Don't retry on validation errors or certain other errors
        if (error instanceof ValidationError ||
            (error instanceof ApiError && error.status >= 400 && error.status < 500 && error.status !== 429)) {
          throw error;
        }

        // Handle rate limit errors with appropriate delay
        if (this.isRateLimitError(error)) {
          const retryAfter = error.retryAfter || delay * Math.pow(2, i);
          console.log(`Rate limited, waiting ${retryAfter}ms before retry ${i + 1}/${maxRetries}`);
          await this.delay(retryAfter);
          continue;
        }

        // If this is the last attempt, throw the error
        if (i === maxRetries - 1) {
          break;
        }

        // Wait before retrying for other errors (exponential backoff)
        await this.delay(delay * Math.pow(2, i));
      }
    }

    throw lastError;
  }

  // Helper function to create a delay
  static delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Format error for display to user
  static formatUserError(errorInfo) {
    return {
      message: errorInfo.message,
      type: errorInfo.type,
      severity: errorInfo.severity,
      retryAfter: errorInfo.retryAfter,
      timestamp: new Date().toISOString()
    };
  }

  // Check if an error is a content not found error
  static isContentNotFoundError(error) {
    return error instanceof ContentNotFoundError ||
           (error instanceof ApiError && error.message?.includes('content not found'));
  }

  // Handle graceful degradation when backend is unavailable
  static handleBackendUnavailable(context = '') {
    console.warn(`Backend unavailable in ${context}, providing graceful degradation`);

    return {
      type: 'graceful_degradation',
      message: 'The AI service is temporarily unavailable. Please try again later.',
      severity: 'high'
    };
  }

  // Handle extremely long user queries or selected text
  static handleLongContent(content, maxLength = 10000, context = '') {
    if (content && content.length > maxLength) {
      console.warn(`${context} content exceeds maximum length of ${maxLength} characters`);

      return {
        type: 'content_too_long',
        message: `The input is too long. Please reduce the length to ${maxLength} characters or fewer.`,
        severity: 'medium'
      };
    }

    return {
      type: 'valid',
      isValid: true,
      message: 'Content length is within acceptable limits',
      severity: 'low'
    };
  }
}

export {
  ApiError,
  NetworkError,
  ValidationError,
  RateLimitError,
  ContentNotFoundError,
  ErrorHandler
};

export default ErrorHandler;