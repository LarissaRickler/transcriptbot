# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8-3.11
- FFmpeg: `sudo apt install ffmpeg` (Ubuntu) or `brew install ffmpeg` (macOS)

## Installation
```bash
git clone https://github.com/LarissaRickler/transcriptbot.git
cd transcriptbot
bash setup_venv.sh
```

## Usage
```bash
source .venv/bin/activate
python run_pipeline.py
```

## Optional: AI Summaries
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

## File Sources
- Videos: `~/Videos/OBS/` (automatic)
- Audio: `~/Music/` (automatic)  
- Manual: Drop files in `data/audio/` or `data/video/`

---
📖 **Full documentation**: See main [README.md](README.md)
