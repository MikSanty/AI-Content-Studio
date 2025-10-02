"""Editor Agent - Polishes and refines final article."""
from api_client import APIClient
from config import Config
from utils import read_file

class EditorAgent:
    """Agent 3: Performs final editing and polish."""
    
    def __init__(self):
        """Initialize Editor agent."""
        self.client = APIClient()
        self.temperature = Config.EDITOR_TEMPERATURE
    
    def polish_article(self, article, rules_path):
        """
        Polish and refine article.
        
        Args:
            article: The selected article from LLMON agent
            rules_path: Path to editor_rules.md (editing guidelines)
        
        Returns:
            Polished final article
        """
        rules = read_file(rules_path)
        if not rules:
            raise ValueError("Editor rules file is missing or empty")
        
        polish_prompt = f"""You are a professional editor performing final polish on an article.

# EDITING RULES AND GUIDELINES
{rules}

# ARTICLE TO POLISH
{article}

# YOUR TASK
Review and polish this article by:
1. Fixing any grammar, spelling, or punctuation errors
2. Improving sentence structure and flow
3. Ensuring consistency in tone and style
4. Enhancing clarity and readability
5. Making minor improvements that elevate quality
6. Applying all guidelines from the editing rules

Do NOT make major structural changes. Focus on polish and refinement.

Generate the COMPLETE polished article now:"""

        polished_article = self.client.generate_content(polish_prompt, self.temperature)
        return polished_article
    
    def apply_minor_revisions(self, article, revision_notes):
        """
        Apply minor revisions based on user feedback.
        
        Args:
            article: The polished article
            revision_notes: Specific revision requests
        
        Returns:
            Article with minor revisions applied
        """
        revision_prompt = f"""You are a professional editor applying minor revisions to a polished article.

# CURRENT ARTICLE
{article}

# REVISION REQUESTS
{revision_notes}

# YOUR TASK
Apply the requested minor revisions while:
1. Maintaining the overall structure and flow
2. Keeping the professional polish
3. Making only the necessary changes
4. Ensuring consistency

Generate the COMPLETE revised article now:"""

        revised_article = self.client.generate_content(revision_prompt, self.temperature)
        return revised_article


