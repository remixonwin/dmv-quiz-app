# Install required packages
pip install -r requirements.txt

# Build the executable
pyinstaller --onefile --windowed --name "WindowsApp" main.py
