"""Writer Agent - Creates initial article drafts."""
from api_client import APIClient
from config import Config
from utils import read_file

class WriterAgent:
    """Agent 1: Generates initial article draft."""
    
    def __init__(self):
        """Initialize Writer agent."""
        self.client = APIClient()
        self.temperature = Config.WRITER_TEMPERATURE
    
    def generate_draft(self, manual_path, template_path, references_path, prompt_path):
        """
        Generate initial article draft.
        
        Args:
            manual_path: Path to manual.md (user-filled content brief)
            template_path: Path to template.md (article structure)
            references_path: Path to references.md (reference materials)
            prompt_path: Path to prompt.md (writer instructions)
        
        Returns:
            Generated article draft as string
        """
        # Load all input files
        manual = read_file(manual_path)
        template = read_file(template_path)
        references = read_file(references_path)
        prompt_instructions = read_file(prompt_path)
        
        if not all([manual, template, references, prompt_instructions]):
            raise ValueError("One or more required input files are missing or empty")
        
        # Construct the prompt
        full_prompt = f"""You are a professional content writer. Your task is to create a complete article draft.

{prompt_instructions}

# ARTICLE TEMPLATE STRUCTURE
{template}

# CONTENT BRIEF (from manual.md)
{manual}

# REFERENCE MATERIALS
{references}

# YOUR TASK
Using the template structure, content brief, and reference materials provided:
1. Write a complete, engaging article that follows the template structure
2. Incorporate key information from the content brief
3. Use insights and data from the references where relevant
4. Maintain a professional, informative tone
5. Ensure the article flows naturally and is well-organized

Generate the complete article now:"""

        # Generate content
        article = self.client.generate_content(full_prompt, self.temperature)
        return article
    
    def revise_draft(self, original_draft, feedback):
        """
        Revise draft based on user feedback.
        
        Args:
            original_draft: The original article draft
            feedback: User's revision feedback
        
        Returns:
            Revised article draft
        """
        revision_prompt = f"""You are a professional content writer revising an article based on feedback.

# ORIGINAL ARTICLE DRAFT
{original_draft}

# REVISION FEEDBACK
{feedback}

# YOUR TASK
Revise the article to address the feedback while maintaining:
1. The core structure and flow
2. Professional quality writing
3. Coherence and clarity

Generate the COMPLETE revised article now:"""

        revised_article = self.client.generate_content(revision_prompt, self.temperature)
        return revised_article


