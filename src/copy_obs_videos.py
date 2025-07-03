import shutil
from pathlib import Path

# Eingabe- und Zielverzeichnis definieren
source_dir = Path.home() / "Videos" / "OBS"
target_dir = Path.home() / "Projects" / "whisper" / "data" / "video"

# Zielverzeichnis erstellen, falls es nicht existiert
target_dir.mkdir(parents=True, exist_ok=True)

# Unterstützte Videoformate
video_extensions = [".mp4", ".mkv", ".mov", ".avi"]

# Kopiervorgang
for video_file in source_dir.glob("*"):
    if video_file.suffix.lower() in video_extensions:
        destination = target_dir / video_file.name
        if not destination.exists():
            print(f"🎬 Copying video from {video_file} ...")
            shutil.copy2(video_file, destination)
            print(f"✅ Saved video to {destination}")
        else:
            print(f"⏭️  {video_file.name} – Video already exists.")