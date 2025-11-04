@echo off
REM Emoji == Movie - Quick Start Script for Windows

echo 🎬 Emoji == Movie - Starting Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo 📥 Installing dependencies...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating .env file...
    (
        echo PORT=8000
        echo HOST=0.0.0.0
        echo ENVIRONMENT=development
    ) > .env
)

echo.
echo ✅ Setup complete!
echo.
echo 🚀 Starting server at http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the application
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

