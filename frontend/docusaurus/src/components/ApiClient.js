class ApiClient {
  constructor(baseURL = 'http://127.0.0.1:8000/api/v1') {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('textbook_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(url, config);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  // Textbook content endpoints
  async getChapters(language = 'en') {
    return this.request(`/textbook/chapters?language=${language}`);
  }

  async getChapter(chapterId) {
    return this.request(`/textbook/chapters/${chapterId}`);
  }

  // RAG endpoints
  async queryRag(query, language = 'en', context = null) {
    const result = await this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message: query, selected_text: context }),
    });
    // Map backend response to frontend expected format
    return {
      answer: result.response,
      sources: [],
      session_id: result.session_id,
      mode: result.mode,
    };
  }

  async queryBySelection(selectedText, question = null) {
    const result = await this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message: question || 'Explain this text', selected_text: selectedText }),
    });
    return {
      answer: result.response,
      sources: [],
      session_id: result.session_id,
      mode: result.mode,
    };
  }

  // Authentication endpoints
  async register(username, email, password) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  }

  async login(username, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async logout() {
    // In a real implementation, you might want to call an API endpoint
    // For now, we just clear local storage
    localStorage.removeItem('textbook_token');
    localStorage.removeItem('textbook_user');
  }

  async getPreferences() {
    return this.request('/auth/preferences');
  }

  async updatePreferences(preferences) {
    return this.request('/auth/preferences', {
      method: 'PUT',
      body: JSON.stringify(preferences),
    });
  }

  // OAuth endpoints
  async getOAuthUrl(provider) {
    return this.request(`/oauth/${provider}/auth-url`);
  }

  async handleOAuthLogin(provider, code, redirectUri) {
    return this.request(`/oauth/${provider}`, {
      method: 'POST',
      body: JSON.stringify({ code, provider, redirect_uri: redirectUri }),
    });
  }
}

export default new ApiClient();