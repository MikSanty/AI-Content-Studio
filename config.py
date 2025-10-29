"""Configuration management for AI-Content-Studio Workflow."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the workflow."""
    
    # API Configuration
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai').lower()  # 'openai' or 'gemini'
    
    # OpenAI Configuration - Per-Agent Models
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_WRITER_MODEL = os.getenv('OPENAI_WRITER_MODEL')  # Model for Writer Agent
    OPENAI_LLMON_MODEL = os.getenv('OPENAI_LLMON_MODEL')    # Model for LLMON Agent
    OPENAI_EDITOR_MODEL = os.getenv('OPENAI_EDITOR_MODEL')  # Model for Editor Agent
    
    # Gemini Configuration (fallback)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = 'gemini-2.5-flash'  # Free tier model
    
    # File Paths
    TEMPLATES_DIR = 'templates'
    RULES_DIR = 'rules'
    OUTPUTS_DIR = 'outputs'
    MEMORY_DIR = 'memory'
    
    # Content Mode Selection
    CONTENT_MODE = os.getenv('CONTENT_MODE', 'article')  # 'article' or 'tool_review'
    
    # Tool Review Settings
    TOOL_REVIEW_MIN_QUOTES = 6
    TOOL_REVIEW_MAX_QUOTES = 10
    TOOL_REVIEW_TARGET_WORDS = (900, 1400)  # soft range
    
    # Agent Settings
    WRITER_TEMPERATURE = 0.7
    LLMON_TEMPERATURE = 0.8  # Higher for more variation
    EDITOR_TEMPERATURE = 0.5  # Lower for consistency
    
    LLMON_VERSIONS_COUNT = 3
    
    # Enhancement Feature Flags (Priority 1-6)
    # Priority 1: Outline Generation Phase
    ENABLE_OUTLINE_PHASE = True
    
    # Priority 2: Parallel Variation Generation
    ENABLE_PARALLEL_VARIATIONS = True
    
    # Priority 3: Quality Scoring System
    ENABLE_QUALITY_SCORING = True
    
    # Priority 4: Cross-Stage Memory System
    ENABLE_WORKFLOW_MEMORY = True
    
    # Priority 5: Variation Differentiation Validation
    ENABLE_VARIATION_VALIDATION = True
    MIN_VARIATION_DIFFERENCE = 0.3  # 30% minimum difference
    
    # Priority 6: Multi-Pass Editor
    ENABLE_MULTIPASS_EDITING = True
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if cls.AI_PROVIDER == 'openai':
            if not cls.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY not found. Please add your OpenAI API key to .env file.\n"
                    "Example: OPENAI_API_KEY=sk-proj-..."
                )
            # Validate all three agent models are configured
            missing_models = []
            if not cls.OPENAI_WRITER_MODEL:
                missing_models.append('OPENAI_WRITER_MODEL')
            if not cls.OPENAI_LLMON_MODEL:
                missing_models.append('OPENAI_LLMON_MODEL')
            if not cls.OPENAI_EDITOR_MODEL:
                missing_models.append('OPENAI_EDITOR_MODEL')
            
            if missing_models:
                raise ValueError(
                    f"Missing OpenAI model configuration(s): {', '.join(missing_models)}\n"
                    "Please add all three model configurations to your .env file:\n"
                    "Example:\n"
                    "  OPENAI_WRITER_MODEL=gpt-5-mini\n"
                    "  OPENAI_LLMON_MODEL=gpt-5-mini\n"
                    "  OPENAI_EDITOR_MODEL=gpt-5-mini"
                )
        elif cls.AI_PROVIDER == 'gemini':
            if not cls.GEMINI_API_KEY:
                raise ValueError(
                    "GEMINI_API_KEY not found. Please add your Gemini API key to .env file.\n"
                    "Get a free key from https://makersuite.google.com/app/apikey"
                )
        else:
            raise ValueError(
                f"Invalid AI_PROVIDER: {cls.AI_PROVIDER}. Must be 'openai' or 'gemini'"
            )
        return True


