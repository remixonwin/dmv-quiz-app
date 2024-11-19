import os
import requests
import subprocess
import json

def create_github_repo(token, username, repo_name):
    """Create a new GitHub repository"""
    print("Step 1: Creating/Checking GitHub repository...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    api_url = f'https://api.github.com/repos/{username}/{repo_name}'
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 404:
        # Repository doesn't exist, create it
        create_url = 'https://api.github.com/user/repos'
        data = {
            'name': repo_name,
            'description': 'An interactive DMV quiz application for driver\'s license exam preparation',
            'private': False
        }
        response = requests.post(create_url, headers=headers, json=data)
        if response.status_code != 201:
            print(f"Error creating repository: {response.json().get('message', 'Unknown error')}")
            return False
        print("Repository created successfully!")
    else:
        print("Repository already exists!")
    return True

def push_to_github(username, token, repo_name):
    """Push code to GitHub"""
    print("\nStep 2: Pushing code to GitHub...")
    
    try:
        # Remove existing origin if it exists
        subprocess.run(['git', 'remote', 'remove', 'origin'], 
                      stderr=subprocess.DEVNULL, 
                      stdout=subprocess.DEVNULL)
        print("Removed existing remote origin")
    except:
        pass

    commands = [
        ['git', 'remote', 'add', 'origin', f'https://{token}@github.com/{username}/{repo_name}.git'],
        ['git', 'branch', '-M', 'main'],
        ['git', 'push', '-u', 'origin', 'main', '--force']
    ]

    for cmd in commands:
        try:
            print(f"Executing: {' '.join(cmd[:2])}...")  # Only show first two parts of command for security
            result = subprocess.run(cmd, 
                                 capture_output=True, 
                                 text=True)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error executing command: {str(e)}")
            return False

    print("Code pushed successfully!")
    return True

def main():
    # Configuration
    username = "remixonwin"
    repo_name = "dmv-quiz-app"
    
    print("=== DMV Quiz App - GitHub Setup ===")
    token = input("Enter your GitHub Personal Access Token: ").strip()
    
    if not token:
        print("Error: Token is required!")
        return
    
    if create_github_repo(token, username, repo_name):
        if push_to_github(username, token, repo_name):
            print("\n✓ Setup completed successfully!")
            print(f"Visit your repository at: https://github.com/{username}/{repo_name}")
        else:
            print("\n✗ Failed to push code to GitHub")
    else:
        print("\n✗ Repository setup failed")

if __name__ == "__main__":
    main()
