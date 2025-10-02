"""API client for Google Gemini."""
import google.generativeai as genai
from config import Config

class APIClient:
    """Wrapper for Gemini API calls."""
    
    def __init__(self):
        """Initialize API client."""
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
    def generate_content(self, prompt, temperature=0.7):
        """Generate content using Gemini API."""
        try:
            model = genai.GenerativeModel(Config.MODEL_NAME)
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=8192
            )
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        except Exception as e:
            raise Exception(f"API Error: {str(e)}")


