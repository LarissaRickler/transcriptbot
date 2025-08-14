#!/usr/bin/env python3
"""
Copy audio files from ~/Music to data/audio/
"""
import shutil
import filecmp
from pathlib import Path

# Source and target directories
source_dir = Path.home() / "Music"
target_dir = Path(__file__).resolve().parent.parent / "data" / "audio"

# Create target directory if it doesn't exist
target_dir.mkdir(parents=True, exist_ok=True)

# Supported audio formats
audio_extensions = [".wav", ".mp3", ".m4a", ".flac", ".aac", ".ogg", ".wma"]

# Copy process
for audio_file in source_dir.rglob("*"):  # rglob for recursive search
    if audio_file.is_file() and audio_file.suffix.lower() in audio_extensions:
        destination = target_dir / audio_file.name
        
        # Check if file already exists and is identical
        if destination.exists() and filecmp.cmp(audio_file, destination, shallow=False):
            print(f"⏭️  {audio_file.name} – Audio file already exists and is identical.")
            continue
            
        # Handle duplicate names by adding a counter (only if files are different)
        counter = 1
        original_destination = destination
        while destination.exists():
            # Check if this numbered version is identical
            if filecmp.cmp(audio_file, destination, shallow=False):
                print(f"⏭️  {audio_file.name} – Audio file already exists as {destination.name}.")
                break
            stem = original_destination.stem
            suffix = original_destination.suffix
            destination = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        else:
            # Only copy if we didn't find an identical file
            print(f"🎵 Copying audio from {audio_file} ...")
            shutil.copy2(audio_file, destination)
            print(f"✅ Saved audio to {destination}")
