#!/usr/bin/env python3
"""
VEDRISHI AI - Convert Raw Data to JSONL Format
Converts downloaded Gita data to training format
"""

import json
from pathlib import Path

INPUT_FILE = Path(__file__).parent.parent / "dataset" / "raw" / "bhagavad_gita.json"
OUTPUT_FILE = Path(__file__).parent.parent / "dataset" / "processed" / "vedrishi_train.jsonl"

def convert_to_jsonl():
    """Convert raw Gita data to JSONL training format"""
    
    print("🕉️  VEDRISHI AI - JSONL Converter")
    print("=" * 50)
    
    # Load raw data
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create output directory
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert each verse
    jsonl_lines = []
    
    for chapter in data['chapters']:
        chapter_num = chapter['chapter_number']
        
        for verse in chapter['verses']:
            verse_num = verse.get('verse_number', 0)
            
            # Extract text fields (handle different API formats)
            verse_sanskrit = verse.get('text', verse.get('verse', ''))
            verse_hindi = verse.get('translations', {}).get('hindi', '')
            verse_english = verse.get('translations', {}).get('english', '')
            
            # Create JSONL entry
            entry = {
                "id": f"gita_ch{chapter_num}_verse{verse_num}",
                "source": f"Bhagavad Gita, Chapter {chapter_num}, Verse {verse_num}",
                "language": "hindi",
                "verse_sanskrit": verse_sanskrit,
                "verse_hindi": verse_hindi,
                "verse_english": verse_english,
                "chapter": chapter_num,
                "verse_number": verse_num,
                "theme": determine_theme(verse),
                "difficulty": determine_difficulty(verse_num)
            }
            
            jsonl_lines.append(json.dumps(entry, ensure_ascii=False))
    
    # Write JSONL file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(jsonl_lines))
    
    print(f"✅ Conversion Complete!")
    print(f"📊 Total entries: {len(jsonl_lines)}")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    
    return jsonl_lines

def determine_theme(verse):
    """Determine theme tags based on verse content"""
    themes = []
    
    # Simple keyword-based theme detection
    text = str(verse).lower()
    
    if 'karma' in text or 'कर्म' in text:
        themes.append('karma_yoga')
    if 'bhakti' in text or 'भक्ति' in text:
        themes.append('bhakti_yoga')
    if 'jnana' in text or 'ज्ञान' in text:
        themes.append('jnana_yoga')
    if 'dharma' in text or 'धर्म' in text:
        themes.append('dharma')
    if 'moksha' in text or 'मोक्ष' in text:
        themes.append('moksha')
    
    if not themes:
        themes.append('general_wisdom')
    
    return themes

def determine_difficulty(verse_num):
    """Determine difficulty level"""
    if verse_num <= 20:
        return 'beginner'
    elif verse_num <= 50:
        return 'intermediate'
    else:
        return 'advanced'

if __name__ == "__main__":
    convert_to_jsonl()
