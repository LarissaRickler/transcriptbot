import ffmpeg
from pathlib import Path

# Base directory relative to src/
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
VIDEO_DIR = DATA_DIR / "video"
AUDIO_DIR = DATA_DIR / "audio"

# Create output directory if it doesn't exist
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Supported video extensions
VIDEO_EXTENSIONS = [".mp4", ".mov", ".mkv", ".avi"]

# Process all videos
for video_path in VIDEO_DIR.iterdir():
    if video_path.suffix.lower() not in VIDEO_EXTENSIONS:
        continue

    audio_path = AUDIO_DIR / (video_path.stem + ".wav")  # WAV statt MP3

    if audio_path.exists():
        print(f"⏭️  {video_path.name} – Audio already exists.")
        continue

    print(f"🎞️  Extracting audio from {video_path.name} ...")
    try:
        (
            ffmpeg
            .input(str(video_path))
            .output(str(audio_path), format='wav', acodec='pcm_s16le', ac=1, ar='16000')
            .run(overwrite_output=True, quiet=True)
        )
        print(f"✅ Saved audio to {audio_path}")
    except ffmpeg.Error as e:
        print(f"❌ Error processing {video_path.name}: {e}")
