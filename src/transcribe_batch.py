import whisper
from pathlib import Path
import re

# Base directory relative to src/
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
AUDIO_DIR = DATA_DIR / "audio"

# Output directory for transcripts with auto-detected language
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# Load Whisper model
print("🤖 Loading Whisper model...")
model = whisper.load_model("base")  # Alternative: "small", "medium", "large"

def is_valid_transcript(text):
    """Check if the transcript contains actual text rather than progress indicators."""
    if not text or len(text.strip()) < 10:
        return False
    
    # Check for progress indicators (like "1.5% 1.5% 1.5%...")
    if re.match(r'^[\s\d\.%]*$', text.strip()):
        return False
    
    # Check for repeating test patterns
    words = text.strip().split()
    if len(words) > 10 and len(set(words)) < 5:  # Too many repeated words
        return False
    
    return True

# Supported audio formats
audio_extensions = ["*.wav", "*.m4a", "*.mp3", "*.mp4", "*.flac", "*.aac"]

# Collect all audio files
audio_files = []
for extension in audio_extensions:
    audio_files.extend(AUDIO_DIR.glob(extension))

print(f"🎵 Found {len(audio_files)} audio files to process")

# Process all audio files with language detection limited to German and English
for audio_path in audio_files:
    # Check if transcript already exists with either language suffix
    output_txt_de = TRANSCRIPT_DIR / f"{audio_path.stem}_de.txt"
    output_txt_en = TRANSCRIPT_DIR / f"{audio_path.stem}_en.txt"
    
    if not output_txt_de.exists() and not output_txt_en.exists():
        print(f"📝 Transcribing {audio_path.name} (detecting German/English only)...")
        
        try:
            # First, try automatic detection but limit to German/English
            print("🔍 Trying automatic detection...")
            result = model.transcribe(str(audio_path), verbose=False)
            detected_language = result.get('language', 'unknown')
            
            print(f"🌍 Detected language: {detected_language}")
            
            # If detected language is not German or English, try both explicitly
            if detected_language not in ['de', 'en']:
                print(f"⚠️  Language '{detected_language}' not supported. Trying German first...")
                
                # Try German first (most common in your recordings)
                result_de = model.transcribe(str(audio_path), language='de', verbose=False)
                text_de = result_de.get("text", "").strip()
                
                if is_valid_transcript(text_de):
                    result = result_de
                    detected_language = 'de'
                    print("✅ German transcription successful")
                else:
                    print("❌ German failed, trying English...")
                    # Try English as fallback
                    result_en = model.transcribe(str(audio_path), language='en', verbose=False)
                    text_en = result_en.get("text", "").strip()
                    
                    if is_valid_transcript(text_en):
                        result = result_en
                        detected_language = 'en'
                        print("✅ English transcription successful")
                    else:
                        print("❌ Both German and English failed")
                        continue
            
            # Get the actual text content
            text = result.get("text", "").strip()
            
            if not text:
                print(f"❌ Empty transcription for {audio_path.name}")
                continue
            
            # Validate the transcript
            if not is_valid_transcript(text):
                print(f"❌ Invalid transcript content for {audio_path.name} (contains only progress indicators or repeated words)")
                continue
            
            # Create output filename with language suffix
            output_txt_with_lang = TRANSCRIPT_DIR / f"{audio_path.stem}_{detected_language}.txt"
            
            # Save the transcript
            output_txt_with_lang.write_text(text, encoding='utf-8')
            
            print(f"✅ Saved transcript to {output_txt_with_lang}")
            print(f"� Text length: {len(text)} characters")
            print(f"🔤 First 100 characters: {text[:100]}...")
            
        except Exception as e:
            print(f"❌ Error transcribing {audio_path.name}: {e}")
            
    else:
        # Show which transcript already exists
        if output_txt_de.exists():
            print(f"⏭️  {audio_path.name} – German transcript already exists.")
        elif output_txt_en.exists():
            print(f"⏭️  {audio_path.name} – English transcript already exists.")

print(f"\n🎉 Transcription completed! Check {TRANSCRIPT_DIR} for results.")