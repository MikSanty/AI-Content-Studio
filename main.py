"""Main entry point for AI-Content-Studio Workflow."""
import sys
from workflow import ContentScalingWorkflow
from utils import print_header, print_error, print_info
from colorama import Fore, Style

def main():
    """Run the AI-Content-Studio workflow."""
    print_header("AI-Content-Studio")
    print_info("3-Agent Workflow: WRITER → LLMON → EDITOR")
    print()
    print(f"{Fore.CYAN}Before starting, ensure you have:{Style.RESET_ALL}")
    print(f"  1. Set up your .env file with GEMINI_API_KEY")
    print(f"  2. Filled out templates/manual.md with your content brief")
    print(f"  3. Reviewed templates/template.md for article structure")
    print(f"  4. Added references to templates/references.md")
    print()
    
    try:
        workflow = ContentScalingWorkflow()
        workflow.run()
    except ValueError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()


