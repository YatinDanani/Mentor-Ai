import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'

describe('MessageBubble', () => {
  const mockMessage = {
    role: 'user',
    content: 'Test message',
    timestamp: '2024-01-01T12:00:00Z'
  }

  it('renders user message correctly', () => {
    render(<MessageBubble message={mockMessage} />)
    
    expect(screen.getByText('Test message')).toBeInTheDocument()
  })

  it('renders AI message with correct styling', () => {
    const aiMessage = { ...mockMessage, role: 'model' }
    render(<MessageBubble message={aiMessage} />)
    
    expect(screen.getByText('Test message')).toBeInTheDocument()
  })

  it('displays timestamp', () => {
    render(<MessageBubble message={mockMessage} />)
    
    expect(screen.getByText(/12:00/)).toBeInTheDocument()
  })
})
