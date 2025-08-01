#!/usr/bin/env python3
"""
Copy audio files from ~/Music to data/audio/
"""
import shutil
from pathlib import Path

# Source and target directories
source_dir = Path.home() / "Music"
target_dir = Path(__file__).resolve().parent.parent / "data" / "audio"

# Create target directory if it doesn't exist
target_dir.mkdir(parents=True, exist_ok=True)

# Supported audio formats
audio_extensions = [".wav", ".mp3", ".m4a", ".flac", ".aac", ".ogg", ".wma"]

# Copy process
copied_count = 0
for audio_file in source_dir.rglob("*"):  # rglob for recursive search
    if audio_file.is_file() and audio_file.suffix.lower() in audio_extensions:
        destination = target_dir / audio_file.name
        
        # Handle duplicate names by adding a counter
        counter = 1
        original_destination = destination
        while destination.exists():
            stem = original_destination.stem
            suffix = original_destination.suffix
            destination = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        print(f"🎵 Copying audio from {audio_file} ...")
        shutil.copy2(audio_file, destination)
        print(f"✅ Saved audio to {destination}")
        copied_count += 1

if copied_count == 0:
    print("ℹ️  No audio files found in ~/Music")
else:
    print(f"🎉 Copied {copied_count} audio files successfully!")
