"""
MentorAI - Main Application Entry Point
Restructured to use Flask Blueprints for better organization
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os
from pathlib import Path

# Import configuration
from config.settings import Config

# Import blueprints (each feature is a separate module)
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from routes.session_routes import session_bp
from routes.file_routes import file_bp
from routes.voice_routes import voice_bp

def create_app(config=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    if config:
        app.config.update(config)
    
    # Enable CORS
    CORS(app)
    
    # Ensure required directories exist
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path('data').mkdir(parents=True, exist_ok=True)
    
    # Register blueprints (feature modules)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(session_bp, url_prefix='/session')
    app.register_blueprint(file_bp, url_prefix='/files')
    app.register_blueprint(voice_bp, url_prefix='/voice')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'MentorAI is running!',
            'features': {
                'text_chat': True,
                'voice_chat': app.config.get('VOICE_ENABLED', False),
                'file_upload': app.config.get('FILE_UPLOAD_ENABLED', True)
            }
        })
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" MentorAI Backend Starting...")
    print(" Restructured with Modular Architecture")
    print("="*60)
    print(f" Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f" Database: {app.config.get('DATABASE_PATH', 'data/mentorai.db')}")
    print(f" Debug mode: {app.config.get('DEBUG', False)}")
    print("="*60 + "\n")
    
    app.run(
        debug=app.config.get('DEBUG', True),
        host='0.0.0.0',
        port=5000
    )
