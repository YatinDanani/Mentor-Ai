# MentorAI API Documentation

## Base URL

Development: `http://localhost:5000`
Production: `https://your-backend.railway.app`

## Authentication

All protected endpoints require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

---

## Authentication Endpoints

### Register User

**Endpoint:** `POST /auth/register`

**Description:** Register a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid input or user already exists
- `500 Internal Server Error` - Server error

---

### Login User

**Endpoint:** `POST /auth/login`

**Description:** Authenticate user and receive JWT token

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials
- `500 Internal Server Error` - Server error

---

### Get Current User

**Endpoint:** `GET /auth/me`

**Authentication:** Required

**Description:** Get information about the currently authenticated user

**Response (200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Errors:**
- `401 Unauthorized` - Invalid or missing token
- `500 Internal Server Error` - Server error

---

### Logout User

**Endpoint:** `POST /auth/logout`

**Authentication:** Required

**Description:** Logout the current user (client-side token removal)

**Response (200):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

## Session Management Endpoints

### Create New Session

**Endpoint:** `POST /session/new`

**Authentication:** Required

**Description:** Create a new chat session

**Request Body:**
```json
{
  "title": "Learning Python"
}
```

**Response (201):**
```json
{
  "success": true,
  "session": {
    "id": "session_abc123",
    "user_id": 1,
    "title": "Learning Python",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### List All Sessions

**Endpoint:** `GET /sessions`

**Authentication:** Required

**Description:** Get all chat sessions for the authenticated user

**Response (200):**
```json
{
  "success": true,
  "sessions": [
    {
      "id": "session_abc123",
      "title": "Learning Python",
      "created_at": "2024-01-15T10:30:00Z",
      "message_count": 15
    },
    {
      "id": "session_def456",
      "title": "Data Science Basics",
      "created_at": "2024-01-14T08:20:00Z",
      "message_count": 8
    }
  ]
}
```

---

### Get Session History

**Endpoint:** `GET /history/<session_id>`

**Authentication:** Required

**Description:** Retrieve full conversation history for a session

**Response (200):**
```json
{
  "success": true,
  "session_id": "session_abc123",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "What is Python?",
      "timestamp": "2024-01-15T10:30:05Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Python is a high-level programming language...",
      "timestamp": "2024-01-15T10:30:07Z"
    }
  ]
}
```

---

## Chat Endpoints

### Send Text Message

**Endpoint:** `POST /chat`

**Authentication:** Required

**Description:** Send a text message and receive AI response

**Request Body:**
```json
{
  "session_id": "session_abc123",
  "message": "Explain how lists work in Python"
}
```

**Response (200):**
```json
{
  "success": true,
  "response": "In Python, lists are mutable sequences...",
  "message_id": 42
}
```

---

### Send Voice Message

**Endpoint:** `POST /chat/voice`

**Authentication:** Required

**Content-Type:** `multipart/form-data`

**Description:** Send a voice message and receive AI response (text + audio)

**Request:**
```
session_id: session_abc123
audio: (audio file, MP3/WAV/WEBM)
```

**Response (200):**
```json
{
  "success": true,
  "transcript": "Explain how lists work in Python",
  "response": "In Python, lists are mutable sequences...",
  "audio_url": "/tts/audio/response_abc123.mp3",
  "message_id": 42
}
```

---

## Text-to-Speech Endpoint

### Synthesize Speech

**Endpoint:** `POST /tts/synthesize`

**Authentication:** Required

**Description:** Convert text to speech using Google Cloud TTS

**Request Body:**
```json
{
  "text": "Hello, this is a test message",
  "language_code": "en-US"
}
```

**Response (200):**
```json
{
  "success": true,
  "audio_url": "/tts/audio/synthesis_xyz789.mp3",
  "duration": 2.5
}
```

---

## File Upload Endpoint

### Upload File

**Endpoint:** `POST /upload`

**Authentication:** Required

**Content-Type:** `multipart/form-data`

**Description:** Upload an image or PDF for AI analysis

**Request:**
```
file: (image or PDF file)
session_id: session_abc123 (optional)
```

**Response (200):**
```json
{
  "success": true,
  "file_id": "file_def456",
  "filename": "document.pdf",
  "file_type": "application/pdf",
  "analysis": "This document contains information about..."
}
```

**Supported Formats:**
- Images: PNG, JPG, JPEG, GIF, WEBP
- Documents: PDF

**Error (400):**
```json
{
  "success": false,
  "message": "Invalid file type. Only images and PDFs are allowed."
}
```

---

## Health Check

### Health Status

**Endpoint:** `GET /health`

**Description:** Check API health status

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Rate Limiting

- Authentication endpoints: 10 requests per minute
- Chat endpoints: 30 requests per minute
- File upload: 5 requests per minute

---

## WebSocket Support (Coming Soon)

Real-time chat updates via WebSocket will be available in future updates.

---

For more information or to report issues, please visit our GitHub repository.
