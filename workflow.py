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

class AIContentStudioWorkflow:
    """Orchestrates the 3-agent content creation workflow."""
    
    def __init__(self):
        """Initialize workflow with agents."""
        self.writer = WriterAgent()
        self.llmon = LLMONAgent()
        self.editor = EditorAgent()
        
        # Initialize session tracking
        self.session_id = get_timestamp()
        self.session_dir = os.path.join(Config.OUTPUTS_DIR, self.session_id)
        ensure_dir(self.session_dir)
        
        print_info(f"Session ID: {self.session_id}")
    
    def run(self):
        """Execute the complete workflow."""
        print_header("AI-Content-Studio WORKFLOW")
        print_info("3-Agent Pipeline: WRITER → LLMON → EDITOR")
        
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
        """Execute Writer agent stage with revision loop."""
        print_header("STAGE 1: WRITER AGENT")
        
        # Define input files
        manual_path = os.path.join(Config.TEMPLATES_DIR, "manual.md")
        template_path = os.path.join(Config.TEMPLATES_DIR, "template.md")
        references_path = os.path.join(Config.TEMPLATES_DIR, "references.md")
        prompt_path = os.path.join(Config.TEMPLATES_DIR, "writer_prompt.md")
        
        print_info("Generating initial draft...")
        
        try:
            draft = self.writer.generate_draft(
                manual_path, template_path, references_path, prompt_path
            )
        except Exception as e:
            print_error(f"Failed to generate draft: {str(e)}")
            return None
        
        # Save draft
        draft_path = os.path.join(self.session_dir, "01_writer_draft.md")
        write_file(draft_path, draft)
        
        # Revision loop
        revision_count = 0
        while True:
            display_content("WRITER'S DRAFT", draft)
            
            choice = get_user_choice(
                "What would you like to do?",
                ["✓ Approve and continue to LLMON", 
                 "✎ Revise with feedback", 
                 "✗ Reject and stop workflow"]
            )
            
            if choice == 1:  # Approve
                print_success("Draft approved!")
                return draft
            
            elif choice == 2:  # Revise
                feedback = get_user_input("Enter your revision feedback:")
                if not feedback:
                    continue
                
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
                    
                except Exception as e:
                    print_error(f"Revision failed: {str(e)}")
            
            elif choice == 3 or choice is None:  # Reject
                print_error("Workflow stopped by user")
                return None
    
    def _llmon_stage(self, article):
        """Execute LLMON agent stage with iteration loop."""
        print_header("STAGE 2: LLMON AGENT")
        
        rules_path = os.path.join(Config.RULES_DIR, "llmon_rules.md")
        iteration_count = 0
        
        while True:
            print_info(f"Generating {Config.LLMON_VERSIONS_COUNT} article variations...")
            
            try:
                if iteration_count == 0:
                    variations = self.llmon.generate_variations(article, rules_path)
                else:
                    # User has provided custom rules in previous iteration
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
            
            # Display variations
            for i, variation in enumerate(variations, 1):
                display_content(f"VARIATION {i}", variation, max_lines=25)
            
            # User choice
            options = [f"Select Variation {i}" for i in range(1, len(variations) + 1)]
            options.extend([
                "↻ Iterate with edited rules",
                "✗ Reject all and stop workflow"
            ])
            
            choice = get_user_choice("What would you like to do?", options)
            
            if choice and 1 <= choice <= len(variations):  # Select variation
                selected = variations[choice - 1]
                print_success(f"Variation {choice} selected!")
                return selected
            
            elif choice == len(variations) + 1:  # Iterate with edited rules
                print_section("EDIT LLMON RULES")
                print_info("Current rules will be opened for editing...")
                print_info("Provide your custom rules for the next iteration:")
                
                custom_rules = get_user_input(
                    "Enter modified rules (or press Enter to use original rules):"
                )
                
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
                return None
    
    def _editor_stage(self, article):
        """Execute Editor agent stage with revision option."""
        print_header("STAGE 3: EDITOR AGENT")
        
        rules_path = os.path.join(Config.RULES_DIR, "editor_rules.md")
        
        print_info("Polishing article...")
        
        try:
            polished = self.editor.polish_article(article, rules_path)
        except Exception as e:
            print_error(f"Failed to polish article: {str(e)}")
            return None
        
        # Save polished version
        polished_path = os.path.join(self.session_dir, "03_editor_polished.md")
        write_file(polished_path, polished)
        
        # Minor revision loop
        revision_count = 0
        while True:
            display_content("POLISHED ARTICLE", polished)
            
            choice = get_user_choice(
                "What would you like to do?",
                ["✓ Approve as final output",
                 "✎ Request minor revisions",
                 "✗ Reject and stop workflow"]
            )
            
            if choice == 1:  # Approve
                print_success("Article approved as final!")
                return polished
            
            elif choice == 2:  # Request revisions
                revision_notes = get_user_input("Enter your revision requests:")
                if not revision_notes:
                    continue
                
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
                    
                except Exception as e:
                    print_error(f"Revision failed: {str(e)}")
            
            elif choice == 3 or choice is None:  # Reject
                print_error("Workflow stopped by user")
                return None


