# Next.js Frontend Setup Guide

This guide will help you set up the MentorAI Next.js frontend from scratch or configure an existing installation.

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Backend API running (see [main README](../README.md))

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mentorai/frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXTAUTH_SECRET=your_nextauth_secret_here
NEXTAUTH_URL=http://localhost:3000
```

**Environment Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:5000` or `https://your-backend.railway.app` |
| `NEXTAUTH_SECRET` | Secret for NextAuth.js | Generate with: `openssl rand -base64 32` |
| `NEXTAUTH_URL` | Frontend URL | `http://localhost:3000` or `https://your-frontend.railway.app` |

### 4. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/                    # Next.js 14+ App Router
│   ├── (auth)/            # Auth pages (login, register)
│   │   ├── login/
│   │   └── register/
│   ├── chat/              # Chat pages
│   │   ├── page.tsx       # New chat
│   │   └── [session_id]/  # Session chat
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Landing page
├── components/            # React components
│   ├── ChatInterface.tsx  # Main chat UI
│   ├── MessageBubble.tsx  # Message component
│   ├── SessionList.tsx    # Session sidebar
│   ├── SessionManager.tsx # Session CRUD
│   ├── VoiceButton.tsx    # Voice recording
│   ├── VoicePlayer.tsx    # Audio playback
│   └── FileUpload.tsx     # File upload UI
├── lib/                   # Utilities
│   ├── api.ts            # API client
│   └── auth.ts           # Auth utilities
├── types/                # TypeScript types
│   └── index.ts          # Shared types
├── public/               # Static assets
├── __tests__/           # Jest tests
├── next.config.js       # Next.js config
├── tailwind.config.ts   # Tailwind CSS config
├── tsconfig.json        # TypeScript config
└── package.json         # Dependencies
```

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm test` | Run Jest tests |
| `npm run test:watch` | Run tests in watch mode |
| `npm run test:coverage` | Run tests with coverage |

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **UI**: React 18+
- **Styling**: Tailwind CSS (Dark Professional Theme)
- **Authentication**: NextAuth.js
- **HTTP Client**: Axios
- **Testing**: Jest + React Testing Library

## Dark Professional Theme

The application uses a custom dark theme configuration in `tailwind.config.ts`:

```typescript
colors: {
  background: '#0f0f0f',
  surface: '#1a1a1a',
  'surface-hover': '#252525',
  border: '#333333',
  primary: '#6366f1',
  'primary-hover': '#4f46e5',
  secondary: '#8b5cf6',
  'text-primary': '#ffffff',
  'text-secondary': '#a1a1aa',
  'text-muted': '#71717a',
}
```

See [THEME.md](./THEME.md) for customization guide.

## API Client

The `lib/api.ts` module provides a centralized API client with:

- Automatic JWT token injection
- Request/response interceptors
- Error handling
- File upload support

Example usage:

```typescript
import api from '@/lib/api';

// Send chat message
const response = await api.post('/chat', {
  session_id: 'session_123',
  message: 'Hello, AI!'
});

// Upload file
const formData = new FormData();
formData.append('file', file);
const response = await api.post('/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

## Authentication

Authentication is handled by NextAuth.js with a Credentials provider:

1. User registers/logs in via API
2. JWT token received from backend
3. Token stored in cookies
4. Protected routes validated via middleware

See `app/api/auth/[...nextauth]/route.ts` for configuration.

## Testing

Run the test suite:

```bash
npm test
```

Run with coverage:

```bash
npm run test:coverage
```

Tests are located in the `__tests__` directory.

## Building for Production

```bash
npm run build
npm start
```

This will create an optimized production build in the `.next` directory.

## Deployment

### Railway

The frontend is configured for Railway deployment with:
- `frontend/Procfile` - Process definition
- Auto-deploy from GitHub via CI/CD

See [main README](../README.md) for full deployment instructions.

### Vercel

You can also deploy to Vercel:

```bash
npm run build
vercel --prod
```

Make sure to set environment variables in Vercel dashboard.

## Troubleshooting

### Issues with API Connection

1. Verify backend is running on correct port
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Ensure CORS is configured on backend

### Authentication Issues

1. Verify `NEXTAUTH_SECRET` is set
2. Check `NEXTAUTH_URL` matches your domain
3. Clear browser cookies and localStorage

### Build Errors

1. Delete `node_modules` and `.next` directories
2. Run `npm install` again
3. Ensure Node.js version is 18+

## Contributing

When adding new components:

1. Follow existing patterns in `components/`
2. Use TypeScript for type safety
3. Apply dark theme classes
4. Add tests in `__tests__/`
5. Run `npm run lint` before committing

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [NextAuth.js Docs](https://next-auth.js.org)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [React Testing Library](https://testing-library.com/react)
