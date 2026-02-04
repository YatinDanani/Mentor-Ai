# MentorAI Project Plan

## Project Overview
MentorAI is an autonomous learning companion built for the Gemini 3 Hackathon (Dec 17, 2025 - Feb 9, 2026) using Google's Gemini API.

## Tech Stack
| Component | Technology | Status |
|-----------|-----------|--------|
| Backend | Flask + Python 3.x | Complete |
| AI Model | Google Gemini 3 Flash Preview | Complete |
| Voice - Speech-to-Text | OpenAI Whisper | Complete |
| Voice - Text-to-Speech | Gemini TTS | Complete |
| Database | SQLite | Complete |
| Frontend | Next.js 14+ (App Router) + React 18+ | Complete |
| Styling | Tailwind CSS (Dark Professional Theme) | Complete |
| Authentication | Backend + Frontend | Complete |
| Multimodal | Image & PDF upload | Complete |
| Deployment | Railway | Pending |
| Testing | Pytest + Jest + Playwright | In Progress |

## Design Theme: Dark Professional

### Color Palette
Background: #0f0f0f
Surface: #1a1a1a
Surface-hover: #252525
Border: #333333

Primary: #6366f1
Primary-hover: #4f46e5
Secondary: #8b5cf6

Text-primary: #ffffff
Text-secondary: #a1a1aa
Text-muted: #71717a

Success: #22c55e
Warning: #f59e0b
Error: #ef4444
Info: #3b82f6

### Typography
- Font: Inter (Google Fonts)
- Heading weights: 600-700
- Body weights: 400-500
- Monospace for code: JetBrains Mono or Fira Code

### Component Guidelines
- Cards: Surface background with subtle border
- Buttons: Primary color with hover states, rounded corners (md)
- Inputs: Dark surface with light border, focus ring
- Message Bubbles:
  - User: Primary color (#6366f1)
  - AI: Surface (#1a1a1a) with accent border
- Sidebar: Dark surface (#1a1a1a)
- Modals: Semi-transparent overlay (#000000, 70% opacity)

## Code Changes Required

### Add OpenAI Whisper & Gemini TTS Integration

New files to create:
- whisper_service.py - OpenAI Whisper service for speech-to-text
- tts_service.py - Gemini TTS service for text-to-speech

Dependencies to add:
- openai
- pydub
- google-cloud-texttospeech

### New File: whisper_service.py
```python
import openai
import os
from pydub import AudioSegment
import tempfile

class WhisperService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def transcribe_audio(self, audio_file_path, model='whisper-1'):
        """Transcribe audio using OpenAI Whisper"""
        with open(audio_file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model=model,
                file=audio_file
            )
        return transcript['text']
```

### New File: tts_service.py
```python
from google.cloud import texttospeech
import os

class TTSService:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text, language_code='en-US'):
        """Synthesize speech from text using Gemini TTS"""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
```

## Phase 1: Core Backend (COMPLETE)
Status: Done
- Gemini 3 Flash Preview Integration (stateful chat sessions)
- Persistent Memory (SQLite database)
- RESTful API (Flask backend)
- Test Suite (Pytest infrastructure)
- Environment configuration (.env file)
- Database initialization verified

## Phase 2: Authentication & User Management (HIGH PRIORITY)

### 2.1 User Authentication System (Backend)

Status: Complete

Description: Add secure user authentication to the backend

Tasks:
- [x] Add user registration endpoint: /auth/register (POST)
- [x] Add user login endpoint: /auth/login (POST)
- [x] Add session validation middleware
- [x] Add /auth/me (GET) to get current user info
- [x] Add /auth/logout (POST) for logout
- [x] Implement JWT token generation and validation
- [x] Add password hashing (bcrypt)

Database Updates Required:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Security Requirements:
- Password minimum length: 8 characters
- Email validation
- Rate limiting on auth endpoints
- JWT expiration (24 hours)

Acceptance Criteria:
- [x] Users can register with email/password
- [x] Users can login and receive JWT token
- [x] Protected routes validate JWT tokens
- [x] Session management across page reloads

### 2.2 Frontend Authentication (Next.js) - Dark Theme

Status: Complete

Description: Integrate NextAuth.js for frontend authentication with dark professional styling

Tasks:
- [x] Set up NextAuth.js with Credentials provider
- [x] Create login page (/login) with dark theme
- [x] Create registration page (/register) with dark theme
- [x] Add protected routes middleware
- [x] Implement JWT persistence
- [x] Add logout functionality
- [x] Apply dark professional theme to all auth pages

Design Requirements:
- Background: #0f0f0f
- Cards/Surfaces: #1a1a1a
- Primary buttons: #6366f1
- Text: #ffffff (primary), #a1a1aa (secondary)
- Input fields: #1a1a1a background, #333333 border
- Hover states with subtle transitions

Pages to Create:
- app/login/page.tsx - Login form (dark theme)
- app/register/page.tsx - Registration form (dark theme)
- middleware.ts - Route protection
- Update all pages to check auth status

## Phase 3: Next.js Frontend (HIGH PRIORITY)

### 3.1 Next.js Project Setup

Tasks:
- [ ] Initialize Next.js 14+ project with TypeScript
- [ ] Set up folder structure (App Router)
- [ ] Configure environment variables
- [ ] Set up Tailwind CSS with dark theme configuration
- [ ] Configure ESLint and Prettier
- [ ] Add Inter font family

Tailwind Configuration:
```javascript
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
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
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
}
```

Project Structure:
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── chat/
│   │   ├── [session_id]/page.tsx
│   │   └── page.tsx (new chat)
│   ├── layout.tsx
│   └── page.tsx (landing)
├── components/
│   ├── ChatInterface.tsx
│   ├── MessageBubble.tsx
│   ├── SessionList.tsx
│   ├── SessionManager.tsx
│   └── auth/
│       ├── LoginForm.tsx
│       └── RegisterForm.tsx
├── lib/
│   ├── api.ts (API client)
│   ├── auth.ts (Auth utilities)
│   └── utils.ts
└── types/
    └── index.ts (TypeScript types)
```

### 3.2 Core UI Components (Dark Professional Theme)

Status: Complete

Tasks:
- [x] Create ChatInterface component with dark theme
- [x] Create MessageBubble (user: primary color, AI: surface color)
- [x] Create SessionList sidebar with dark theme
- [x] Create NewSessionModal with dark theme
- [x] Create SessionManager with dark theme
- [x] Add responsive layout with mobile support

Component Styling Guidelines:
- All backgrounds: #0f0f0f or #1a1a1a
- All text: #ffffff (primary) or #a1a1aa (secondary)
- All borders: #333333
- Primary actions: #6366f1
- Smooth transitions (150-200ms)
- Rounded corners (rounded-md)

API Integration:
- All API calls through lib/api.ts
- Error handling and loading states
- Optimistic UI updates

## Phase 4: Voice Interaction Features (HIGH PRIORITY)

### 4.1 Backend Voice Integration

Status: Complete

Description: Add OpenAI Whisper for speech-to-text

Tasks:
- [x] Add OpenAI Whisper service (whisper_service.py)
- [x] Implement speech-to-text using OpenAI Whisper API
- [x] Add /chat/voice (POST) endpoint for voice input
- [x] Add voice message processing
- [x] Return AI response
- [x] Add voice session management

### 4.2 Frontend Voice UI (Dark Theme)

Status: Complete

Description: Add voice controls to chat interface with dark professional styling

Tasks:
- [x] Add microphone button with dark theme
- [x] Implement audio recording with MediaRecorder API
- [x] Show visual recording indicator (pulsing effect)
- [x] Display audio transcription
- [x] Add voice mode toggle
- [x] Apply dark theme to all voice components

## Phase 5: Text-to-Speech (HIGH PRIORITY)

Status: Complete

Description: Add Gemini TTS for AI responses

Tasks:
- [x] Implement Gemini TTS service (tts_service.py)
- [x] Add TTS endpoint: /tts/synthesize (POST)
- [x] Return audio file URL in /chat/voice response
- [x] Create VoicePlayer component for audio playback
- [x] Apply dark theme to voice player

### New File: tts_service.py
```python
from google.cloud import texttospeech
import os

class TTSService:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text, language_code='en-US'):
        """Synthesize speech from text using Gemini TTS"""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
```

## Phase 6: Multimodal Features (OPTIONAL - Time Permitting)

### 6.1 Backend Multimodal Integration

Status: Complete

Tasks:
- [x] Add /upload (POST) endpoint for files
- [x] Implement image analysis with Gemini 3 Flash Preview
- [x] Add PDF text extraction (PyPDF2)
- [x] Store file metadata in database
- [x] Inject file context into chat sessions

### 6.2 Frontend Multimodal UI (Dark Theme)

Status: Complete

Tasks:
- [x] Add file upload component with drag-drop (dark theme)
- [x] Create image preview component (dark background)
- [x] Add document attachment display (dark theme)
- [x] Implement file removal
- [x] Add file type validation
- [x] Apply dark professional theme

## Phase 7: Testing & Quality Assurance

### 7.1 Backend Tests

Tasks:
- [ ] Add authentication tests
- [ ] Test all new endpoints
- [ ] Test edge cases and error handling
- [ ] Test Whisper transcription
- [ ] Add integration tests

### 7.2 Frontend Tests

Tasks:
- [ ] Set up Jest + React Testing Library
- [ ] Test auth flows
- [ ] Test chat interface components
- [ ] Add E2E tests with Playwright
- [ ] Test voice UI components
- [ ] Test dark theme consistency

## Phase 8: Deployment (Railway)

### 8.1 Backend Deployment

Tasks:
- [ ] Create Railway project for Flask backend
- [ ] Configure environment variables:
  - GOOGLE_GEMINI_KEY
  - OPENAI_API_KEY
- [ ] Set up PostgreSQL (optional, or keep SQLite)
- [ ] Configure auto-deploy from GitHub

### 8.2 Frontend Deployment

Tasks:
- [ ] Create Railway project for Next.js
- [ ] Configure environment variables (API URL)
- [ ] Set up build and start commands
- [ ] Configure custom domain (optional)

### 8.3 CI/CD Setup

Tasks:
- [ ] Add GitHub Actions workflow
- [ ] Run tests on every push
- [ ] Auto-deploy to Railway on merge to main
- [ ] Add linting checks

## Phase 9: Documentation & Demo

### 9.1 Documentation

Tasks:
- [ ] Update README with auth, voice features, model update
- [ ] Create API documentation
- [ ] Add setup/deployment guides
- [ ] Document Next.js frontend setup
- [ ] Include dark theme customization guide

### 9.2 Demo Preparation

Tasks:
- [ ] Create demo script showcasing dark theme
- [ ] Record demo video
- [ ] Prepare hackathon presentation
- [ ] Set up demo environment

## Timeline

Hackathon Deadline: Feb 9, 2026

| Week | Phase | Priority | Estimated Days | Status |
|------|-------|----------|----------------|--------|
| Week 1 | Core Backend | HIGH | 5 days | Complete |
| Week 2 | Auth System | HIGH | 3-4 days | Complete |
| Week 2 | Next.js Frontend (Dark Theme) | HIGH | 3-4 days | Complete |
| Week 3 | Voice Features (Whisper + TTS) | HIGH | 3-4 days | Complete |
| Week 3 | Multimodal (Optional) | LOW | 2-3 days | Complete |
| Week 4 | Testing & QA | HIGH | 2-3 days | Pending |
| Week 4 | Deployment (Railway) | HIGH | 1-2 days | Pending |
| Week 5 | Documentation & Demo | HIGH | 2-3 days | Pending |

Total Estimated Time: 18-23 days

## Implementation Priority Order

Must Have (Core Product):
1. Backend API (complete)
2. User Authentication (backend + frontend complete)
3. Next.js Frontend with dark professional theme (complete)
4. Voice interaction (Whisper + Gemini TTS) (complete)

Should Have:
5. Session management (rename, delete) - complete
6. Full testing coverage
7. Mobile responsive design (complete)

Nice to Have (Time Permitting):
8. Multimodal file upload
9. Export sessions
10. Advanced voice features

## Success Criteria

Minimum Viable Product (MVP):
- AI powered by gemini-3-flash-preview (complete)
- Dark professional theme throughout (complete)
- Users can register and login (frontend & backend complete)
- Users can create chat sessions (complete)
- Users can send text messages (complete)
- Users can send voice messages (Whisper) (complete)
- AI responses with context retention (complete)
- AI responses spoken aloud (Gemini TTS) (complete)
- Users can view conversation history (complete)
- Users can manage multiple sessions (complete)
- Users can upload images and PDFs for AI analysis (complete)

Polished Product:
- Voice recording with visual feedback
- Beautiful dark UI with smooth animations
- Full testing coverage
- Deployed and accessible
- Demo-ready

## Summary of All Changes

| Change Type | Details |
|-------------|---------|
| AI Model | Keep gemini-3-flash-preview (no change) |
| Speech-to-Text | OpenAI Whisper (complete) |
| Text-to-Speech | Gemini TTS (complete) |
| Theme | Dark professional theme with specific color palette (complete) |
| Multimodal | Image & PDF upload with AI analysis (complete) |
| New Files | whisper_service.py, tts_service.py, Next.js frontend with dark theme, voice components, file upload (complete) |

## Open Questions

1. Whisper Model: Which OpenAI Whisper model should we use?
   - whisper-1 (fastest, good for real-time)
   - whisper-large-v3 (most accurate, slower)
2. Audio Recording: Should we support both real-time recording and file upload for voice messages?
3. Gemini TTS Model: Which voice model for Gemini TTS should we use?
   - Standard WaveNet (balanced)
   - Standard Neural2 (more natural)
4. Dark Theme Customization: Are you happy with the color palette specified?

## API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| /health | GET | Health check | No |
| /auth/register | POST | User registration | No |
| /auth/login | POST | User login | No |
| /auth/me | GET | Get current user | Yes |
| /auth/logout | POST | User logout | Yes |
| /session/new | POST | Create new chat session | Yes |
| /chat | POST | Send message and get AI response | Yes |
| /chat/voice | POST | Send voice message | Yes |
| /tts/synthesize | POST | Synthesize speech from text | Yes |
| /history/<session_id> | GET | Retrieve conversation history | Yes |
| /sessions | GET | List all user sessions | Yes |

## Environment Variables

Backend:
```
GOOGLE_GEMINI_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET=your_jwt_secret_here
DATABASE_URL=sqlite:///data/mentorai.db
```

Frontend:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXTAUTH_SECRET=your_nextauth_secret_here
NEXTAUTH_URL=http://localhost:3000
```

## Resources

Documentation:
- Google Gemini API Docs: https://ai.google.dev/docs
- OpenAI Whisper Docs: https://platform.openai.com/docs/guides/speech-to-text
- Next.js Documentation: https://nextjs.org/docs
- NextAuth.js Docs: https://next-auth.js.org
- Tailwind CSS Docs: https://tailwindcss.com/docs

Deployment:
- Railway Docs: https://docs.railway.app
- Flask Deployment Guide: https://flask.palletsprojects.com/en/latest/deploying/
- Next.js Deployment: https://nextjs.org/docs/deployment

## License

MIT License - Built for educational purposes

Built by Yatin for the Gemini 3 Hackathon
