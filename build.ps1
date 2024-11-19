# Stop on any error
$ErrorActionPreference = "Stop"

Write-Host "Starting DMV Quiz build process..." -ForegroundColor Green

try {
    # Clean previous build artifacts
    Write-Host "Cleaning previous build artifacts..." -ForegroundColor Yellow
    Remove-Item -Path "dist" -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path "build" -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path "__pycache__" -Recurse -ErrorAction SilentlyContinue

    # Install/Update dependencies
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

    # Run tests
    Write-Host "Running tests..." -ForegroundColor Yellow
    python -m pytest test_dmv_quiz.py -v
    if ($LASTEXITCODE -ne 0) {
        throw "Tests failed!"
    }

    # Build the application
    Write-Host "Building application..." -ForegroundColor Yellow
    python -m PyInstaller `
        --name="DMV Quiz" `
        --windowed `
        --icon="src/assets/app_icon.ico" `
        --add-data="questions_db.json;." `
        --add-data="src/assets;src/assets" `
        --hidden-import="PIL._tkinter_finder" `
        --hidden-import="customtkinter" `
        --clean `
        --noconfirm `
        main.py
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller build failed!"
    }

    # Create release directory
    $version = "1.0.0"
    $releaseDir = "release_v$version"
    Write-Host "Creating release package v$version..." -ForegroundColor Yellow
    
    # Remove existing release directory if it exists
    Remove-Item -Path $releaseDir -Recurse -ErrorAction SilentlyContinue
    New-Item -Path $releaseDir -ItemType Directory -Force | Out-Null

    # Copy release files
    Copy-Item -Path "dist/DMV Quiz/*" -Destination $releaseDir -Recurse
    Copy-Item -Path "README.md" -Destination $releaseDir
    Copy-Item -Path "LICENSE" -Destination $releaseDir -ErrorAction SilentlyContinue

    # Create release archive
    Remove-Item -Path "DMVQuiz_v$version.zip" -ErrorAction SilentlyContinue
    Compress-Archive -Path "$releaseDir/*" -DestinationPath "DMVQuiz_v$version.zip" -Force

    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "Release package created: DMVQuiz_v$version.zip" -ForegroundColor Green
}
catch {
    Write-Host "Build failed: $_" -ForegroundColor Red
    exit 1
}
