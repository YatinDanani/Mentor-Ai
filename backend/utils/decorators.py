"""
Decorators for route protection and validation
"""
from functools import wraps
from flask import request, jsonify
from services.auth_service import AuthService

# Initialize auth service
auth = AuthService()

def token_required(f):
    """
    Decorator to protect routes that require authentication
    Validates JWT token from Authorization header
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(user_id, user_email):
            # user_id and user_email are automatically passed
            return jsonify({'message': f'Hello {user_email}'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Token is missing'
            }), 401
        
        # Decode token
        payload = auth.decode_token(token)
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        # Add user_id and user_email to kwargs
        kwargs['user_id'] = payload['user_id']
        kwargs['user_email'] = payload['email']
        
        return f(*args, **kwargs)
    
    return decorated
