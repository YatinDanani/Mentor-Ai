'use client'

import { useState } from 'react'

interface FileUploadProps {
  sessionId: string | null
  onFileAnalyzed: (result: any) => void
  disabled: boolean
}

export default function FileUpload({ sessionId, onFileAnalyzed, disabled }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    if (disabled || !sessionId || loading) return

    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      await uploadFile(files[0])
    }
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (disabled || !sessionId || loading) return

    const files = e.target.files
    if (files && files.length > 0) {
      await uploadFile(files[0])
    }
  }

  const uploadFile = async (file: File) => {
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('session_id', sessionId)

      const token = localStorage.getItem('token')
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

      const response = await fetch(`${API_URL}/files/upload`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      })

      const result = await response.json()

      if (result.success) {
        onFileAnalyzed(result)
      } else {
        console.error('File upload failed:', result.error)
        alert('Failed to upload file: ' + result.error)
      }
    } catch (error) {
      console.error('Error uploading file:', error)
      alert('Failed to upload file. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        border-2 border-dashed rounded-lg p-6 transition-colors duration-200 cursor-pointer
        ${isDragging 
          ? 'border-primary bg-primary/10' 
          : 'border-border hover:border-border-hover hover:bg-surface-hover'
        }
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      <label className="flex flex-col items-center justify-center gap-3 cursor-pointer">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-12 w-12 text-text-muted"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 17a5 5 0 01-2.412 3.927 5 5 0 00-.389-1.393l-3.5-6.378a1 1 0 00-.395-.823l-4-7.425a1 1 0 00-1.393.554l-3.5 6.379a1 1 0 00.394.822l4 7.426a1 1 0 001.393-.554l3.5-6.38a1 1 0 00-.394-.823L7 16z"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M14.5 9a2.25 2.25 0 00-4.5 0v5.625a.75.75 0 00.75.75h10.5a.75.75 0 00.75-.75V9a2.25 2.25 0 00-4.5 0z"
          />
        </svg>
        <div className="text-center">
          {loading ? (
            <p className="text-text-secondary">Processing file...</p>
          ) : (
            <>
              <p className="text-text-primary font-medium">
                {isDragging ? 'Drop file here' : 'Click or drag file here'}
              </p>
              <p className="text-xs text-muted mt-1">
                PNG, JPG, JPEG, GIF, WEBP, PDF (max 10MB)
              </p>
            </>
          )}
        </div>
        <input
          type="file"
          accept="image/*,.pdf"
          onChange={handleFileSelect}
          disabled={disabled || loading}
          className="hidden"
        />
      </label>
    </div>
  )
}
