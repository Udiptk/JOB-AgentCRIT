import axios from 'axios';

const api = axios.create({
  // Empty baseURL → requests go through the Vite proxy (vite.config.ts)
  // which forwards them to http://localhost:8000 — no CORS in dev.
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    // Global error handling could dispatch a toast notification here
    return Promise.reject(error);
  }
);

export default api;
