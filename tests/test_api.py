import pytest
import os
import sys
import json
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import Database

@pytest.fixture
def test_db():
    db = Database("data/test.db")
    yield db
    if os.path.exists("data/test.db"):
        os.remove("data/test.db")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_register_success(client, test_db):
    response = client.post('/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert 'token' in data
    assert 'user' in data

def test_register_missing_email(client):
    response = client.post('/auth/register', json={
        'password': 'password123'
    })
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['success'] == False

def test_register_invalid_email(client):
    response = client.post('/auth/register', json={
        'email': 'invalid-email',
        'password': 'password123'
    })
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'Invalid email format' in data['error']

def test_register_short_password(client):
    response = client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'short'
    })
    data = json.loads(response.data)
    assert response.status_code == 400
    assert '8 characters' in data['error']

def test_login_success(client, test_db):
    test_db.create_user(999, 'test@example.com', 'hash123', 'Test User')
    
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert 'token' in data

def test_login_invalid_credentials(client, test_db):
    test_db.create_user(999, 'test@example.com', 'hash123', 'Test User')
    
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['success'] == False
    assert 'Invalid credentials' in data['error']

def test_login_nonexistent_user(client):
    response = client.post('/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'password123'
    })
    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['success'] == False

def test_create_session(client, test_db):
    test_db.create_user(999, 'test@example.com', 'hash123', 'Test User')
    session_id = 'test-session-123'
    test_db.create_session(session_id, 999, 'Test Chat')
    
    response = client.post('/session/new', json={
        'title': 'New Test Session'
    }, headers={'Authorization': 'Bearer valid.token'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert 'session_id' in data

def test_send_message(client, test_db):
    session_id = 'test-session-456'
    test_db.create_session(session_id, 999, 'Test Chat')
    
    response = client.post('/chat', json={
        'session_id': session_id,
        'message': 'Hello, AI!'
    }, headers={'Authorization': 'Bearer valid.token'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True

def test_get_history(client, test_db):
    session_id = 'test-session-789'
    test_db.create_session(session_id, 999, 'Test Chat')
    
    response = client.get(f'/history/{session_id}', 
                       headers={'Authorization': 'Bearer valid.token'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert 'history' in data

def test_get_sessions(client, test_db):
    test_db.create_user(999, 'test@example.com', 'hash123', 'Test User')
    test_db.create_session('session-1', 999, 'Chat 1')
    test_db.create_session('session-2', 999, 'Chat 2')
    
    response = client.get('/sessions', 
                       headers={'Authorization': 'Bearer valid.token'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert len(data['sessions']) == 2

def test_delete_session(client, test_db):
    session_id = 'test-session-delete'
    test_db.create_session(session_id, 999, 'Test Chat')
    
    response = client.delete(f'/session/{session_id}', 
                          headers={'Authorization': 'Bearer valid.token'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert not test_db.session_exists(session_id)

def test_rename_session(client, test_db):
    session_id = 'test-session-rename'
    test_db.create_session(session_id, 999, 'Old Title')
    
    response = client.put(f'/session/{session_id}', json={
        'title': 'New Title'
    }, headers={'Authorization': 'Bearer valid.token'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True

def test_logout(client):
    response = client.post('/auth/logout', 
                       headers={'Authorization': 'Bearer valid.token'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
