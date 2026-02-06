import Link from 'next/link'
import RegisterForm from '@/components/auth/RegisterForm'

export default function RegisterPage() {
  return (
    <main className="min-h-screen flex items-center justify-center p-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-text-primary mb-2">Create Account</h1>
          <p className="text-text-secondary">Start your learning journey today</p>
        </div>

        <div className="bg-surface border border-border rounded-lg p-8">
          <RegisterForm />

          <p className="text-center text-text-secondary text-sm mt-6">
            Already have an account?{' '}
            <Link href="/login" className="text-primary hover:underline">
              Login
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
