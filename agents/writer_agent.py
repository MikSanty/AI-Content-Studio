"""Writer Agent - Creates initial article drafts."""
from api_client import APIClient
from config import Config
from utils import read_file

class WriterAgent:
    """Agent 1: Generates initial article draft."""
    
    def __init__(self):
        """Initialize Writer agent."""
        # Pass the specific model for Writer agent if using OpenAI
        model = Config.OPENAI_WRITER_MODEL if Config.AI_PROVIDER == 'openai' else None
        self.client = APIClient(model=model)
        self.temperature = Config.WRITER_TEMPERATURE
        self.last_outline = None  # Store outline for reference
    
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
    
    def generate_outline(self, manual_path, template_path, references_path, prompt_path, historical_context=""):
        """
        Generate article outline before writing.
        
        Args:
            manual_path: Path to manual.md (user-filled content brief)
            template_path: Path to template.md (article structure)
            references_path: Path to references.md (reference materials)
            prompt_path: Path to prompt.md (writer instructions)
            historical_context: Optional context from workflow memory
        
        Returns:
            Generated outline as string
        """
        # Load all input files
        manual = read_file(manual_path)
        template = read_file(template_path)
        references = read_file(references_path)
        prompt_instructions = read_file(prompt_path)
        
        if not all([manual, template, references, prompt_instructions]):
            raise ValueError("One or more required input files are missing or empty")
        
        # Construct outline generation prompt
        outline_prompt = f"""You are a professional content strategist. Your task is to create a detailed article outline.

{prompt_instructions}

# ARTICLE TEMPLATE STRUCTURE
{template}

# CONTENT BRIEF (from manual.md)
{manual}

# REFERENCE MATERIALS
{references}"""

        if historical_context:
            outline_prompt += f"""

# HISTORICAL CONTEXT (User Preferences)
{historical_context}"""

        outline_prompt += """

# YOUR TASK
Create a comprehensive article outline that:
1. Follows the template structure provided
2. Incorporates all key points from the content brief
3. Identifies specific data, examples, and references to use from the reference materials
4. Plans the narrative flow and transitions between sections
5. Specifies the main argument/thesis for each major section

Format the outline with:
- Clear section headings (using ## for main sections)
- Bullet points for key points under each section
- [REFERENCE: ...] tags to indicate which reference material to use
- [DATA: ...] tags to note specific statistics or facts to include
- [EXAMPLE: ...] tags for examples or case studies to incorporate

Generate the detailed outline now:"""

        # Generate outline
        outline = self.client.generate_content(outline_prompt, self.temperature)
        self.last_outline = outline
        return outline
    
    def revise_outline(self, original_outline, feedback):
        """
        Revise outline based on user feedback.
        
        Args:
            original_outline: The original outline
            feedback: User's revision feedback
        
        Returns:
            Revised outline
        """
        revision_prompt = f"""You are a professional content strategist revising an article outline based on feedback.

# ORIGINAL OUTLINE
{original_outline}

# REVISION FEEDBACK
{feedback}

# YOUR TASK
Revise the outline to address the feedback while maintaining:
1. Clear structure and organization
2. Comprehensive coverage of topics
3. Logical flow between sections
4. Specific references to data and examples

Generate the COMPLETE revised outline now:"""

        revised_outline = self.client.generate_content(revision_prompt, self.temperature)
        self.last_outline = revised_outline
        return revised_outline
    
    def write_from_outline(self, outline, manual_path, template_path, references_path, prompt_path):
        """
        Generate article draft from approved outline.
        
        Args:
            outline: Approved article outline
            manual_path: Path to manual.md
            template_path: Path to template.md
            references_path: Path to references.md
            prompt_path: Path to prompt.md
        
        Returns:
            Generated article draft
        """
        # Load input files
        manual = read_file(manual_path)
        template = read_file(template_path)
        references = read_file(references_path)
        prompt_instructions = read_file(prompt_path)
        
        # Construct writing prompt with outline
        writing_prompt = f"""You are a professional content writer. Your task is to write a complete article based on an approved outline.

{prompt_instructions}

# APPROVED OUTLINE
{outline}

# ARTICLE TEMPLATE STRUCTURE
{template}

# CONTENT BRIEF (from manual.md)
{manual}

# REFERENCE MATERIALS
{references}

# YOUR TASK
Write a complete, engaging article that:
1. Follows the approved outline exactly
2. Expands each section with well-written, flowing prose
3. Incorporates the specific data, examples, and references noted in the outline
4. Maintains consistency with the template structure
5. Creates smooth transitions between sections
6. Achieves the tone and style specified in the instructions

The outline is your roadmap - follow it closely while bringing it to life with compelling writing.

Generate the COMPLETE article now:"""

        # Generate article
        article = self.client.generate_content(writing_prompt, self.temperature)
        return article


