// OAuthService.js - Handles OAuth flows for Facebook and Google
class OAuthService {
  constructor() {
    // Access environment variables safely for browser environment
    // In Docusaurus, environment variables can be passed via config
    this.facebookClientId = this.getEnvVar('REACT_APP_FACEBOOK_APP_ID');
    this.googleClientId = this.getEnvVar('REACT_APP_GOOGLE_CLIENT_ID');
    this.backendUrl = this.getEnvVar('REACT_APP_API_URL') || 'http://127.0.0.1:8000/api/v1';
  }

  // Helper method to safely get environment variables in browser
  getEnvVar(varName) {
    // Check for variables in window object (set by Docusaurus config)
    if (typeof window !== 'undefined' && window[varName]) {
      return window[varName];
    }
    // For Node.js environment (build time), we'll use a different approach
    // since process is not available in browser runtime
    return null;
  }

  // Facebook OAuth
  async initiateFacebookLogin() {
    try {
      // Get the authorization URL from the backend
      const response = await fetch(`${this.backendUrl}/oauth/facebook/auth-url`);
      const data = await response.json();

      if (data.auth_url) {
        // Store the state parameter for security verification
        localStorage.setItem('oauth_state', data.state);

        // Redirect to Facebook OAuth
        window.location.href = data.auth_url;
      } else {
        throw new Error('Failed to get Facebook auth URL');
      }
    } catch (error) {
      console.error('Facebook OAuth error:', error);
      throw error;
    }
  }

  // Google OAuth
  async initiateGoogleLogin() {
    try {
      // Get the authorization URL from the backend
      const response = await fetch(`${this.backendUrl}/oauth/google/auth-url`);
      const data = await response.json();

      if (data.auth_url) {
        // Store the state parameter for security verification
        localStorage.setItem('oauth_state', data.state);

        // Redirect to Google OAuth
        window.location.href = data.auth_url;
      } else {
        throw new Error('Failed to get Google auth URL');
      }
    } catch (error) {
      console.error('Google OAuth error:', error);
      throw error;
    }
  }

  // Handle OAuth callback from backend
  async handleOAuthCallback(provider, code, state) {
    try {
      // Verify state parameter for security
      const storedState = localStorage.getItem('oauth_state');
      if (!storedState || storedState !== state) {
        throw new Error('Invalid OAuth state parameter');
      }

      // Exchange code for token with backend
      const response = await fetch(`${this.backendUrl}/oauth/${provider}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          provider,
          redirect_uri: window.location.origin
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store token and user info
        localStorage.setItem('textbook_token', data.token);
        localStorage.setItem('textbook_user', JSON.stringify({
          id: data.user_id,
          username: data.username,
          email: data.email,
          is_new_user: data.is_new_user
        }));

        // Clear the stored state
        localStorage.removeItem('oauth_state');

        return {
          success: true,
          user: {
            id: data.user_id,
            username: data.username,
            email: data.email,
            is_new_user: data.is_new_user
          }
        };
      } else {
        throw new Error(data.detail || `OAuth ${provider} login failed`);
      }
    } catch (error) {
      console.error('OAuth callback error:', error);
      // Clear the stored state on error
      localStorage.removeItem('oauth_state');
      throw error;
    }
  }

  // Check if we're handling an OAuth callback
  checkOAuthCallback() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state');

    // Check for specific provider in the URL or infer from path
    let provider = null;
    if (window.location.pathname.includes('/auth/facebook/callback')) {
      provider = 'facebook';
    } else if (window.location.pathname.includes('/auth/google/callback')) {
      provider = 'google';
    }

    if (code && state && provider) {
      // Remove OAuth params from URL to clean up
      const cleanUrl = window.location.pathname;
      window.history.replaceState({}, document.title, cleanUrl);

      return { code, state, provider };
    }

    return null;
  }
}

export default new OAuthService();