from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from database import Database
from gemini_service import GeminiService

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# Initialize services
db = Database()
gemini = GeminiService()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'MentorAI is running!'})

@app.route('/session/new', methods=['POST'])
def create_session():
    """Create a new chat session"""
    data = request.json
    user_id = data.get('user_id', 'default_user')
    title = data.get('title', 'New Chat')
    
    session_id = str(uuid.uuid4())
    db.create_session(session_id, user_id, title)
    
    return jsonify({
        'success': True,
        'session_id': session_id
    })

@app.route('/chat', methods=['POST'])
def chat():
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
def get_history(session_id):
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
def get_sessions():
    """Get all sessions for a user"""
    user_id = request.args.get('user_id', 'default_user')
    sessions = db.get_all_sessions(user_id)
    
    return jsonify({
        'success': True,
        'sessions': sessions
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎓 MentorAI Backend Starting...")
    print("="*50)
    app.run(debug=True, port=5000)