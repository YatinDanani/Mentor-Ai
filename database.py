import sqlite3
import json
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path="data/mentorai.db"):
        self.db_path = db_path
        # Create data directory if doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_db(self):
        """Create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                title TEXT
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(" Database initialized ")
    
    def create_session(self, session_id, user_id="default_user", title="New Chat"):
        """Create a new chat session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (id, user_id, title)
            VALUES (?, ?, ?)
        ''', (session_id, user_id, title))
        
        conn.commit()
        conn.close()
        return session_id
    
    def add_message(self, session_id, role, content):
        """Add a message to a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (session_id, role, content)
            VALUES (?, ?, ?)
        ''', (session_id, role, content))
        
        # Update session last_active
        cursor.execute('''
            UPDATE sessions 
            SET last_active = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def get_session_history(self, session_id):
        """Get all messages for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, content, timestamp
            FROM messages
            WHERE session_id = ?
            ORDER BY timestamp ASC
        ''', (session_id,))
        
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return messages
    
    def get_all_sessions(self, user_id="default_user"):
        """Get all sessions for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, created_at, last_active
            FROM sessions
            WHERE user_id = ?
            ORDER BY last_active DESC
        ''', (user_id,))
        
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return sessions
    
    def session_exists(self, session_id):
        """Check if session exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM sessions WHERE id = ?', (session_id,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists