# 🤖 TranscriptBot

**Automated audio/video transcription pipeline with AI-powered meeting summaries.**

TranscriptBot combines OpenAI Whisper for accurate transcription with GPT-4 for intelligent meeting summarization. Perfect for academic meetings, technical discussions, and thesis coaching sessions.

## ✨ Features

- 🎵 **Multi-format support**: Audio (`.wav`, `.m4a`, `.mp3`, `.mp4`, `.flac`, `.aac`) and Video (`.mkv`, `.mp4`, `.avi`, `.mov`)
- 🗣️ **Automatic language detection** with Whisper (German/English)
- 🤖 **AI-powered summaries** with structured Markdown output
- 📋 **TODO extraction** - Actionable task lists from meetings
- 🎬 **Video processing** - Automatic audio extraction from videos
- 🔄 **Complete workflow automation** - From video/audio to summaries
- 📁 **Smart file organization** with language detection
- 🎯 **Multiple sources** - OBS videos, Music folder, manual uploads

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/LarissaRickler/transcriptbot.git
cd transcriptbot
bash setup_venv.sh
```

### 2. Run the Pipeline

```bash
source .venv/bin/activate
python run_pipeline.py
```

### 3. Add OpenAI API for Summaries (Optional)

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 📂 Project Structure

```
transcriptbot/
├── data/
│   ├── audio/         # Input audio files + extracted audio from videos
│   ├── video/         # Input video files (OBS recordings)
│   ├── transcripts/   # Generated transcripts (language auto-detected)
│   └── summaries/     # AI-generated summaries and TODO lists
├── src/
│   ├── constants.py              # Configuration and constants
│   ├── copy_obs_videos.py        # Copy from ~/Videos/OBS
│   ├── copy_music_files.py       # Copy from ~/Music
│   ├── extract_audio_from_videos.py # Video → Audio conversion
│   ├── transcribe_batch.py       # Whisper transcription
│   ├── summarize_transcripts.py  # GPT-4 summarization
│   └── extract_todos.py          # TODO extraction
├── run_pipeline.py    # Main automated workflow
├── setup_venv.sh      # Setup script
└── requirements.txt   # Python dependencies
```

## 🎯 Workflow

1. **📂 Copy Videos**: Automatically copies OBS videos from `~/Videos/OBS`
2. **🎵 Copy Audio**: Copies audio files from `~/Music` folder  
3. **🎬 Extract Audio**: Converts video files to high-quality WAV audio
4. **🗣️ Transcribe**: Uses Whisper for automatic language detection (German/English)
5. **🤖 Summarize**: Creates structured Markdown summaries with GPT-4
6. **📋 Extract TODOs**: Generates actionable task lists from meetings

## ⚙️ Requirements

- Python 3.8-3.11
- FFmpeg
- Optional: OpenAI API key for summaries

## 🛠️ Manual Scripts

```bash
# Individual components
python src/copy_obs_videos.py        # Copy OBS videos only
python src/copy_music_files.py       # Copy music files only
python src/extract_audio_from_videos.py  # Extract audio only
python src/transcribe_batch.py       # Transcription only
python src/summarize_transcripts.py  # Summaries only  
python src/extract_todos.py          # TODO extraction only
```

## 🎯 Use Cases

- **🎓 Academic Meetings**: Thesis coaching, supervisor meetings
- **💼 Business Meetings**: Team meetings, project discussions  
- **🎤 Presentations**: Conference talks, lectures
- **📞 Interviews**: Research interviews, user feedback sessions
- **🧠 Brainstorming**: Creative sessions, planning meetings

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

