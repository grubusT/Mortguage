const API_BASE_URL = 'https://mortguage.onrender.com';

export const API_ENDPOINTS = {
  // Auth endpoints
  AUTH: {
    LOGIN: `${API_BASE_URL}/auth/login/`,
    REGISTER: `${API_BASE_URL}/auth/register/`,
    LOGOUT: `${API_BASE_URL}/auth/logout/`,
    ME: `${API_BASE_URL}/auth/me/`,
  },
  
  // Client endpoints
  CLIENTS: {
    LIST: `${API_BASE_URL}/clients/`,
    CREATE: `${API_BASE_URL}/clients/`,
    DETAIL: (id: string) => `${API_BASE_URL}/clients/${id}/`,
    UPDATE: (id: string) => `${API_BASE_URL}/clients/${id}/`,
    DELETE: (id: string) => `${API_BASE_URL}/clients/${id}/`,
    SEARCH: `${API_BASE_URL}/clients/search/`,
  },
  
  // Document endpoints
  DOCUMENTS: {
    LIST: `${API_BASE_URL}/documents/`,
    CREATE: (clientId: string) => `${API_BASE_URL}/clients/${clientId}/documents/`,
    LIST_CLIENT: (clientId: string) => `${API_BASE_URL}/clients/${clientId}/documents/`,
    UPDATE: (id: string) => `${API_BASE_URL}/documents/${id}/`,
    DELETE: (id: string) => `${API_BASE_URL}/documents/${id}/`,
  },
  
  // Application endpoints
  APPLICATIONS: {
    LIST: `${API_BASE_URL}/applications/`,
    CREATE: `${API_BASE_URL}/applications/`,
    LIST_CLIENT: (clientId: string) => `${API_BASE_URL}/clients/${clientId}/applications/`,
    UPDATE: (id: string) => `${API_BASE_URL}/applications/${id}/`,
    UPDATE_STATUS: (id: string) => `${API_BASE_URL}/applications/${id}/status/`,
  },
  
  // Dashboard endpoints
  DASHBOARD: {
    SUMMARY: `${API_BASE_URL}/dashboard/summary/`,
    ACTIVITY: `${API_BASE_URL}/dashboard/activity/`,
    REMINDERS: `${API_BASE_URL}/dashboard/reminders/`,
    TASKS: `${API_BASE_URL}/dashboard/tasks/`,
  },
};

export const createApiRequest = async (endpoint: string, options: RequestInit = {}) => {
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  };

  const response = await fetch(endpoint, {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
};
