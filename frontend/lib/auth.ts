import { apiClient } from './api'

export const authService = {
  async register(email: string, password: string, name?: string) {
    try {
      const data = await apiClient.register(email, password, name)
      if (data.success && data.token) {
        localStorage.setItem('token', data.token)
        apiClient.setAuthToken(data.token)
        localStorage.setItem('user', JSON.stringify(data.user))
      }
      return data
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Registration failed'
      }
    }
  },

  async login(email: string, password: string) {
    try {
      const data = await apiClient.login(email, password)
      if (data.success && data.token) {
        localStorage.setItem('token', data.token)
        apiClient.setAuthToken(data.token)
        localStorage.setItem('user', JSON.stringify(data.user))
      }
      return data
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed'
      }
    }
  },

  async logout() {
    try {
      await apiClient.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      apiClient.clearAuthToken()
    }
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token')
  },

  getUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  getToken(): string | null {
    return localStorage.getItem('token')
  },

  initAuth() {
    const token = this.getToken()
    if (token) {
      apiClient.setAuthToken(token)
    }
  },
}
