import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const portfolioApi = {
  getProjects: () => api.get('/projects').then(res => res.data.projects),
  getSkills: () => api.get('/skills').then(res => res.data.skills),
  getAbout: () => api.get('/about').then(res => res.data.about),
  sendMessage: (message: any) => api.post('/contact', message).then(res => res.data),
};

export const adminApi = {
  login: (credentials: any) => api.post('/auth/login', credentials).then(res => res.data),
  getMessages: () => api.get('/admin/messages').then(res => res.data.messages),
  getProjects: () => api.get('/admin/projects').then(res => res.data.projects),
  createProject: (project: any) => api.post('/admin/projects', project).then(res => res.data),
  updateProject: (id: string, project: any) => api.patch(`/admin/projects/${id}`, project).then(res => res.data),
  deleteProject: (id: string) => api.delete(`/admin/projects/${id}`).then(res => res.data),
  getSkills: () => api.get('/admin/skills').then(res => res.data.skills),
  createSkill: (skill: any) => api.post('/admin/skills', skill).then(res => res.data),
  updateSkill: (id: string, skill: any) => api.patch(`/admin/skills/${id}`, skill).then(res => res.data),
  deleteSkill: (id: string) => api.delete(`/admin/skills/${id}`).then(res => res.data),
  getAbout: () => api.get('/admin/about').then(res => res.data.about),
  updateAbout: (about: any) => api.put('/admin/about', about).then(res => res.data),
};

export default api;
