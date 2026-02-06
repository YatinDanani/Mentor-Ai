export interface User {
  id: number
  email: string
  name?: string
}

export interface AuthResponse {
  success: boolean
  user?: User
  token?: string
  error?: string
}

export interface Message {
  role: 'user' | 'model'
  content: string
  timestamp: string
  audio_url?: string
}

export interface Session {
  id: string
  title: string
  created_at: string
  last_active: string
}

export interface ChatResponse {
  success: boolean
  response?: string
  error?: string
}
