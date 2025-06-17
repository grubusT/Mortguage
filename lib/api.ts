const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

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
    LIST: `${API_BASE_URL}/api/clients/`,
    CREATE: `${API_BASE_URL}/api/clients/`,
    DETAIL: (id: string) => `${API_BASE_URL}/api/clients/${id}/`,
    UPDATE: (id: string) => `${API_BASE_URL}/api/clients/${id}/`,
    DELETE: (id: string) => `${API_BASE_URL}/api/clients/${id}/`,
    SEARCH: `${API_BASE_URL}/api/clients/search/`,
  },

  // Document endpoints
  DOCUMENTS: {
    LIST: `${API_BASE_URL}/api/documents/`,
    CREATE: (clientId: string) => `${API_BASE_URL}/api/clients/${clientId}/documents/`,
    LIST_CLIENT: (clientId: string) => `${API_BASE_URL}/api/clients/${clientId}/documents/`,
    UPDATE: (id: string) => `${API_BASE_URL}/api/documents/${id}/`,
    DELETE: (id: string) => `${API_BASE_URL}/api/documents/${id}/`,
  },

  // Application endpoints
  APPLICATIONS: {
    LIST: `${API_BASE_URL}/api/applications/`,
    CREATE: `${API_BASE_URL}/api/applications/`,
    LIST_CLIENT: (clientId: string) => `${API_BASE_URL}/api/clients/${clientId}/applications/`,
    UPDATE: (id: string) => `${API_BASE_URL}/api/applications/${id}/`,
    UPDATE_STATUS: (id: string) => `${API_BASE_URL}/api/applications/${id}/status/`,
  },

  // Dashboard endpoints
  DASHBOARD: {
    SUMMARY: `${API_BASE_URL}/api/dashboard/summary/`,
    ACTIVITY: `${API_BASE_URL}/api/dashboard/activity/`,
    REMINDERS: `${API_BASE_URL}/api/dashboard/reminders/`,
    TASKS: `${API_BASE_URL}/api/dashboard/tasks/`,
  },

  // Interview Scripts endpoints
  INTERVIEW_SCRIPTS: {
    LIST: `${API_BASE_URL}/api/interview-scripts/`,
    CREATE: `${API_BASE_URL}/api/interview-scripts/`,
    DETAIL: (id: string) => `${API_BASE_URL}/api/interview-scripts/${id}/`,
    UPDATE: (id: string) => `${API_BASE_URL}/api/interview-scripts/${id}/`,
    DELETE: (id: string) => `${API_BASE_URL}/api/interview-scripts/${id}/`,
  },

  // Health check
  HEALTH: `${API_BASE_URL}/api/health/`,
}

export const createApiRequest = async (endpoint: string, options: RequestInit = {}) => {
  const token = localStorage.getItem("authToken")

  const defaultOptions: RequestInit = {
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    credentials: "include",
  }

  const response = await fetch(endpoint, {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  })

  if (!response.ok) {
    if (response.status === 401) {
      // Handle unauthorized - redirect to login
      localStorage.removeItem("authToken")
      window.location.href = "/login"
      return
    }
    throw new Error(`API request failed: ${response.statusText}`)
  }

  return response.json()
}

// API helper functions
export const apiClient = {
  get: (endpoint: string) => createApiRequest(endpoint, { method: "GET" }),
  post: (endpoint: string, data: any) =>
    createApiRequest(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    }),
  put: (endpoint: string, data: any) =>
    createApiRequest(endpoint, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  patch: (endpoint: string, data: any) =>
    createApiRequest(endpoint, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  delete: (endpoint: string) => createApiRequest(endpoint, { method: "DELETE" }),
}
