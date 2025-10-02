"""Configuration management for AI-Content-Studio Workflow."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the workflow."""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = 'gemini-2.5-flash'  # Free tier model
    
    # File Paths
    TEMPLATES_DIR = 'templates'
    RULES_DIR = 'rules'
    OUTPUTS_DIR = 'outputs'
    
    # Agent Settings
    WRITER_TEMPERATURE = 0.7
    LLMON_TEMPERATURE = 0.8  # Higher for more variation
    EDITOR_TEMPERATURE = 0.5  # Lower for consistency
    
    LLMON_VERSIONS_COUNT = 3
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. Please copy .env.example to .env "
                "and add your Gemini API key from https://makersuite.google.com/app/apikey"
            )
        return True


