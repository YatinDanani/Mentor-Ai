import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth import auth
from database import Database

@pytest.fixture
def test_db():
    db = Database("data/test.db")
    yield db
    if os.path.exists("data/test.db"):
        os.remove("data/test.db")

def test_validate_email(test_db):
    assert auth.validate_email("test@example.com") == True
    assert auth.validate_email("invalid-email") == False
    assert auth.validate_email("test@") == False
    assert auth.validate_email("@example.com") == False

def test_validate_password(test_db):
    valid, msg = auth.validate_password("short")
    assert valid == False
    assert "8 characters" in msg
    
    valid, msg = auth.validate_password("longpassword")
    assert valid == True
    assert msg == ""

def test_password_hashing(test_db):
    password = "testpassword123"
    hash1 = auth.hash_password(password)
    hash2 = auth.hash_password(password)
    
    assert hash1 != hash2
    assert auth.verify_password(password, hash1) == True
    assert auth.verify_password(password, hash2) == True
    assert auth.verify_password("wrongpassword", hash1) == False

def test_token_generation(test_db):
    user_id = 1
    email = "test@example.com"
    
    token = auth.generate_token(user_id, email)
    assert token is not None
    assert isinstance(token, str)

def test_token_decode_valid(test_db):
    user_id = 1
    email = "test@example.com"
    
    token = auth.generate_token(user_id, email)
    payload = auth.decode_token(token)
    
    assert payload is not None
    assert payload['user_id'] == user_id
    assert payload['email'] == email

def test_token_decode_invalid(test_db):
    invalid_token = "invalid.token.string"
    payload = auth.decode_token(invalid_token)
    
    assert payload is None
