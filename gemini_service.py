from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_GEMINI_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_GEMINI_KEY not found in environment")
        
        self.client = genai.Client(api_key=self.api_key)
        self.active_chats = {}  # session_id -> chat object
    
    def get_or_create_chat(self, session_id, history=None):
        """Get existing chat or create new one"""
        if session_id not in self.active_chats:
            # Create new chat
            chat = self.client.chats.create(
                model="gemini-3-flash-preview"
            )
            
            # If there's history, replay it to rebuild context
            if history:
                for msg in history:
                    if msg['role'] == 'user':
                        # Send message without storing response
                        # (responses already in DB)
                        try:
                            chat.send_message(msg['content'])
                        except:
                            pass  # Skip if replay fails
            
            self.active_chats[session_id] = chat
        
        return self.active_chats[session_id]
    
    def send_message(self, session_id, message, history=None):
        """Send message and get response"""
        chat = self.get_or_create_chat(session_id, history)
        
        try:
            response = chat.send_message(message)
            return {
                'success': True,
                'response': response.text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def clear_chat(self, session_id):
        """Remove chat from memory (called when session ends)"""
        if session_id in self.active_chats:
            del self.active_chats[session_id]