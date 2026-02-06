# Complete MentorAI Setup - Backend + Frontend

This guide covers setting up both the backend (Flask) and frontend (Next.js).

## Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- [Google Gemini API Key](https://aistudio.google.com/apikey)

---

## Part 1: Backend Setup (5 minutes)

### Step 1: Setup Backend

```bash
# Navigate to backend
cd mentor-ai-restructured/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### Step 2: Add API Keys

Edit `.env` and add:
```
GOOGLE_GEMINI_KEY=your_gemini_api_key_here
JWT_SECRET=some_random_secret_string
```

### Step 3: Start Backend

```bash
python app.py
```

You should see:
```
 MentorAI Backend Starting...
 * Running on http://0.0.0.0:5000
```

**✅ Backend is ready!**

---

## Part 2: Frontend Setup (5 minutes)

### Step 1: Setup Frontend

Open a **NEW terminal** (keep backend running):

```bash
# Navigate to frontend
cd mentor-ai-restructured/frontend

# Install dependencies
npm install
```

### Step 2: Configure Environment

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXTAUTH_SECRET=same_secret_as_backend
NEXTAUTH_URL=http://localhost:3000
```

### Step 3: Start Frontend

```bash
npm run dev
```

You should see:
```
- ready started server on 0.0.0.0:3000
- Local: http://localhost:3000
```

**✅ Frontend is ready!**

---

## Part 3: Test the Application

### Open Your Browser

Go to: **http://localhost:3000**

You should see the MentorAI landing page!

### Test the Flow

1. **Register** a new account
   - Email: sahil@test.com
   - Password: password123
   - Name: Sahil

2. **Login** with your credentials

3. **Create a new chat session**

4. **Send a message** to the AI
   - Try: "Explain binary search in simple terms"

5. **Test file upload** (optional)
   - Upload an image and ask about it

---

## Running Both Services

You need **TWO terminals**:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## Quick Reference

| Service | URL | Port |
|---------|-----|------|
| Backend API | http://localhost:5000 | 5000 |
| Frontend | http://localhost:3000 | 3000 |
| API Health | http://localhost:5000/health | - |

---

## Architecture

```
┌─────────────────────┐
│  Browser (You)      │
│  localhost:3000     │
└──────────┬──────────┘
           │
           │ HTTP Requests
           ▼
┌─────────────────────┐
│  Next.js Frontend   │
│  (React/TypeScript) │
│  Port: 3000         │
└──────────┬──────────┘
           │
           │ API Calls
           ▼
┌─────────────────────┐
│  Flask Backend      │
│  (Python)           │
│  Port: 5000         │
└──────────┬──────────┘
           │
           ├──► Gemini API (AI)
           ├──► SQLite (Database)
           └──► File Storage
```

---

## Troubleshooting

### "Cannot connect to backend"

**Problem:** Frontend can't reach backend

**Solution:**
1. Make sure backend is running: `curl http://localhost:5000/health`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Check no firewall blocking port 5000

### "CORS Error"

**Problem:** Cross-Origin Request Blocked

**Solution:**
Backend already has CORS enabled. Make sure:
- Backend is running
- You're accessing frontend via `localhost:3000` (not `127.0.0.1`)

### "Module not found" (Backend)

**Problem:** Python dependencies missing

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Dependencies not found" (Frontend)

**Problem:** npm packages missing

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Ports Already in Use

**Backend (5000):**
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Frontend (3000):**
```bash
# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Or run on different port
npm run dev -- -p 3001
```

---

## Development Workflow

### Starting Fresh Each Day

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Making Changes

**Backend Changes:**
- Flask auto-reloads on code changes
- Just save your file and test

**Frontend Changes:**
- Next.js auto-reloads with Hot Module Replacement
- Changes appear instantly in browser

---

## Production Deployment

### Backend (Railway/Heroku)

See `backend/SETUP_GUIDE.md` for deployment instructions.

### Frontend (Vercel/Netlify)

```bash
cd frontend
npm run build
```

Then deploy to Vercel/Netlify with:
- Build command: `npm run build`
- Output directory: `.next`
- Environment variables from `.env.local`

---

## Next Steps

1. ✅ Both services running
2. ✅ Can login and chat
3. 📝 Read the code in `backend/routes/` and `frontend/components/`
4. 🎨 Customize the UI in `frontend/app/`
5. 🚀 Add new features

---

## Additional Documentation

- **Backend Details:** `backend/SETUP_GUIDE.md`
- **Frontend Details:** `frontend/FRONTEND_SETUP.md`
- **API Reference:** `QUICK_REFERENCE.md`
- **Architecture:** `RESTRUCTURING_EXPLAINED.md`

---

**You're all set! Happy coding! 🚀**
