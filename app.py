from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import os
import tempfile
import base64
from werkzeug.utils import secure_filename
from database import Database
from gemini_service import GeminiService
from auth import auth, token_required
from whisper_service import WhisperService
from tts_service import TTSService
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'ogg', 'webm', 'm4a'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf'}
MAX_AUDIO_SIZE = 25 * 1024 * 1024  # 25MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = max(MAX_AUDIO_SIZE, MAX_FILE_SIZE)

# Initialize services
db = Database()
gemini = GeminiService()
whisper = WhisperService()
tts = TTSService()

def allowed_audio_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_document_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_DOCUMENT_EXTENSIONS

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'MentorAI is running!'})

@app.route('/auth/register', methods=['POST'])
def register():
    """User registration"""
    data = request.json
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    
    # Validate email
    if not auth.validate_email(email):
        return jsonify({
            'success': False,
            'error': 'Invalid email format'
        }), 400
    
    # Validate password
    valid, msg = auth.validate_password(password)
    if not valid:
        return jsonify({
            'success': False,
            'error': msg
        }), 400
    
    # Check if user already exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        return jsonify({
            'success': False,
            'error': 'Email already registered'
        }), 409
    
    # Hash password and create user
    password_hash = auth.hash_password(password)
    user_id = db.create_user(email, password_hash, name or None)
    
    if user_id is None:
        return jsonify({
            'success': False,
            'error': 'Failed to create user'
        }), 500
    
    # Generate token
    token = auth.generate_token(user_id, email)
    
    return jsonify({
        'success': True,
        'user': {
            'id': user_id,
            'email': email,
            'name': name
        },
        'token': token
    })

@app.route('/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({
            'success': False,
            'error': 'Email and password required'
        }), 400
    
    # Get user
    user = db.get_user_by_email(email)
    if not user:
        return jsonify({
            'success': False,
            'error': 'Invalid credentials'
        }), 401
    
    # Verify password
    if not auth.verify_password(password, user['password_hash']):
        return jsonify({
            'success': False,
            'error': 'Invalid credentials'
        }), 401
    
    # Generate token
    token = auth.generate_token(user['id'], user['email'])
    
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name']
        },
        'token': token
    })

@app.route('/auth/me', methods=['GET'])
@token_required
def get_current_user(user_id, user_email):
    """Get current user info"""
    user = db.get_user_by_id(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name']
        }
    })

@app.route('/auth/logout', methods=['POST'])
@token_required
def logout(user_id, user_email):
    """User logout (client-side token deletion)"""
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@app.route('/session/new', methods=['POST'])
@token_required
def create_session(user_id, user_email):
    """Create a new chat session"""
    data = request.json
    title = data.get('title', 'New Chat')
    
    session_id = str(uuid.uuid4())
    db.create_session(session_id, str(user_id), title)
    
    return jsonify({
        'success': True,
        'session_id': session_id
    })

@app.route('/chat', methods=['POST'])
@token_required
def chat(user_id, user_email):
    """Send message and get AI response"""
    data = request.json
    session_id = data.get('session_id')
    message = data.get('message')
    
    if not session_id or not message:
        return jsonify({
            'success': False,
            'error': 'session_id and message required'
        }), 400
    
    # Check if session exists
    if not db.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    # Get conversation history for context
    history = db.get_session_history(session_id)
    
    # Save user message
    db.add_message(session_id, 'user', message)
    
    # Get AI response
    result = gemini.send_message(session_id, message, history)
    
    if result['success']:
        # Save AI response
        db.add_message(session_id, 'model', result['response'])
        
        return jsonify({
            'success': True,
            'response': result['response']
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@app.route('/history/<session_id>', methods=['GET'])
@token_required
def get_history(user_id, user_email, session_id):
    """Get conversation history"""
    if not db.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    history = db.get_session_history(session_id)
    
    return jsonify({
        'success': True,
        'history': history
    })

@app.route('/sessions', methods=['GET'])
@token_required
def get_sessions(user_id, user_email):
    """Get all sessions for a user"""
    sessions = db.get_all_sessions(str(user_id))
    
    return jsonify({
        'success': True,
        'sessions': sessions
    })

@app.route('/session/<session_id>', methods=['DELETE'])
@token_required
def delete_session(user_id, user_email, session_id):
    """Delete a session"""
    if not db.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    db.delete_session(session_id)
    
    return jsonify({
        'success': True,
        'message': 'Session deleted'
    })

@app.route('/session/<session_id>', methods=['PUT'])
@token_required
def rename_session(user_id, user_email, session_id):
    """Rename a session"""
    data = request.json
    new_title = data.get('title', '').strip()
    
    if not new_title:
        return jsonify({
            'success': False,
            'error': 'Title required'
        }), 400
    
    if not db.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    db.rename_session(session_id, new_title)
    
    return jsonify({
        'success': True,
        'message': 'Session renamed'
    })

@app.route('/chat/voice', methods=['POST'])
@token_required
def chat_voice(user_id, user_email):
    """Send voice message and get AI response"""
    if 'audio' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No audio file provided'
        }), 400
    
    file = request.files['audio']
    session_id = request.form.get('session_id')
    
    if not session_id:
        return jsonify({
            'success': False,
            'error': 'session_id required'
        }), 400
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    if not allowed_audio_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Invalid file type. Allowed: wav, mp3, ogg, webm, m4a'
        }), 400
    
    # Check if session exists
    if not db.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    # Save audio file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Transcribe audio
        whisper_result = whisper.transcribe_audio(filepath)
        
        if not whisper_result['success']:
            return jsonify({
                'success': False,
                'error': f'Transcription failed: {whisper_result.get("error")}'
            }), 500
        
        transcribed_text = whisper_result['text']
        
        # Get conversation history for context
        history = db.get_session_history(session_id)
        
        # Save transcribed message
        db.add_message(session_id, 'user', transcribed_text)
        
        # Get AI response
        gemini_result = gemini.send_message(session_id, transcribed_text, history)
        
        if gemini_result['success']:
            ai_response = gemini_result['response']
            
            # Save AI response
            db.add_message(session_id, 'model', ai_response)
            
            # Synthesize speech from AI response
            tts_result = tts.synthesize_speech(ai_response)
            
            # Save TTS audio to file
            audio_filename = f"tts_{session_id}_{uuid.uuid4().hex[:8]}.mp3"
            audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            
            if tts_result['success']:
                with open(audio_filepath, 'wb') as f:
                    f.write(tts_result['audio_content'])
                audio_url = f"/uploads/{audio_filename}"
            else:
                audio_url = None
            
            return jsonify({
                'success': True,
                'transcription': transcribed_text,
                'response': ai_response,
                'audio_url': audio_url
            })
        else:
            return jsonify({
                'success': False,
                'error': gemini_result['error']
            }), 500
    finally:
        # Clean up uploaded audio file
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/tts/synthesize', methods=['POST'])
@token_required
def synthesize_text_to_speech(user_id, user_email):
    """Synthesize speech from text"""
    data = request.json
    text = data.get('text', '').strip()
    language_code = data.get('language_code', 'en-US')
    
    if not text:
        return jsonify({
            'success': False,
            'error': 'Text is required'
        }), 400
    
    tts_result = tts.synthesize_speech(text, language_code)
    
    if tts_result['success']:
        # Save TTS audio to file
        audio_filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        
        with open(audio_filepath, 'wb') as f:
            f.write(tts_result['audio_content'])
        
        audio_url = f"/uploads/{audio_filename}"
        
        return jsonify({
            'success': True,
            'audio_url': audio_url
        })
    else:
        return jsonify({
            'success': False,
            'error': tts_result['error']
        }), 500

@app.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    """Serve uploaded files"""
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
@token_required
def upload_file(user_id, user_email):
    """Upload file (image or PDF) and analyze with AI"""
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file provided'
        }), 400
    
    file = request.files['file']
    session_id = request.form.get('session_id')
    
    if not session_id:
        return jsonify({
            'success': False,
            'error': 'session_id required'
        }), 400
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    # Determine file type
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # Validate file type
    file_type = None
    if file_ext in ALLOWED_IMAGE_EXTENSIONS:
        file_type = 'image'
    elif file_ext in ALLOWED_DOCUMENT_EXTENSIONS:
        file_type = 'document'
    else:
        return jsonify({
            'success': False,
            'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp, pdf'
        }), 400
    
    # Check if session exists
    if not db.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    # Save file
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)
    
    try:
        # Analyze file with AI
        analysis_result = analyze_file(filepath, file_type)
        
        # Save file metadata to database
        db.add_file(session_id, filepath, file_type, filename)
        
        return jsonify({
            'success': True,
            'file_type': file_type,
            'analysis': analysis_result
        })
    except Exception as e:
        # Clean up file on error
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({
            'success': False,
            'error': f'File analysis failed: {str(e)}'
        }), 500

def analyze_file(file_path, file_type):
    """Analyze file (image or PDF) with AI"""
    if file_type == 'image':
        # Read and analyze image
        with Image.open(file_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()
            
            # Encode to base64
            base64_image = base64.b64encode(img_bytes).decode('utf-8')
            
            # Send to Gemini for image analysis
            prompt = "Analyze this image and describe what you see in detail."
            result = gemini.client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            )
            
            return {
                'type': 'image_analysis',
                'description': result.text
            }
    
    elif file_type == 'document':
        # For PDF, extract text and analyze
        # For now, we'll do basic text extraction
        # In production, use PyPDF2 or similar
        prompt = "I've attached a PDF document. Please analyze it and provide a summary."
        
        result = gemini.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        
        return {
            'type': 'document_analysis',
            'description': 'Document attached. Ask me specific questions about its content.'
        }
    
    return {'type': 'unknown', 'description': 'Unable to analyze file.'}

@app.route('/files/<session_id>', methods=['GET'])
@token_required
def get_files(user_id, user_email, session_id):
    """Get all files for a session"""
    if not db.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    files = db.get_session_files(session_id)
    
    return jsonify({
        'success': True,
        'files': files
    })

@app.route('/files/<file_id>', methods=['DELETE'])
@token_required
def delete_file(user_id, user_email, file_id):
    """Delete a file"""
    try:
        db.delete_file(file_id)
        return jsonify({
            'success': True,
            'message': 'File deleted'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("MentorAI Backend Starting...")
    print("="*50)
    app.run(debug=True, port=5000)