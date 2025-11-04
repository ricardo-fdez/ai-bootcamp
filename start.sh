#!/bin/bash
# Emoji == Movie - Quick Start Script

echo "🎬 Emoji == Movie - Starting Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << EOF
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development
EOF
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting server at http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the application
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

