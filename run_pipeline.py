#!/usr/bin/env python3
"""
TranscriptBot - Complete Audio Processing Pipeline
- Copies OBS videos (optional)
- Extracts audio from videos
- Transcribes audio files with Whisper (auto language detection)
- Creates AI-powered summaries
"""

import subprocess
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
DATA_DIR = Path(__file__).resolve().parent / "data"

def run_script(script_path: Path, description: str, optional: bool = False) -> bool:
    """Run a script and return success status"""
    
    if not script_path.exists():
        if optional:
            print(f"⏭️  {script_path.name} not found - skipping {description}")
            return True
        else:
            print(f"❌ {script_path.name} not found - {description} failed")
            return False
    
    print(f"\n🚀 Starting: {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            return True
        else:
            if optional:
                print(f"⚠️  {description} finished with warnings (optional step)")
                return True
            else:
                print(f"❌ {description} failed!")
                return False
            
    except Exception as e:
        print(f"❌ Error running {script_path.name}: {e}")
        return False

def check_prerequisites():
    """Check if necessary directories and files exist"""
    print("🔍 Checking prerequisites...")
    
    # Check if data directories exist
    audio_dir = DATA_DIR / "audio"
    video_dir = DATA_DIR / "video"
    
    audio_files = list(audio_dir.glob("*")) if audio_dir.exists() else []
    video_files = list(video_dir.glob("*.mkv")) if video_dir.exists() else []
    
    print(f"📁 Audio files found: {len(audio_files)}")
    print(f"🎬 Video files found: {len(video_files)}")
    
    return len(audio_files) > 0 or len(video_files) > 0

def main():
    """Main pipeline function"""
    print("🤖 TRANSCRIPTBOT - COMPLETE AUDIO PROCESSING PIPELINE")
    print("=" * 60)
    print("This pipeline will:")
    print("1. 📂 Copy OBS videos (optional)")
    print("2. 🎬 Extract audio from video files")
    print("3. 🗣️  Transcribe audio files with Whisper (auto language detection)")
    print("4. 🤖 Generate AI-powered summaries")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n⚠️  No audio or video files found to process!")
        print("Add files to data/audio/ or data/video/ and try again.")
        return
    
    # Step 1: Copy OBS videos (optional)
    copy_script = SRC_DIR / "copy_obs_videos.py"
    run_script(copy_script, "Copy OBS videos from ~/Videos/OBS", optional=True)
    
    # Step 2: Extract audio from videos
    extract_script = SRC_DIR / "extract_audio_from_videos.py"
    video_dir = DATA_DIR / "video"
    if video_dir.exists() and list(video_dir.glob("*.mkv")):
        run_script(extract_script, "Audio extraction from videos", optional=True)
    else:
        print("\n⏭️  No video files found - skipping audio extraction")
    
    # Step 3: Transcribe audio files
    transcribe_script = SRC_DIR / "transcribe_batch.py"
    success_transcription = run_script(transcribe_script, "Audio transcription with Whisper")
    
    if not success_transcription:
        print("\n❌ Transcription failed - stopping pipeline")
        return
    
    # Step 4: Generate summaries (optional, requires OpenAI API)
    summarize_script = SRC_DIR / "summarize_transcripts.py"
    success_summary = run_script(summarize_script, "AI-powered summary generation", optional=True)
    
    # Final status report
    print("\n" + "=" * 60)
    print("📊 PIPELINE RESULTS:")
    print("=" * 60)
    
    if success_transcription and success_summary:
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("✅ Transcription: Done")
        print("✅ Summarization: Done")
    elif success_transcription:
        print("⚠️  PIPELINE PARTIALLY COMPLETED")
        print("✅ Transcription: Done")
        print("⚠️  Summarization: Skipped or failed (requires OPENAI_API_KEY)")
    else:
        print("❌ PIPELINE FAILED")
        return
    
    # Show results
    transcript_dir = DATA_DIR / "transcripts"
    summary_dir = DATA_DIR / "summaries"
    
    transcript_count = len(list(transcript_dir.glob("*.txt"))) if transcript_dir.exists() else 0
    summary_count = len(list(summary_dir.glob("*.md"))) if summary_dir.exists() else 0
    
    print(f"\n📈 Results generated:")
    print(f"   📝 Transcripts: {transcript_count} files in data/transcripts/")
    print(f"   📋 Summaries: {summary_count} files in data/summaries/")
    
    print(f"\n💡 Next steps:")
    if summary_count == 0 and transcript_count > 0:
        print("   - Set OPENAI_API_KEY to enable automatic summaries")
        print("   - Or run: python src/summarize_transcripts.py")
    print("   - Check the generated files for accuracy")
    print("=" * 60)

if __name__ == "__main__":
    main()
