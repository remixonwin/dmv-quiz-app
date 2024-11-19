# DMV Quiz Application

A comprehensive Windows desktop application for driver's license exam preparation.

## Quick Start ⚡

### [⬇️ Download DMVQuiz.exe](https://github.com/remixonwin/dmv-quiz-app/releases/latest/download/DMVQuiz.exe)

1. Click the download link above
2. Double-click the downloaded `DMVQuiz.exe`
3. Start practicing for your DMV test!

## Features

- Interactive quiz interface with modern design
- Comprehensive DMV question database
- Real-time score tracking and progress monitoring
- Immediate feedback on answers
- Practice mode for learning
- Test mode to simulate real exam
- Review mode for missed questions
- Dark mode support
- Keyboard shortcuts for quick navigation
- Standalone executable - no installation needed

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
- Minimum 2GB RAM
- 100MB free disk space
- 1024x768 minimum screen resolution

## How to Use

1. **Starting a Quiz**
   - Launch the application
   - Click "Start Quiz" or press `Enter`
   - Choose your quiz mode (Practice/Test)

2. **During the Quiz**
   - Read the question carefully
   - Select your answer (A, B, C, or D)
   - Click "Next" or press `Space` to proceed
   - Use "Previous" or press `Backspace` to review earlier questions

3. **Reviewing Results**
   - View your score at the end
   - Review incorrect answers
   - See detailed explanations
   - Track your progress over time

## Keyboard Shortcuts

| Key           | Action                    |
|---------------|---------------------------|
| `Enter`       | Start Quiz / Confirm     |
| `Space`       | Next Question            |
| `Backspace`   | Previous Question        |
| `1-4`         | Select Answer (A-D)      |
| `Esc`         | Exit Quiz / Return       |
| `R`           | Restart Quiz             |
| `D`           | Toggle Dark Mode         |
| `F`           | Toggle Fullscreen        |

## Troubleshooting

### Common Issues

1. **App won't start**
   - Verify Windows 10 or later
   - Run as administrator
   - Check antivirus settings
   - Ensure sufficient disk space

2. **Windows SmartScreen warning**
   - This is normal for new applications
   - Click "More info"
   - Select "Run anyway"
   - The app is safe to use

3. **Display issues**
   - Ensure 1024x768 minimum resolution
   - Update graphics drivers
   - Try windowed mode (press `F`)

4. **Performance issues**
   - Close other applications
   - Ensure 2GB free RAM
   - Restart the application

### Need Help?

If you encounter any issues:
1. Check the troubleshooting guide above
2. [Submit an issue](https://github.com/remixonwin/dmv-quiz-app/issues)
3. Include your Windows version and error details

## Development

To build from source:

1. Clone the repository:
   ```bash
   git clone https://github.com/remixonwin/dmv-quiz-app.git
   cd dmv-quiz-app
   ```

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
- No data collection or tracking
- No internet connection required
- Local-only operation
- Secure token management for development
- Regular security updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints
- Write unit tests for new features

## Updates

- Check the [Releases page](https://github.com/remixonwin/dmv-quiz-app/releases) for new versions
- Each release includes:
  * New features and improvements
  * Bug fixes
  * Security updates
  * Updated question database

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- Icons by [Material Design Icons](https://materialdesignicons.com/)
- UI Framework: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Question Database: Official DMV materials
