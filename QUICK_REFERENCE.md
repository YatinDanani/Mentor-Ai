# MentorAI - Quick Reference Card

## 🚀 Start the App

```bash
# Activate virtual environment
source venv/bin/activate         # macOS/Linux
venv\Scripts\activate           # Windows

# Run the app
python app.py
```

## 🔑 Required Environment Variables

```bash
GOOGLE_GEMINI_KEY=your_key_here
JWT_SECRET=your_secret_here
```

## 📁 File Structure

```
backend/
├── app.py                    # Main entry point
├── config/settings.py        # Configuration
├── routes/                   # API endpoints (Blueprints)
│   ├── auth_routes.py       # /auth/*
│   ├── chat_routes.py       # /chat/*
│   ├── session_routes.py    # /session/*
│   ├── file_routes.py       # /files/*
│   └── voice_routes.py      # /voice/*
├── services/                 # Business logic
│   ├── auth_service.py
│   ├── database_service.py
│   ├── gemini_service.py
│   ├── whisper_service.py
│   ├── tts_service.py
│   └── file_service.py
└── utils/decorators.py      # @token_required
```

## 🛠️ Common Tasks

### Add a New Route

1. Create file: `routes/myfeature_routes.py`
2. Define blueprint:
```python
from flask import Blueprint
myfeature_bp = Blueprint('myfeature', __name__)

@myfeature_bp.route('/endpoint', methods=['POST'])
def my_endpoint():
    return jsonify({'success': True})
```
3. Register in `app.py`:
```python
from routes.myfeature_routes import myfeature_bp
app.register_blueprint(myfeature_bp, url_prefix='/myfeature')
```

### Add a New Service

1. Create file: `services/myservice_service.py`
2. Define class:
```python
class MyService:
    def __init__(self):
        pass
    
    def do_something(self):
        return {'success': True}
```
3. Use in routes:
```python
from services.myservice_service import MyService
service = MyService()
```

### Protect a Route

```python
from utils.decorators import token_required

@myfeature_bp.route('/protected', methods=['GET'])
@token_required
def protected_route(user_id, user_email):
    # user_id and user_email available here
    return jsonify({'user_id': user_id})
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:5000/health

# Register user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# Create session (with token)
curl -X POST http://localhost:5000/session/new \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"Test Chat"}'

# Send message
curl -X POST http://localhost:5000/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"session_id":"SESSION_ID","message":"Hello!"}'
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| "Token is missing" | Add `Authorization: Bearer TOKEN` header |
| "Session not found" | Create session first with `/session/new` |
| Port 5000 in use | Change port in `app.py` or kill process |
| Voice not working | Set `VOICE_ENABLED=True` and add API keys |

## 📊 Feature Status

Check what's enabled:
```bash
curl http://localhost:5000/health
curl http://localhost:5000/voice/status
```

## 🔧 Configuration

Edit `config/settings.py` or `.env`:

```python
# Feature flags
VOICE_ENABLED = True/False
FILE_UPLOAD_ENABLED = True/False

# Limits
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB
TOKEN_EXPIRATION_HOURS = 24

# Database
DATABASE_PATH = 'data/mentorai.db'
```

## 📝 API Response Format

### Success Response
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message here"
}
```

## 🎯 Key Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check |
| `/auth/register` | POST | No | Register user |
| `/auth/login` | POST | No | Login |
| `/auth/me` | GET | Yes | Get user info |
| `/session/new` | POST | Yes | Create session |
| `/session/list` | GET | Yes | List sessions |
| `/chat/` | POST | Yes | Send message |
| `/chat/history/<id>` | GET | Yes | Get history |
| `/files/upload` | POST | Yes | Upload file |
| `/voice/chat` | POST | Yes | Voice chat |
| `/voice/status` | GET | No | Check voice status |

## 💡 Tips

1. **Always activate venv before running**
2. **Keep .env file secure** (never commit it!)
3. **Use DEBUG=False in production**
4. **Check logs** if something breaks
5. **Test with curl** before connecting frontend

---

**For detailed setup:** See `SETUP_GUIDE.md`
**For architecture:** See `RESTRUCTURING_EXPLAINED.md`
**For project overview:** See `PROJECT_OVERVIEW.md`
