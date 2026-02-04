'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { authService } from '@/lib/auth'

export default function ChatPage() {
  const router = useRouter()
  const user = authService.getUser()

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
    }
  }, [router])

  const handleLogout = async () => {
    await authService.logout()
    router.push('/')
  }

  return (
    <main className="min-h-screen flex flex-col">
      <header className="bg-surface border-b border-border px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold text-text-primary">MentorAI</h1>
          <div className="flex items-center gap-4">
            <span className="text-text-secondary">Hello, {user?.name || user?.email}</span>
            <button
              onClick={handleLogout}
              className="bg-surface hover:bg-surface-hover border border-border text-text-primary px-4 py-2 rounded-md transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-text-primary mb-2">
            Chat Interface Coming Soon
          </h2>
          <p className="text-text-secondary">
            Full chat UI will be implemented in Phase 3
          </p>
        </div>
      </div>
    </main>
  )
}
