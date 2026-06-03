import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
})

export const chatAPI = {
  sendMessage: (message: string, context?: any) =>
    api.post('/chat', { message, context }),
}

export const jobAPI = {
  getJobs: (params?: { limit?: number; match?: string; sponsored?: boolean }) =>
    api.get('/jobs', { params }),
  runJobHunt: (payload: any) => api.post('/agents/job-hunt', payload),
}

export const profileAPI = {
  getProfile: () => api.get('/profile'),
  updateProfile: (data: any) => api.put('/profile', data),
}

export default api