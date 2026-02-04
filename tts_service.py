from google.cloud import texttospeech
import os
import tempfile

class TTSService:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
    
    def synthesize_speech(self, text, language_code='en-US'):
        """Synthesize speech from text using Gemini TTS"""
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            return {
                'success': True,
                'audio_content': response.audio_content
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
