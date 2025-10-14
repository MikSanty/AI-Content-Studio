"""Editor Agent - Polishes and refines final article."""
from api_client import APIClient
from config import Config
from utils import read_file

class EditorAgent:
    """Agent 3: Performs final editing and polish."""
    
    def __init__(self):
        """Initialize Editor agent."""
        # Pass the specific model for Editor agent if using OpenAI
        model = Config.OPENAI_EDITOR_MODEL if Config.AI_PROVIDER == 'openai' else None
        self.client = APIClient(model=model)
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
    
    def polish_article_multipass(self, article, rules_path):
        """
        Polish article using multiple focused editing passes.
        
        Args:
            article: The article to polish
            rules_path: Path to editor_rules.md
        
        Returns:
            Polished article after all passes
        """
        rules = read_file(rules_path)
        if not rules:
            raise ValueError("Editor rules file is missing or empty")
        
        # Pass 1: Grammar and Mechanics
        article = self._grammar_pass(article, rules)
        
        # Pass 2: Style and Voice
        article = self._style_pass(article, rules)
        
        # Pass 3: Flow and Transitions
        article = self._flow_pass(article, rules)
        
        # Pass 4: Final Consistency Check
        article = self._consistency_pass(article, rules)
        
        return article
    
    def _grammar_pass(self, article, rules):
        """First pass: Focus on grammar, spelling, and punctuation."""
        prompt = f"""You are a professional copy editor performing a GRAMMAR AND MECHANICS pass.

# EDITING GUIDELINES
{rules}

# ARTICLE
{article}

# YOUR TASK - PASS 1: GRAMMAR & MECHANICS
Focus ONLY on:
1. Grammar errors and corrections
2. Spelling mistakes
3. Punctuation accuracy
4. Sentence structure (fragments, run-ons)
5. Subject-verb agreement
6. Proper capitalization

Do NOT make stylistic changes or reorganize content. Fix only mechanical issues.

Generate the COMPLETE article with grammar corrections:"""

        return self.client.generate_content(prompt, self.temperature - 0.1)  # Lower temp for precision
    
    def _style_pass(self, article, rules):
        """Second pass: Focus on style, voice, and tone consistency."""
        prompt = f"""You are a professional editor performing a STYLE AND VOICE pass.

# EDITING GUIDELINES
{rules}

# ARTICLE (after grammar pass)
{article}

# YOUR TASK - PASS 2: STYLE & VOICE
Focus on:
1. Consistent tone and voice throughout
2. Appropriate word choice and vocabulary
3. Eliminating jargon or overly complex language
4. Active vs. passive voice (prefer active)
5. Sentence variety and rhythm
6. Professional, engaging language

Do NOT reorganize structure. Focus on stylistic improvements.

Generate the COMPLETE article with style improvements:"""

        return self.client.generate_content(prompt, self.temperature)
    
    def _flow_pass(self, article, rules):
        """Third pass: Focus on flow, transitions, and coherence."""
        prompt = f"""You are a professional editor performing a FLOW AND TRANSITIONS pass.

# EDITING GUIDELINES
{rules}

# ARTICLE (after style pass)
{article}

# YOUR TASK - PASS 3: FLOW & TRANSITIONS
Focus on:
1. Smooth transitions between paragraphs and sections
2. Logical flow of ideas
3. Paragraph coherence and unity
4. Connection between related concepts
5. Ensuring each section builds on the previous
6. Reader journey through the content

Make only minor structural adjustments to improve flow.

Generate the COMPLETE article with improved flow:"""

        return self.client.generate_content(prompt, self.temperature)
    
    def _consistency_pass(self, article, rules):
        """Fourth pass: Final consistency and quality check."""
        prompt = f"""You are a professional editor performing a FINAL CONSISTENCY CHECK.

# EDITING GUIDELINES
{rules}

# ARTICLE (after flow pass)
{article}

# YOUR TASK - PASS 4: FINAL CONSISTENCY
Perform final checks on:
1. Consistent formatting (headings, lists, emphasis)
2. Consistent terminology throughout
3. Proper heading hierarchy (H1, H2, H3)
4. Complete sentences and paragraphs
5. Overall professional polish
6. No contradictions or repetitions

This is the final pass - ensure everything is perfect.

Generate the COMPLETE polished article:"""

        return self.client.generate_content(prompt, self.temperature - 0.1)  # Lower temp for precision


