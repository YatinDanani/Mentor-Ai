import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { authService } from '@/lib/auth'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MentorAI - Your Autonomous Learning Companion',
  description: 'AI-powered learning assistant built for the Gemini 3 Hackathon',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  authService.initAuth()

  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
