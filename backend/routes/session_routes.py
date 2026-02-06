"""
Session Routes
Handles chat session management (create, list, delete, rename)
"""
from flask import Blueprint, request, jsonify
import uuid
from services.database_service import DatabaseService
from utils.decorators import token_required

session_bp = Blueprint('session', __name__)

# Initialize service
db = DatabaseService()

@session_bp.route('/new', methods=['POST'])
@token_required
def create_session(user_id, user_email):
    """
    Create a new chat session
    
    Request body:
        title: string (optional, default: "New Chat")
    
    Returns:
        success: boolean
        session_id: string (UUID)
    """
    try:
        data = request.json or {}
        title = data.get('title', 'New Chat')
        
        session_id = str(uuid.uuid4())
        db.create_session(session_id, str(user_id), title)
        
        return jsonify({
            'success': True,
            'session_id': session_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@session_bp.route('/list', methods=['GET'])
@token_required
def get_sessions(user_id, user_email):
    """
    Get all sessions for the current user
    
    Returns:
        success: boolean
        sessions: array of session objects
    """
    try:
        sessions = db.get_all_sessions(str(user_id))
        
        return jsonify({
            'success': True,
            'sessions': sessions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@session_bp.route('/<session_id>', methods=['DELETE'])
@token_required
def delete_session(user_id, user_email, session_id):
    """
    Delete a chat session and all its messages
    
    Parameters:
        session_id: string (in URL)
    
    Returns:
        success: boolean
        message: string
    """
    try:
        if not db.session_exists(session_id):
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        db.delete_session(session_id)
        
        return jsonify({
            'success': True,
            'message': 'Session deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@session_bp.route('/<session_id>/rename', methods=['PUT'])
@token_required
def rename_session(user_id, user_email, session_id):
    """
    Rename a chat session
    
    Parameters:
        session_id: string (in URL)
    
    Request body:
        title: string (required)
    
    Returns:
        success: boolean
        message: string
    """
    try:
        data = request.json
        new_title = data.get('title')
        
        if not new_title:
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        if not db.session_exists(session_id):
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        db.rename_session(session_id, new_title)
        
        return jsonify({
            'success': True,
            'message': 'Session renamed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
