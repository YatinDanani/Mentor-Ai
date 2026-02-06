import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl w-full">
        <h1 className="text-5xl font-bold text-center mb-4 text-text-primary">
          MentorAI
        </h1>
        <p className="text-center text-text-secondary text-xl mb-12">
          Your Autonomous Learning Companion
        </p>

        <div className="bg-surface border border-border rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold mb-4 text-text-primary">
            Welcome to the Future of Learning
          </h2>
          <p className="text-text-secondary mb-6">
            MentorAI is an intelligent assistant powered by Google Gemini 3, 
            designed to help you learn, explore, and discover new knowledge through 
            natural conversation.
          </p>
          <div className="space-y-3 text-text-secondary">
            <div className="flex items-center gap-3">
              <span className="text-primary">✓</span>
              <span>Natural conversations with AI</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-primary">✓</span>
              <span>Voice interaction support</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-primary">✓</span>
              <span>Multi-session learning</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-primary">✓</span>
              <span>Persistent memory</span>
            </div>
          </div>
        </div>

        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="bg-primary hover:bg-primary-hover text-white font-medium py-3 px-8 rounded-md transition-colors duration-200"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="bg-surface border border-border hover:bg-surface-hover text-text-primary font-medium py-3 px-8 rounded-md transition-colors duration-200"
          >
            Register
          </Link>
        </div>
      </div>
    </main>
  )
}
