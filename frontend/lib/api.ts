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

  async sendVoiceMessage(sessionId: string, audioFile: File) {
    const formData = new FormData()
    formData.append('audio', audioFile)
    formData.append('session_id', sessionId)

    const response = await api.post('/chat/voice', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async uploadFile(sessionId: string, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('session_id', sessionId)

    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async getSessionFiles(sessionId: string) {
    const response = await api.get(`/files/${sessionId}`)
    return response.data
  },

  async deleteFile(fileId: string) {
    const response = await api.delete(`/files/${fileId}`)
    return response.data
  },
}

export default api
