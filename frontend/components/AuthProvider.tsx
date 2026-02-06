'use client'

import { useEffect } from 'react'
import { authService } from '@/lib/auth'

export default function AuthProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize auth on client side
    authService.initAuth()
  }, [])

  return <>{children}</>
}
