'use client'

import { Message } from '@/types'
import VoicePlayer from './VoicePlayer'

interface MessageBubbleProps {
  message: Message
  audioUrl?: string | null
}

export default function MessageBubble({ message, audioUrl }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-primary text-white'
            : 'bg-surface border border-border text-text-primary'
        }`}
      >
        <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>
        <div className="flex items-center justify-between mt-2 gap-4">
          <p className={`text-xs ${isUser ? 'text-white/70' : 'text-muted'}`}>
            {new Date(message.timestamp).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
          {!isUser && <VoicePlayer audioUrl={audioUrl || null} />}
        </div>
      </div>
    </div>
  )
}
