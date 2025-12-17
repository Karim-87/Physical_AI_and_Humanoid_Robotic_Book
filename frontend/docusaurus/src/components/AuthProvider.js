import React, { createContext, useContext, useState, useEffect } from 'react';
import OAuthService from './OAuthService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for OAuth callback and handle it
  useEffect(() => {
    const handleOAuthCallback = async () => {
      const oauthData = OAuthService.checkOAuthCallback();

      if (oauthData) {
        try {
          const result = await OAuthService.handleOAuthCallback(
            oauthData.provider,
            oauthData.code,
            oauthData.state
          );

          if (result.success) {
            setUser(result.user);
          }
        } catch (error) {
          console.error('OAuth callback error:', error);
          // Could optionally show an error message to the user
        }
        return; // Exit early if we're handling an OAuth callback
      }

      // Check for existing session on component mount
      const token = localStorage.getItem('textbook_token');
      const userData = localStorage.getItem('textbook_user');

      if (token && userData) {
        try {
          const parsedUser = JSON.parse(userData);
          setUser({ ...parsedUser, token });
        } catch (error) {
          console.error('Error parsing user data:', error);
          // Clear invalid data
          localStorage.removeItem('textbook_token');
          localStorage.removeItem('textbook_user');
        }
      }

      setLoading(false);
    };

    handleOAuthCallback();
  }, []);

  const login = async (username, password) => {
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        const { token, user_id, username: returnedUsername } = data;

        // Store token and user info
        localStorage.setItem('textbook_token', token);
        localStorage.setItem('textbook_user', JSON.stringify({
          id: user_id,
          username: returnedUsername
        }));

        setUser({ id: user_id, username: returnedUsername, token });
        return { success: true, user: { id: user_id, username: returnedUsername } };
      } else {
        return { success: false, error: data.detail || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Auto-login after registration
        return await login(username, password);
      } else {
        return { success: false, error: data.detail || 'Registration failed' };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  const logout = () => {
    localStorage.removeItem('textbook_token');
    localStorage.removeItem('textbook_user');
    setUser(null);
  };

  const initiateFacebookLogin = async () => {
    try {
      await OAuthService.initiateFacebookLogin();
      return { success: true };
    } catch (error) {
      console.error('Facebook login error:', error);
      return { success: false, error: error.message || 'Facebook login failed' };
    }
  };

  const initiateGoogleLogin = async () => {
    try {
      await OAuthService.initiateGoogleLogin();
      return { success: true };
    } catch (error) {
      console.error('Google login error:', error);
      return { success: false, error: error.message || 'Google login failed' };
    }
  };

  const value = {
    user,
    login,
    register,
    logout,
    initiateFacebookLogin,
    initiateGoogleLogin,
    isAuthenticated: !!user,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};