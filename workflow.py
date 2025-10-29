"""Main workflow orchestrator for AI-Content-Studio."""
import os
from datetime import datetime
from agents import WriterAgent, LLMONAgent, EditorAgent
from config import Config
from utils import (
    ensure_dir, write_file, get_timestamp, print_header, print_section,
    print_success, print_error, print_info, get_user_choice, get_user_input,
    display_content
)
from citation_validator import validate_citations

# Import enhancement modules if enabled
if Config.ENABLE_QUALITY_SCORING:
    from quality_analyzer import QualityAnalyzer

if Config.ENABLE_WORKFLOW_MEMORY:
    from workflow_memory import WorkflowMemory

if Config.ENABLE_VARIATION_VALIDATION:
    from variation_differentiator import VariationDifferentiator

class AIContentStudioWorkflow:
    """Orchestrates the 3-agent content creation workflow."""
    
    def __init__(self):
        """Initialize workflow with agents."""
        self.writer = WriterAgent()
        self.llmon = LLMONAgent()
        self.editor = EditorAgent()
        
        # Initialize enhancement modules
        self.quality_analyzer = QualityAnalyzer() if Config.ENABLE_QUALITY_SCORING else None
        self.workflow_memory = WorkflowMemory(Config.MEMORY_DIR) if Config.ENABLE_WORKFLOW_MEMORY else None
        self.differentiator = VariationDifferentiator(Config.MIN_VARIATION_DIFFERENCE) if Config.ENABLE_VARIATION_VALIDATION else None
        
        # Initialize session tracking
        self.session_id = get_timestamp()
        self.session_dir = os.path.join(Config.OUTPUTS_DIR, self.session_id)
        ensure_dir(self.session_dir)
        
        # Detect content mode
        self.content_mode = Config.CONTENT_MODE
        
        # Track template and reference paths for quality scoring
        self.template_content = None
        self.references_content = None
        
        print_info(f"Session ID: {self.session_id}")
        
        # Display content mode
        mode_display = "Tool Review" if self.content_mode == 'tool_review' else "General Article"
        print_info(f"Content Mode: {mode_display}")
        
        # Display enabled enhancements
        enhancements = []
        if Config.ENABLE_OUTLINE_PHASE:
            enhancements.append("Outline Generation")
        if Config.ENABLE_PARALLEL_VARIATIONS:
            enhancements.append("Parallel Processing")
        if Config.ENABLE_QUALITY_SCORING:
            enhancements.append("Quality Scoring")
        if Config.ENABLE_WORKFLOW_MEMORY:
            enhancements.append("Workflow Memory")
        if Config.ENABLE_VARIATION_VALIDATION:
            enhancements.append("Variation Validation")
        if Config.ENABLE_MULTIPASS_EDITING:
            enhancements.append("Multi-Pass Editing")
        
        if enhancements:
            print_info(f"Active Enhancements: {', '.join(enhancements)}")
    
    def run(self):
        """Execute the complete workflow."""
        print_header("AI-Content-Studio WORKFLOW")
        print_info("3-Agent Pipeline: WRITER -> LLMON -> EDITOR")
        
        try:
            # Stage 1: Writer Agent
            article = self._writer_stage()
            if article is None:
                return
            
            # Stage 2: LLMON Agent
            selected_article = self._llmon_stage(article)
            if selected_article is None:
                return
            
            # Stage 3: Editor Agent
            final_article = self._editor_stage(selected_article)
            if final_article is None:
                return
            
            # Save final output
            final_path = os.path.join(self.session_dir, "FINAL_ARTICLE.md")
            write_file(final_path, final_article)
            
            print_header("WORKFLOW COMPLETE")
            print_success(f"Final article saved to: {final_path}")
            
        except KeyboardInterrupt:
            print_error("\n\nWorkflow interrupted by user")
        except Exception as e:
            print_error(f"Workflow error: {str(e)}")
    
    def _writer_stage(self):
        """Execute Writer agent stage with optional outline and revision loop."""
        print_header("STAGE 1: WRITER AGENT")
        
        # Define input files based on content mode
        if self.content_mode == 'tool_review':
            manual_path = os.path.join(Config.TEMPLATES_DIR, "tool_review_brief.md")
            template_path = os.path.join(Config.TEMPLATES_DIR, "tool_review_structure.md")
            references_path = os.path.join(Config.TEMPLATES_DIR, "references.md")  # Not used for tool reviews
            prompt_path = os.path.join(Config.TEMPLATES_DIR, "tool_review_writer_prompt.md")
        else:
            manual_path = os.path.join(Config.TEMPLATES_DIR, "manual.md")
            template_path = os.path.join(Config.TEMPLATES_DIR, "template.md")
            references_path = os.path.join(Config.TEMPLATES_DIR, "references.md")
            prompt_path = os.path.join(Config.TEMPLATES_DIR, "writer_prompt.md")
        
        # Load template and references for quality scoring
        if Config.ENABLE_QUALITY_SCORING:
            from utils import read_file
            self.template_content = read_file(template_path)
            self.references_content = read_file(references_path)
        
        # Get historical context if memory is enabled
        historical_context = ""
        if self.workflow_memory:
            historical_context = self.workflow_memory.get_context_for_agent('writer')
        
        # Outline phase (if enabled)
        approved_outline = None
        if Config.ENABLE_OUTLINE_PHASE:
            approved_outline = self._outline_approval_loop(
                manual_path, template_path, references_path, prompt_path, historical_context
            )
            if approved_outline is None:
                return None
        
        # Draft generation
        print_info("Generating initial draft...")
        
        try:
            if Config.ENABLE_OUTLINE_PHASE and approved_outline:
                # Use appropriate method based on content mode
                if self.content_mode == 'tool_review':
                    draft = self.writer.write_from_outline_tool_review(
                        approved_outline, manual_path, template_path, references_path, prompt_path
                    )
                else:
                    draft = self.writer.write_from_outline(
                        approved_outline, manual_path, template_path, references_path, prompt_path
                    )
            else:
                # Use appropriate method based on content mode
                if self.content_mode == 'tool_review':
                    draft = self.writer.generate_draft_tool_review(
                        manual_path, template_path, references_path, prompt_path
                    )
                else:
                    draft = self.writer.generate_draft(
                        manual_path, template_path, references_path, prompt_path
                    )
        except Exception as e:
            print_error(f"Failed to generate draft: {str(e)}")
            return None
        
        # Save draft
        draft_path = os.path.join(self.session_dir, "01_writer_draft.md")
        write_file(draft_path, draft)
        
        # Validate citations
        print_section("CITATION VALIDATION")
        citation_passed, citation_report = validate_citations(draft, references_path)
        print(citation_report)
        
        if not citation_passed:
            print_error("⚠️  WARNING: Citation issues detected!")
            print_info("The draft has missing hyperlinks or hallucinated URLs.")
            print_info("Consider requesting revisions to fix citation issues.")
        
        # Show quality scores
        if self.quality_analyzer:
            scores = self.quality_analyzer.analyze(draft, self.template_content, self.references_content)
            print(self.quality_analyzer.format_score_summary(scores))
        
        # Revision loop
        revision_count = 0
        while True:
            display_content("WRITER'S DRAFT", draft)
            
            choice = get_user_choice(
                "What would you like to do?",
                ["[OK] Approve and continue to LLMON", 
                 "[EDIT] Revise with feedback", 
                 "[STOP] Reject and stop workflow"]
            )
            
            if choice == 1:  # Approve
                print_success("Draft approved!")
                
                # Record approval in memory
                if self.workflow_memory:
                    quality_scores = self.quality_analyzer.analyze(draft, self.template_content, self.references_content) if self.quality_analyzer else None
                    self.workflow_memory.add_approval('writer', quality_scores)
                
                return draft
            
            elif choice == 2:  # Revise
                feedback = get_user_input("Enter your revision feedback:")
                if not feedback:
                    continue
                
                # Record feedback in memory
                if self.workflow_memory:
                    self.workflow_memory.add_feedback('writer', feedback, approved=False, content_snippet=draft)
                
                print_info("Generating revised draft...")
                try:
                    draft = self.writer.revise_draft(draft, feedback)
                    revision_count += 1
                    
                    # Save revision
                    revision_path = os.path.join(
                        self.session_dir, 
                        f"01_writer_draft_rev{revision_count}.md"
                    )
                    write_file(revision_path, draft)
                    
                    # Validate citations after revision
                    print_section("CITATION VALIDATION")
                    citation_passed, citation_report = validate_citations(draft, references_path)
                    print(citation_report)
                    
                    if not citation_passed:
                        print_error("⚠️  WARNING: Citation issues still present!")
                    
                    # Show updated quality scores
                    if self.quality_analyzer:
                        scores = self.quality_analyzer.analyze(draft, self.template_content, self.references_content)
                        print(self.quality_analyzer.format_score_summary(scores))
                    
                except Exception as e:
                    print_error(f"Revision failed: {str(e)}")
            
            elif choice == 3 or choice is None:  # Reject
                print_error("Workflow stopped by user")
                
                # Record rejection in memory
                if self.workflow_memory:
                    self.workflow_memory.add_feedback('writer', "Rejected final draft", approved=False, content_snippet=draft)
                
                return None
    
    def _outline_approval_loop(self, manual_path, template_path, references_path, prompt_path, historical_context):
        """Handle outline generation and approval."""
        print_section("OUTLINE GENERATION PHASE")
        
        # Use appropriate message based on mode
        if self.content_mode == 'tool_review':
            print_info("Generating tool review outline...")
        else:
            print_info("Generating article outline...")
        
        try:
            # Use appropriate method based on content mode
            if self.content_mode == 'tool_review':
                outline = self.writer.generate_outline_tool_review(
                    manual_path, template_path, references_path, prompt_path, historical_context
                )
            else:
                outline = self.writer.generate_outline(
                    manual_path, template_path, references_path, prompt_path, historical_context
                )
        except Exception as e:
            print_error(f"Failed to generate outline: {str(e)}")
            return None
        
        # Save outline
        outline_path = os.path.join(self.session_dir, "01_writer_outline.md")
        write_file(outline_path, outline)
        
        # Outline revision loop
        revision_count = 0
        while True:
            display_content("ARTICLE OUTLINE", outline)
            
            choice = get_user_choice(
                "What would you like to do with this outline?",
                ["[OK] Approve and proceed to writing",
                 "[EDIT] Revise outline with feedback",
                 "[STOP] Reject and stop workflow"]
            )
            
            if choice == 1:  # Approve
                print_success("Outline approved!")
                return outline
            
            elif choice == 2:  # Revise
                feedback = get_user_input("Enter your outline revision feedback:")
                if not feedback:
                    continue
                
                print_info("Revising outline...")
                try:
                    # Use appropriate method based on content mode
                    if self.content_mode == 'tool_review':
                        outline = self.writer.revise_outline_tool_review(outline, feedback)
                    else:
                        outline = self.writer.revise_outline(outline, feedback)
                    revision_count += 1
                    
                    # Save revised outline
                    revised_outline_path = os.path.join(
                        self.session_dir,
                        f"01_writer_outline_rev{revision_count}.md"
                    )
                    write_file(revised_outline_path, outline)
                    
                except Exception as e:
                    print_error(f"Outline revision failed: {str(e)}")
            
            elif choice == 3 or choice is None:  # Reject
                print_error("Workflow stopped by user")
                return None
    
    def _llmon_stage(self, article):
        """Execute LLMON agent stage with iteration loop and enhanced features."""
        print_header("STAGE 2: LLMON AGENT")
        
        # Use appropriate rules based on content mode
        if self.content_mode == 'tool_review':
            rules_path = os.path.join(Config.RULES_DIR, "llmon_tool_review_rules.md")
        else:
            rules_path = os.path.join(Config.RULES_DIR, "llmon_rules.md")
        
        iteration_count = 0
        
        while True:
            print_info(f"Generating {Config.LLMON_VERSIONS_COUNT} article variations...")
            
            if Config.ENABLE_PARALLEL_VARIATIONS:
                print_info("Using parallel generation for faster processing...")
            
            try:
                # Choose method based on content mode
                if self.content_mode == 'tool_review':
                    # Tool review variations preserve story elements and factual details
                    variations = self.llmon.generate_variations_tool_review(
                        article, rules_path, self.differentiator
                    )
                else:
                    # Regular article variations
                    if Config.ENABLE_PARALLEL_VARIATIONS:
                        variations = self.llmon.generate_variations_parallel(
                            article, rules_path, self.differentiator
                        )
                    else:
                        variations = self.llmon.generate_variations(article, rules_path)
                
            except Exception as e:
                print_error(f"Failed to generate variations: {str(e)}")
                return None
            
            # Save variations
            for i, variation in enumerate(variations, 1):
                var_path = os.path.join(
                    self.session_dir, 
                    f"02_llmon_variation{i}_iter{iteration_count}.md"
                )
                write_file(var_path, variation)
            
            # Show differentiation report
            if self.differentiator:
                diff_report = self.differentiator.get_differentiation_report(variations)
                print(diff_report)
            
            # Show quality scores for each variation
            if self.quality_analyzer:
                print_section("VARIATION QUALITY SCORES")
                for i, variation in enumerate(variations, 1):
                    scores = self.quality_analyzer.analyze(variation, self.template_content, self.references_content)
                    print(f"\n--- Variation {i} ---")
                    print(f"Overall: {scores['overall_score']}/100 | "
                          f"Readability: {scores['readability']['score']}/100 | "
                          f"SEO: {scores['seo']['score']}/100 | "
                          f"Engagement: {scores['engagement']['score']}/100")
            
            # Display variations
            for i, variation in enumerate(variations, 1):
                display_content(f"VARIATION {i}", variation, max_lines=25)
            
            # User choice
            options = [f"Select Variation {i}" for i in range(1, len(variations) + 1)]
            options.extend([
                "[RETRY] Iterate with edited rules",
                "[STOP] Reject all and stop workflow"
            ])
            
            choice = get_user_choice("What would you like to do?", options)
            
            if choice and 1 <= choice <= len(variations):  # Select variation
                selected = variations[choice - 1]
                print_success(f"Variation {choice} selected!")
                
                # Record approval in memory
                if self.workflow_memory:
                    quality_scores = self.quality_analyzer.analyze(selected, self.template_content, self.references_content) if self.quality_analyzer else None
                    self.workflow_memory.add_approval('llmon', quality_scores)
                
                return selected
            
            elif choice == len(variations) + 1:  # Iterate with edited rules
                print_section("EDIT LLMON RULES")
                print_info("Current rules will be opened for editing...")
                print_info("Provide your custom rules for the next iteration:")
                
                custom_rules = get_user_input(
                    "Enter modified rules (or press Enter to use original rules):"
                )
                
                # Record feedback in memory
                if self.workflow_memory and custom_rules:
                    self.workflow_memory.add_feedback('llmon', f"Requested iteration with custom rules", approved=False)
                
                if custom_rules:
                    # Save custom rules temporarily
                    temp_rules_path = os.path.join(
                        self.session_dir, 
                        f"02_llmon_custom_rules_iter{iteration_count + 1}.md"
                    )
                    write_file(temp_rules_path, custom_rules)
                    rules_path = temp_rules_path
                
                iteration_count += 1
                continue
            
            else:  # Reject or cancel
                print_error("Workflow stopped by user")
                
                # Record rejection in memory
                if self.workflow_memory:
                    self.workflow_memory.add_feedback('llmon', "Rejected all variations", approved=False)
                
                return None
    
    def _editor_stage(self, article):
        """Execute Editor agent stage with multi-pass editing and revision option."""
        print_header("STAGE 3: EDITOR AGENT")
        
        # Use appropriate rules based on content mode
        if self.content_mode == 'tool_review':
            rules_path = os.path.join(Config.RULES_DIR, "editor_tool_review_rules.md")
            print_info("Polishing tool review with format validation...")
        else:
            rules_path = os.path.join(Config.RULES_DIR, "editor_rules.md")
        
        # Choose method based on content mode
        if self.content_mode == 'tool_review':
            # Tool review polishing with special format validation
            try:
                polished = self.editor.polish_article_tool_review(article, rules_path)
            except Exception as e:
                print_error(f"Failed to polish tool review: {str(e)}")
                return None
        else:
            # Regular article polishing
            if Config.ENABLE_MULTIPASS_EDITING:
                print_info("Polishing article with multi-pass editing...")
                print_info("Pass 1: Grammar & Mechanics -> Pass 2: Style & Voice -> Pass 3: Flow & Transitions -> Pass 4: Final Consistency")
                
                try:
                    polished = self.editor.polish_article_multipass(article, rules_path)
                except Exception as e:
                    print_error(f"Failed to polish article: {str(e)}")
                    return None
            else:
                print_info("Polishing article...")
                
                try:
                    polished = self.editor.polish_article(article, rules_path)
                except Exception as e:
                    print_error(f"Failed to polish article: {str(e)}")
                    return None
        
        # Save polished version
        polished_path = os.path.join(self.session_dir, "03_editor_polished.md")
        write_file(polished_path, polished)
        
        # Show quality scores
        if self.quality_analyzer:
            scores = self.quality_analyzer.analyze(polished, self.template_content, self.references_content)
            print(self.quality_analyzer.format_score_summary(scores))
        
        # Minor revision loop
        revision_count = 0
        while True:
            display_content("POLISHED ARTICLE", polished)
            
            choice = get_user_choice(
                "What would you like to do?",
                ["[OK] Approve as final output",
                 "[EDIT] Request minor revisions",
                 "[STOP] Reject and stop workflow"]
            )
            
            if choice == 1:  # Approve
                print_success("Article approved as final!")
                
                # Record approval in memory
                if self.workflow_memory:
                    quality_scores = self.quality_analyzer.analyze(polished, self.template_content, self.references_content) if self.quality_analyzer else None
                    self.workflow_memory.add_approval('editor', quality_scores)
                    
                    # Extract and save preferences
                    self.workflow_memory.extract_preferences()
                
                return polished
            
            elif choice == 2:  # Request revisions
                revision_notes = get_user_input("Enter your revision requests:")
                if not revision_notes:
                    continue
                
                # Record feedback in memory
                if self.workflow_memory:
                    self.workflow_memory.add_feedback('editor', revision_notes, approved=False, content_snippet=polished)
                
                print_info("Applying revisions...")
                try:
                    polished = self.editor.apply_minor_revisions(polished, revision_notes)
                    revision_count += 1
                    
                    # Save revision
                    revision_path = os.path.join(
                        self.session_dir,
                        f"03_editor_polished_rev{revision_count}.md"
                    )
                    write_file(revision_path, polished)
                    
                    # Show updated quality scores
                    if self.quality_analyzer:
                        scores = self.quality_analyzer.analyze(polished, self.template_content, self.references_content)
                        print(self.quality_analyzer.format_score_summary(scores))
                    
                except Exception as e:
                    print_error(f"Revision failed: {str(e)}")
            
            elif choice == 3 or choice is None:  # Reject
                print_error("Workflow stopped by user")
                
                # Record rejection in memory
                if self.workflow_memory:
                    self.workflow_memory.add_feedback('editor', "Rejected final polish", approved=False, content_snippet=polished)
                
                return None


