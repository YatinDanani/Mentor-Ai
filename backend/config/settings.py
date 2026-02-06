"""
Configuration Settings for MentorAI
Centralized configuration management
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB max upload
    
    ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'ogg', 'webm', 'm4a'}
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf'}
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/mentorai.db')
    
    # API Keys (required)
    GOOGLE_GEMINI_KEY = os.getenv('GOOGLE_GEMINI_KEY')
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-change-in-production')
    
    # Optional API Keys (for voice features)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    # Feature flags
    VOICE_ENABLED = os.getenv('VOICE_ENABLED', 'False').lower() == 'true'
    FILE_UPLOAD_ENABLED = os.getenv('FILE_UPLOAD_ENABLED', 'True').lower() == 'true'
    
    # Token settings
    TOKEN_EXPIRATION_HOURS = int(os.getenv('TOKEN_EXPIRATION_HOURS', '24'))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        # Check required keys
        if not cls.GOOGLE_GEMINI_KEY:
            errors.append("GOOGLE_GEMINI_KEY is required")
        
        # Check optional keys based on features
        if cls.VOICE_ENABLED:
            if not cls.OPENAI_API_KEY:
                errors.append("OPENAI_API_KEY required for voice features")
            if not cls.GOOGLE_APPLICATION_CREDENTIALS:
                errors.append("GOOGLE_APPLICATION_CREDENTIALS required for TTS")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for tests
