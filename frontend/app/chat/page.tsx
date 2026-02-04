'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { authService } from '@/lib/auth'
import ChatInterface from '@/components/ChatInterface'

export default function ChatPage() {
  const router = useRouter()

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
    }
  }, [router])

  if (!authService.isAuthenticated()) {
    return null
  }

  return <ChatInterface />
}
