"""Test script to verify AI-Content-Studio setup."""
import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def print_header(text):
    """Print test header."""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text.center(60)}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_test(name, passed, message=""):
    """Print test result."""
    if passed:
        print(f"{Fore.GREEN}✓ {name}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ {name}{Style.RESET_ALL}")
        if message:
            print(f"  {Fore.YELLOW}→ {message}{Style.RESET_ALL}")

def test_python_version():
    """Test Python version."""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 8
    message = f"Python {version.major}.{version.minor}.{version.micro} " + \
              ("(OK)" if passed else "(Need 3.8+)")
    return passed, message

def test_dependencies():
    """Test required dependencies."""
    dependencies = {
        'google.generativeai': 'google-generativeai',
        'dotenv': 'python-dotenv',
        'colorama': 'colorama'
    }
    
    missing = []
    for module, package in dependencies.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    passed = len(missing) == 0
    message = "All installed" if passed else f"Missing: {', '.join(missing)}"
    return passed, message

def test_env_file():
    """Test .env file existence and content."""
    if not os.path.exists('.env'):
        return False, ".env file not found. Run: python setup_env.py"
    
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'GEMINI_API_KEY' not in content:
        return False, "GEMINI_API_KEY not found in .env"
    
    if 'your_api_key_here' in content or 'AIza' not in content:
        return False, "API key appears to be placeholder. Add your real key."
    
    return True, "API key configured"

def test_directory_structure():
    """Test required directories."""
    required_dirs = ['templates', 'rules', 'agents']
    missing = [d for d in required_dirs if not os.path.exists(d)]
    
    passed = len(missing) == 0
    message = "All present" if passed else f"Missing: {', '.join(missing)}"
    return passed, message

def test_template_files():
    """Test template files."""
    required_files = [
        'templates/manual.md',
        'templates/template.md',
        'templates/references.md',
        'templates/writer_prompt.md'
    ]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    
    passed = len(missing) == 0
    message = "All present" if passed else f"Missing: {', '.join(missing)}"
    return passed, message

def test_rules_files():
    """Test rules files."""
    required_files = [
        'rules/llmon_rules.md',
        'rules/editor_rules.md'
    ]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    
    passed = len(missing) == 0
    message = "All present" if passed else f"Missing: {', '.join(missing)}"
    return passed, message

def test_agent_modules():
    """Test agent module files."""
    required_files = [
        'agents/__init__.py',
        'agents/writer_agent.py',
        'agents/llmon_agent.py',
        'agents/editor_agent.py'
    ]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    
    passed = len(missing) == 0
    message = "All present" if passed else f"Missing: {', '.join(missing)}"
    return passed, message

def test_core_files():
    """Test core application files."""
    required_files = [
        'main.py',
        'workflow.py',
        'config.py',
        'api_client.py',
        'utils.py'
    ]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    
    passed = len(missing) == 0
    message = "All present" if passed else f"Missing: {', '.join(missing)}"
    return passed, message

def test_manual_filled():
    """Test if manual.md appears to be filled out."""
    if not os.path.exists('templates/manual.md'):
        return False, "manual.md not found"
    
    with open('templates/manual.md', 'r') as f:
        content = f.read()
    
    # Check for placeholder brackets
    placeholders = content.count('[') + content.count(']')
    
    if placeholders > 20:  # Still has many placeholders
        return False, "Appears unfilled (has many placeholders)"
    
    if len(content) < 100:
        return False, "Content too short"
    
    return True, "Appears to be filled out"

def main():
    """Run all setup tests."""
    print_header("AI-Content-Studio - SETUP VERIFICATION")
    
    print(f"{Fore.YELLOW}Running setup tests...{Style.RESET_ALL}\n")
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies Installed", test_dependencies),
        ("Environment File (.env)", test_env_file),
        ("Directory Structure", test_directory_structure),
        ("Template Files", test_template_files),
        ("Rules Files", test_rules_files),
        ("Agent Modules", test_agent_modules),
        ("Core Application Files", test_core_files),
        ("Content Brief (manual.md)", test_manual_filled),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed, message = test_func()
            print_test(f"{test_name}: {message}", passed)
            results.append(passed)
        except Exception as e:
            print_test(f"{test_name}: Error", False, str(e))
            results.append(False)
    
    # Summary
    passed_count = sum(results)
    total_count = len(results)
    
    print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}Results: {passed_count}/{total_count} tests passed{Style.RESET_ALL}\n")
    
    if passed_count == total_count:
        print(f"{Fore.GREEN}{'✓ ALL TESTS PASSED!'}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}Your setup is complete and ready to use!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Next step:{Style.RESET_ALL}")
        print(f"  Run: {Fore.YELLOW}python main.py{Style.RESET_ALL}\n")
        return 0
    else:
        print(f"{Fore.YELLOW}⚠ SOME TESTS FAILED{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Please fix the issues above before running the workflow.{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Quick fixes:{Style.RESET_ALL}")
        print(f"  Dependencies: {Fore.YELLOW}pip install -r requirements.txt{Style.RESET_ALL}")
        print(f"  API Key: {Fore.YELLOW}python setup_env.py{Style.RESET_ALL}")
        print(f"  Content Brief: {Fore.YELLOW}Edit templates/manual.md{Style.RESET_ALL}\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Test interrupted by user{Style.RESET_ALL}")
        sys.exit(1)


