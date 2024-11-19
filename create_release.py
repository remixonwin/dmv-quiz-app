import os
import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import argparse

def create_github_release(token, repo_owner, repo_name, tag_name, name, body, files):
    """
    Create a new GitHub release and upload assets.
    
    Args:
        token (str): GitHub personal access token
        repo_owner (str): Repository owner
        repo_name (str): Repository name
        tag_name (str): Tag name for the release
        name (str): Release title
        body (str): Release description
        files (list): List of file paths to upload
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Create release
    release_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases'
    release_data = {
        'tag_name': tag_name,
        'name': name,
        'body': body,
        'draft': False,
        'prerelease': False
    }

    try:
        response = requests.post(release_url, headers=headers, json=release_data)
        response.raise_for_status()
        release = response.json()
        print(f"Created release: {release['name']}")

        # Upload assets
        upload_url = release['upload_url'].split('{')[0]
        for file_path in files:
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}")
                continue

            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                file_data = f.read()

            upload_headers = headers.copy()
            upload_headers['Content-Type'] = 'application/octet-stream'
            upload_response = requests.post(
                f"{upload_url}?name={file_name}",
                headers=upload_headers,
                data=file_data
            )
            upload_response.raise_for_status()
            print(f"Uploaded: {file_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error creating release: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None

    return release

def main():
    parser = argparse.ArgumentParser(description='Create a GitHub release for DMV Quiz')
    parser.add_argument('--owner', required=True, help='Repository owner')
    parser.add_argument('--repo', required=True, help='Repository name')
    args = parser.parse_args()

    # Load GitHub token from .env
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN not found in environment variables")
        return

    # Release information
    current_time = datetime.now()
    version = current_time.strftime('v%Y.%m.%d.%H%M')
    
    release_info = {
        'tag_name': version,
        'name': f'DMV Quiz {version}',
        'body': f"""# DMV Quiz Application Release {version}

## What's New
- Verified executable with all tests passing
- Comprehensive test suite (16 tests)
- Enhanced documentation with keyboard shortcuts
- Improved error handling and stability
- Custom application icon

## Features
- Interactive quiz interface with modern design
- Practice and Test modes
- Real-time score tracking
- High score management
- Sound feedback
- Dark mode support
- Keyboard navigation

## Installation
1. Download the DMVQuiz_v1.0.0.zip file
2. Extract the contents
3. Run DMV Quiz.exe
4. No installation required - runs directly on Windows

## System Requirements
- Windows 10 or later
- 2GB RAM minimum
- 100MB free disk space
- 1024x768 minimum screen resolution

## Notes
- Standalone executable with all dependencies included
- No internet connection required
- Local-only operation for privacy
- Regular updates planned

## Keyboard Shortcuts
- Enter: Start Quiz / Confirm
- Space: Next Question
- Backspace: Previous Question
- 1-4: Select Answer (A-D)
- Esc: Exit Quiz / Return
- R: Restart Quiz
- D: Toggle Dark Mode
- F: Toggle Fullscreen

## Need Help?
Visit our [Documentation](https://github.com/{args.owner}/{args.repo}#readme) for:
- Detailed usage instructions
- Troubleshooting guide
- Development setup
"""
    }

    # Files to upload
    release_info['files'] = ['DMVQuiz_v1.0.0.zip']

    print("\nCreating release with the following information:")
    print(json.dumps(release_info, indent=2))
    
    release = create_github_release(
        token,
        args.owner,
        args.repo,
        release_info['tag_name'],
        release_info['name'],
        release_info['body'],
        release_info['files']
    )
    
    if release:
        print(f"\nRelease created successfully!")
        print(f"Download URL: {release['html_url']}")

if __name__ == '__main__':
    main()
