#!/usr/bin/env python3
"""
VEDRISHI AI - Instruction Pair Generator
Generates Q&A pairs from verses for fine-tuning
"""

import json
from pathlib import Path

INPUT_FILE = Path(__file__).parent.parent / "dataset" / "processed" / "vedrishi_train.jsonl"
OUTPUT_FILE = Path(__file__).parent.parent / "dataset" / "instruction-pairs" / "instruction_pairs.jsonl"

# Instruction templates for different scenarios
INSTRUCTION_TEMPLATES = {
    "seeking_advice": [
        "मुझे {topic} के बारे में मार्गदर्शन चाहिए।",
        "मेरी {problem} है, कृपया बताएं क्या करूँ?",
        "{topic} पर भगवद गीता क्या कहती है?",
    ],
    "daily_guidance": [
        "आज का श्लोक क्या है?",
        "मुझे आज के लिए एक श्लोक बताइए।",
        "गीता का आज का संदेश क्या है?",
    ],
    "understanding": [
        "{verse} का क्या अर्थ है?",
        "गीता में {topic} के बारे में क्या कहा गया है?",
        "यह श्लोक {verse} मुझे समझाइए।",
    ]
}

# Guru response templates
GURU_RESPONSE_TEMPLATES = [
    "वत्स, {explanation}",
    "प्रणाम, {explanation}",
    "आयुष्मान भव! {explanation}",
]

def generate_instruction_pairs():
    """Generate instruction pairs from verses"""
    
    print("🕉️  VEDRISHI AI - Instruction Pair Generator")
    print("=" * 50)
    
    # Load processed verses
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        verses = [json.loads(line) for line in f]
    
    # Create output directory
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    instruction_pairs = []
    
    for verse in verses:
        # Generate multiple instruction pairs per verse
        pairs = create_pairs_from_verse(verse)
        instruction_pairs.extend(pairs)
    
    # Write instruction pairs
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for pair in instruction_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')
    
    print(f"✅ Generated {len(instruction_pairs)} instruction pairs")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    
    return instruction_pairs

def create_pairs_from_verse(verse):
    """Create multiple instruction pairs from a single verse"""
    pairs = []
    
    # Extract verse info
    verse_text = verse.get('verse_sanskrit', '')
    verse_hindi = verse.get('verse_hindi', '')
    verse_english = verse.get('verse_english', '')
    themes = verse.get('theme', ['general_wisdom'])
    
    # Create different types of instruction pairs
    
    # 1. Direct question about the verse
    pairs.append({
        "instruction": f"भगवद गीता के इस श्लोक का अर्थ समझाइए:\n{verse_text}",
        "input": "",
        "output": f"वत्स, यह श्लोक भगवद गीता का अत्यंत महत्वपूर्ण श्लोक है।\n\n{verse_hindi}\n\nइसका अर्थ है: {verse_english}",
        "metadata": {
            "verse_id": verse['id'],
            "themes": themes,
            "type": "verse_explanation"
        }
    })
    
    # 2. Problem-solution format
    pairs.append({
        "instruction": f"मुझे जीवन में {', '.join(themes)} के बारे में मार्गदर्शन चाहिए।",
        "input": "",
        "output": f"वत्स, {verse_hindi}\n\nयाद रखो, भगवान ने कहा है:\n{verse_text}\n\nइसका व्यावहारिक अर्थ है: {verse_english}",
        "metadata": {
            "verse_id": verse['id'],
            "themes": themes,
            "type": "practical_guidance"
        }
    })
    
    # 3. Daily guidance format
    pairs.append({
        "instruction": "मुझे आज के लिए एक श्लोक और उसका अर्थ बताइए।",
        "input": "",
        "output": f"आज का श्लोक:\n\n{verse_text}\n\n{verse_hindi}\n\nसंदेश: {verse_english}\n\nवत्स, इस श्लोक को अपने जीवन में उतारो। कर्म करो, फल की चिंता मत करो।",
        "metadata": {
            "verse_id": verse['id'],
            "themes": themes,
            "type": "daily_guidance"
        }
    })
    
    return pairs

if __name__ == "__main__":
    generate_instruction_pairs()
