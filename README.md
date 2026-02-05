# MentorAI - Step-by-Step Guide

## Getting Started

### Step 1: Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mentorai
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Configuration

1. **Create `.env` file** in the root directory with:
   ```
   GOOGLE_GEMINI_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   JWT_SECRET=your_jwt_secret
   DATABASE_URL=sqlite:///data/mentorai.db
   ```

2. **Create `.gitignore`** to protect sensitive data:
   ```
   .env
   data/mentorai.db
   __pycache__/
   venv/
   ```

3. **Initialize the database** (auto-created on first run)
   ```bash
   mkdir -p data
   ```

### Step 3: Backend Setup

1. **Run backend tests** to verify setup:
   ```bash
   pytest tests/
   ```

2. **Start the Flask server**:
   ```bash
   python app.py
   ```

3. **Verify backend health**:
   - Navigate to `http://localhost:5000/health`
   - Should return health status

### Step 4: Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   ```

3. **Configure frontend environment**:
   - Create `.env.local` file:
     ```
     NEXT_PUBLIC_API_URL=http://localhost:5000
     NEXTAUTH_SECRET=your_nextauth_secret
     NEXTAUTH_URL=http://localhost:3000
     ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

5. **Access the application**:
   - Open `http://localhost:3000` in your browser

### Step 5: Testing the Application

1. **Register a new user**:
   - Go to registration page
   - Create account with email/password

2. **Login**:
   - Use credentials to login
   - JWT token generated (24-hour expiration)

3. **Create a chat session**:
   - Click "New Session"
   - Session created in database

4. **Send a message**:
   - Type message and send
   - Gemini AI responds with context memory

5. **Test voice features** (optional):
   - Upload voice message (MP3/WAV)
   - Whisper transcribes to text
   - Gemini responds, TTS synthesizes speech

6. **Test multimodal features** (optional):
   - Upload image for analysis
   - Upload PDF for text extraction

---

## Development Workflow

### Step 6: Making Changes

1. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make code changes**:
   - Backend: Edit Python files in root
   - Frontend: Edit files in `frontend/`

3. **Run tests**:
   ```bash
   # Backend tests
   pytest tests/
   
   # Frontend tests
   cd frontend
   npm test
   npm run test:coverage
   ```

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

5. **Merge to main**:
   - Create pull request on GitHub
   - Review and merge
   - CI/CD pipeline runs automatically

---

## Deployment

### Step 7: Railway Deployment

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize Railway project**:
   ```bash
   railway init
   ```

4. **Deploy backend service**:
   ```bash
   railway up --service=backend
   ```

5. **Deploy frontend service**:
   ```bash
   railway up --service=frontend
   ```

6. **Configure environment variables in Railway dashboard**:
   
   **Backend**:
   - `GOOGLE_GEMINI_KEY` - Your Google Gemini API key
   - `OPENAI_API_KEY` - Your OpenAI API key for Whisper
   - `JWT_SECRET` - Your JWT secret token
   - `DATABASE_URL` - SQLite database path (default: `sqlite:///data/mentorai.db`)
   
   **Frontend**:
   - `NEXT_PUBLIC_API_URL` - Backend URL (e.g., `https://your-backend.railway.app`)
   - `NEXTAUTH_SECRET` - Your NextAuth secret
   - `NEXTAUTH_URL` - Frontend URL (e.g., `https://your-frontend.railway.app`)

### Step 8: CI/CD Setup

1. **Add Railway token to GitHub**:
   - Go to GitHub repository → Settings → Secrets
   - Add `RAILWAY_TOKEN`

2. **Push to main branch**:
   ```bash
   git push origin main
   ```

3. **CI/CD automatically**:
   - ✅ Runs pytest tests
   - ✅ Runs jest tests
   - ✅ Runs linting checks
   - ✅ Deploys to Railway

---

## Hackathon Submission

### Step 9: Documentation

1. ✅ Complete API documentation (`API.md`)
2. ✅ Write demo script (`DEMO.md`)
3. ✅ Create presentation outline (`PRESENTATION.md`)
4. ✅ Document theme customization (`frontend/THEME.md`)
5. ✅ Update frontend setup guide (`frontend/SETUP.md`)

### Step 10: Demo Preparation

1. **Prepare test accounts**:
   - Create demo user account
   - Pre-populate sample conversations

2. **Test all features**:
   - ✅ User registration/login
   - ✅ Chat with context memory
   - ✅ Voice input/output
   - ✅ Image analysis
   - ✅ PDF processing

3. **Record demo video**:
   - Follow script in `DEMO.md`
   - Showcase all Gemini 3 features

### Step 11: Final Submission (Deadline: Feb 9, 2026)

1. **Verify deployment**:
   - Backend URL working
   - Frontend URL working
   - All features functional

2. **Submit to Devpost**:
   - Project description
   - Demo video/screenshots
   - GitHub repository link
   - Live deployment link

3. **Final checklist**:
   - ✅ Code tested and working
   - ✅ Documentation complete
   - ✅ Deployed and accessible
   - ✅ Demo prepared
   - ✅ Submission submitted

---

## Quick Reference

### API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/health` | GET | Health check | No |
| `/auth/register` | POST | User registration | No |
| `/auth/login` | POST | User login | No |
| `/auth/me` | GET | Get current user | Yes |
| `/auth/logout` | POST | User logout | Yes |
| `/session/new` | POST | Create new chat session | Yes |
| `/chat` | POST | Send message and get AI response | Yes |
| `/chat/voice` | POST | Send voice message | Yes |
| `/tts/synthesize` | POST | Synthesize speech from text | Yes |
| `/upload` | POST | Upload file for analysis | Yes |
| `/history/<session_id>` | GET | Retrieve conversation history | Yes |
| `/sessions` | GET | List all user sessions | Yes |

### Project Structure

```
mentorai/
├── app.py                    # Flask application & routes
├── auth.py                   # Authentication handlers
├── database.py               # SQLite operations
├── gemini_service.py         # Gemini API wrapper
├── whisper_service.py        # OpenAI Whisper service
├── tts_service.py            # Gemini TTS service
├── requirements.txt          # Dependencies
├── .env                      # API keys (not in repo)
├── .gitignore               # Git exclusions
├── railway.json             # Railway backend config
├── railway.toml             # Railway multi-service config
├── Procfile                 # Backend process definition
├── tests/
│   └── test_database.py     # Database unit tests
├── data/
│   └── mentorai.db          # SQLite database (auto-created)
└── frontend/                # Next.js application
    ├── app/                 # Next.js app directory
    ├── components/          # React components
    ├── lib/                 # Utilities and API client
    ├── types/               # TypeScript types
    ├── package.json         # Frontend dependencies
    └── next.config.js       # Next.js configuration
```

### Development Timeline

- ✅ Week 1: API integration, database, testing
- ✅ Week 2: Auth system, Next.js frontend, dark theme
- ✅ Week 3: Voice features, multimodal capabilities
- ✅ Week 4: Testing, QA, deployment setup (Railway + CI/CD)
- ✅ Week 5: Documentation (API, Setup, Theme), demo prep, presentation

---

**Ready to impress the judges! 🚀**

**Built with ❤️ by Yatin for the Gemini 3 Hackathon**
