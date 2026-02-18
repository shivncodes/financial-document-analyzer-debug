#!/bin/bash
# Script to run the Financial Document Analyzer

# Activate virtual environment
source venv/bin/activate

# Check if packages are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies (this may take 5-10 minutes)..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please create .env file with your API keys:"
    echo "   cp .env.example .env"
    echo "   Then edit .env and add your GEMINI_API_KEY and SERPER_API_KEY"
    exit 1
fi

# Run the application
echo "🚀 Starting Financial Document Analyzer..."
python main.py

