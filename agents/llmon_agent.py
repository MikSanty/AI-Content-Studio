"""LLMON Agent - Creates multiple article variations."""
from api_client import APIClient
from config import Config
from utils import read_file

class LLMONAgent:
    """Agent 2: Generates three distinct article variations."""
    
    def __init__(self):
        """Initialize LLMON agent."""
        self.client = APIClient()
        self.temperature = Config.LLMON_TEMPERATURE
        self.versions_count = Config.LLMON_VERSIONS_COUNT
    
    def generate_variations(self, article, rules_path):
        """
        Generate multiple variations of an article.
        
        Args:
            article: The approved article from Writer agent
            rules_path: Path to llmon_rules.md (stylistic rules)
        
        Returns:
            List of article variations
        """
        rules = read_file(rules_path)
        if not rules:
            raise ValueError("LLMON rules file is missing or empty")
        
        variations = []
        
        for i in range(1, self.versions_count + 1):
            variation_prompt = f"""You are a content transformation specialist creating variation #{i} of {self.versions_count}.

# STYLISTIC RULES
{rules}

# ORIGINAL ARTICLE
{article}

# YOUR TASK FOR VARIATION {i}
Transform the article according to the stylistic rules while:
1. Maintaining all key information and facts
2. Applying the style guidelines distinctly
3. Creating a DIFFERENT feel/approach than other variations would have
4. Ensuring professional quality

For variation {i}, emphasize: {self._get_variation_emphasis(i)}

Generate the COMPLETE transformed article now:"""

            variation = self.client.generate_content(variation_prompt, self.temperature)
            variations.append(variation)
        
        return variations
    
    def generate_variations_with_custom_rules(self, article, custom_rules):
        """
        Generate variations with user-edited rules.
        
        Args:
            article: The article to transform
            custom_rules: User-modified rules for this iteration
        
        Returns:
            List of article variations
        """
        variations = []
        
        for i in range(1, self.versions_count + 1):
            variation_prompt = f"""You are a content transformation specialist creating variation #{i} of {self.versions_count}.

# CUSTOM STYLISTIC RULES
{custom_rules}

# ORIGINAL ARTICLE
{article}

# YOUR TASK FOR VARIATION {i}
Transform the article according to these CUSTOM rules while:
1. Maintaining all key information and facts
2. Applying the style guidelines distinctly
3. Creating a DIFFERENT approach for this variation
4. Ensuring professional quality

For variation {i}, emphasize: {self._get_variation_emphasis(i)}

Generate the COMPLETE transformed article now:"""

            variation = self.client.generate_content(variation_prompt, self.temperature)
            variations.append(variation)
        
        return variations
    
    def _get_variation_emphasis(self, variation_num):
        """Get emphasis instruction for each variation."""
        emphases = {
            1: "Clarity and directness - make it highly accessible",
            2: "Depth and detail - add more nuance and examples",
            3: "Engagement and storytelling - make it more compelling"
        }
        return emphases.get(variation_num, "Balanced approach")


