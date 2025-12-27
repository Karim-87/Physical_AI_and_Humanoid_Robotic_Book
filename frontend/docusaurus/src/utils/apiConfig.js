// Environment configuration for switching between local and deployed backend
const DEFAULT_ENVIRONMENTS = {
  development: {
    apiBaseUrl: 'http://localhost:8000',
    name: 'development',
    isLocal: true
  },
  production: {
    apiBaseUrl: process.env.REACT_APP_API_BASE_URL || 'https://your-deployed-backend-url.vercel.app',
    name: 'production',
    isLocal: false
  },
  test: {
    apiBaseUrl: 'http://localhost:8000',
    name: 'test',
    isLocal: true
  }
};

// Environment manager class for flexible configuration
class EnvironmentManager {
  constructor() {
    this.environments = { ...DEFAULT_ENVIRONMENTS };
    this.currentEnv = this.detectEnvironment();
  }

  // Detect the current environment based on various factors
  detectEnvironment() {
    if (typeof window !== 'undefined') {
      // Client-side environment detection
      const hostname = window.location.hostname;

      if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'development';
      } else if (hostname.includes('vercel.app') ||
                 hostname.includes('netlify.app') ||
                 hostname.includes('github.io')) {
        return 'production';
      } else if (process.env.NODE_ENV === 'test') {
        return 'test';
      }
      return 'production';
    }

    // Server-side (SSR) - fallback to environment variable or production
    return process.env.NODE_ENV || 'production';
  }

  // Get current environment configuration
  getCurrentEnvironment() {
    return this.environments[this.currentEnv] || this.environments.production;
  }

  // Get current API base URL
  getCurrentApiBaseUrl() {
    return this.getCurrentEnvironment().apiBaseUrl;
  }

  // Get current environment name
  getCurrentEnvironmentName() {
    return this.getCurrentEnvironment().name;
  }

  // Check if current environment is local
  isLocalEnvironment() {
    return this.getCurrentEnvironment().isLocal;
  }

  // Switch to a different environment
  switchEnvironment(envName) {
    if (this.environments[envName]) {
      this.currentEnv = envName;
      return true;
    }
    return false;
  }

  // Add or update an environment configuration
  setEnvironment(envName, config) {
    this.environments[envName] = {
      name: envName,
      apiBaseUrl: config.apiBaseUrl,
      isLocal: config.isLocal !== undefined ? config.isLocal : false,
      ...config
    };
  }

  // Get all available environments
  getAvailableEnvironments() {
    return Object.keys(this.environments);
  }

  // Check if running in a specific environment
  isEnvironment(envName) {
    return this.currentEnv === envName;
  }

  // Get environment-specific configuration
  getEnvironmentConfig(envName) {
    return this.environments[envName];
  }
}

// Create a singleton instance
const envManager = new EnvironmentManager();

// API endpoints configuration
const API_ENDPOINTS = {
  CHAT: '/api/v1/chat',
  HEALTH: '/health',
  INGESTION: '/api/v1/ingestion'
};

// Full API URL builder using environment manager
const buildApiUrl = (endpoint) => {
  return `${envManager.getCurrentApiBaseUrl()}${endpoint}`;
};

// Export functions and the environment manager
export {
  envManager,
  API_ENDPOINTS,
  buildApiUrl,
  EnvironmentManager
};

// Backward compatibility exports
export const getApiBaseUrl = () => envManager.getCurrentApiBaseUrl();
export const getEnvironment = () => envManager.getCurrentEnvironmentName();

export default envManager;