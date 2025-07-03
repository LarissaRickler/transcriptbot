# 🤖 TranscriptBot

**Automated audio/video transcription pipeline with AI-powered meeting summaries.**

TranscriptBot combines OpenAI Whisper for accurate transcription with GPT-4 for intelligent meeting summarization. Perfect for academic meetings, technical discussions, and thesis coaching sessions.

## ✨ Features

- 🎵 **Multi-format support**: `.wav`, `.m4a`, `.mp3`, `.mp4`, `.flac`, `.aac`
- 🗣️ **Automatic language detection** with Whisper
- 🤖 **AI-powered summaries** with structured Markdown output
- 📋 **Meeting-type detection** (technical meetings vs thesis coaching)
- 🔄 **Complete workflow automation**
- 📁 **Organized data structure**

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
│   ├── audio/         # Input audio files
│   ├── transcripts/   # Generated transcripts  
│   ├── summaries/     # AI-generated summaries
│   └── video/         # Input video files
├── src/
│   ├── transcribe_batch.py      # Whisper transcription
│   ├── summarize_transcripts.py # GPT summarization
│   └── ...
├── run_pipeline.py    # Main workflow
└── requirements.txt
```

## 🎯 Workflow

1. **📂 Import**: Copy videos from OBS (optional)
2. **🎬 Extract**: Audio from video files
3. **🗣️ Transcribe**: With automatic language detection
4. **🤖 Summarize**: Create structured Markdown summaries

## 📋 Example Output

### Transcript
```
meeting_2025-07-03_de.txt
```

### AI Summary
```markdown
# 📝 Zusammenfassung (03.07.2025)

## 🔧 Server-Konfiguration
- **Elastic vs. Viscoelastic** Binary-Auswahl implementiert
- Problem mit `config` Parameter identifiziert

## ✅ Nächste Schritte
- MLDA Inversion mit Umbridge testen
- Settings-Dateien konfigurieren
```

## ⚙️ Requirements

- Python 3.8-3.11
- FFmpeg
- Optional: OpenAI API key for summaries

## 🛠️ Manual Steps

```bash
# Transcription only
python src/transcribe_batch.py

# Summaries only
python src/summarize_transcripts.py
```

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

**Built with ❤️ for researchers and meeting organizers**
