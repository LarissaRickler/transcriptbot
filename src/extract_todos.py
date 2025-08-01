#!/usr/bin/env python3
"""
Extract TODO items and action items from transcripts
This script specifically focuses on creating actionable task lists
"""

import os
import json
from pathlib import Path
from datetime import datetime
import openai
from typing import Optional, List

# Base directories
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
TODO_DIR = DATA_DIR / "summaries" / "todos"

# Ensure TODO directory exists
TODO_DIR.mkdir(parents=True, exist_ok=True)

def setup_openai_client():
    """Setup OpenAI client with API key from environment variable"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return None
    
    return openai.OpenAI(api_key=api_key)

def create_todo_prompt(transcript_text: str, filename: str) -> str:
    """Create a prompt for extracting TODOs and action items"""
    
    # Detect language from filename or content
    # Only English or German recordings exist - treat "nn" (Norwegian) as German since it's misdetected
    is_english = "_en.txt" in filename.lower() or "_english.txt" in filename.lower()
    use_german = not is_english  # This includes "_de.txt" and "_nn.txt" (misdetected German)
    
    language_instruction = "deutsche Sprache" if use_german else "English language"
    
    if use_german:
        return f"""
Du bist ein Experte darin, aus Meeting-Transkripten konkrete Aufgaben und Action Items zu extrahieren.
Analysiere das folgende Transkript und erstelle eine strukturierte TODO-Liste.

TRANSKRIPT:
{transcript_text}

AUFGABE:
Extrahiere ALLE konkreten Aufgaben, Aktionspunkte und nächsten Schritte. Fokussiere auf:

✅ KONKRETE AUFGABEN:
- Spezifische Aktivitäten die erledigt werden müssen
- Technische Implementierungen
- Recherche-Aufgaben
- Code-Änderungen
- Tests und Validierungen

📅 DEADLINES & TERMINE:
- Erwähnte Fristen
- Geplante Meetings
- Milestone-Termine

🔧 TECHNISCHE TODOS:
- Bug-Fixes
- Feature-Implementierungen
- Konfigurationsänderungen
- Tool-Setups

📚 LERN-/RECHERCHE-AUFGABEN:
- Literatur lesen
- Technologien evaluieren
- Best Practices recherchieren

AUSGABEFORMAT (Markdown):
```markdown
# 📋 TODO Liste - [DATUM]

## 🚀 Sofortige Aktionen (bis [Datum])
- [ ] Aufgabe 1 mit konkreter Beschreibung
- [ ] Aufgabe 2 mit Kontext

## 📅 Diese Woche 
- [ ] Aufgabe mit Deadline
- [ ] Weitere Aufgabe

## 🔧 Technische Aufgaben
- [ ] Code-Änderung XYZ
- [ ] Test Implementation ABC

## 📚 Recherche & Lernen
- [ ] Thema ABC erforschen
- [ ] Tutorial XYZ durcharbeiten

## 📞 Follow-ups & Meetings
- [ ] Meeting mit Person X planen
- [ ] Feedback einholen von Y

## 💡 Ideen für später
- [ ] Verbesserungsidee 1
- [ ] Feature-Idee 2
```

Erstelle eine actionable, priorisierte TODO-Liste aus dem Transkript:
"""
    else:
        return f"""
You are an expert at extracting concrete tasks and action items from meeting transcripts.
Analyze the following transcript and create a structured TODO list.

TRANSCRIPT:
{transcript_text}

TASK:
Extract ALL concrete tasks, action points and next steps. Focus on:

✅ CONCRETE TASKS:
- Specific activities that need to be completed
- Technical implementations
- Research tasks
- Code changes
- Tests and validations

📅 DEADLINES & APPOINTMENTS:
- Mentioned deadlines
- Planned meetings
- Milestone dates

🔧 TECHNICAL TODOS:
- Bug fixes
- Feature implementations
- Configuration changes
- Tool setups

📚 LEARNING/RESEARCH TASKS:
- Literature to read
- Technologies to evaluate
- Best practices to research

OUTPUT FORMAT (Markdown):
```markdown
# 📋 TODO List - [DATE]

## 🚀 Immediate Actions (by [date])
- [ ] Task 1 with concrete description
- [ ] Task 2 with context

## 📅 This Week
- [ ] Task with deadline
- [ ] Another task

## 🔧 Technical Tasks
- [ ] Code change XYZ
- [ ] Test implementation ABC

## 📚 Research & Learning
- [ ] Research topic ABC
- [ ] Work through tutorial XYZ

## 📞 Follow-ups & Meetings
- [ ] Plan meeting with person X
- [ ] Get feedback from Y

## 💡 Ideas for Later
- [ ] Improvement idea 1
- [ ] Feature idea 2
```

Create an actionable, prioritized TODO list from the transcript:
"""

def extract_todos(client: openai.OpenAI, transcript_path: Path) -> Optional[str]:
    """Extract TODOs from a single transcript using OpenAI"""
    
    try:
        # Read transcript
        transcript_text = transcript_path.read_text(encoding='utf-8')
        
        # Skip if transcript is too short
        if len(transcript_text.strip()) < 100:
            print(f"⏭️  Skipping {transcript_path.name} - too short")
            return None
        
        print(f"📋 Extracting TODOs from {transcript_path.name}...")
        
        # Create prompt
        prompt = create_todo_prompt(transcript_text, transcript_path.name)
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist ein Projektmanagement-Experte, der aus Meetings konkrete, actionable TODO-Listen erstellt."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.2
        )
        
        todos = response.choices[0].message.content
        print(f"✅ TODOs extracted from {transcript_path.name}")
        return todos
        
    except Exception as e:
        print(f"❌ Error extracting TODOs from {transcript_path.name}: {e}")
        return None

def save_todos(todos: str, transcript_path: Path) -> Path:
    """Save TODOs to the appropriate directory"""
    
    # Create filename
    todo_filename = f"{transcript_path.stem}_TODOs.md"
    todo_path = TODO_DIR / todo_filename
    
    # Check if TODO file already exists
    if todo_path.exists():
        print(f"⚠️  TODO file {todo_filename} already exists - overwriting")
    
    # Save TODOs
    todo_path.write_text(todos, encoding='utf-8')
    print(f"💾 TODOs saved to {todo_path}")
    
    return todo_path

def main():
    """Main function to process all transcripts for TODO extraction"""
    
    print("📋 Starting TODO extraction from transcripts...")
    
    # Setup OpenAI client
    client = setup_openai_client()
    if not client:
        return
    
    # Find all transcripts
    transcript_files = list(TRANSCRIPT_DIR.glob("*.txt"))
    
    if not transcript_files:
        print("❌ No transcript files found!")
        return
    
    print(f"📄 Found {len(transcript_files)} transcript files")
    
    # Process each transcript
    success_count = 0
    for transcript_path in sorted(transcript_files):
        
        # Check if TODO file already exists
        todo_filename = f"{transcript_path.stem}_TODOs.md"
        todo_path = TODO_DIR / todo_filename
        
        if todo_path.exists():
            print(f"⏭️  TODOs for {transcript_path.name} already exist")
            continue
        
        # Extract TODOs
        todos = extract_todos(client, transcript_path)
        
        if todos:
            save_todos(todos, transcript_path)
            success_count += 1
        
        print()  # Empty line for readability
    
    print(f"🎉 Finished! Created {success_count} new TODO lists")

if __name__ == "__main__":
    main()
