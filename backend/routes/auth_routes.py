"""
Authentication Routes
Handles user registration, login, and token management
"""
from flask import Blueprint, request, jsonify
from services.database_service import DatabaseService
from services.auth_service import AuthService
from utils.decorators import token_required

auth_bp = Blueprint('auth', __name__)

# Initialize services
db = DatabaseService()
auth = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint
    
    Request body:
        email: string (required)
        password: string (required)
        name: string (optional)
    
    Returns:
        success: boolean
        user: object (id, email, name)
        token: string (JWT token)
    """
    try:
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
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Request body:
        email: string (required)
        password: string (required)
    
    Returns:
        success: boolean
        user: object (id, email, name)
        token: string (JWT token)
    """
    try:
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
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id, user_email):
    """
    Get current user information
    Requires valid JWT token in Authorization header
    
    Returns:
        success: boolean
        user: object (id, email, name)
    """
    try:
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
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(user_id, user_email):
    """
    User logout (client-side token deletion)
    Token is invalidated on client side
    
    Returns:
        success: boolean
        message: string
    """
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })
