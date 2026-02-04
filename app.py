from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from database import Database
from gemini_service import GeminiService
from auth import auth, token_required

app = Flask(__name__)
CORS(app)

# Initialize services
db = Database()
gemini = GeminiService()

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

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎓 MentorAI Backend Starting...")
    print("="*50)
    app.run(debug=True, port=5000)