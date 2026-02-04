import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database
from auth import auth

@pytest.fixture
def test_db():
    """Create a test database"""
    db = Database("data/test.db")
    yield db
    if os.path.exists("data/test.db"):
        os.remove("data/test.db")

def test_validate_email(test_db):
    """Test email validation"""
    assert auth.validate_email("test@example.com") == True
    assert auth.validate_email("invalid-email") == False
    assert auth.validate_email("test@") == False
    assert auth.validate_email("@example.com") == False

def test_validate_password(test_db):
    """Test password validation"""
    valid, msg = auth.validate_password("short")
    assert valid == False
    assert "8 characters" in msg
    
    valid, msg = auth.validate_password("longpassword")
    assert valid == True
    assert msg == ""

def test_create_user(test_db):
    """Test user creation"""
    email = "test@example.com"
    password_hash = auth.hash_password("password123")
    user_id = db.create_user(email, password_hash, "Test User")
    
    assert user_id is not None
    assert isinstance(user_id, int)

def test_get_user_by_email(test_db):
    """Test get user by email"""
    email = "test@example.com"
    password_hash = auth.hash_password("password123")
    db.create_user(email, password_hash, "Test User")
    
    user = db.get_user_by_email(email)
    assert user is not None
    assert user['email'] == email
    assert user['name'] == "Test User"

def test_duplicate_user(test_db):
    """Test duplicate user creation"""
    email = "test@example.com"
    password_hash = auth.hash_password("password123")
    
    user_id1 = db.create_user(email, password_hash)
    user_id2 = db.create_user(email, password_hash)
    
    assert user_id1 is not None
    assert user_id2 is None

def test_password_hashing(test_db):
    """Test password hashing and verification"""
    password = "testpassword123"
    hash1 = auth.hash_password(password)
    hash2 = auth.hash_password(password)
    
    # Hashes should be different (different salts)
    assert hash1 != hash2
    
    # Both should verify correctly
    assert auth.verify_password(password, hash1) == True
    assert auth.verify_password(password, hash2) == True
    assert auth.verify_password("wrongpassword", hash1) == False

def test_token_generation(test_db):
    """Test JWT token generation and decoding"""
    user_id = 1
    email = "test@example.com"
    
    token = auth.generate_token(user_id, email)
    assert token is not None
    assert isinstance(token, str)
    
    # Decode and verify
    payload = auth.decode_token(token)
    assert payload is not None
    assert payload['user_id'] == user_id
    assert payload['email'] == email

def test_token_expiry(test_db):
    """Test token expiration handling (invalid token)"""
    # This would require mocking time or using an expired token
    # For now, we test that invalid tokens are rejected
    invalid_token = "invalid.token.string"
    payload = auth.decode_token(invalid_token)
    assert payload is None
