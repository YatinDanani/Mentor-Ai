"""
File Routes
Handles image and PDF upload/analysis
"""
from flask import Blueprint, request, jsonify, send_from_directory, current_app
import os
import uuid
from werkzeug.utils import secure_filename
from services.database_service import DatabaseService
from services.file_service import FileService
from utils.decorators import token_required
from config.settings import Config

file_bp = Blueprint('files', __name__)

# Initialize services
db = DatabaseService()
file_service = FileService()

@file_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(user_id, user_email):
    """
    Upload and analyze a file (image or PDF)
    
    Form data:
        file: file (required)
        session_id: string (required)
    
    Returns:
        success: boolean
        file_type: string ('image' or 'document')
        analysis: object (AI analysis result)
        file_id: integer
    """
    try:
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
        
        # Check if session exists
        if not db.session_exists(session_id):
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Validate and save file
        result = file_service.save_and_analyze_file(file, session_id)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify({
            'success': True,
            'file_type': result['file_type'],
            'analysis': result['analysis'],
            'file_id': result['file_id']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@file_bp.route('/<session_id>', methods=['GET'])
@token_required
def get_files(user_id, user_email, session_id):
    """
    Get all files for a session
    
    Parameters:
        session_id: string (in URL)
    
    Returns:
        success: boolean
        files: array of file objects
    """
    try:
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
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@file_bp.route('/<int:file_id>', methods=['DELETE'])
@token_required
def delete_file(user_id, user_email, file_id):
    """
    Delete a file
    
    Parameters:
        file_id: integer (in URL)
    
    Returns:
        success: boolean
        message: string
    """
    try:
        db.delete_file(file_id)
        
        return jsonify({
            'success': True,
            'message': 'File deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@file_bp.route('/serve/<filename>', methods=['GET'])
def serve_file(filename):
    """
    Serve uploaded files
    Public endpoint for file access
    
    Parameters:
        filename: string (in URL)
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
