import pytest
import os
import sys 

# Add parent directory to path so we can import from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database

@pytest.fixture
def test_db():
    """Create a test database"""
    db = Database("data/test.db")
    yield db
    # Cleanup
    if os.path.exists("data/test.db"):
        os.remove("data/test.db")

def test_create_session(test_db):
    """Test session creation"""
    session_id = test_db.create_session("test-123", "user-1", "Test Chat")
    assert session_id == "test-123"
    assert test_db.session_exists("test-123")

def test_add_message(test_db):
    """Test adding messages"""
    test_db.create_session("test-123")
    test_db.add_message("test-123", "user", "Hello")
    test_db.add_message("test-123", "model", "Hi there!")
    
    history = test_db.get_session_history("test-123")
    assert len(history) == 2
    assert history[0]['content'] == "Hello"
    assert history[1]['content'] == "Hi there!"

def test_get_all_sessions(test_db):
    """Test retrieving all sessions"""
    test_db.create_session("test-1", "user-1")
    test_db.create_session("test-2", "user-1")
    
    sessions = test_db.get_all_sessions("user-1")
    assert len(sessions) == 2
    