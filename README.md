# DMV Quiz Application

A comprehensive Windows desktop application for driver's license exam preparation.

## Quick Start ⚡

### [⬇️ Download DMVQuiz.exe](https://github.com/remixonwin/dmv-quiz-app/releases/latest/download/DMVQuiz.exe)

1. Click the download link above
2. Double-click the downloaded `DMVQuiz.exe`
3. Start practicing for your DMV test!

## Features

- Interactive quiz interface
- Comprehensive question database
- Score tracking and progress monitoring
- User-friendly design
- Standalone Windows executable

## Detailed Installation Steps

1. Visit the [Latest Release Page](https://github.com/remixonwin/dmv-quiz-app/releases/latest)
2. Under "Assets", click `DMVQuiz.exe` to download
3. If Windows SmartScreen appears:
   - Click "More info"
   - Click "Run anyway" (the app is safe but not yet signed)
4. Double-click `DMVQuiz.exe` to run the application

No installation required - the application runs directly on Windows!

## System Requirements

- Windows 10 or later
- No additional software required

## Usage

1. Launch the application by double-clicking `DMVQuiz.exe`
2. Click "Start Quiz" to begin
3. Select your answer for each question
4. View your score and review incorrect answers at the end
5. Use "Try Again" to restart the quiz

## Development

To build from source:

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Building the Executable

To create the executable:

```bash
pyinstaller --onefile --windowed --name DMVQuiz --icon=src/assets/app.ico --add-data "questions_db.json;." --add-data "src/assets;assets" main.py
```

## Security

This application prioritizes security:
- No data collection
- No internet connection required
- Local-only operation
- Secure token management for development

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
