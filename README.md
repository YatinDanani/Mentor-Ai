# 🎓 MentorAI

An autonomous learning companion built with Google's Gemini 3 API for the Gemini 3 Hackathon. Interactive AI tutoring with persistent conversation history and multimodal capabilities.

## Features

- ✅ **Gemini 3 Integration** - Stateful chat sessions with context retention
- ✅ **Persistent Memory** - SQLite database for conversation history
- ✅ **RESTful API** - Flask backend with session management
- ✅ **Test Suite** - Pytest infrastructure with database tests
- 🚧 **Voice Tutoring** - Live API integration (coming soon)
- 🚧 **Multimodal Learning** - Document upload and image analysis (coming soon)

## Tech Stack

- **Backend**: Flask + Python 3.x
- **AI**: Google Gemini 3 Flash Preview (1M token context)
- **Database**: SQLite
- **Testing**: Pytest
- **Deployment**: Render (planned)

## Quick Start

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd mentorai
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the root directory:
```env
GOOGLE_GEMINI_KEY=your_gemini_api_key_here
```

### 3. Run Backend
```bash
python app.py
```
Server runs on `http://localhost:5000`

### 4. Test the API
```bash
# Health check
curl http://localhost:5000/health

# Create session
curl -X POST http://localhost:5000/session/new \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","title":"My Chat"}'

# Send message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<session_id>","message":"Explain quantum computing"}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/session/new` | POST | Create new chat session |
| `/chat` | POST | Send message and get AI response |
| `/history/<session_id>` | GET | Retrieve conversation history |
| `/sessions` | GET | List all user sessions |

## Testing

Run the test suite:
```bash
pytest tests/
```

Test individual features:
```bash
python test_memory_problem.py  # Shows stateless API behavior
python test_memory_solution.py  # Shows stateful chat sessions
```

## Project Structure

```
mentorai/
├── app.py                    # Flask application & routes
├── database.py               # SQLite operations
├── gemini_service.py         # Gemini API wrapper
├── requirements.txt          # Dependencies
├── .env                      # API keys (not in repo)
├── .gitignore               # Git exclusions
├── tests/
│   └── test_database.py     # Database unit tests
└── data/
    └── mentorai.db          # SQLite database (auto-created)
```

## How It Works

**Stateless vs Stateful**:
- Gemini API calls via `generate_content()` are stateless (no memory)
- Chat sessions via `client.chats.create()` maintain conversation context
- Database stores full history for session recovery

**Memory Management**:
- Active chat objects stored in `GeminiService.active_chats`
- On session reload, history is replayed to rebuild context
- Leverages Gemini's 1M token context window for long conversations

## Hackathon Highlights

Built for [Gemini 3 Hackathon](https://gemini3.devpost.com) (Dec 17, 2025 - Feb 9, 2026)

**Why MentorAI Stands Out**:
- Interactive tutoring vs static note generation
- Production-ready architecture with testing & CI/CD
- Comprehensive use of Gemini 3 features (Flash, Live API, multimodal)
- Professional development practices (pytest, security, documentation)

## Development Timeline

- ✅ Week 1: API integration, database, testing
- 🚧 Week 2: Voice features, multimodal capabilities
- 🚧 Week 3: Frontend, deployment, demo prep

## Contributing

This is a hackathon project, but feedback welcome! Feel free to open issues or submit PRs.

## License

MIT License - Built for educational purposes

---

**Built with** ❤️ **by Yatin for the Gemini 3 Hackathon**
