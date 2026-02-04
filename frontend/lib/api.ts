import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiClient = {
  setAuthToken(token: string) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  },

  clearAuthToken() {
    delete api.defaults.headers.common['Authorization']
  },

  async register(email: string, password: string, name?: string) {
    const response = await api.post('/auth/register', { email, password, name })
    return response.data
  },

  async login(email: string, password: string) {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  async getMe() {
    const response = await api.get('/auth/me')
    return response.data
  },

  async logout() {
    const response = await api.post('/auth/logout')
    return response.data
  },

  async createSession(title?: string) {
    const response = await api.post('/session/new', { title })
    return response.data
  },

  async sendMessage(sessionId: string, message: string) {
    const response = await api.post('/chat', { session_id: sessionId, message })
    return response.data
  },

  async getHistory(sessionId: string) {
    const response = await api.get(`/history/${sessionId}`)
    return response.data
  },

  async getSessions() {
    const response = await api.get('/sessions')
    return response.data
  },
}

export default api
