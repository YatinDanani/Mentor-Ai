# 🎓 MentorAI Backend

**An autonomous AI tutoring platform built for the Gemini 3 Hackathon**

MentorAI is an interactive learning companion that provides real-time conversational tutoring with persistent memory and context awareness. Built with Flask and Google's Gemini 3 API, it showcases advanced AI capabilities including conversation persistence, multimodal learning support, and intelligent session management.

---

## ✨ What's Built

### 🏗️ Core Architecture

**Three-Layer Architecture:**
- **Database Layer** (`database.py`) - SQLite-based persistence with proper schema design
- **Service Layer** (`gemini_service.py`) - Gemini API wrapper with intelligent session management
- **API Layer** (`app.py`) - RESTful Flask endpoints with CORS support

### 🎯 Key Features Implemented

#### 1. **Persistent Conversation Memory**
- ✅ Chat sessions with full conversation history
- ✅ Context-aware responses using Gemini's 1M token window
- ✅ No vector database needed - full history maintained in-session
- ✅ Automatic session replay for context restoration

#### 2. **Session Management**
- ✅ Create and track multiple chat sessions per user
- ✅ Retrieve conversation history
- ✅ Last active timestamp tracking
- ✅ Custom session titles

#### 3. **Database Design**
```sql
sessions (id, user_id, created_at, last_active, title)
messages (id, session_id, role, content, timestamp)
```

#### 4. **RESTful API**
- `GET  /health` - Health check
- `POST /session/new` - Create new chat session
- `POST /chat` - Send message and get AI response
- `GET  /history/<session_id>` - Retrieve conversation history
- `GET  /sessions` - Get all user sessions

#### 5. **Testing Infrastructure**
- ✅ Pytest test suite for database operations
- ✅ Test fixtures for isolated testing
- ✅ Automatic cleanup after tests
- ✅ Memory problem/solution demonstrations

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd MentorAI-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the root directory:
```env
GOOGLE_GEMINI_KEY=your_api_key_here
```

5. **Run the server**
```bash
python app.py
```

Server starts on `http://localhost:5000`

---

## 🧪 Testing

### Run all tests
```bash
pytest tests/
```

### Test memory functionality
```bash
# Test the problem (no memory)
python test_memory_problem.py

# Test the solution (with sessions)
python test_memory_solution.py
```

### Test basic Gemini connection
```bash
python test_gemini.py
```

---

## 📡 API Usage Examples

### Create a new session
```bash
curl -X POST http://localhost:5000/session/new \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "title": "Physics Tutoring"}'
```

**Response:**
```json
{
  "success": true,
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Send a message
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "Explain quantum entanglement"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "Quantum entanglement is a phenomenon where..."
}
```

### Get conversation history
```bash
curl http://localhost:5000/history/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### Get all sessions
```bash
curl http://localhost:5000/sessions?user_id=user123
```

---

## 🔧 Technical Implementation Details

### Memory Management Strategy

**The Problem:**
```python
# This DOESN'T work - each call is independent
response1 = client.models.generate_content(model="gemini-3-flash-preview", 
                                           contents="My favorite color is purple")
response2 = client.models.generate_content(model="gemini-3-flash-preview", 
                                           contents="What is my favorite color?")
# Gemini doesn't remember!
```

**The Solution:**
```python
# Use chat sessions for persistent memory
chat = client.chats.create(model="gemini-3-flash-preview")
chat.send_message("My favorite color is purple")
chat.send_message("What is my favorite color?")  
# Gemini remembers within the session!
```

### Session Replay Mechanism
When a session is restored from the database:
1. Load conversation history from SQLite
2. Create new Gemini chat session
3. Replay user messages to rebuild context
4. Continue from current state

This leverages Gemini's 1M token context window instead of traditional RAG approaches.

### Database Auto-Initialization
- SQLite database auto-creates on first run
- Tables created with proper foreign key relationships
- Data directory automatically generated
- No manual database setup required

---

## 📁 Project Structure

```
MentorAI-backend/
├── app.py                      # Flask application & API endpoints
├── database.py                 # Database operations layer
├── gemini_service.py           # Gemini API service wrapper
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── data/                       # SQLite database (auto-generated)
│   └── mentorai.db
├── tests/
│   └── test_database.py        # Database unit tests
├── test_gemini.py              # Basic Gemini API test
├── test_memory_problem.py      # Demonstrates memory issue
└── test_memory_solution.py     # Demonstrates memory solution
```

---

## 🎯 Hackathon Features Showcased

### ✅ Implemented
- **Conversation Persistence** - Full chat history with context
- **Session Management** - Multi-session support per user
- **RESTful API** - Professional backend architecture
- **Database Integration** - Proper data persistence with SQLite
- **Testing Suite** - Comprehensive pytest coverage
- **Error Handling** - Graceful error responses
- **CORS Support** - Ready for frontend integration

### 🔄 In Progress
- **Frontend Integration** - Next.js 14 + TypeScript
- **Voice I/O** - Gemini Live API integration
- **Multimodal Support** - Image and PDF processing
- **Advanced Features** - Self-correction, enhanced tutoring modes

---

## 🔐 Security Best Practices

- ✅ Environment variables for API keys
- ✅ `.gitignore` properly configured
- ✅ No sensitive data in repository
- ✅ CORS enabled for controlled access
- ✅ Input validation on API endpoints

---

## 🚢 Deployment

### Railway Deployment
Backend is configured for Railway deployment with automatic CI/CD via GitHub Actions.

**Environment Variables Required:**
- `GOOGLE_GEMINI_KEY`

---

## 🤝 Development Workflow

### Git Best Practices
- Separate branches for features
- Clean commit messages
- Proper .gitignore for Python projects
- Virtual environment excluded from version control

### Testing Before Commit
```bash
pytest tests/  # Run all tests
python app.py  # Verify server starts
```

---

## 📊 Performance Characteristics

- **Context Window**: Leverages Gemini's 1M token capacity
- **Database**: SQLite for simplicity, easily upgradable to PostgreSQL
- **Session Storage**: In-memory chat objects for active sessions
- **API Response Time**: Sub-second for typical queries

---

## 🎓 Learning Resources

### Gemini API Documentation
- [Gemini 3 API Docs](https://ai.google.dev/gemini-api/docs)
- [Chat Sessions Guide](https://ai.google.dev/gemini-api/docs/chat)

### Related Technologies
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pytest Documentation](https://docs.pytest.org/)

---

## 🐛 Known Issues & Future Improvements

### Current Limitations
- Session replay might fail for very long conversations (>1M tokens)
- In-memory chat storage clears on server restart
- No authentication/authorization yet

### Planned Enhancements
- Persistent session caching with Redis
- User authentication with JWT
- Rate limiting for API endpoints
- Conversation export functionality
- Voice interaction with Live API
- Advanced multimodal features

---

## 📝 License

Built for the Gemini 3 Hackathon - February 2026

---

**Status**: ✅ Backend Complete | 🔄 Frontend Integration In Progress

**Tech Stack**: Python + Flask + Gemini 3 + SQLite + Pytest
