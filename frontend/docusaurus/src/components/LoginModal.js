import React, { useState } from 'react';
import './LoginModal.css';
import OAuthService from './OAuthService';

const LoginModal = ({ isOpen, onClose, onLoginSuccess }) => {
  const [activeTab, setActiveTab] = useState('login'); // 'login' or 'register'
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleTraditionalLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

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
        // Store token and user info
        localStorage.setItem('textbook_token', data.token);
        localStorage.setItem('textbook_user', JSON.stringify({
          id: data.user_id,
          username: data.username
        }));

        onLoginSuccess({ id: data.user_id, username: data.username });
        onClose();
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

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
        await handleTraditionalLogin({ preventDefault: () => {} });
      } else {
        setError(data.detail || 'Registration failed');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  const handleFacebookLogin = async (e) => {
    e.preventDefault();
    try {
      await OAuthService.initiateFacebookLogin();
    } catch (err) {
      setError('Facebook login failed');
    }
  };

  const handleGoogleLogin = async (e) => {
    e.preventDefault();
    try {
      await OAuthService.initiateGoogleLogin();
    } catch (err) {
      setError('Google login failed');
    }
  };

  return (
    <div className="login-modal-overlay" onClick={onClose}>
      <div className="login-modal" onClick={(e) => e.stopPropagation()}>
        <div className="login-modal-header">
          <h2>{activeTab === 'login' ? 'Login' : 'Register'}</h2>
          <button className="login-modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="login-modal-content">
          <div className="login-modal-tabs">
            <button
              className={activeTab === 'login' ? 'active' : ''}
              onClick={() => setActiveTab('login')}
            >
              Login
            </button>
            <button
              className={activeTab === 'register' ? 'active' : ''}
              onClick={() => setActiveTab('register')}
            >
              Register
            </button>
          </div>

          {error && <div className="login-error">{error}</div>}

          {activeTab === 'login' ? (
            <form onSubmit={handleTraditionalLogin} className="login-form">
              <div className="form-group">
                <label htmlFor="login-username">Username or Email</label>
                <input
                  id="login-username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="login-password">Password</label>
                <input
                  id="login-password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <button type="submit" disabled={loading} className="login-button">
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleRegister} className="login-form">
              <div className="form-group">
                <label htmlFor="register-username">Username</label>
                <input
                  id="register-username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="register-email">Email</label>
                <input
                  id="register-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="register-password">Password</label>
                <input
                  id="register-password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="register-confirm-password">Confirm Password</label>
                <input
                  id="register-confirm-password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
              <button type="submit" disabled={loading} className="login-button">
                {loading ? 'Registering...' : 'Register'}
              </button>
            </form>
          )}

          <div className="login-separator">
            <span>or</span>
          </div>

          <div className="oauth-buttons">
            <button
              onClick={handleFacebookLogin}
              className="oauth-button facebook"
              disabled={loading}
            >
              <span className="oauth-icon">f</span>
              Continue with Facebook
            </button>
            <button
              onClick={handleGoogleLogin}
              className="oauth-button google"
              disabled={loading}
            >
              <span className="oauth-icon">G</span>
              Continue with Google
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginModal;