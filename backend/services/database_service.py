import sqlite3
import json
from datetime import datetime
from pathlib import Path

class DatabaseService:
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
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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
        
        # Files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                file_path TEXT,
                file_type TEXT,
                original_name TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    
    def create_user(self, email, password_hash, name=None):
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (email, password_hash, name)
                VALUES (?, ?, ?)
            ''', (email, password_hash, name))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, password_hash, name, created_at
            FROM users WHERE email = ?
        ''', (email,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, password_hash, name, created_at
            FROM users WHERE id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def delete_session(self, session_id):
        """Delete a session and all its messages"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
        cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
        
        conn.commit()
        conn.close()
    
    def rename_session(self, session_id, new_title):
        """Rename a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions SET title = ? WHERE id = ?
        ''', (new_title, session_id))
        
        conn.commit()
        conn.close()
    
    def add_file(self, session_id, file_path, file_type, original_name):
        """Add a file attachment to a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO files (session_id, file_path, file_type, original_name)
            VALUES (?, ?, ?, ?)
        ''', (session_id, file_path, file_type, original_name))
        
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return file_id
    
    def get_session_files(self, session_id):
        """Get all files for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, file_path, file_type, original_name, uploaded_at
            FROM files WHERE session_id = ?
            ORDER BY uploaded_at DESC
        ''', (session_id,))
        
        files = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return files
    
    def delete_file(self, file_id):
        """Delete a file"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT file_path FROM files WHERE id = ?', (file_id,))
        row = cursor.fetchone()
        
        if row:
            file_path = row[0]
            import os
            if os.path.exists(file_path):
                os.remove(file_path)
            
            cursor.execute('DELETE FROM files WHERE id = ?', (file_id,))
            conn.commit()
        
        conn.close()