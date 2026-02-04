# MentorAI Demo Script

This script is designed to showcase all the features of MentorAI during demos, presentations, or hackathons.

## Demo Overview

**Duration**: 5-7 minutes
**Audience**: Judges, developers, or users
**Goal**: Demonstrate the complete MentorAI learning experience

---

## Preparation Checklist

Before starting the demo:

- [ ] Backend server is running (`python app.py`)
- [ ] Frontend server is running (`cd frontend && npm run dev`)
- [ ] API keys are configured (Gemini, OpenAI, etc.)
- [ ] Browser is open at `http://localhost:3000`
- [ ] Test images are available for multimodal demo
- [ ] Microphone is connected and working
- [ ] Speakers/audio are enabled

---

## Demo Script

### 0. Introduction (30 seconds)

**What to say:**
"Welcome to MentorAI, an autonomous learning companion powered by Google's Gemini 3. MentorAI provides interactive tutoring with persistent memory, voice interaction, and multimodal capabilities. Let me show you how it works."

**What to show:**
- Landing page with dark professional theme
- Brief mention of tech stack (Flask, Next.js, Gemini 3, Whisper, TTS)

---

### 1. User Authentication (45 seconds)

**What to say:**
"MentorAI includes secure user authentication. Let me log in to access my personalized learning experience."

**What to show:**
- Login page with dark theme
- Enter credentials (use test account)
- Show successful login redirect

**Note:** If no account exists, briefly show registration page and mention password hashing with bcrypt.

---

### 2. Chat Interface & Dark Theme (30 seconds)

**What to say:**
"After logging in, you're greeted with a clean, professional dark interface designed for focused learning. The dark theme reduces eye strain during long study sessions."

**What to show:**
- Landing page with dark theme
- Sidebar showing existing sessions
- Empty chat interface

---

### 3. Text-Based Learning (1 minute)

**What to say:**
"Let's start with a simple text-based interaction. I'll ask MentorAI about machine learning fundamentals."

**What to show:**
- Type: "Explain what machine learning is in simple terms"
- Show AI response appearing
- Highlight context retention with follow-up:
  - Type: "What are the main types of machine learning?"
  - Show AI response referencing previous conversation

**Key feature to highlight:** Persistent memory - the AI remembers context across messages.

---

### 4. Voice Interaction (1.5 minutes)

**What to say:**
"Now let's try voice interaction. MentorAI supports both speech-to-text and text-to-speech, making it feel like you're talking to a real tutor."

**What to show:**
- Click the microphone button
- Show visual recording indicator (pulsing effect)
- Speak: "What is the difference between supervised and unsupervised learning?"
- Show transcription appearing in the message box
- Show AI response
- Play audio response using VoicePlayer component

**Technical note (optional):** "We use OpenAI Whisper for speech-to-text and Google Cloud TTS for text-to-speech."

---

### 5. Multimodal Capabilities (1.5 minutes)

**What to say:**
"One of MentorAI's most powerful features is multimodal learning. You can upload images or PDFs, and the AI will analyze them and help you understand the content."

**What to show:**
- Click the file upload button (paperclip icon)
- Show drag-drop interface
- Upload a diagram or code screenshot
- Show AI analyzing the image
- AI explains what's in the image with context

**Example prompts:**
- "Can you explain this diagram?"
- "What does this code do?"
- "Help me understand this chart"

**Technical note (optional):** "We use Gemini Vision API for image analysis and PyPDF2 for text extraction from PDFs."

---

### 6. Session Management (45 seconds)

**What to say:**
"MentorAI allows you to manage multiple learning sessions. You can create different sessions for different topics, track your progress, and easily switch between them."

**What to show:**
- Show sidebar with existing sessions
- Create a new session: "Learning Python"
- Switch between sessions
- Show conversation history in each session
- Mention that all data is persisted in SQLite database

---

### 7. Responsive Design (30 seconds)

**What to say:**
"The interface is fully responsive and works on any device. Let me show you how it adapts to different screen sizes."

**What to show:**
- Resize browser window
- Show sidebar collapsing on mobile
- Show touch-friendly mobile layout
- Mention that it's built with Next.js and Tailwind CSS

---

### 8. Wrap-up & Technical Highlights (45 seconds)

**What to say:**
"That's MentorAI in action! Here's what makes it special:"

**What to highlight:**
- **AI Model**: Google Gemini 3 Flash Preview with 1M token context
- **Backend**: Flask with SQLite database
- **Frontend**: Next.js 14+ with App Router
- **Theme**: Dark professional design optimized for learning
- **Authentication**: JWT-based with bcrypt password hashing
- **Voice**: Whisper (speech-to-text) + Gemini TTS (text-to-speech)
- **Multimodal**: Image and PDF analysis
- **Deployment**: Configured for Railway with CI/CD
- **Testing**: Pytest + Jest with coverage

---

## Alternative Demo Scenarios

### Quick Demo (3 minutes)

Skip to these key features:
1. Login
2. One text interaction
3. One voice interaction
4. Session switching
5. Wrap-up

### Technical Demo (10 minutes)

Add deeper technical explanations:
- Show API responses in browser DevTools
- Explain database schema
- Show CI/CD pipeline in GitHub Actions
- Explain Railway deployment configuration

### Educational Demo (5 minutes)

Focus on learning use cases:
1. Ask about a specific topic (e.g., "Explain React hooks")
2. Voice interaction for conversational learning
3. Upload a diagram and ask for explanation
4. Reference previous learning in new session

---

## Backup Plans

### If Backend is Down

- Show frontend mockups or screenshots
- Explain the architecture and features
- Mention deployment on Railway for production

### If Microphone Doesn't Work

- Demonstrate text chat instead
- Explain voice features conceptually
- Show that the interface supports both modes

### If File Upload Fails

- Demonstrate other features
- Explain multimodal capabilities with examples
- Show that the feature is implemented in the code

---

## Demo Tips

1. **Practice beforehand** - Know where to click and what to say
2. **Keep it simple** - Don't explain every technical detail
3. **Focus on value** - Emphasize how it helps users learn
4. **Be enthusiastic** - Show excitement about the product
5. **Handle errors gracefully** - If something fails, acknowledge and move on
6. **Stay on time** - Respect the time limit

---

## Demo Environment Setup

For a flawless demo, ensure:

```bash
# Terminal 1 - Backend
cd /path/to/mentorai
python app.py

# Terminal 2 - Frontend
cd /path/to/mentorai/frontend
npm run dev

# Terminal 3 - (Optional) Watch for changes
cd /path/to/mentorai
npm run lint
```

Open browser: `http://localhost:3000`

---

## Questions to Prepare For

1. "How does it maintain context across conversations?"
   - Answer: Using Gemini's stateful chat sessions and SQLite database for persistence

2. "Is this production-ready?"
   - Answer: Yes, it's configured for Railway deployment with CI/CD pipeline

3. "Can it handle multiple users?"
   - Answer: Yes, with JWT authentication and user-specific sessions

4. "What makes this different from ChatGPT?"
   - Answer: Purpose-built for education with persistent sessions, voice interaction, and multimodal learning

5. "How scalable is it?"
   - Answer: Railway handles horizontal scaling; database can be upgraded to PostgreSQL if needed

---

## Demo Recording Tips

If recording a demo video:

- Use a screen recording tool (OBS, Loom, etc.)
- Ensure good audio quality
- Use high resolution (1080p or higher)
- Add captions or subtitles
- Keep segments short and focused
- Include a brief intro and outro

---

End of Demo Script - Good luck with your presentation!
