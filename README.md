# MentorAI - Restructured & Modularized 🚀

> **AI-Powered Mentoring Platform** with Text Chat, Voice Chat, Image Analysis, and PDF Support
> Built with Flask, Google Gemini 3, OpenAI Whisper, and modular architecture

---

## ✨ What's New in This Version?

This is a **completely restructured** version of MentorAI with professional-grade architecture:

### 🎯 Key Improvements

✅ **Modular Design** - Each feature is a separate, self-contained module  
✅ **Flask Blueprints** - Clean separation of routes by feature  
✅ **Service Layer** - Business logic separated from HTTP layer  
✅ **Optional Features** - Voice features work without breaking the app  
✅ **Better Error Handling** - Meaningful error messages  
✅ **Easier Testing** - Test each component independently  
✅ **Cleaner Code** - 70-line main file instead of 600+ lines  
✅ **Professional Structure** - Industry best practices  

### 📂 New Structure

```
backend/
├── app.py                    # Clean entry point (70 lines!)
├── config/                   # Centralized configuration
│   └── settings.py
├── routes/                   # Feature-based route modules
│   ├── auth_routes.py       # User authentication
│   ├── chat_routes.py       # Text chat with Gemini
│   ├── session_routes.py    # Session management
│   ├── file_routes.py       # Image/PDF upload & analysis
│   └── voice_routes.py      # Voice input/output
├── services/                 # Business logic & external APIs
│   ├── auth_service.py
│   ├── database_service.py
│   ├── gemini_service.py
│   ├── whisper_service.py
│   ├── tts_service.py
│   └── file_service.py
└── utils/                    # Reusable utilities
    └── decorators.py
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites

- Python 3.8+
- [Google Gemini API Key](https://aistudio.google.com/apikey)

### 2. Setup

```bash
# Clone and navigate
cd mentor-ai-restructured/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_GEMINI_KEY

# Run!
python app.py
```

### 3. Test It

```bash
# Health check
curl http://localhost:5000/health

# You should see:
{
  "status": "healthy",
  "message": "MentorAI is running!",
  "features": {
    "text_chat": true,
    "voice_chat": false,
    "file_upload": true
  }
}
```

**That's it! You have MentorAI running with text chat.** 🎉

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Complete setup instructions (basic + advanced) |
| **[RESTRUCTURING_EXPLAINED.md](RESTRUCTURING_EXPLAINED.md)** | Why and how we restructured the code |
| **[PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md)** | Technical overview and architecture |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Quick commands and API reference |

---

## 🎯 Features

### ✅ Core Features (Enabled by Default)

- **User Authentication** - Secure registration/login with JWT
- **Text Chat** - Intelligent conversations with Gemini 3 Flash
- **Session Management** - Multiple chat sessions per user
- **Image Upload & Analysis** - AI-powered image understanding
- **PDF Upload & Analysis** - Document analysis capabilities
- **Conversation History** - Full chat history with context

### 🔊 Optional Features (Configure API Keys)

- **Voice Input** - Speak to the AI (OpenAI Whisper)
- **Voice Output** - AI responds with speech (Google TTS)
- **Full Voice Chat** - Complete voice conversation experience

---

## 🛠️ Technology Stack

**Backend:**
- Flask 3.0 - Web framework with Blueprints
- Google Gemini 3 - AI chat & vision
- SQLite - Lightweight database
- JWT - Secure authentication
- bcrypt - Password hashing

**Optional (Voice):**
- OpenAI Whisper - Speech-to-text
- Google Cloud TTS - Text-to-speech

**Frontend (Separate):**
- Next.js 14
- TypeScript
- Tailwind CSS

---

## 📖 API Documentation

### Authentication

```bash
# Register
POST /auth/register
Body: {"email": "user@example.com", "password": "pass123", "name": "User"}

# Login
POST /auth/login
Body: {"email": "user@example.com", "password": "pass123"}

# Get current user
GET /auth/me
Headers: {"Authorization": "Bearer TOKEN"}
```

### Chat

```bash
# Create session
POST /session/new
Headers: {"Authorization": "Bearer TOKEN"}
Body: {"title": "My Chat"}

# Send message
POST /chat/
Headers: {"Authorization": "Bearer TOKEN"}
Body: {"session_id": "UUID", "message": "Hello!"}

# Get history
GET /chat/history/{session_id}
Headers: {"Authorization": "Bearer TOKEN"}
```

### Files

```bash
# Upload image/PDF
POST /files/upload
Headers: {"Authorization": "Bearer TOKEN"}
Form Data: file=@image.jpg, session_id=UUID

# Get session files
GET /files/{session_id}
Headers: {"Authorization": "Bearer TOKEN"}
```

### Voice (Optional)

```bash
# Voice chat
POST /voice/chat
Headers: {"Authorization": "Bearer TOKEN"}
Form Data: audio=@recording.mp3, session_id=UUID

# Check voice status
GET /voice/status
```

**See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for more examples**

---

## 🧪 Testing

### Manual Testing (curl)

```bash
# See QUICK_REFERENCE.md for complete curl examples
```

### Automated Testing (Coming Soon)

```bash
pytest tests/
pytest tests/ --cov=. --cov-report=html
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Required
GOOGLE_GEMINI_KEY=your_key
JWT_SECRET=your_secret

# Optional (for voice)
OPENAI_API_KEY=your_key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Feature Flags
VOICE_ENABLED=False
FILE_UPLOAD_ENABLED=True

# Other
DEBUG=True
DATABASE_PATH=data/mentorai.db
```

### Feature Flags

Enable/disable features in `config/settings.py` or `.env`:

```python
VOICE_ENABLED = True  # Requires OpenAI + Google Cloud credentials
FILE_UPLOAD_ENABLED = True
```

---

## 📊 How It Works

### Architecture

```
┌─────────────┐
│   Frontend  │
│  (Next.js)  │
└──────┬──────┘
       │ HTTP/REST API
       ▼
┌─────────────┐
│   Flask     │
│  (Routes)   │  ← routes/ (auth, chat, session, file, voice)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Services   │  ← services/ (business logic)
└──────┬──────┘
       │
       ├──► Gemini API (AI chat & vision)
       ├──► Whisper API (speech-to-text)
       ├──► Google TTS (text-to-speech)
       └──► SQLite (data storage)
```

### Request Flow Example (Chat)

```
1. User sends message → Frontend
2. POST /chat/ → routes/chat_routes.py
3. Validate token → utils/decorators.py
4. Get history → services/database_service.py
5. Send to Gemini → services/gemini_service.py
6. Save response → services/database_service.py
7. Return response → Frontend
```

---

## 🎓 Learning Resources

### For Beginners

1. Start with [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Read [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md)
3. Experiment with the API using curl
4. Try adding a simple route (see [QUICK_REFERENCE.md](QUICK_REFERENCE.md))

### For Advanced Developers

1. Read [RESTRUCTURING_EXPLAINED.md](RESTRUCTURING_EXPLAINED.md)
2. Study the service layer pattern
3. Add new features using blueprints
4. Write tests for your additions

---

## 🚧 Roadmap

- [ ] Complete test suite with pytest
- [ ] Docker containerization
- [ ] Redis caching for sessions
- [ ] PostgreSQL support
- [ ] Rate limiting
- [ ] WebSocket support for real-time chat
- [ ] Multi-language support
- [ ] Admin dashboard
- [ ] Analytics & monitoring

---

## 🤝 Contributing

This project follows clean code principles and modular architecture. When contributing:

1. **One feature = One blueprint** - Keep routes organized
2. **Business logic in services** - Not in routes
3. **Test your code** - Write unit tests
4. **Document your changes** - Update README and docs
5. **Follow the structure** - Match existing patterns

---

## 📝 License

MIT License - Built for educational purposes as part of the Gemini 3 Hackathon.

---

## 🙏 Acknowledgments

- **Google Gemini** - Amazing AI capabilities
- **OpenAI** - Whisper API for speech recognition
- **Flask Community** - Excellent web framework
- **You!** - For using and improving this project

---

## 📞 Support

- 📖 **Documentation**: See docs in this repo
- 🐛 **Issues**: Open an issue on GitHub
- 💬 **Questions**: Check SETUP_GUIDE.md troubleshooting section

---

## 🌟 Star This Repo!

If you find this project helpful, please star it on GitHub! ⭐

---

**Built with ❤️ using clean architecture and modern best practices**

**From hackathon prototype → Production-ready application**
