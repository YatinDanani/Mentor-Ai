"""
Voice Routes
Handles voice input/output (speech-to-text and text-to-speech)
Requires OPENAI_API_KEY and GOOGLE_APPLICATION_CREDENTIALS
"""
from flask import Blueprint, request, jsonify, current_app
import os
import uuid
from werkzeug.utils import secure_filename
from services.database_service import DatabaseService
from services.gemini_service import GeminiService
from services.whisper_service import WhisperService
from services.tts_service import TTSService
from utils.decorators import token_required

voice_bp = Blueprint('voice', __name__)

# Initialize services (will be None if API keys not configured)
db = DatabaseService()
gemini = GeminiService()

try:
    whisper = WhisperService()
    WHISPER_AVAILABLE = True
except Exception as e:
    print(f"Warning: Whisper service not available: {e}")
    whisper = None
    WHISPER_AVAILABLE = False

try:
    tts = TTSService()
    TTS_AVAILABLE = True
except Exception as e:
    print(f"Warning: TTS service not available: {e}")
    tts = None
    TTS_AVAILABLE = False

@voice_bp.route('/chat', methods=['POST'])
@token_required
def voice_chat(user_id, user_email):
    """
    Send voice message and get AI response with audio
    
    Form data:
        audio: file (required, audio formats: wav, mp3, ogg, webm, m4a)
        session_id: string (required)
    
    Returns:
        success: boolean
        transcription: string (what user said)
        response: string (AI text response)
        audio_url: string (URL to AI audio response, optional)
    """
    if not WHISPER_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Voice features not enabled. Configure OPENAI_API_KEY.'
        }), 503
    
    try:
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        audio_file = request.files['audio']
        session_id = request.form.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'session_id required'
            }), 400
        
        if not db.session_exists(session_id):
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Save audio file temporarily
        filename = secure_filename(audio_file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        audio_file.save(filepath)
        
        try:
            # Transcribe audio
            whisper_result = whisper.transcribe_audio(filepath)
            
            if not whisper_result['success']:
                return jsonify({
                    'success': False,
                    'error': f'Transcription failed: {whisper_result.get("error")}'
                }), 500
            
            transcribed_text = whisper_result['text']
            
            # Get conversation history for context
            history = db.get_session_history(session_id)
            
            # Save transcribed message
            db.add_message(session_id, 'user', transcribed_text)
            
            # Get AI response
            gemini_result = gemini.send_message(session_id, transcribed_text, history)
            
            if not gemini_result['success']:
                return jsonify({
                    'success': False,
                    'error': gemini_result['error']
                }), 500
            
            ai_response = gemini_result['response']
            
            # Save AI response
            db.add_message(session_id, 'model', ai_response)
            
            # Synthesize speech from AI response (if TTS available)
            audio_url = None
            if TTS_AVAILABLE and tts:
                tts_result = tts.synthesize_speech(ai_response)
                
                if tts_result['success']:
                    # Save TTS audio to file
                    audio_filename = f"tts_{session_id}_{uuid.uuid4().hex[:8]}.mp3"
                    audio_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], audio_filename)
                    
                    with open(audio_filepath, 'wb') as f:
                        f.write(tts_result['audio_content'])
                    
                    audio_url = f"/files/serve/{audio_filename}"
            
            return jsonify({
                'success': True,
                'transcription': transcribed_text,
                'response': ai_response,
                'audio_url': audio_url
            })
            
        finally:
            # Clean up uploaded audio file
            if os.path.exists(filepath):
                os.remove(filepath)
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@voice_bp.route('/tts', methods=['POST'])
@token_required
def synthesize_text_to_speech(user_id, user_email):
    """
    Synthesize speech from text
    
    Request body:
        text: string (required)
        language_code: string (optional, default: 'en-US')
    
    Returns:
        success: boolean
        audio_url: string (URL to audio file)
    """
    if not TTS_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'TTS not enabled. Configure GOOGLE_APPLICATION_CREDENTIALS.'
        }), 503
    
    try:
        data = request.json
        text = data.get('text', '').strip()
        language_code = data.get('language_code', 'en-US')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        tts_result = tts.synthesize_speech(text, language_code)
        
        if not tts_result['success']:
            return jsonify({
                'success': False,
                'error': tts_result['error']
            }), 500
        
        # Save TTS audio to file
        audio_filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        audio_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], audio_filename)
        
        with open(audio_filepath, 'wb') as f:
            f.write(tts_result['audio_content'])
        
        audio_url = f"/files/serve/{audio_filename}"
        
        return jsonify({
            'success': True,
            'audio_url': audio_url
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@voice_bp.route('/status', methods=['GET'])
def voice_status():
    """
    Check voice features availability
    
    Returns:
        whisper_available: boolean
        tts_available: boolean
    """
    return jsonify({
        'whisper_available': WHISPER_AVAILABLE,
        'tts_available': TTS_AVAILABLE
    })
