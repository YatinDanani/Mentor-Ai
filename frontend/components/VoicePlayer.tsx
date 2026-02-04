'use client'

import { useRef, useState } from 'react'

interface VoicePlayerProps {
  audioUrl: string | null
}

export default function VoicePlayer({ audioUrl }: VoicePlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)

  if (!audioUrl) return null

  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause()
      } else {
        audioRef.current.play()
      }
    }
  }

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
  const fullAudioUrl = audioUrl.startsWith('http') ? audioUrl : `${API_URL}${audioUrl}`

  return (
    <button
      onClick={togglePlay}
      className="mt-2 bg-surface hover:bg-surface-hover border border-border text-text-primary p-2 rounded-full transition-colors"
      title={isPlaying ? 'Pause' : 'Play'}
    >
      <audio
        ref={audioRef}
        src={fullAudioUrl}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onEnded={() => setIsPlaying(false)}
        className="hidden"
      />
      {isPlaying ? (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
        </svg>
      )}
    </button>
  )
}
