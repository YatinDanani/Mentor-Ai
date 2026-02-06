'use client'

import { Session } from '@/types'
import SessionManager from './SessionManager'

interface SessionListProps {
  sessions: Session[]
  activeSessionId: string | null
  onSessionSelect: (sessionId: string) => void
  onNewSession: () => void
  onSessionUpdate: () => void
}

export default function SessionList({ sessions, activeSessionId, onSessionSelect, onNewSession, onSessionUpdate }: SessionListProps) {
  return (
    <div className="h-full flex flex-col bg-surface border-r border-border">
      <div className="p-4 border-b border-border">
        <button
          onClick={onNewSession}
          className="w-full bg-primary hover:bg-primary-hover text-white font-medium py-3 px-4 rounded-md transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 ? (
          <div className="p-4 text-center text-muted text-sm">
            No chat sessions yet. Start a new conversation!
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {sessions.map((session) => (
              <div
                key={session.id}
                className={`flex items-center gap-2 px-3 py-2 rounded-md transition-colors duration-150 group ${
                  activeSessionId === session.id
                    ? 'bg-surface-hover text-text-primary'
                    : 'text-text-secondary hover:bg-surface-hover hover:text-text-primary'
                }`}
              >
                <button
                  onClick={() => onSessionSelect(session.id)}
                  className="flex-1 text-left truncate"
                >
                  <div className="font-medium text-sm truncate">{session.title}</div>
                  <div className="text-xs text-muted mt-1">
                    {new Date(session.last_active).toLocaleDateString([], {
                      month: 'short',
                      day: 'numeric',
                    })}
                  </div>
                </button>
                <SessionManager
                  session={session}
                  onUpdate={onSessionUpdate}
                  onDelete={onSessionUpdate}
                />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
