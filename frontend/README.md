# MentorAI Frontend

Next.js 14 frontend with TypeScript and Tailwind CSS (Dark Professional Theme)

## Getting Started

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS (Dark Professional Theme)
- **HTTP Client**: Axios
- **Font**: Inter

## Project Structure

```
frontend/
├── app/
│   ├── login/page.tsx          # Login page
│   ├── register/page.tsx       # Registration page
│   ├── chat/page.tsx           # Chat interface (placeholder)
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Landing page
│   └── globals.css             # Global styles
├── components/
│   └── auth/
│       ├── LoginForm.tsx       # Login form component
│       └── RegisterForm.tsx    # Registration form component
├── lib/
│   ├── api.ts                  # API client
│   ├── auth.ts                 # Auth utilities
│   └── utils.ts                # Utility functions
├── types/
│   └── index.ts                # TypeScript types
└── middleware.ts              # Route protection
```

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXTAUTH_SECRET=your_nextauth_secret_here
NEXTAUTH_URL=http://localhost:3000
```

## Theme Configuration

Dark Professional Theme colors:
- Background: #0f0f0f
- Surface: #1a1a1a
- Primary: #6366f1
- Text Primary: #ffffff
- Text Secondary: #a1a1aa
