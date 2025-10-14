"""LLMON Agent - Creates multiple article variations."""
import asyncio
import concurrent.futures
from api_client import APIClient
from config import Config
from utils import read_file

class LLMONAgent:
    """Agent 2: Generates three distinct article variations."""
    
    def __init__(self):
        """Initialize LLMON agent."""
        # Pass the specific model for LLMON agent if using OpenAI
        model = Config.OPENAI_LLMON_MODEL if Config.AI_PROVIDER == 'openai' else None
        self.client = APIClient(model=model)
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
    
    def generate_variations_parallel(self, article, rules_path, differentiator=None):
        """
        Generate variations in parallel for faster execution.
        
        Args:
            article: The article to transform
            rules_path: Path to llmon_rules.md
            differentiator: Optional VariationDifferentiator instance for validation
        
        Returns:
            List of article variations
        """
        rules = read_file(rules_path)
        if not rules:
            raise ValueError("LLMON rules file is missing or empty")
        
        # Use ThreadPoolExecutor for parallel API calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.versions_count) as executor:
            # Submit all variation generation tasks
            futures = []
            for i in range(1, self.versions_count + 1):
                future = executor.submit(
                    self._generate_single_variation,
                    article, rules, i
                )
                futures.append(future)
            
            # Collect results
            variations = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    variation = future.result()
                    variations.append(variation)
                except Exception as e:
                    raise Exception(f"Parallel generation error: {str(e)}")
        
        # Validate differentiation if differentiator provided
        if differentiator and Config.ENABLE_VARIATION_VALIDATION:
            validation = differentiator.validate_variations(variations)
            
            # If variations are too similar, regenerate problematic ones
            max_retries = 2
            retry_count = 0
            
            while not validation['valid'] and retry_count < max_retries:
                retry_count += 1
                
                # Identify which variation to regenerate
                suggestion = differentiator.suggest_regeneration(variations)
                if suggestion is not None:
                    # Regenerate with stronger emphasis
                    var_num = suggestion + 1
                    variations[suggestion] = self._generate_single_variation(
                        article, rules, var_num, stronger_emphasis=True
                    )
                    
                    # Re-validate
                    validation = differentiator.validate_variations(variations)
        
        return variations
    
    def _generate_single_variation(self, article, rules, variation_num, stronger_emphasis=False):
        """
        Generate a single variation.
        
        Args:
            article: The article to transform
            rules: Rules text
            variation_num: Variation number (1-3)
            stronger_emphasis: If True, use stronger differentiation prompts
        
        Returns:
            Generated variation text
        """
        emphasis_instruction = self._get_variation_emphasis(variation_num)
        
        if stronger_emphasis:
            emphasis_instruction += " - IMPORTANT: Make this variation DISTINCTLY DIFFERENT from others, use unique phrasing, examples, and structure while keeping the same core information."
        
        variation_prompt = f"""You are a content transformation specialist creating variation #{variation_num} of {self.versions_count}.

# STYLISTIC RULES
{rules}

# ORIGINAL ARTICLE
{article}

# YOUR TASK FOR VARIATION {variation_num}
Transform the article according to the stylistic rules while:
1. Maintaining all key information and facts
2. Applying the style guidelines distinctly
3. Creating a DIFFERENT feel/approach than other variations would have
4. Ensuring professional quality

For variation {variation_num}, emphasize: {emphasis_instruction}

Generate the COMPLETE transformed article now:"""

        return self.client.generate_content(variation_prompt, self.temperature)
    
    def generate_variations_with_custom_rules_parallel(self, article, custom_rules, differentiator=None):
        """
        Generate variations with custom rules in parallel.
        
        Args:
            article: The article to transform
            custom_rules: User-modified rules
            differentiator: Optional VariationDifferentiator instance
        
        Returns:
            List of article variations
        """
        # Use ThreadPoolExecutor for parallel API calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.versions_count) as executor:
            # Submit all variation generation tasks
            futures = []
            for i in range(1, self.versions_count + 1):
                future = executor.submit(
                    self._generate_single_variation,
                    article, custom_rules, i
                )
                futures.append(future)
            
            # Collect results
            variations = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    variation = future.result()
                    variations.append(variation)
                except Exception as e:
                    raise Exception(f"Parallel generation error: {str(e)}")
        
        # Validate differentiation if differentiator provided
        if differentiator and Config.ENABLE_VARIATION_VALIDATION:
            validation = differentiator.validate_variations(variations)
            
            # If variations are too similar, regenerate problematic ones
            max_retries = 2
            retry_count = 0
            
            while not validation['valid'] and retry_count < max_retries:
                retry_count += 1
                
                # Identify which variation to regenerate
                suggestion = differentiator.suggest_regeneration(variations)
                if suggestion is not None:
                    # Regenerate with stronger emphasis
                    var_num = suggestion + 1
                    variations[suggestion] = self._generate_single_variation(
                        article, custom_rules, var_num, stronger_emphasis=True
                    )
                    
                    # Re-validate
                    validation = differentiator.validate_variations(variations)
        
        return variations


