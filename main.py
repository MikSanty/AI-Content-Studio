"""Main entry point for AI-Content-Studio Workflow."""
import sys
from workflow import AIContentStudioWorkflow
from utils import print_header, print_error, print_info
from colorama import Fore, Style

def main():
    """Run the AI-Content-Studio workflow."""
    from config import Config
    
    print_header("AI-Content-Studio")
    print_info("3-Agent Workflow: WRITER -> LLMON -> EDITOR")
    print()
    
    # Show current AI provider and model configuration
    provider_display = Config.AI_PROVIDER.upper()
    if Config.AI_PROVIDER == 'openai':
        print(f"{Fore.CYAN}AI Provider: {provider_display}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Writer Agent:  {Config.OPENAI_WRITER_MODEL}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  LLMON Agent:   {Config.OPENAI_LLMON_MODEL}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Editor Agent:  {Config.OPENAI_EDITOR_MODEL}{Style.RESET_ALL}")
    else:
        model_display = Config.MODEL_NAME
        print(f"{Fore.CYAN}AI Provider: {provider_display} ({model_display}){Style.RESET_ALL}")
    print()
    
    print(f"{Fore.CYAN}Before starting, ensure you have:{Style.RESET_ALL}")
    print(f"  1. Set up your .env file with {Config.AI_PROVIDER.upper()}_API_KEY")
    print(f"  2. Filled out templates/manual.md with your content brief")
    print(f"  3. Reviewed templates/template.md for article structure")
    print(f"  4. Added references to templates/references.md")
    print()
    
    try:
        workflow = AIContentStudioWorkflow()
        workflow.run()
    except ValueError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()


