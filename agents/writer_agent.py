"""Writer Agent - Creates initial article drafts."""
from api_client import APIClient
from config import Config
from utils import read_file
import os

class WriterAgent:
    """Agent 1: Generates initial article draft."""
    
    def __init__(self):
        """Initialize Writer agent."""
        # Pass the specific model for Writer agent if using OpenAI
        model = Config.OPENAI_WRITER_MODEL if Config.AI_PROVIDER == 'openai' else None
        self.client = APIClient(model=model)
        self.temperature = Config.WRITER_TEMPERATURE
        self.last_outline = None  # Store outline for reference
        self.content_mode = None  # Will be detected from manual file
    
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

# CRITICAL CITATION REQUIREMENTS
**EVERY source citation MUST be a properly hyperlinked markdown link:**
- Use format: [Source Name](exact_url)
- NEVER write "according to Source Name" without a hyperlink
- NEVER invent or modify URLs - use only exact URLs from your reference materials
- Verify every citation has a clickable link before finalizing

**Examples:**
- ✅ "according to [Miquido UI/UX Trends](https://www.miquido.com/blog/ui-ux-design-trends/)"
- ❌ "according to Miquido UI/UX Trends" (missing hyperlink)
- ❌ "according to [Miquido](https://miquido.com/trends)" (invented/wrong URL)

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
- [LINK: exact_url] tags next to each source citation to ensure proper hyperlinking later

# CRITICAL CITATION PLANNING
For every data point, quote, or reference you plan to cite:
- Include the [LINK: exact_url] tag with the precise URL from REFERENCE MATERIALS
- This ensures the final article will have properly hyperlinked citations
- Example: "[DATA: 50% users abandon slow pages] [LINK: https://www.miquido.com/blog/ui-ux-design-trends/]"

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

# CRITICAL CITATION REQUIREMENTS
**EVERY source citation MUST be a properly hyperlinked markdown link:**
- Convert ALL source mentions to format: [Source Name](exact_url)
- Use ONLY the exact URLs from the REFERENCE MATERIALS section below
- NEVER invent, modify, guess, or hallucinate URLs
- If the outline includes [LINK: url] tags, use those exact URLs
- Before finishing, verify every "according to" or data citation has a clickable hyperlink

**Mandatory Format:**
- ✅ "according to [Miquido UI/UX Trends](https://www.miquido.com/blog/ui-ux-design-trends/)"
- ✅ "as [Userpilot SaaS Research](https://userpilot.com/blog/saas-landing-pages/) reports"
- ❌ "according to Miquido UI/UX Trends" (NO HYPERLINK - UNACCEPTABLE)
- ❌ "according to [Source](https://fake-url.com)" (INVENTED URL - UNACCEPTABLE)

**Final Check Before Submitting:**
- Scan your article for any source mentions without hyperlinks
- Verify all URLs exactly match the REFERENCE MATERIALS section
- No plain text source citations are acceptable

Generate the COMPLETE article now:"""

        # Generate article
        article = self.client.generate_content(writing_prompt, self.temperature)
        return article
    
    def _detect_content_mode(self, manual_path):
        """
        Detect content mode from manual file.
        
        Args:
            manual_path: Path to manual/brief file
        
        Returns:
            'tool_review' or 'article'
        """
        # First check config
        if Config.CONTENT_MODE == 'tool_review':
            return 'tool_review'
        
        # Try to detect from file name
        if 'tool_review' in os.path.basename(manual_path).lower():
            return 'tool_review'
        
        # Try to detect from content
        try:
            manual_content = read_file(manual_path)
            if manual_content:
                # Look for tool review markers
                markers = [
                    'Pre-Writing Interview Questions',
                    'Target Audience',
                    'Reader Motivation',
                    'Collected Quotes',
                    'Tool Information'
                ]
                if any(marker in manual_content for marker in markers):
                    return 'tool_review'
        except:
            pass
        
        return 'article'
    
    def generate_draft_tool_review(self, manual_path, template_path, references_path, prompt_path):
        """
        Generate tool review draft.
        
        Args:
            manual_path: Path to tool_review_brief.md
            template_path: Path to tool_review_structure.md
            references_path: Path to references.md (not used for tool reviews)
            prompt_path: Path to tool_review_writer_prompt.md
        
        Returns:
            Generated tool review as string
        """
        # Load input files
        brief = read_file(manual_path)
        structure = read_file(template_path)
        prompt_instructions = read_file(prompt_path)
        
        if not all([brief, structure, prompt_instructions]):
            raise ValueError("One or more required tool review input files are missing or empty")
        
        # Construct the prompt
        full_prompt = f"""You are a professional tool review writer. Your task is to create a complete, story-driven tool review.

{prompt_instructions}

# TOOL REVIEW STRUCTURE TEMPLATE
{structure}

# TOOL REVIEW BRIEF (Your Source Material)
{brief}

# YOUR TASK
Using the structure template and the brief provided:
1. Write a complete tool review following the required structure exactly
2. Answer the 4 pre-writing questions to understand context and audience
3. Integrate all 6-10 collected quotes naturally into the narrative
4. Use story-driven, first-person narrative throughout
5. Apply conditional framing ("If you're X... if you're Y...")
6. Provide honest pros, cons, and fit guidance
7. Include all product details (pricing, implementation, migration)
8. Create Sources appendix with all quote URLs at the end

# CRITICAL REMINDERS
- Use ONLY quotes from the brief (6-10 minimum)
- Place quote URLs in Sources appendix, NOT inline
- No em dashes anywhere
- No parenthetical text in headers
- No divider lines
- Target 900-1,400 words (soft range)
- First-person voice required

Generate the complete tool review now:"""

        # Generate review
        review = self.client.generate_content(full_prompt, self.temperature)
        return review
    
    def generate_outline_tool_review(self, manual_path, template_path, references_path, prompt_path, historical_context=""):
        """
        Generate tool review outline.
        
        Args:
            manual_path: Path to tool_review_brief.md
            template_path: Path to tool_review_structure.md
            references_path: Path to references.md (not used)
            prompt_path: Path to tool_review_writer_prompt.md
            historical_context: Optional context from workflow memory
        
        Returns:
            Generated outline as string
        """
        # Load input files
        brief = read_file(manual_path)
        structure = read_file(template_path)
        prompt_instructions = read_file(prompt_path)
        
        if not all([brief, structure, prompt_instructions]):
            raise ValueError("One or more required tool review input files are missing or empty")
        
        # Construct outline prompt
        outline_prompt = f"""You are a professional tool review strategist. Your task is to create a detailed outline for a tool review.

{prompt_instructions}

# TOOL REVIEW STRUCTURE TEMPLATE
{structure}

# TOOL REVIEW BRIEF (Your Source Material)
{brief}"""

        if historical_context:
            outline_prompt += f"""

# HISTORICAL CONTEXT (User Preferences)
{historical_context}"""

        outline_prompt += """

# YOUR TASK
Create a comprehensive tool review outline that:
1. Follows the required structure exactly
2. Addresses the 4 pre-writing questions (title, audience, motivation, benefit)
3. Plans where each of the 6-10 quotes will be used
4. Maps out the "How I Use [Tool]" narrative
5. Identifies conditional framing callouts (2-4 minimum)
6. Structures pricing breakdown with scaling details
7. Plans comparative guidance and exclusion criteria
8. Outlines pros, cons, and fit analysis

Format the outline with:
- Clear section headings (## for main sections)
- Bullet points for key content under each section
- [QUOTE: #] tags to indicate which quote to use where
- [CONDITIONAL: ...] tags for "If you're X... if you're Y..." callouts
- [PRICING: ...] tags for specific pricing details to include
- [COMPARISON: ...] tags for comparative guidance

# CRITICAL PLANNING
For each quote in the brief:
- Plan which section it will appear in
- Note how it will be integrated naturally
- Remember all quote URLs go in Sources appendix only

Generate the detailed tool review outline now:"""

        # Generate outline
        outline = self.client.generate_content(outline_prompt, self.temperature)
        self.last_outline = outline
        self.content_mode = 'tool_review'
        return outline
    
    def revise_outline_tool_review(self, original_outline, feedback):
        """
        Revise tool review outline based on feedback.
        
        Args:
            original_outline: The original outline
            feedback: User's revision feedback
        
        Returns:
            Revised outline
        """
        revision_prompt = f"""You are a professional tool review strategist revising an outline based on feedback.

# ORIGINAL OUTLINE
{original_outline}

# REVISION FEEDBACK
{feedback}

# YOUR TASK
Revise the outline to address the feedback while maintaining:
1. Required tool review structure
2. Quote placement planning
3. Conditional framing callouts
4. Pricing and product detail planning
5. Story-driven narrative structure

Generate the COMPLETE revised outline now:"""

        revised_outline = self.client.generate_content(revision_prompt, self.temperature)
        self.last_outline = revised_outline
        return revised_outline
    
    def write_from_outline_tool_review(self, outline, manual_path, template_path, references_path, prompt_path):
        """
        Generate tool review from approved outline.
        
        Args:
            outline: Approved tool review outline
            manual_path: Path to tool_review_brief.md
            template_path: Path to tool_review_structure.md
            references_path: Path to references.md (not used)
            prompt_path: Path to tool_review_writer_prompt.md
        
        Returns:
            Generated tool review
        """
        # Load input files
        brief = read_file(manual_path)
        structure = read_file(template_path)
        prompt_instructions = read_file(prompt_path)
        
        # Construct writing prompt
        writing_prompt = f"""You are a professional tool review writer. Your task is to write a complete tool review based on an approved outline.

{prompt_instructions}

# APPROVED OUTLINE
{outline}

# TOOL REVIEW STRUCTURE TEMPLATE
{structure}

# TOOL REVIEW BRIEF (Your Source Material)
{brief}

# YOUR TASK
Write a complete tool review that:
1. Follows the approved outline exactly
2. Expands each section with well-written, flowing prose
3. Integrates the specific quotes noted in the outline
4. Uses story-driven, first-person narrative throughout
5. Applies conditional framing as planned
6. Includes all product details (pricing, implementation, migration)
7. Maintains a personable, colleague-to-colleague tone
8. Creates Sources appendix with all quote URLs

# CRITICAL REQUIREMENTS
- Use ONLY quotes from the brief
- Place ALL quote URLs in Sources appendix at the end
- NO inline quote links in the article body
- NO em dashes anywhere
- NO parenthetical text in headers
- NO divider lines
- Target 900-1,400 words (soft range)
- First-person voice required

Generate the COMPLETE tool review now:"""

        # Generate review
        review = self.client.generate_content(writing_prompt, self.temperature)
        return review


