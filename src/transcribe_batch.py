import whisper
from pathlib import Path

# Base directory relative to src/
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
AUDIO_DIR = DATA_DIR / "audio"

# Output directory for transcripts with auto-detected language
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# Load Whisper model
model = whisper.load_model("base")  # Alternative: "small", "medium", "large"

# Supported audio formats
audio_extensions = ["*.wav", "*.m4a", "*.mp3", "*.mp4", "*.flac", "*.aac"]

# Collect all audio files
audio_files = []
for extension in audio_extensions:
    audio_files.extend(AUDIO_DIR.glob(extension))

print(f"🎵 Found {len(audio_files)} audio files to process")

# Process all audio files with automatic language detection
for audio_path in audio_files:
    output_txt = TRANSCRIPT_DIR / (audio_path.stem + ".txt")
    
    if not output_txt.exists():
        print(f"📝 Transcribing {audio_path.name} (auto-detecting language)...")
        
        # Let Whisper automatically detect the language
        result = model.transcribe(str(audio_path))
        
        # Get detected language
        detected_language = result.get('language', 'unknown')
        
        # Save transcript with language info in filename
        output_txt_with_lang = TRANSCRIPT_DIR / f"{audio_path.stem}_{detected_language}.txt"
        output_txt_with_lang.write_text(result["text"])
        
        print(f"✅ Saved transcript to {output_txt_with_lang}")
        print(f"🗣️  Detected language: {detected_language}")
    else:
        print(f"⏭️  {audio_path.name} – Transcript already exists.")

print(f"\n🎉 Transcription completed! Check {TRANSCRIPT_DIR} for results.")