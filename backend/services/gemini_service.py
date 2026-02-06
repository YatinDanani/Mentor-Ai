from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_GEMINI_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_GEMINI_KEY not found in environment")

        self.client = genai.Client(api_key=self.api_key)
        self.model = "models/gemini-2.5-flash"

    def send_message(self, session_id, message, history=None):
        """Send message and get response with conversation context"""
        try:
            # Build conversation history for context
            contents = []

            # Add history if available
            if history:
                for msg in history[-10:]:  # Use last 10 messages for context
                    role = "user" if msg['role'] == 'user' else "model"
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part(text=msg['content'])]
                        )
                    )

            # Add current message
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part(text=message)]
                )
            )

            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )

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
        """Clear chat (no-op since we don't maintain state)"""
        pass