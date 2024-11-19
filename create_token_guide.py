"""
GitHub Token Creation Guide

This script will guide you through creating a secure GitHub token with minimum required permissions.
"""

def print_instructions():
    print("\n=== GitHub Token Creation Guide ===\n")
    print("1. Go to GitHub Settings:")
    print("   https://github.com/settings/tokens\n")
    
    print("2. Click 'Generate new token (classic)'\n")
    
    print("3. Set the following:")
    print("   - Note: DMV Quiz App Deployment")
    print("   - Expiration: 30 days (recommended)")
    print("   - Select only these permissions:")
    print("     [x] repo (Full control of private repositories)")
    print("     [x] workflow (Update GitHub Action workflows)")
    print("\n")
    
    print("4. Click 'Generate token'\n")
    
    print("5. Copy the generated token\n")
    
    print("6. Create a .env file in your project root with:")
    print("   GITHUB_TOKEN=your_token_here\n")
    
    print("Security Best Practices:")
    print("- Never commit the token to version control")
    print("- Regenerate the token periodically")
    print("- Use the minimum required permissions")
    print("- Keep the .env file secure\n")

if __name__ == "__main__":
    print_instructions()
