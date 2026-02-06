import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import LoginForm from '@/components/auth/LoginForm'

jest.mock('@/lib/auth', () => ({
    authService: {
        login: jest.fn(),
        isAuthenticated: jest.fn(() => false)
    }
}))

jest.mock('next/navigation', () => ({
    useRouter: jest.fn(() => ({
        push: jest.fn()
    }))
}))

describe('LoginForm', () => {
    beforeEach(() => {
        jest.clearAllMocks()
    })

    it('renders email and password fields', () => {
        render(<LoginForm />)
        
        expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
        expect(screen.getByPlaceholderText(/your@email.com/i)).toBeInTheDocument()
        expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument()
    })

    it('shows validation error for missing email', async () => {
        const { login } = require('@/lib/auth').authService
        login.mockResolvedValue({ success: false, error: 'Email and password required' })
        
        render(<LoginForm />)
        
        const submitButton = screen.getByRole('button', { name: /login/i })
        fireEvent.click(submitButton)
        
        await waitFor(() => {
            expect(screen.getByText(/Email and password required/)).toBeInTheDocument()
        })
    })

    it('calls login with correct data', async () => {
        const { login } = require('@/lib/auth').authService
        login.mockResolvedValue({ 
            success: true, 
            token: 'test-token',
            user: { id: 1, email: 'test@example.com' }
        })
        
        const { push } = require('next/navigation').useRouter()
        
        render(<LoginForm />)
        
        const emailInput = screen.getByLabelText(/email/i)
        const passwordInput = screen.getByPlaceholderText(/password/i)
        const submitButton = screen.getByRole('button', { name: /login/i })
        
        await userEvent.type(emailInput, 'test@example.com')
        await userEvent.type(passwordInput, 'password123')
        fireEvent.click(submitButton)
        
        await waitFor(() => {
            expect(login).toHaveBeenCalledWith('test@example.com', 'password123')
            expect(push).toHaveBeenCalledWith('/chat')
        })
    })

    it('shows error message on login failure', async () => {
        const { login } = require('@/lib/auth').authService
        login.mockResolvedValue({ 
            success: false, 
            error: 'Invalid credentials' 
        })
        
        render(<LoginForm />)
        
        const emailInput = screen.getByLabelText(/email/i)
        const passwordInput = screen.getByPlaceholderText(/password/i)
        const submitButton = screen.getByRole('button', { name: /login/i })
        
        await userEvent.type(emailInput, 'test@example.com')
        await userEvent.type(passwordInput, 'wrongpassword')
        fireEvent.click(submitButton)
        
        await waitFor(() => {
            expect(screen.getByText(/Invalid credentials/)).toBeInTheDocument()
        })
    })
})
