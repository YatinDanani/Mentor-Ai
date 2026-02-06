'use client'

import { useState } from 'react'
import { Session } from '@/types'
import { apiClient } from '@/lib/api'

interface SessionManagerProps {
  session: Session
  onUpdate: () => void
  onDelete: () => void
}

export default function SessionManager({ session, onUpdate, onDelete }: SessionManagerProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(session.title)

  const handleRename = async () => {
    try {
      const result = await apiClient.renameSession(session.id, editTitle)
      if (result.success) {
        onUpdate()
      }
      setIsEditing(false)
      setIsOpen(false)
    } catch (error) {
      console.error('Failed to rename session:', error)
    }
  }

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this session?')) {
      try {
        const result = await apiClient.deleteSession(session.id)
        if (result.success) {
          onDelete()
        }
        setIsOpen(false)
      } catch (error) {
        console.error('Failed to delete session:', error)
      }
    }
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-1 rounded hover:bg-surface-hover text-muted hover:text-text-primary transition-colors"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-1 w-40 bg-surface border border-border rounded-md shadow-lg z-10">
          {isEditing ? (
            <div className="p-2">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full bg-background border border-border rounded px-2 py-1 text-sm text-text-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
              <div className="flex gap-1 mt-2">
                <button
                  onClick={() => setIsEditing(false)}
                  className="flex-1 text-xs px-2 py-1 bg-surface-hover rounded text-text-secondary hover:text-text-primary"
                >
                  Cancel
                </button>
                <button
                  onClick={handleRename}
                  className="flex-1 text-xs px-2 py-1 bg-primary rounded text-white"
                >
                  Save
                </button>
              </div>
            </div>
          ) : (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="w-full text-left px-3 py-2 text-sm text-text-secondary hover:bg-surface-hover hover:text-text-primary transition-colors"
              >
                Rename
              </button>
              <button
                onClick={handleDelete}
                className="w-full text-left px-3 py-2 text-sm text-red-400 hover:bg-red-500/10 transition-colors"
              >
                Delete
              </button>
            </>
          )}
        </div>
      )}
    </div>
  )
}
