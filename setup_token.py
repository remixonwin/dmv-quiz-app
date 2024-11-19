"""
Secure GitHub Token Setup Script
This script helps securely set up your GitHub token with proper permissions and security measures.
Usage: 
1. python setup_token.py                 # Will prompt for token
2. python setup_token.py YOUR_TOKEN      # Pass token as argument
"""
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

def validate_token(token):
    """Validate GitHub token and check its permissions."""
    headers = {'Authorization': f'token {token}'}
    
    try:
        # Check authentication
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        if response.status_code != 200:
            return False, "Authentication failed. Invalid token."
            
        # Check token permissions
        response = requests.get('https://api.github.com/user/repos', headers=headers, timeout=10)
        if response.status_code != 200:
            return False, "Token lacks required repository permissions."
            
        return True, "Token validation successful!"
    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {str(e)}"

def create_env_file(token):
    """Securely create .env file with the token."""
    env_path = Path('.env')
    
    # Backup existing .env if it exists
    if env_path.exists():
        backup_path = Path(f'.env.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        env_path.rename(backup_path)
        print(f"Backed up existing .env to {backup_path}")
    
    # Create new .env file with secure permissions
    try:
        with open(env_path, 'w') as f:
            f.write(f'GITHUB_TOKEN={token}\n')
        
        # Set file permissions to be readable only by owner
        if os.name != 'nt':  # Unix-like systems
            os.chmod(env_path, 0o600)
        
        print("Created .env file with secure permissions")
        return True
    except Exception as e:
        print(f"Error creating .env file: {str(e)}")
        return False

def setup_gitignore():
    """Ensure .env is in .gitignore."""
    gitignore_path = Path('.gitignore')
    env_patterns = {'.env', '.env.*', '*.env'}
    
    # Read existing patterns or create new file
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            patterns = set(f.read().splitlines())
    else:
        patterns = set()
    
    # Add missing patterns
    missing_patterns = env_patterns - patterns
    if missing_patterns:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Environment variables\n')
            for pattern in missing_patterns:
                f.write(f'{pattern}\n')
        print("Updated .gitignore with environment file patterns")

def main():
    print("=== Secure GitHub Token Setup ===")
    
    # Get token from command line argument or environment
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
    else:
        # Try to read from existing .env file first
        env_path = Path('.env')
        if env_path.exists():
            try:
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('GITHUB_TOKEN='):
                            token = line.split('=', 1)[1].strip()
                            print("Found existing token in .env file")
                            break
            except Exception:
                pass
    
    # If no token found, show usage
    if not token:
        print("\nNo token provided. Please use one of these methods:")
        print("1. python setup_token.py YOUR_TOKEN")
        print("2. Create .env file with GITHUB_TOKEN=YOUR_TOKEN")
        sys.exit(1)
    
    # Validate token
    print("\nValidating token...")
    is_valid, message = validate_token(token)
    if not is_valid:
        print(f"Error: {message}")
        sys.exit(1)
    print(message)
    
    # Create .env file
    if not create_env_file(token):
        sys.exit(1)
    
    # Update .gitignore
    setup_gitignore()
    
    print("\nToken setup completed successfully!")
    print("\nSecurity Reminders:")
    print("- Keep your .env file secure and never commit it")
    print("- Regenerate your token before it expires")
    print("- Review GitHub security alerts regularly")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)
