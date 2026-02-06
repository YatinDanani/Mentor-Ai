# MentorAI - Complete Setup Guide

This guide will help you set up and run MentorAI locally on your machine.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (Text Chat Only)](#quick-start-text-chat-only)
3. [Full Setup (All Features)](#full-setup-all-features)
4. [Running the Application](#running-the-application)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.8+**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **pip** (Python package manager)
   ```bash
   pip --version
   ```

3. **Git** (for cloning the repository)
   ```bash
   git --version
   ```

### Required API Keys

**Minimum (for text chat):**
- Google Gemini API Key - [Get it here](https://aistudio.google.com/apikey)

**Optional (for voice features):**
- OpenAI API Key - [Get it here](https://platform.openai.com/api-keys)
- Google Cloud credentials - [Setup guide](https://cloud.google.com/text-to-speech/docs/before-you-begin)

---

## Quick Start (Text Chat Only)

This gets you up and running with basic text chat in ~5 minutes.

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd mentor-ai-restructured/backend
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages. It might take 2-3 minutes.

### Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in a text editor and add your Gemini API key:
   ```
   GOOGLE_GEMINI_KEY=your_actual_api_key_here
   JWT_SECRET=my_secret_key_12345
   ```

### Step 5: Run the Application

```bash
python app.py
```

You should see:
```
==============================================================
 MentorAI Backend Starting...
 Restructured with Modular Architecture
==============================================================
 Upload folder: uploads
 Database: data/mentorai.db
 Debug mode: True
==============================================================

 Database initialized 
 * Running on http://0.0.0.0:5000
```

### Step 6: Test the API

Open a new terminal and run:

```bash
# Health check
curl http://localhost:5000/health
```

You should get:
```json
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

**Congratulations! 🎉 You have MentorAI running with text chat.**

---

## Full Setup (All Features)

To enable voice features, follow these additional steps:

### Step 1: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy the key

### Step 2: Get Google Cloud TTS Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Text-to-Speech API
4. Create a service account:
   - Go to IAM & Admin → Service Accounts
   - Click "Create Service Account"
   - Give it a name (e.g., "mentorai-tts")
   - Grant it "Cloud Text-to-Speech User" role
5. Create a JSON key:
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key" → JSON
   - Save the downloaded JSON file to a safe location

### Step 3: Update Environment Variables

Open `.env` and add:

```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
VOICE_ENABLED=True
```

### Step 4: Restart the Application

```bash
# Stop the current app (Ctrl+C)
# Start it again
python app.py
```

### Step 5: Verify Voice Features

```bash
curl http://localhost:5000/voice/status
```

You should see:
```json
{
  "whisper_available": true,
  "tts_available": true
}
```

---

## Running the Application

### Development Mode

```bash
# With virtual environment activated
python app.py
```

The server will run on `http://localhost:5000` with debug mode enabled.

### Production Mode

1. Update `.env`:
   ```
   DEBUG=False
   ```

2. Use a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

---

## Testing

### Manual API Testing

You can test endpoints using curl or tools like Postman.

#### 1. Register a User

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'
```

Response:
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "test@example.com",
    "name": "Test User"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Save the token for next requests!

#### 2. Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### 3. Create a Session

```bash
curl -X POST http://localhost:5000/session/new \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title": "My First Chat"}'
```

Response:
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 4. Send a Message

```bash
curl -X POST http://localhost:5000/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "Hello! Can you help me learn Python?"
  }'
```

Response:
```json
{
  "success": true,
  "response": "Of course! I'd be happy to help you learn Python..."
}
```

### Automated Testing

```bash
# Install pytest if not already installed
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage report
pytest tests/ --cov=. --cov-report=html
```

---

## Troubleshooting

### Common Issues

#### 1. "GOOGLE_GEMINI_KEY not found"

**Solution:**
- Make sure you created a `.env` file (not `.env.example`)
- Check that your API key is correctly pasted
- Restart the application

#### 2. "ModuleNotFoundError"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. "Address already in use" (Port 5000)

**Solution:**
```bash
# Find and kill the process using port 5000
# On macOS/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Or run on a different port:
```python
# In app.py, change:
app.run(debug=True, port=5001)  # Use port 5001 instead
```

#### 4. Voice features not working

**Symptoms:**
- "Voice features not enabled" error
- `whisper_available: false` or `tts_available: false`

**Solution:**
1. Check if API keys are set in `.env`:
   ```bash
   cat .env | grep OPENAI_API_KEY
   cat .env | grep GOOGLE_APPLICATION_CREDENTIALS
   ```

2. Verify Google credentials file exists:
   ```bash
   ls /path/to/your/google-credentials.json
   ```

3. Set `VOICE_ENABLED=True` in `.env`

4. Restart the application

#### 5. Database errors

**Solution:**
```bash
# Delete existing database and restart
rm -rf data/
python app.py  # Will create fresh database
```

#### 6. Import errors

**Problem:**
```
ImportError: cannot import name 'DatabaseService'
```

**Solution:**
Make sure you're in the `backend` directory:
```bash
pwd  # Should show .../mentor-ai-restructured/backend
python app.py
```

---

## Project Structure

```
backend/
├── app.py                      # Main application entry point
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration management
├── routes/                     # Feature-based route blueprints
│   ├── auth_routes.py         # Authentication endpoints
│   ├── chat_routes.py         # Text chat endpoints
│   ├── session_routes.py      # Session management
│   ├── file_routes.py         # File upload/analysis
│   └── voice_routes.py        # Voice chat endpoints
├── services/                   # Business logic & external APIs
│   ├── auth_service.py        # JWT & password handling
│   ├── database_service.py    # SQLite operations
│   ├── gemini_service.py      # Gemini API integration
│   ├── whisper_service.py     # Speech-to-text
│   ├── tts_service.py         # Text-to-speech
│   └── file_service.py        # File processing
├── utils/
│   └── decorators.py          # Route decorators
├── tests/                      # Unit tests
├── data/                       # SQLite database (auto-created)
├── uploads/                    # User uploads (auto-created)
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (create this!)
```

---

## API Endpoints Reference

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user (requires token)
- `POST /auth/logout` - Logout

### Sessions
- `POST /session/new` - Create new chat session
- `GET /session/list` - List all user sessions
- `DELETE /session/<id>` - Delete session
- `PUT /session/<id>/rename` - Rename session

### Chat
- `POST /chat/` - Send message and get AI response
- `GET /chat/history/<session_id>` - Get conversation history

### Files
- `POST /files/upload` - Upload image/PDF
- `GET /files/<session_id>` - Get files for session
- `DELETE /files/<file_id>` - Delete file
- `GET /files/serve/<filename>` - Serve uploaded file

### Voice (Optional)
- `POST /voice/chat` - Voice input/output
- `POST /voice/tts` - Text-to-speech only
- `GET /voice/status` - Check voice features availability

### Health
- `GET /health` - Health check

---

## Next Steps

1. **Frontend Setup**: Follow the frontend setup guide to connect the UI
2. **Deploy**: Deploy to Railway, Heroku, or your preferred platform
3. **Customize**: Modify prompts, add features, or change the UI
4. **Contribute**: Submit PRs to improve the project

---

## Need Help?

- Check the [Troubleshooting](#troubleshooting) section
- Review the [API Documentation](API.md)
- Open an issue on GitHub

---

**Happy coding! 🚀**
