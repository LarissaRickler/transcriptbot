import os
import json
from pathlib import Path
from datetime import datetime
import openai
from typing import Optional

# Base directories
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
SUMMARY_DIR = DATA_DIR / "summaries"

# Ensure summary directory exists
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

def setup_openai_client():
    """Setup OpenAI client with API key from environment variable"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return None
    
    return openai.OpenAI(api_key=api_key)

def create_summary_prompt(transcript_text: str, filename: str) -> str:
    """Create a prompt for summarizing the transcript"""
    
    # Detect if it's a thesis coaching session
    is_thesis_coaching = "thesis-coaching" in filename.lower()
    
    # Detect language from filename (e.g., "meeting_de.txt" or "meeting_en.txt")
    is_german = "_de.txt" in filename.lower() or "_german.txt" in filename.lower()
    is_english = "_en.txt" in filename.lower() or "_english.txt" in filename.lower()
    
    # Default to German if not clearly English
    use_german = not is_english
    
    if is_thesis_coaching:
        prompt_type = "Thesis Coaching Session" if is_english else "Thesis Coaching Session"
        additional_instructions = """
        - Fokussiere auf Fortschritte bei der Masterarbeit
        - Erwähne konkrete nächste Schritte und Deadlines
        - Hebe wichtige Feedback-Punkte hervor
        - Notiere technische Diskussionen und Methodenentscheidungen
        """ if use_german else """
        - Focus on thesis progress and milestones
        - Mention concrete next steps and deadlines
        - Highlight important feedback points
        - Note technical discussions and methodological decisions
        """
    else:
        prompt_type = "Technical Meeting"
        additional_instructions = """
        - Fokussiere auf technische Diskussionen und Problemlösungen
        - Erwähne verwendete Tools, Methoden und Algorithmen
        - Hebe wichtige Entscheidungen und nächste Schritte hervor
        - Notiere Code-Änderungen oder technische Konfigurationen
        """ if use_german else """
        - Focus on technical discussions and problem-solving
        - Mention tools, methods, and algorithms used
        - Highlight important decisions and next steps
        - Note code changes or technical configurations
        """
    
    language_instruction = "deutsche Sprache" if use_german else "English language"
    title_format = "# 📝 Zusammenfassung (DD.MM.YYYY)" if use_german else "# 📝 Summary (DD.MM.YYYY)"
    
    return f"""
Du bist ein Experte darin, technische Meeting-Transkripte zusammenzufassen. 
Erstelle eine strukturierte Zusammenfassung des folgenden {prompt_type}-Transkripts.

TRANSKRIPT:
{transcript_text}

ANFORDERUNGEN:
- Verwende {language_instruction} für die Zusammenfassung
- Strukturiere mit Markdown (# ## ### und Emojis)
- Beginne mit einem Titel im Format "{title_format}"
- Gliedere in logische Abschnitte mit aussagekräftigen Überschriften
- Verwende Bullet Points für Details
- Hebe wichtige technische Begriffe mit **Bold** hervor
- Filtere "ähs", "ums" und Wiederholungen heraus
{additional_instructions}

STRUKTUR:
- Titel mit Datum
- Hauptthemen/Abschnitte (mit Emojis wie 🔧 ⚙️ 📊 ✅ ❌ 🚀)
- Wichtige Erkenntnisse
- Nächste Schritte (falls erwähnt)
- Technische Details in separaten Abschnitten

Erstelle eine professionelle, gut lesbare Zusammenfassung:
"""

def summarize_transcript(client: openai.OpenAI, transcript_path: Path) -> Optional[str]:
    """Summarize a single transcript using OpenAI"""
    
    try:
        # Read transcript
        transcript_text = transcript_path.read_text(encoding='utf-8')
        
        # Skip if transcript is too short
        if len(transcript_text.strip()) < 100:
            print(f"⏭️  Skipping {transcript_path.name} - too short")
            return None
        
        print(f"📝 Summarizing {transcript_path.name}...")
        
        # Create prompt
        prompt = create_summary_prompt(transcript_text, transcript_path.name)
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for faster/cheaper
            messages=[
                {"role": "system", "content": "Du bist ein Experte für technische Dokumentation und Meeting-Zusammenfassungen."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        summary = response.choices[0].message.content
        print(f"✅ Summary created for {transcript_path.name}")
        return summary
        
    except Exception as e:
        print(f"❌ Error summarizing {transcript_path.name}: {e}")
        return None

def extract_date_from_filename(filename: str) -> Optional[str]:
    """Extract date from filename and format it for summary"""
    
    # Try to extract date patterns like "2025-05-23"
    import re
    
    # Pattern for YYYY-MM-DD
    date_pattern = r'(\d{4}-\d{2}-\d{2})'
    match = re.search(date_pattern, filename)
    
    if match:
        date_str = match.group(1)
        try:
            # Convert to DD.MM.YYYY format
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%d.%m.%Y')
        except ValueError:
            pass
    
    return None

def save_summary(summary: str, transcript_path: Path) -> Path:
    """Save summary to the appropriate directory"""
    
    # Extract date for filename
    date_from_filename = extract_date_from_filename(transcript_path.stem)
    
    if date_from_filename:
        # Use extracted date
        summary_filename = f"{transcript_path.stem.split()[0]}.md"
    else:
        # Fallback to original stem
        summary_filename = f"{transcript_path.stem}.md"
    
    summary_path = SUMMARY_DIR / summary_filename
    
    # Check if summary already exists
    if summary_path.exists():
        print(f"⚠️  Summary {summary_filename} already exists - overwriting")
    
    # Save summary
    summary_path.write_text(summary, encoding='utf-8')
    print(f"💾 Summary saved to {summary_path}")
    
    return summary_path

def main():
    """Main function to process all transcripts"""
    
    print("🤖 Starting transcript summarization...")
    
    # Setup OpenAI client
    client = setup_openai_client()
    if not client:
        return
    
    # Find all transcripts (any language)
    transcript_files = list(TRANSCRIPT_DIR.glob("*.txt"))
    
    if not transcript_files:
        print("❌ No transcript files found!")
        return
    
    print(f"📄 Found {len(transcript_files)} transcript files")
    
    # Process each transcript
    success_count = 0
    for transcript_path in sorted(transcript_files):
        
        # Check if summary already exists
        date_from_filename = extract_date_from_filename(transcript_path.stem)
        if date_from_filename:
            summary_filename = f"{transcript_path.stem.split()[0]}.md"
        else:
            summary_filename = f"{transcript_path.stem}.md"
        
        summary_path = SUMMARY_DIR / summary_filename
        
        if summary_path.exists():
            print(f"⏭️  Summary for {transcript_path.name} already exists")
            continue
        
        # Create summary
        summary = summarize_transcript(client, transcript_path)
        
        if summary:
            save_summary(summary, transcript_path)
            success_count += 1
        
        print()  # Empty line for readability
    
    print(f"🎉 Finished! Created {success_count} new summaries")

if __name__ == "__main__":
    main()
