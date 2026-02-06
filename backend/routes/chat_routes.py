"""
Chat Routes
Handles text-based chat with Gemini AI
"""
from flask import Blueprint, request, jsonify
from services.database_service import DatabaseService
from services.gemini_service import GeminiService
from utils.decorators import token_required

chat_bp = Blueprint('chat', __name__)

# Initialize services
db = DatabaseService()
gemini = GeminiService()

@chat_bp.route('/', methods=['POST'])
@token_required
def send_message(user_id, user_email):
    """
    Send a message and get AI response
    
    Request body:
        session_id: string (required)
        message: string (required)
    
    Returns:
        success: boolean
        response: string (AI response)
    """
    try:
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
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/history/<session_id>', methods=['GET'])
@token_required
def get_history(user_id, user_email, session_id):
    """
    Get conversation history for a session
    
    Parameters:
        session_id: string (in URL)
    
    Returns:
        success: boolean
        history: array of messages
    """
    try:
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
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
