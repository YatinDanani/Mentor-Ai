'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/lib/api'
import { authService } from '@/lib/auth'
import { Message, Session } from '@/types'
import MessageBubble from '@/components/MessageBubble'
import SessionList from '@/components/SessionList'
import NewSessionModal from '@/components/NewSessionModal'
import VoiceRecorder from '@/components/VoiceRecorder'
import FileUpload from '@/components/FileUpload'

export default function ChatInterface() {
  const router = useRouter()
  const [sessions, setSessions] = useState<Session[]>([])
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [showFileUpload, setShowFileUpload] = useState(false)
  const [lastAudioUrl, setLastAudioUrl] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
      return
    }

    loadSessions()
  }, [router])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadSessions = async () => {
    try {
      const result = await apiClient.getSessions()
      if (result.success) {
        setSessions(result.sessions || [])
        if (result.sessions && result.sessions.length > 0 && !activeSessionId) {
          setActiveSessionId(result.sessions[0].id)
          loadHistory(result.sessions[0].id)
        }
      }
    } catch (error) {
      console.error('Failed to load sessions:', error)
    }
  }

  const loadHistory = async (sessionId: string) => {
    try {
      const result = await apiClient.getHistory(sessionId)
      if (result.success) {
        setMessages(result.history || [])
      }
    } catch (error) {
      console.error('Failed to load history:', error)
    }
  }

  const handleSessionSelect = async (sessionId: string) => {
    setActiveSessionId(sessionId)
    await loadHistory(sessionId)
  }

  const handleCreateSession = async (title: string) => {
    try {
      const result = await apiClient.createSession(title)
      if (result.success && result.session_id) {
        await loadSessions()
        setActiveSessionId(result.session_id)
        setMessages([])
      }
    } catch (error) {
      console.error('Failed to create session:', error)
    }
  }

  const handleNewSession = () => {
    setIsModalOpen(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !activeSessionId || loading) return
    
    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString(),
    }
    
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)
    
    try {
      const result = await apiClient.sendMessage(activeSessionId, input.trim())
      if (result.success && result.response) {
        const aiMessage: Message = {
          role: 'model',
          content: result.response,
          timestamp: new Date().toISOString(),
          audio_url: result.audio_url || undefined,
        }
        setMessages((prev) => [...prev, aiMessage])
        setLastAudioUrl(result.audio_url || null)
        await loadSessions()
      }
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleVoiceTranscription = async (transcription: string) => {
    if (!transcription.trim() || !activeSessionId || loading) return
    
    const userMessage: Message = {
      role: 'user',
      content: transcription,
      timestamp: new Date().toISOString(),
    }
    
    setMessages((prev) => [...prev, userMessage])
    setLoading(true)
    
    try {
      const result = await apiClient.sendMessage(activeSessionId, transcription)
      if (result.success && result.response) {
        const aiMessage: Message = {
          role: 'model',
          content: result.response,
          timestamp: new Date().toISOString(),
          audio_url: result.audio_url || undefined,
        }
        setMessages((prev) => [...prev, aiMessage])
        setLastAudioUrl(result.audio_url || null)
        await loadSessions()
      }
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFileAnalyzed = async (result: any) => {
    if (!result || !activeSessionId || loading) return
    
    const fileContext = `\n\n[File analyzed: ${result.file_type}]\n${result.analysis.description}`
    
    const userMessage: Message = {
      role: 'user',
      content: `[Uploaded ${result.file_type}]`,
      timestamp: new Date().toISOString(),
    }
    
    setMessages((prev) => [...prev, userMessage])
    setLoading(true)
    
    try {
      const finalMessage = `Analyze this ${result.file_type}: ${result.file_type === 'image' ? 'image' : 'document'} and incorporate the analysis: ${result.analysis.description}`
      const apiResult = await apiClient.sendMessage(activeSessionId, finalMessage)
      
      if (apiResult.success && apiResult.response) {
        const aiMessage: Message = {
          role: 'model',
          content: apiResult.response,
          timestamp: new Date().toISOString(),
          audio_url: apiResult.audio_url || undefined,
        }
        setMessages((prev) => [...prev, aiMessage])
        setLastAudioUrl(apiResult.audio_url || null)
        await loadSessions()
      }
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setLoading(false)
      setShowFileUpload(false)
    }
  }

  const handleLogout = async () => {
    await authService.logout()
    router.push('/')
  }

  return (
    <div className="h-screen flex flex-col">
      <header className="bg-surface border-b border-border px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="lg:hidden text-text-secondary hover:text-text-primary transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 className="text-lg font-semibold text-text-primary">MentorAI</h1>
        </div>

        <div className="flex items-center gap-4">
          <span className="hidden sm:block text-sm text-text-secondary">
            {authService.getUser()?.email}
          </span>
          <button
            onClick={handleLogout}
            className="bg-surface hover:bg-surface-hover border border-border text-text-primary px-4 py-2 rounded-md transition-colors text-sm"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <aside
          className={`${isSidebarOpen ? 'flex' : 'hidden'} lg:flex w-80 flex-shrink-0`}
        >
          <SessionList
            sessions={sessions}
            activeSessionId={activeSessionId}
            onSessionSelect={handleSessionSelect}
            onNewSession={handleNewSession}
            onSessionUpdate={loadSessions}
          />
        </aside>

        <main className="flex-1 flex flex-col bg-background">
          {showFileUpload && (
            <div className="p-4 border-b border-border bg-surface">
              <div className="max-w-4xl mx-auto">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-text-primary font-medium">Upload File</h3>
                  <button
                    onClick={() => setShowFileUpload(false)}
                    className="text-text-secondary hover:text-text-primary"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                <FileUpload
                  sessionId={activeSessionId}
                  onFileAnalyzed={handleFileAnalyzed}
                  disabled={loading}
                />
              </div>
            </div>
          )}

          <div className="flex-1 overflow-y-auto p-4">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center">
                <h2 className="text-2xl font-semibold text-text-primary mb-2">
                  Welcome to MentorAI
                </h2>
                <p className="text-text-secondary">
                  Start a conversation by typing a message below
                </p>
              </div>
            ) : (
              <div className="max-w-4xl mx-auto">
                {messages.map((message, index) => (
                  <MessageBubble 
                    key={index} 
                    message={message}
                    audioUrl={message.role === 'model' && index === messages.length - 1 ? lastAudioUrl : undefined}
                  />
                ))}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          <div className="p-4 border-t border-border bg-surface">
            <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
              <div className="flex gap-3 items-center">
                <button
                  type="button"
                  onClick={() => setShowFileUpload(!showFileUpload)}
                  disabled={!activeSessionId || loading}
                  className="bg-surface hover:bg-surface-hover border border-border text-text-primary p-3 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  title="Attach file"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 00-.586 1.414l6 6a2 2 0 001.414.586l6.586-6.586a2 2 0 001.414-1.414l-6-6a2 2 0 00-1.414-.586l-6.586 6.586a2 2 0 00-.586 1.414L12 13.586V9a1 1 0 10-1 0v4.586a1 1 0 001 1l6.586-6.586a1 1 0 00-.586-1.414l-6-6z" />
                  </svg>
                </button>
                <VoiceRecorder 
                  onTranscription={handleVoiceTranscription}
                  disabled={!activeSessionId || loading}
                />
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  disabled={!activeSessionId || loading}
                  className="flex-1 bg-background border border-border rounded-md px-4 py-3 text-text-primary placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all disabled:opacity-50"
                />
                <button
                  type="submit"
                  disabled={!input.trim() || !activeSessionId || loading}
                  className="bg-primary hover:bg-primary-hover text-white font-medium px-6 py-3 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Sending...' : 'Send'}
                </button>
              </div>
            </form>
          </div>
        </main>
      </div>

      <NewSessionModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreate={handleCreateSession}
      />
    </div>
  )
}
