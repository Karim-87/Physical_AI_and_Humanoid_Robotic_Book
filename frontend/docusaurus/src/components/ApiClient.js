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
    return this.request('/rag/query', {
      method: 'POST',
      body: JSON.stringify({ query, language, context }),
    });
  }

  async queryBySelection(selectedText, question = null) {
    return this.request('/rag/query-by-selection', {
      method: 'POST',
      body: JSON.stringify({ selected_text: selectedText, question }),
    });
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
}

export default new ApiClient();