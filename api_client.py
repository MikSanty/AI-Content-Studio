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
        
        # Configure safety settings to be less restrictive
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]
        
        generation_config = self.genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=8192
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Check if response was blocked by safety filters
        if not response.candidates or not response.candidates[0].content.parts:
            # Get the finish reason
            finish_reason = response.candidates[0].finish_reason if response.candidates else "UNKNOWN"
            
            # Provide helpful error message
            if finish_reason == 2:  # SAFETY
                raise Exception(
                    "Content was blocked by Gemini's safety filters. "
                    "This usually happens with certain topics or phrasing. "
                    "Try: 1) Revising your input content, 2) Adjusting safety_settings, "
                    "or 3) Using OpenAI instead (set AI_PROVIDER=openai in .env)"
                )
            else:
                raise Exception(f"No content returned. Finish reason: {finish_reason}")
        
        return response.text


