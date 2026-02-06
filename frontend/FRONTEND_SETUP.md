# Frontend Setup Guide

## Quick Start

### Step 1: Navigate to Frontend

```bash
cd mentor-ai-restructured/frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install all the Next.js dependencies.

### Step 3: Configure Environment

```bash
cp .env.example .env.local
```

Edit `.env.local` and set:

```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXTAUTH_SECRET=your_secret_here
NEXTAUTH_URL=http://localhost:3000
```

### Step 4: Run the Frontend

```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Make Sure Backend is Running

The frontend needs the backend API to be running:

```bash
# In another terminal, go to backend folder
cd ../backend
source venv/bin/activate
python app.py
```

Now you should have:
- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:3000

## Frontend Structure

```
frontend/
├── app/                      # Next.js 14 app directory
│   ├── page.tsx             # Landing page
│   ├── login/               # Login page
│   ├── register/            # Register page
│   └── chat/                # Chat interface
│       ├── page.tsx         # Main chat
│       └── [session_id]/    # Individual sessions
├── components/              # React components
│   ├── ChatInterface.tsx
│   ├── MessageBubble.tsx
│   ├── VoiceRecorder.tsx
│   ├── VoicePlayer.tsx
│   ├── FileUpload.tsx
│   ├── SessionManager.tsx
│   └── auth/
│       ├── LoginForm.tsx
│       └── RegisterForm.tsx
├── lib/                     # Utilities
│   ├── api.ts              # API client
│   └── auth.ts             # Auth helpers
├── types/                   # TypeScript types
└── package.json
```

## Development

```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test
```

## Connecting to Backend

The frontend is already configured to connect to your backend at `http://localhost:5000`.

All API calls go through `lib/api.ts` which handles:
- Authentication tokens
- Request/response formatting
- Error handling

## Features Included

- ✅ User authentication (login/register)
- ✅ Chat interface with Gemini AI
- ✅ Session management
- ✅ File upload (images/PDFs)
- ✅ Voice recording/playback
- ✅ Dark theme
- ✅ Responsive design

## Next Steps

1. Start the backend (see backend/SETUP_GUIDE.md)
2. Start the frontend (this guide)
3. Open http://localhost:3000
4. Register a new account
5. Start chatting!

## Troubleshooting

### "Cannot connect to backend"

Make sure:
1. Backend is running on port 5000
2. NEXT_PUBLIC_API_URL is set correctly
3. No CORS issues (backend has CORS enabled)

### "npm install fails"

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port 3000 already in use

```bash
# Kill the process
lsof -ti:3000 | xargs kill -9

# Or run on different port
npm run dev -- -p 3001
```
