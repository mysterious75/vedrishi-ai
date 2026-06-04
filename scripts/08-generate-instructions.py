#!/usr/bin/env python3
"""
VEDRISHI AI - Instruction Pair Generator
Generates Q&A pairs from cleaned scriptures for fine-tuning
"""

import json
import random
from pathlib import Path
from datetime import datetime

# Configuration
FINAL_DIR = Path(__file__).parent.parent / "dataset" / "final"
OUTPUT_DIR = Path(__file__).parent.parent / "dataset" / "instruction-pairs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Use Hindi-enriched dataset if available
MAIN_DATASET = FINAL_DIR / "vedrishi_complete_hindi.jsonl"
if not MAIN_DATASET.exists():
    MAIN_DATASET = FINAL_DIR / "vedrishi_complete.jsonl"

LOG_FILE = OUTPUT_DIR / "generation_log.txt"

def log(message):
    """Log message to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ===========================
# INSTRUCTION TEMPLATES
# ===========================

GITA_TEMPLATES = {
    'seeking_advice': [
        "मुझे जीवन में {topic} के बारे में मार्गदर्शन चाहिए।",
        "{topic} पर भगवद गीता क्या कहती है?",
        "गीता के अनुसार {topic} कैसे करूँ?",
        "मेरी {problem} है, गीता में इसका समाधान क्या है?",
    ],
    'daily_guidance': [
        "आज का श्लोक क्या है?",
        "मुझे आज के लिए एक श्लोक बताइए।",
        "गीता का आज का संदेश क्या है?",
    ],
    'understanding': [
        "गीता के इस श्लोक का अर्थ समझाइए।",
        "कर्मयोग क्या है?",
        "भक्तियोग और ज्ञानयोग में क्या अंतर है?",
        "धर्म क्या है गीता के अनुसार?",
    ]
}

RAMAYANA_TEMPLATES = {
    'seeking_advice': [
        "रामायण में {topic} के बारे में क्या कहा गया है?",
        "श्री राम ने {problem} कैसे सुलझाया?",
        "रामायण से {topic} के बारे में क्या सीख सकते हैं?",
    ],
    'character': [
        "हनुमान जी की भक्ति के बारे में बताइए।",
        "श्री राम आदर्श पुरुष क्यों माने जाते हैं?",
        "सीता जी की वीरता के बारे में बताइए।",
    ]
}

MAHABHARATA_TEMPLATES = {
    'seeking_advice': [
        "महाभारत में {topic} के बारे में क्या कहा गया है?",
        "भीष्म पितामह ने {topic} पर क्या कहा?",
        "विदुर नीति में {topic} के बारे में क्या है?",
    ],
    'wisdom': [
        "चाणक्य नीति में सफलता के लिए क्या कहा गया है?",
        "महाभारत की सबसे बड़ी शिक्षा क्या है?",
        "कर्म का सिद्धांत महाभारत में कैसे समझाया गया है?",
    ]
}

# ===========================
# GURU RESPONSE TEMPLATES
# ===========================

GURU_OPENINGS = [
    "वत्स, ",
    "प्रणाम, ",
    "आयुष्मान भव! ",
    "श्रद्धालु, ",
]

GURU_CLOSINGS = [
    "\n\nयाद रखो, भगवान ने कहा है - कर्म करो, फल की चिंता मत करो।",
    "\n\nइस श्लोक को अपने जीवन में उतारो।",
    "\n\nसत्य और धर्म का मार्ग सदा श्रेष्ठ होता है।",
    "\n\nशांति और समभाव से आगे बढ़ो।",
]

DISCLAIMER = "\n\n[नोट: यह एक AI मार्गदर्शक है। यह भगवद गीता और अन्य शास्त्रों पर आधारित है, लेकिन यह किसी योग्य पंडित या गुरु की सलाह का विकल्प नहीं है।]"

# ===========================
# GENERATE INSTRUCTION PAIRS
# ===========================

def generate_gita_pairs(verses, max_pairs=20000):
    """Generate instruction pairs from Gita verses"""
    log("Generating Gita instruction pairs...")
    
    pairs = []
    topics = ['कर्म', 'भक्ति', 'ज्ञान', 'धर्म', 'योग', 'शांति', 'जीवन', 'मृत्यु', 'सत्य', 'अहिंसा']
    problems = ['तनाव', 'दुख', 'भ्रम', 'डर', 'क्रोध', 'लोभ', 'मोह', 'अहंकार']
    
    for verse in verses:
        if len(pairs) >= max_pairs:
            break
        
        sanskrit = verse.get('sanskrit', '')
        hindi = verse.get('hindi', '')
        english = verse.get('english', '')
        chapter = verse.get('reference', {}).get('chapter', '')
        verse_num = verse.get('reference', {}).get('verse', '')
        
        if not sanskrit or len(sanskrit) < 20:
            continue
        
        # Type 1: Direct question about verse
        template = random.choice(GITA_TEMPLATES['understanding'])
        opening = random.choice(GURU_OPENINGS)
        closing = random.choice(GURU_CLOSINGS)
        
        pairs.append({
            'instruction': template,
            'input': '',
            'output': f"{opening}यह श्लोक भगवद गीता के अध्याय {chapter}, श्लोक {verse_num} का है।\n\n{sanskrit}\n\n{hindi}\n\n{english}{closing}{DISCLAIMER}",
            'metadata': {
                'text_type': 'gita',
                'chapter': chapter,
                'verse': verse_num,
                'type': 'verse_explanation'
            }
        })
        
        # Type 2: Problem-solution format
        if hindi or english:
            template = random.choice(GITA_TEMPLATES['seeking_advice'])
            topic = random.choice(topics)
            problem = random.choice(problems)
            
            instruction = template.format(topic=topic, problem=problem)
            
            pairs.append({
                'instruction': instruction,
                'input': '',
                'output': f"{opening}भगवद गीता के अनुसार:\n\n{sanskrit}\n\n{hindi if hindi else english}{closing}{DISCLAIMER}",
                'metadata': {
                    'text_type': 'gita',
                    'chapter': chapter,
                    'verse': verse_num,
                    'type': 'practical_guidance'
                }
            })
        
        # Type 3: Daily guidance
        if random.random() < 0.3:  # 30% chance
            template = random.choice(GITA_TEMPLATES['daily_guidance'])
            
            pairs.append({
                'instruction': template,
                'input': '',
                'output': f"आज का श्लोक:\n\n{sanskrit}\n\n{hindi if hindi else english}\n\nवत्स, इस श्लोक को अपने जीवन में उतारो।{DISCLAIMER}",
                'metadata': {
                    'text_type': 'gita',
                    'chapter': chapter,
                    'verse': verse_num,
                    'type': 'daily_guidance'
                }
            })
    
    log(f"  Generated {len(pairs)} Gita pairs")
    return pairs

def generate_ramayana_pairs(verses, max_pairs=15000):
    """Generate instruction pairs from Ramayana verses"""
    log("Generating Ramayana instruction pairs...")
    
    pairs = []
    
    for verse in verses:
        if len(pairs) >= max_pairs:
            break
        
        sanskrit = verse.get('sanskrit', '')
        kanda = verse.get('reference', {}).get('kanda', '')
        sarga = verse.get('reference', {}).get('chapter', '')
        verse_num = verse.get('reference', {}).get('verse', '')
        
        if not sanskrit or len(sanskrit) < 20:
            continue
        
        opening = random.choice(GURU_OPENINGS)
        closing = random.choice(GURU_CLOSINGS)
        
        # Type 1: Character wisdom
        template = random.choice(RAMAYANA_TEMPLATES['character'])
        
        pairs.append({
            'instruction': template,
            'input': '',
            'output': f"{opening}रामायण के अनुसार:\n\n{sanskrit}\n\nयह श्लोक {kanda} कांड, सर्ग {sarga} में है।{closing}{DISCLAIMER}",
            'metadata': {
                'text_type': 'ramayana',
                'kanda': kanda,
                'sarga': sarga,
                'verse': verse_num,
                'type': 'character_wisdom'
            }
        })
    
    log(f"  Generated {len(pairs)} Ramayana pairs")
    return pairs

def generate_mahabharata_pairs(verses, max_pairs=15000):
    """Generate instruction pairs from Mahabharata verses"""
    log("Generating Mahabharata instruction pairs...")
    
    pairs = []
    
    for verse in verses:
        if len(pairs) >= max_pairs:
            break
        
        sanskrit = verse.get('sanskrit', '')
        english = verse.get('english', '')
        parva = verse.get('reference', {}).get('parva', '')
        verse_num = verse.get('reference', {}).get('verse', '')
        
        if not sanskrit or len(sanskrit) < 20:
            continue
        
        opening = random.choice(GURU_OPENINGS)
        closing = random.choice(GURU_CLOSINGS)
        
        # Type 1: Wisdom
        template = random.choice(MAHABHARATA_TEMPLATES['wisdom'])
        
        output_text = f"{opening}महाभारत के अनुसार:\n\n{sanskrit}"
        if english:
            output_text += f"\n\n{english}"
        output_text += f"\n\nयह {parva} पर्व में है।{closing}{DISCLAIMER}"
        
        pairs.append({
            'instruction': template,
            'input': '',
            'output': output_text,
            'metadata': {
                'text_type': 'mahabharata',
                'parva': parva,
                'verse': verse_num,
                'type': 'wisdom'
            }
        })
    
    log(f"  Generated {len(pairs)} Mahabharata pairs")
    return pairs

# ===========================
# SAVE INSTRUCTION PAIRS
# ===========================

def save_pairs(pairs, filename):
    """Save instruction pairs"""
    output_file = OUTPUT_DIR / filename
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')
    log(f"Saved {len(pairs)} pairs to {output_file}")

# ===========================
# MAIN
# ===========================

def main():
    """Main function"""
    log("VEDRISHI AI - INSTRUCTION PAIR GENERATOR (V2 - Hindi Enhanced)")
    log("=" * 60)
    
    # Load final dataset
    final_file = MAIN_DATASET
    all_verses = []
    
    with open(final_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                all_verses.append(json.loads(line))
    
    log(f"Loaded {len(all_verses)} verses from final dataset")
    
    # Separate by text type
    gita = [v for v in all_verses if v['text_type'] == 'gita']
    ramayana = [v for v in all_verses if v['text_type'] == 'ramayana']
    mahabharata = [v for v in all_verses if v['text_type'] == 'mahabharata']
    
    log(f"Gita: {len(gita)}, Ramayana: {len(ramayana)}, Mahabharata: {len(mahabharata)}")
    
    # Count Hindi availability
    for name, verses in [("Gita", gita), ("Ramayana", ramayana), ("Mahabharata", mahabharata)]:
        with_hindi = sum(1 for v in verses if v.get('hindi') and len(str(v.get('hindi', ''))) > 10)
        log(f"  {name} with Hindi: {with_hindi}/{len(verses)}")
    
    # Generate pairs - increased caps for Hindi availability
    all_pairs = []
    all_pairs.extend(generate_gita_pairs(gita, max_pairs=50000))
    all_pairs.extend(generate_ramayana_pairs(ramayana, max_pairs=50000))
    all_pairs.extend(generate_mahabharata_pairs(mahabharata, max_pairs=50000))
    
    log(f"\nTotal instruction pairs: {len(all_pairs)}")
    
    # Save
    save_pairs(all_pairs, "vedrishi_instruction_pairs.jsonl")
    
    # Statistics
    stats = {
        'total_pairs': len(all_pairs),
        'by_text_type': {},
        'by_type': {},
        'timestamp': datetime.now().isoformat()
    }
    
    for pair in all_pairs:
        text_type = pair['metadata']['text_type']
        pair_type = pair['metadata']['type']
        stats['by_text_type'][text_type] = stats['by_text_type'].get(text_type, 0) + 1
        stats['by_type'][pair_type] = stats['by_type'].get(pair_type, 0) + 1
    
    stats_file = OUTPUT_DIR / "generation_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    log(f"\nStatistics:")
    log(f"  Total pairs: {stats['total_pairs']}")
    log(f"  By text type: {stats['by_text_type']}")
    log(f"  By type: {stats['by_type']}")
    
    log("\n" + "=" * 60)
    log("INSTRUCTION PAIR GENERATION COMPLETE")
    log("=" * 60)
    
    return stats

if __name__ == "__main__":
    main()
