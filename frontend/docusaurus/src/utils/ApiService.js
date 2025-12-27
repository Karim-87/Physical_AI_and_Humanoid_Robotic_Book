import { getApiBaseUrl, API_ENDPOINTS, buildApiUrl } from './apiConfig';
import { ErrorHandler } from './ErrorHandler';
import logger from './Logger';

class ApiService {
  constructor() {
    this.baseUrl = getApiBaseUrl();
    // Default retry configuration
    this.defaultRetryConfig = {
      maxRetries: 3,
      baseDelay: 1000, // 1 second
      maxDelay: 10000, // 10 seconds
      backoffMultiplier: 2,
      retryableStatusCodes: [429, 500, 502, 503, 504]
    };
  }

  // Generic request method with error handling and retry mechanism
  async request(endpoint, options = {}, retryConfig = null) {
    const url = buildApiUrl(endpoint);
    const startTime = Date.now();

    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const config = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    };

    // Log the request
    logger.info(`Making API request`, {
      url,
      method: config.method || 'GET',
      endpoint
    });

    // Use provided retry config or default
    const configToUse = retryConfig || this.defaultRetryConfig;

    try {
      // Attempt request with retry mechanism
      const result = await this._makeRequestWithRetry(url, config, configToUse, startTime);

      // Log successful request
      logger.logApiRequest(url, config.method || 'GET', startTime, { status: 200 });

      return result;
    } catch (error) {
      // Log failed request
      logger.logApiRequest(url, config.method || 'GET', startTime, null, error);
      throw error;
    }
  }

  // Internal method to make request with retry logic
  async _makeRequestWithRetry(url, config, retryConfig, startTime) {
    let lastError;
    let attempt = 0;

    while (attempt < retryConfig.maxRetries) {
      try {
        const response = await fetch(url, config);

        // Handle different response status codes
        if (!response.ok) {
          // Log the error response
          logger.error(`API request failed`, {
            url,
            method: config.method || 'GET',
            status: response.status,
            statusText: response.statusText,
            attempt: attempt + 1,
            maxRetries: retryConfig.maxRetries
          });

          // Check if this status code should trigger a retry
          if (retryConfig.retryableStatusCodes.includes(response.status)) {
            // Log retry attempt
            logger.info(`Retrying API request`, {
              url,
              method: config.method || 'GET',
              status: response.status,
              attempt: attempt + 1,
              maxRetries: retryConfig.maxRetries
            });

            throw new Error(`HTTP error! status: ${response.status}`);
          } else {
            // For non-retryable errors, throw immediately
            throw new Error(`HTTP error! status: ${response.status}`);
          }
        }

        // Attempt to parse JSON response
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          return await response.json();
        } else {
          return await response.text();
        }
      } catch (error) {
        lastError = error;
        attempt++;

        // Don't retry on network errors that indicate client issues
        if (attempt >= retryConfig.maxRetries) {
          logger.error(`API request failed after all retries`, {
            url,
            method: config.method || 'GET',
            error: error.message,
            totalAttempts: attempt,
            totalDuration: Date.now() - startTime
          });
          break;
        }

        // Calculate delay with exponential backoff
        const delay = Math.min(
          retryConfig.baseDelay * Math.pow(retryConfig.backoffMultiplier, attempt - 1),
          retryConfig.maxDelay
        );

        // Log the retry delay
        logger.debug(`Waiting before retry`, {
          url,
          method: config.method || 'GET',
          attempt,
          delay: delay
        });

        // Wait before retrying
        await this._delay(delay);
      }
    }

    // If we've exhausted retries, throw the last error
    logger.error(`API request failed after ${retryConfig.maxRetries} attempts for ${url}`, {
      error: lastError.message,
      duration: Date.now() - startTime
    });

    throw lastError;
  }

  // Helper method to create a delay
  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Chat endpoint - send user message and get AI response
  async chat(message, selectedText = null, sessionId = null) {
    const payload = {
      message: message,
      selected_text: selectedText,
      session_id: sessionId,
    };

    return this.request(API_ENDPOINTS.CHAT, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  // Health check endpoint
  async healthCheck() {
    return this.request(API_ENDPOINTS.HEALTH, {
      method: 'GET',
    });
  }

  // Ingestion endpoint - for future use
  async ingestion(data) {
    return this.request(API_ENDPOINTS.INGESTION, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Method to update base URL (useful for testing or dynamic configuration)
  updateBaseUrl(newBaseUrl) {
    this.baseUrl = newBaseUrl;
  }

  // Method to update retry configuration
  updateRetryConfig(newConfig) {
    this.defaultRetryConfig = { ...this.defaultRetryConfig, ...newConfig };
  }

  // Get current retry configuration
  getRetryConfig() {
    return this.defaultRetryConfig;
  }
}

// Create a singleton instance
const apiService = new ApiService();
export default apiService;

// Also export the class for cases where multiple instances might be needed
export { ApiService };