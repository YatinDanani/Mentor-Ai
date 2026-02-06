"""
File Service
Handles file upload validation and AI-powered file analysis
"""
import os
import uuid
import base64
from werkzeug.utils import secure_filename
from PIL import Image
import io
from config.settings import Config
from services.gemini_service import GeminiService
from services.database_service import DatabaseService

class FileService:
    def __init__(self):
        self.upload_folder = Config.UPLOAD_FOLDER
        self.allowed_image_extensions = Config.ALLOWED_IMAGE_EXTENSIONS
        self.allowed_document_extensions = Config.ALLOWED_DOCUMENT_EXTENSIONS
        self.gemini = GeminiService()
        self.db = DatabaseService()
        
        # Ensure upload folder exists
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def allowed_file(self, filename, allowed_extensions):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    def save_and_analyze_file(self, file, session_id):
        """
        Save file to disk and analyze with AI
        
        Args:
            file: FileStorage object from request
            session_id: Session ID to associate file with
        
        Returns:
            dict with success, file_type, analysis, file_id
        """
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # Determine file type
        file_type = None
        if file_ext in self.allowed_image_extensions:
            file_type = 'image'
        elif file_ext in self.allowed_document_extensions:
            file_type = 'document'
        else:
            return {
                'success': False,
                'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp, pdf'
            }
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(self.upload_folder, unique_filename)
        
        try:
            # Save file
            file.save(filepath)
            
            # Analyze file with AI
            analysis_result = self.analyze_file(filepath, file_type)
            
            # Save file metadata to database
            file_id = self.db.add_file(session_id, filepath, file_type, filename)
            
            return {
                'success': True,
                'file_type': file_type,
                'analysis': analysis_result,
                'file_id': file_id
            }
            
        except Exception as e:
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
    
    def analyze_file(self, file_path, file_type):
        """
        Analyze file with Gemini AI
        
        Args:
            file_path: Path to the file
            file_type: 'image' or 'document'
        
        Returns:
            dict with analysis results
        """
        if file_type == 'image':
            return self._analyze_image(file_path)
        elif file_type == 'document':
            return self._analyze_document(file_path)
        else:
            return {
                'type': 'unknown',
                'description': 'Unable to analyze file.'
            }
    
    def _analyze_image(self, file_path):
        """Analyze image using Gemini Vision API"""
        try:
            import google.generativeai as genai

            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Save to temporary file for upload
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
                    img.save(temp, format='JPEG')
                    temp_path = temp.name

                try:
                    # Upload file to Gemini
                    uploaded_file = genai.upload_file(temp_path)

                    # Send to Gemini for image analysis
                    prompt = "Analyze this image and describe what you see in detail."
                    response = self.gemini.model.generate_content([prompt, uploaded_file])

                    return {
                        'type': 'image_analysis',
                        'description': response.text
                    }
                finally:
                    # Clean up temp file
                    import os as os_module
                    if os_module.path.exists(temp_path):
                        os_module.remove(temp_path)

        except Exception as e:
            return {
                'type': 'image_analysis',
                'description': f'Image analysis failed: {str(e)}'
            }
    
    def _analyze_document(self, file_path):
        """Analyze PDF document"""
        try:
            # For PDF, could use PyPDF2 for text extraction
            # For now, return a placeholder
            return {
                'type': 'document_analysis',
                'description': 'Document attached. Ask me specific questions about its content.'
            }
            
        except Exception as e:
            return {
                'type': 'document_analysis',
                'description': f'Document analysis failed: {str(e)}'
            }
