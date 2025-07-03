#!/bin/bash

# TranscriptBot Setup Script
# Creates virtual environment and installs dependencies

echo "🤖 Setting up TranscriptBot..."
echo "=================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8-3.11 and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $python_version"

# Check if ffmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found. Installing it is recommended for video processing."
    echo "Install with: sudo apt install ffmpeg (Ubuntu/Debian)"
    echo "             brew install ffmpeg (macOS)"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf .venv
fi

python3 -m venv .venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/audio
mkdir -p data/video  
mkdir -p data/transcripts
mkdir -p data/summaries

echo ""
echo "🎉 Setup completed successfully!"
echo "=================================="
echo ""
echo "🚀 To get started:"
echo "   source .venv/bin/activate"
echo "   python run_pipeline.py"
echo ""
echo "📋 For AI summaries, set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-key-here'"
echo ""
echo "📖 Check README.md for more details."
