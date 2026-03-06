import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', new URLSearchParams(data)),
  getMe: () => api.get('/auth/me'),
};

// Projects API
export const projectsAPI = {
  getAll: () => api.get('/projects'),
  getById: (id) => api.get(`/projects/${id}`),
  create: (data) => api.post('/projects', data),
  update: (id, data) => api.put(`/projects/${id}`, data),
  delete: (id) => api.delete(`/projects/${id}`),
};

// Activities API
export const activitiesAPI = {
  getAll: (params) => api.get('/activity', { params }),
  create: (data) => api.post('/activity/manual', data),
  upload: (projectId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/activity/upload?project_id=${projectId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/analytics/dashboard'),
  getProductivity: () => api.get('/analytics/productivity'),
  getChurn: () => api.get('/analytics/churn'),
  getCommits: () => api.get('/analytics/commits'),
};

// AI API
export const aiAPI = {
  predictRisk: (moduleName) => api.post(`/ai/predict-risk?module_name=${moduleName}`),
  getRiskAnalysis: () => api.get('/ai/risk-analysis'),
  getInsights: () => api.get('/ai/insights'),
};

export default api;
