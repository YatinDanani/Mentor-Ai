'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { authService } from '@/lib/auth'

export default function RegisterForm() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }

    setLoading(true)
    const result = await authService.register(email, password, name || undefined)

    if (result.success) {
      router.push('/chat')
    } else {
      setError(result.error || 'Registration failed')
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-md text-sm">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-text-secondary mb-2">
          Name <span className="text-muted">(optional)</span>
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full bg-surface border border-border rounded-md px-4 py-3 text-text-primary placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
          placeholder="Your name"
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-text-secondary mb-2">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full bg-surface border border-border rounded-md px-4 py-3 text-text-primary placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
          placeholder="your@email.com"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-text-secondary mb-2">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="w-full bg-surface border border-border rounded-md px-4 py-3 text-text-primary placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
          placeholder="••••••••"
        />
        <p className="text-xs text-muted mt-1">Must be at least 8 characters</p>
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-text-secondary mb-2">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          minLength={8}
          className="w-full bg-surface border border-border rounded-md px-4 py-3 text-text-primary placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-primary hover:bg-primary-hover text-white font-medium py-3 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Creating account...' : 'Register'}
      </button>
    </form>
  )
}
