import openai
import os
from pydub import AudioSegment
import tempfile

class WhisperService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        openai.api_key = self.api_key
    
    def transcribe_audio(self, audio_file_path, model='whisper-1'):
        """Transcribe audio using OpenAI Whisper"""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = openai.Audio.transcribe(
                    model=model,
                    file=audio_file
                )
            return {
                'success': True,
                'text': transcript['text']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
