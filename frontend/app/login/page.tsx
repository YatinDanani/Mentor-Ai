import Link from 'next/link'
import LoginForm from '@/components/auth/LoginForm'

export default function LoginPage() {
  return (
    <main className="min-h-screen flex items-center justify-center p-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-text-primary mb-2">Welcome Back</h1>
          <p className="text-text-secondary">Sign in to continue learning</p>
        </div>

        <div className="bg-surface border border-border rounded-lg p-8">
          <LoginForm />

          <p className="text-center text-text-secondary text-sm mt-6">
            Don't have an account?{' '}
            <Link href="/register" className="text-primary hover:underline">
              Register
            </Link>
          </p>
        </div>

        <p className="text-center text-muted text-sm mt-6">
          <Link href="/" className="hover:text-text-secondary transition-colors">
            Back to home
          </Link>
        </p>
      </div>
    </main>
  )
}
