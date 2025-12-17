import React, { useState, useEffect } from 'react';
import './UserProfile.css';

const UserProfile = ({ user, onLogout }) => {
  const [preferences, setPreferences] = useState({
    language: 'en',
    personalization_enabled: true
  });
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  // Load user preferences on component mount
  useEffect(() => {
    const loadPreferences = async () => {
      try {
        const response = await fetch('/api/v1/auth/preferences', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('textbook_token')}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          setPreferences({
            language: data.language || 'en',
            personalization_enabled: data.personalization_enabled ?? true
          });
        }
      } catch (error) {
        console.error('Error loading preferences:', error);
      }
    };

    if (user) {
      loadPreferences();
    }
  }, [user]);

  const handleSavePreferences = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/auth/preferences', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('textbook_token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          language: preferences.language,
          personalization_enabled: preferences.personalization_enabled
        }),
      });

      if (response.ok) {
        setIsEditing(false);
        alert('Preferences saved successfully!');
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Failed to save preferences');
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
      alert('Network error');
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageChange = (e) => {
    setPreferences({
      ...preferences,
      language: e.target.value
    });
  };

  const handlePersonalizationToggle = () => {
    setPreferences({
      ...preferences,
      personalization_enabled: !preferences.personalization_enabled
    });
  };

  if (!user) return null;

  return (
    <div className="user-profile">
      <div className="user-info">
        <h3>Welcome, {user.username}!</h3>
        {user.email && <p className="user-email">{user.email}</p>}
      </div>

      <div className="user-preferences">
        <h4>Preferences</h4>

        {isEditing ? (
          <div className="preferences-form">
            <div className="form-group">
              <label htmlFor="language-select">Language:</label>
              <select
                id="language-select"
                value={preferences.language}
                onChange={handleLanguageChange}
              >
                <option value="en">English</option>
                <option value="ur">Urdu</option>
              </select>
            </div>

            <div className="form-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  checked={preferences.personalization_enabled}
                  onChange={handlePersonalizationToggle}
                />
                Enable Personalization
              </label>
            </div>

            <div className="preferences-actions">
              <button
                onClick={handleSavePreferences}
                disabled={loading}
                className="save-button"
              >
                {loading ? 'Saving...' : 'Save'}
              </button>
              <button
                onClick={() => setIsEditing(false)}
                className="cancel-button"
                disabled={loading}
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div className="preferences-display">
            <div className="preference-item">
              <span className="preference-label">Language:</span>
              <span className="preference-value">
                {preferences.language === 'en' ? 'English' : 'Urdu'}
              </span>
            </div>
            <div className="preference-item">
              <span className="preference-label">Personalization:</span>
              <span className="preference-value">
                {preferences.personalization_enabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>
            <button
              onClick={() => setIsEditing(true)}
              className="edit-button"
            >
              Edit Preferences
            </button>
          </div>
        )}
      </div>

      <div className="user-actions">
        <button onClick={onLogout} className="logout-button">
          Logout
        </button>
      </div>
    </div>
  );
};

export default UserProfile;