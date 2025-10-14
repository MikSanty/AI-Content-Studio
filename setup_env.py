"""Helper script to create .env file with API key."""
import os

def setup_env():
    """Interactive setup for .env file."""
    print("=" * 60)
    print("AI-Content-Studio - Environment Setup")
    print("=" * 60)
    print()
    
    if os.path.exists('.env'):
        print("[WARNING] .env file already exists!")
        response = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Setup cancelled.")
            return
    
    print("\nTo get your free Gemini API key:")
    print("1. Visit: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the key")
    print()
    
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"# Google Gemini API Configuration\n")
        f.write(f"GEMINI_API_KEY={api_key}\n")
    
    print("\n✅ .env file created successfully!")
    print("\nNext steps:")
    print("1. Fill out templates/manual.md with your content brief")
    print("2. Add references to templates/references.md")
    print("3. Run: python main.py")
    print()

if __name__ == "__main__":
    setup_env()


