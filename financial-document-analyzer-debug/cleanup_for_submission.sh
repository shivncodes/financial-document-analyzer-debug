#!/bin/bash

# Script to clean up project before creating zip for submission
# This removes unnecessary files that shouldn't be included

echo "🧹 Cleaning up project for submission..."

# Remove virtual environment (1.4GB - too large for submission)
if [ -d "venv" ]; then
    echo "  ❌ Removing venv/ (1.4GB)..."
    rm -rf venv
    echo "  ✅ Removed venv/"
fi

# Remove Python cache files
if [ -d "__pycache__" ]; then
    echo "  ❌ Removing __pycache__/..."
    find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    echo "  ✅ Removed Python cache files"
fi

# Remove .env file (contains API keys - sensitive!)
if [ -f ".env" ]; then
    echo "  ❌ Removing .env (contains API keys)..."
    rm -f .env
    echo "  ✅ Removed .env (keep .env.example for reference)"
fi

# Remove macOS system files
if [ -f ".DS_Store" ]; then
    echo "  ❌ Removing .DS_Store..."
    find . -name ".DS_Store" -delete 2>/dev/null || true
    find . -name "._*" -delete 2>/dev/null || true
    echo "  ✅ Removed macOS system files"
fi

# Remove temporary files
echo "  ❌ Removing temporary files..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.log" -delete 2>/dev/null || true
find . -name "*.bak" -delete 2>/dev/null || true
echo "  ✅ Removed temporary files"

# Optional: Remove outputs (uncomment if you don't want to include generated files)
# if [ -d "outputs" ]; then
#     echo "  ❌ Removing outputs/..."
#     rm -rf outputs
#     echo "  ✅ Removed outputs/"
# fi

echo ""
echo "✅ Cleanup complete! Files to keep:"
echo "   ✓ All .py source files"
echo "   ✓ requirements.txt"
echo "   ✓ README.md"
echo "   ✓ BUGS_FIXED.md"
echo "   ✓ FREE_MODEL_SETUP.md"
echo "   ✓ .env.example (template)"
echo "   ✓ .gitignore"
echo "   ✓ run.sh"
echo "   ✓ data/ (sample PDF)"
echo "   ✓ outputs/ (if you want to include API docs)"
echo ""
echo "📦 Now you can create a zip file of the project!"

