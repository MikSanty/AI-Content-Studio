"""Utility functions for the AI-Content-Studio Workflow."""
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def ensure_dir(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_file(filepath):
    """Read and return file contents."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File not found: {filepath}{Style.RESET_ALL}")
        return None

def write_file(filepath, content):
    """Write content to file."""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{Fore.GREEN}✓ Saved: {filepath}{Style.RESET_ALL}")

def get_timestamp():
    """Get current timestamp for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def print_header(text):
    """Print a styled header."""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text.center(60)}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_section(text):
    """Print a styled section header."""
    print(f"\n{Fore.YELLOW}{'─'*60}")
    print(f"{Fore.YELLOW}{text}")
    print(f"{Fore.YELLOW}{'─'*60}{Style.RESET_ALL}\n")

def print_success(text):
    """Print success message."""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message."""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    """Print info message."""
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")

def get_user_choice(prompt, options):
    """Get user choice from options."""
    print(f"\n{Fore.CYAN}{prompt}{Style.RESET_ALL}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            choice = input(f"\n{Fore.GREEN}Enter your choice (1-{len(options)}): {Style.RESET_ALL}")
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num
            else:
                print_error(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print_error("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n")
            return None

def get_user_input(prompt):
    """Get text input from user."""
    try:
        return input(f"\n{Fore.CYAN}{prompt}{Style.RESET_ALL}\n> ")
    except KeyboardInterrupt:
        print("\n")
        return None

def display_content(title, content, max_lines=30):
    """Display content with optional truncation."""
    print_section(title)
    lines = content.split('\n')
    if len(lines) > max_lines:
        print('\n'.join(lines[:max_lines]))
        print(f"\n{Fore.YELLOW}... ({len(lines) - max_lines} more lines) ...{Style.RESET_ALL}")
    else:
        print(content)


