#!/usr/bin/env python3
"""
VEDRISHI AI - Mahabharata Data Cleaner
Merges all Mahabharata sources into one clean dataset
"""

import json
import os
import hashlib
from pathlib import Path
from datetime import datetime

# Configuration
RAW_DIR = Path(__file__).parent.parent / "dataset" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "dataset" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = PROCESSED_DIR / "mahabharata_cleaning_log.txt"

def log(message):
    """Log message to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def normalize_text(text):
    """Normalize text"""
    if not text or not isinstance(text, str):
        return ""
    text = ' '.join(text.split())
    return text.strip()

# ===========================
# SOURCE 1: DharmicData Mahabharata
# ===========================

def load_dharmicdata_mahabharata():
    """Load Mahabharata from DharmicData"""
    log("Loading DharmicData Mahabharata...")
    
    mb_dir = RAW_DIR / "DharmicData" / "Mahabharata"
    all_verses = []
    
    if not mb_dir.exists():
        log("  DharmicData Mahabharata directory not found")
        return all_verses
    
    for file_path in mb_dir.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict):
                        verse = {
                            'source': 'DharmicData_Mahabharata',
                            'text': 'mahabharata',
                            'parva': entry.get('parva', entry.get('book', '')),
                            'section': entry.get('section', entry.get('chapter', '')),
                            'verse': entry.get('verse', 0),
                            'sanskrit': normalize_text(entry.get('text', entry.get('sanskrit', ''))),
                            'hindi': normalize_text(entry.get('hindi', '')),
                            'english': normalize_text(entry.get('english', '')),
                            'commentaries': {}
                        }
                        if verse['sanskrit']:
                            all_verses.append(verse)
        except Exception as e:
            log(f"  Error loading {file_path.name}: {str(e)[:100]}")
    
    log(f"  Loaded {len(all_verses)} verses from DharmicData Mahabharata")
    return all_verses

# ===========================
# SOURCE 2: snskrt-mahabharat
# ===========================

def load_snskrt_mahabharat():
    """Load from snskrt-mahabharat (HuggingFace)"""
    log("Loading snskrt-mahabharat...")
    
    dataset_dir = RAW_DIR / "snskrt-mahabharat"
    all_verses = []
    
    if not dataset_dir.exists():
        log("  snskrt-mahabharat directory not found")
        return all_verses
    
    for file_path in dataset_dir.rglob("*.arrow"):
        try:
            from datasets import Dataset
            ds = Dataset.from_file(str(file_path))
            
            for entry in ds:
                verse = {
                    'source': 'snskrt-mahabharat',
                    'text': 'mahabharata',
                    'parva': entry.get('parva', entry.get('book', '')),
                    'section': entry.get('section', entry.get('chapter', '')),
                    'verse': entry.get('verse', 0),
                    'sanskrit': normalize_text(entry.get('sanskrit', entry.get('text', ''))),
                    'hindi': normalize_text(entry.get('hindi', '')),
                    'english': normalize_text(entry.get('english', '')),
                    'commentaries': {}
                }
                if verse['sanskrit']:
                    all_verses.append(verse)
        except Exception as e:
            log(f"  Error loading {file_path.name}: {str(e)[:100]}")
    
    log(f"  Loaded {len(all_verses)} verses from snskrt-mahabharat")
    return all_verses

# ===========================
# SOURCE 3: VedicRAG_AI
# ===========================

def load_vedicrag_mahabharata():
    """Load Mahabharata from VedicRAG_AI"""
    log("Loading VedicRAG_AI Mahabharata...")
    
    corpus_dir = RAW_DIR / "VedicRAG_AI" / "nalanda_library"
    all_verses = []
    
    if not corpus_dir.exists():
        log("  VedicRAG_AI directory not found")
        return all_verses
    
    # Load corpus files
    for file_path in corpus_dir.glob("nalanda_corpus_part_*.txt"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse structured text format
            blocks = content.split('---')
            
            for block in blocks:
                lines = block.strip().split('\n')
                verse_data = {}
                
                for line in lines:
                    if line.startswith('Source:'):
                        verse_data['source_text'] = line[7:].strip()
                    elif line.startswith('Category:'):
                        verse_data['category'] = line[9:].strip()
                    elif line.startswith('Verse:'):
                        try:
                            verse_data['verse'] = int(line[6:].strip())
                        except:
                            verse_data['verse'] = 0
                    elif line.startswith('Sanskrit:'):
                        verse_data['sanskrit'] = line[9:].strip()
                    elif line.startswith('English:'):
                        verse_data['english'] = line[8:].strip()
                
                if verse_data.get('sanskrit') and verse_data.get('category') == 'Mahabharata':
                    verse = {
                        'source': 'VedicRAG_AI',
                        'text': 'mahabharata',
                        'parva': verse_data.get('source_text', ''),
                        'section': '',
                        'verse': verse_data.get('verse', 0),
                        'sanskrit': normalize_text(verse_data['sanskrit']),
                        'hindi': '',
                        'english': normalize_text(verse_data.get('english', '')),
                        'commentaries': {}
                    }
                    all_verses.append(verse)
        except Exception as e:
            log(f"  Error loading {file_path.name}: {str(e)[:100]}")
    
    log(f"  Loaded {len(all_verses)} verses from VedicRAG_AI Mahabharata")
    return all_verses

# ===========================
# MERGE & DEDUPLICATE
# ===========================

def merge_all_mahabharata():
    """Merge all Mahabharata sources"""
    log("=" * 60)
    log("MERGING ALL MAHABHARATA SOURCES")
    log("=" * 60)
    
    sources = []
    sources.extend(load_dharmicdata_mahabharata())
    sources.extend(load_snskrt_mahabharat())
    sources.extend(load_vedicrag_mahabharata())
    
    log(f"\nTotal verses loaded: {len(sources)}")
    
    # Deduplicate
    seen = set()
    unique_verses = []
    duplicates = 0
    
    for verse in sources:
        key = f"{verse['parva']}_{verse['section']}_{verse['verse']}_{verse['sanskrit'][:50]}"
        key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
        
        if key_hash not in seen:
            seen.add(key_hash)
            unique_verses.append(verse)
        else:
            duplicates += 1
    
    log(f"Unique verses: {len(unique_verses)}")
    log(f"Duplicates removed: {duplicates}")
    
    return unique_verses

# ===========================
# QUALITY CHECK
# ===========================

def quality_check(verses):
    """Quality check"""
    log("\n" + "=" * 60)
    log("QUALITY CHECK")
    log("=" * 60)
    
    valid_verses = []
    issues = {'no_sanskrit': 0, 'too_short': 0}
    
    for verse in verses:
        if not verse['sanskrit'] or len(verse['sanskrit']) < 10:
            issues['no_sanskrit'] += 1
            continue
        if len(verse['sanskrit']) < 20:
            issues['too_short'] += 1
            continue
        valid_verses.append(verse)
    
    log(f"Valid verses: {len(valid_verses)}")
    log(f"Issues: {issues}")
    
    return valid_verses

# ===========================
# SAVE
# ===========================

def save_cleaned_data(verses):
    """Save cleaned data"""
    log("\n" + "=" * 60)
    log("SAVING CLEANED DATA")
    log("=" * 60)
    
    output_file = PROCESSED_DIR / "vedrishi_mahabharata_clean.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')
    
    log(f"Saved {len(verses)} verses to {output_file}")
    
    stats = {
        'total_verses': len(verses),
        'sources': list(set(v['source'] for v in verses)),
        'with_hindi': sum(1 for v in verses if v['hindi']),
        'with_english': sum(1 for v in verses if v['english']),
        'timestamp': datetime.now().isoformat()
    }
    
    stats_file = PROCESSED_DIR / "mahabharata_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    log(f"Statistics: {stats}")
    return stats

# ===========================
# MAIN
# ===========================

def main():
    """Main function"""
    log("VEDRISHI AI - MAHABHARATA DATA CLEANER")
    log("=" * 60)
    
    verses = merge_all_mahabharata()
    valid_verses = quality_check(verses)
    stats = save_cleaned_data(valid_verses)
    
    log("\n" + "=" * 60)
    log("MAHABHARATA CLEANING COMPLETE")
    log("=" * 60)
    
    return stats

if __name__ == "__main__":
    main()
