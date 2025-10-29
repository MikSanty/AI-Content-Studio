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
    
    def polish_article_tool_review(self, article, rules_path):
        """
        Polish tool review with special format validation.
        
        Args:
            article: The tool review to polish
            rules_path: Path to editor_tool_review_rules.md
        
        Returns:
            Polished tool review
        """
        rules = read_file(rules_path)
        if not rules:
            raise ValueError("Tool review editor rules file is missing or empty")
        
        # Multi-pass editing for tool reviews
        if Config.ENABLE_MULTIPASS_EDITING:
            # Pass 1: Format compliance (critical for tool reviews)
            article = self._tool_review_format_pass(article, rules)
            
            # Pass 2: Factual & structural check
            article = self._tool_review_factual_pass(article, rules)
            
            # Pass 3: Grammar, clarity & flow
            article = self._tool_review_clarity_pass(article, rules)
            
            # Pass 4: Final consistency & polish
            article = self._tool_review_final_pass(article, rules)
        else:
            # Single-pass editing
            article = self._tool_review_single_pass(article, rules)
        
        return article
    
    def _tool_review_format_pass(self, article, rules):
        """First pass: Format compliance for tool reviews."""
        prompt = f"""You are a professional editor performing TOOL REVIEW FORMAT COMPLIANCE check.

# TOOL REVIEW EDITING RULES
{rules}

# TOOL REVIEW ARTICLE
{article}

# YOUR TASK - PASS 1: FORMAT COMPLIANCE (CRITICAL)
Focus ONLY on format violations:

1. **ELIMINATE ALL EM DASHES (—)**
   - Replace with semicolons, periods, commas, or parentheses
   - Search the entire article and remove every instance

2. **CLEAN ALL HEADERS**
   - Remove any parenthetical text: "How I Use Tool (Story)" → "How I Use Tool"
   - Remove text after dashes: "Why It Matters - Outcomes" → "Why It Matters"

3. **REMOVE ALL DIVIDER LINES**
   - Delete all ---, ***, ___ divider lines

4. **VERIFY SOURCES APPENDIX**
   - Must be at the very end
   - Proper format: [1] Source Name, Description, Date - URL

Do NOT make other changes in this pass. Focus solely on format compliance.

Generate the COMPLETE article with format fixes:"""

        return self.client.generate_content(prompt, 0.4)  # Low temp for precision
    
    def _tool_review_factual_pass(self, article, rules):
        """Second pass: Factual accuracy and structural check."""
        prompt = f"""You are a professional editor performing TOOL REVIEW FACTUAL CHECK.

# TOOL REVIEW EDITING RULES
{rules}

# TOOL REVIEW ARTICLE (after format pass)
{article}

# YOUR TASK - PASS 2: FACTUAL & STRUCTURAL CHECK
Focus on:

1. **Pricing accuracy** - Numbers are specific and clear
2. **Quote preservation** - All quotes remain word-for-word
3. **Required sections** - All sections present in correct order
4. **Sources appendix** - Every quote has corresponding entry
5. **Product details** - Features, implementation, migration paths accurate

Do NOT change the narrative voice or story elements.

Generate the COMPLETE article with factual checks:"""

        return self.client.generate_content(prompt, 0.4)
    
    def _tool_review_clarity_pass(self, article, rules):
        """Third pass: Grammar, clarity, and flow."""
        prompt = f"""You are a professional editor performing TOOL REVIEW CLARITY & FLOW pass.

# TOOL REVIEW EDITING RULES
{rules}

# TOOL REVIEW ARTICLE (after factual pass)
{article}

# YOUR TASK - PASS 3: GRAMMAR, CLARITY & FLOW
Focus on:

1. **Grammar and spelling** - Fix errors
2. **Clarity** - Improve confusing sentences
3. **Flow** - Smooth transitions between sections
4. **Readability** - Break up overly long paragraphs

BUT PRESERVE:
- First-person voice and personal anecdotes
- Conditional framing ("If you're X... if you're Y...")
- Conversational tone
- Story-driven narrative

Generate the COMPLETE article with clarity improvements:"""

        return self.client.generate_content(prompt, 0.5)
    
    def _tool_review_final_pass(self, article, rules):
        """Fourth pass: Final consistency and polish."""
        prompt = f"""You are a professional editor performing TOOL REVIEW FINAL POLISH.

# TOOL REVIEW EDITING RULES
{rules}

# TOOL REVIEW ARTICLE (after clarity pass)
{article}

# YOUR TASK - PASS 4: FINAL CONSISTENCY & POLISH
Final checks:

1. **Consistent terminology** throughout
2. **Proper markdown formatting**
3. **Word count** - Target 900-1,400 words (soft range)
4. **Voice consistency** - First-person maintained
5. **All format rules** - No em dashes, clean headers, no dividers

This is the final pass. Ensure publication-ready quality.

Generate the COMPLETE polished tool review:"""

        return self.client.generate_content(prompt, 0.4)
    
    def _tool_review_single_pass(self, article, rules):
        """Single-pass editing for tool reviews when multipass disabled."""
        prompt = f"""You are a professional editor polishing a tool review article.

# TOOL REVIEW EDITING RULES
{rules}

# TOOL REVIEW ARTICLE
{article}

# YOUR TASK
Polish this tool review by:

1. **FORMAT COMPLIANCE (CRITICAL)**
   - ELIMINATE all em dashes (—)
   - Remove parenthetical text from headers
   - Remove all divider lines
   - Verify Sources appendix format

2. **FACTUAL ACCURACY**
   - Verify pricing numbers are specific
   - Preserve all quotes word-for-word
   - Check all required sections present

3. **GRAMMAR & CLARITY**
   - Fix grammar and spelling
   - Improve clarity and flow

4. **PRESERVE VOICE**
   - Keep first-person narrative
   - Maintain conditional framing
   - Preserve conversational tone

Generate the COMPLETE polished tool review:"""

        return self.client.generate_content(prompt, self.temperature)
    
    def _validate_tool_review_format(self, article):
        """
        Validate tool review format compliance.
        
        Args:
            article: Tool review article to validate
        
        Returns:
            dict with validation results
        """
        issues = []
        
        # Check for em dashes
        if '—' in article:
            issues.append("Em dashes (—) found in article")
        
        # Check for divider lines
        if '\n---\n' in article or '\n***\n' in article or '\n___\n' in article:
            issues.append("Divider lines found in article")
        
        # Check for Sources appendix
        if '## Sources' not in article and '# Sources' not in article:
            issues.append("Sources appendix missing")
        
        # Check for parenthetical headers (basic check)
        lines = article.split('\n')
        for line in lines:
            if line.startswith('#') and '(' in line and ')' in line:
                issues.append(f"Potential parenthetical in header: {line[:50]}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }


