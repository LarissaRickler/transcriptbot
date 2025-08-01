#!/usr/bin/env python3
"""
Constants and configuration for TranscriptBot
"""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"

# Data subdirectories
AUDIO_DIR = DATA_DIR / "audio"
VIDEO_DIR = DATA_DIR / "video"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
SUMMARY_DIR = DATA_DIR / "summaries"
TODO_DIR = SUMMARY_DIR / "todos"

# Supported file formats
AUDIO_EXTENSIONS = [".wav", ".m4a", ".mp3", ".mp4", ".flac", ".aac", ".ogg", ".wma"]
VIDEO_EXTENSIONS = [".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv"]

# External source directories
MUSIC_SOURCE = Path.home() / "Music"
OBS_SOURCE = Path.home() / "Videos" / "OBS"

# Whisper model options
WHISPER_MODEL = "base"  # Options: "tiny", "base", "small", "medium", "large"

# OpenAI settings
OPENAI_MODEL = "gpt-4"
OPENAI_MAX_TOKENS = 2000
OPENAI_TEMPERATURE = 0.3
