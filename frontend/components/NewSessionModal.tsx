'use client'

import { useState } from 'react'

interface NewSessionModalProps {
  isOpen: boolean
  onClose: () => void
  onCreate: (title: string) => void
}

export default function NewSessionModal({ isOpen, onClose, onCreate }: NewSessionModalProps) {
  const [title, setTitle] = useState('')

  if (!isOpen) return null

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (title.trim()) {
      onCreate(title.trim())
      setTitle('')
      onClose()
    }
  }

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-surface border border-border rounded-lg w-full max-w-md p-6">
        <h2 className="text-xl font-semibold text-text-primary mb-4">New Chat</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label htmlFor="sessionTitle" className="block text-sm font-medium text-text-secondary mb-2">
              Title
            </label>
            <input
              id="sessionTitle"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter chat title..."
              className="w-full bg-background border border-border rounded-md px-4 py-3 text-text-primary placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              autoFocus
            />
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-surface hover:bg-surface-hover border border-border text-text-primary font-medium py-3 rounded-md transition-colors duration-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 bg-primary hover:bg-primary-hover text-white font-medium py-3 rounded-md transition-colors duration-200"
            >
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
