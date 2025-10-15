"""Unified API client for OpenAI and Google Gemini."""
from config import Config

class APIClient:
    """Wrapper for AI API calls with multi-provider support."""
    
    def __init__(self, model=None):
        """Initialize API client for the configured provider.
        
        Args:
            model: Optional model override. For OpenAI, this should be the specific
                   agent model. For Gemini, this parameter is ignored and the 
                   default model is used.
        """
        Config.validate()
        
        self.provider = Config.AI_PROVIDER
        
        if self.provider == 'openai':
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = model  # Use the passed model for OpenAI
        elif self.provider == 'gemini':
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.genai = genai
            self.model = Config.MODEL_NAME  # Gemini uses single model
        
    def generate_content(self, prompt, temperature=0.7):
        """Generate content using the configured AI provider."""
        try:
            if self.provider == 'openai':
                return self._generate_openai(prompt, temperature)
            elif self.provider == 'gemini':
                return self._generate_gemini(prompt, temperature)
        except Exception as e:
            raise Exception(f"API Error ({self.provider}): {str(e)}")
    
    def _generate_openai(self, prompt, temperature):
        """Generate content using OpenAI API."""
        # Handle models that only support default temperature (like gpt-5-mini)
        if self.model == 'gpt-5-mini':
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional content writer and editor. Follow the instructions precisely and generate high-quality content."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=8192
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional content writer and editor. Follow the instructions precisely and generate high-quality content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_completion_tokens=8192
            )
        return response.choices[0].message.content
    
    def _generate_gemini(self, prompt, temperature):
        """Generate content using Google Gemini API."""
        model = self.genai.GenerativeModel(self.model)
        generation_config = self.genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=8192
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text


