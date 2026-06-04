#!/usr/bin/env python3
"""
VEDRISHI AI - Ramayana Data Cleaner
Merges all Ramayana sources into one clean dataset
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

LOG_FILE = PROCESSED_DIR / "ramayana_cleaning_log.txt"

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
# SOURCE 1: DharmicData Ramayana
# ===========================

def load_dharmicdata_ramayana():
    """Load Ramayana from DharmicData"""
    log("Loading DharmicData Ramayana...")
    
    ramayana_dir = RAW_DIR / "DharmicData" / "ValmikiRamayana"
    all_verses = []
    
    if not ramayana_dir.exists():
        log("  DharmicData Ramayana directory not found")
        return all_verses
    
    # Load all JSON files
    for file_path in ramayana_dir.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                for entry in data:
                    verse = {
                        'source': 'DharmicData_Ramayana',
                        'text': 'ramayana',
                        'kanda': entry.get('kanda', entry.get('book', '')),
                        'sarga': entry.get('sarga', entry.get('chapter', '')),
                        'verse': entry.get('verse', 0),
                        'sanskrit': normalize_text(entry.get('text', entry.get('sanskrit', ''))),
                        'hindi': normalize_text(entry.get('hindi', '')),
                        'english': normalize_text(entry.get('english', '')),
                        'commentaries': {}
                    }
                    if verse['sanskrit']:
                        all_verses.append(verse)
            elif isinstance(data, dict):
                # Try to extract verses from dict
                for key, value in data.items():
                    if isinstance(value, list):
                        for entry in value:
                            if isinstance(entry, dict):
                                verse = {
                                    'source': 'DharmicData_Ramayana',
                                    'text': 'ramayana',
                                    'kanda': entry.get('kanda', entry.get('book', '')),
                                    'sarga': entry.get('sarga', entry.get('chapter', '')),
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
    
    log(f"  Loaded {len(all_verses)} verses from DharmicData Ramayana")
    return all_verses

# ===========================
# SOURCE 2: Valmiki_Ramayan_Dataset
# ===========================

def load_valmiki_ramayan():
    """Load from Valmiki_Ramayan_Dataset"""
    log("Loading Valmiki_Ramayan_Dataset...")
    
    dataset_dir = RAW_DIR / "Valmiki_Ramayan_Dataset"
    all_verses = []
    
    if not dataset_dir.exists():
        log("  Valmiki_Ramayan_Dataset directory not found")
        return all_verses
    
    # Check for different file structures
    for file_path in dataset_dir.rglob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict):
                        verse = {
                            'source': 'Valmiki_Ramayan_Dataset',
                            'text': 'ramayana',
                            'kanda': entry.get('kanda', entry.get('book', '')),
                            'sarga': entry.get('sarga', entry.get('chapter', '')),
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
    
    # Also check for text files
    for file_path in dataset_dir.rglob("*.txt"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse text format (if structured)
            lines = content.split('\n')
            current_verse = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    if current_verse and current_verse.get('sanskrit'):
                        verse = {
                            'source': 'Valmiki_Ramayan_Dataset',
                            'text': 'ramayana',
                            'kanda': current_verse.get('kanda', ''),
                            'sarga': current_verse.get('sarga', ''),
                            'verse': current_verse.get('verse', 0),
                            'sanskrit': normalize_text(current_verse.get('sanskrit', '')),
                            'hindi': normalize_text(current_verse.get('hindi', '')),
                            'english': normalize_text(current_verse.get('english', '')),
                            'commentaries': {}
                        }
                        all_verses.append(verse)
                    current_verse = {}
                elif line.startswith('Sanskrit:'):
                    current_verse['sanskrit'] = line[8:].strip()
                elif line.startswith('Hindi:'):
                    current_verse['hindi'] = line[6:].strip()
                elif line.startswith('English:'):
                    current_verse['english'] = line[8:].strip()
        except Exception as e:
            log(f"  Error loading {file_path.name}: {str(e)[:100]}")
    
    log(f"  Loaded {len(all_verses)} verses from Valmiki_Ramayan_Dataset")
    return all_verses

# ===========================
# SOURCE 3: snskrt-ramayan
# ===========================

def load_snskrt_ramayan():
    """Load from snskrt-ramayan (HuggingFace)"""
    log("Loading snskrt-ramayan...")
    
    dataset_dir = RAW_DIR / "snskrt-ramayan"
    all_verses = []
    
    if not dataset_dir.exists():
        log("  snskrt-ramayan directory not found")
        return all_verses
    
    # Check for arrow/parquet files
    for file_path in dataset_dir.rglob("*.arrow"):
        try:
            # Try to load with datasets library
            from datasets import Dataset
            ds = Dataset.from_file(str(file_path))
            
            for entry in ds:
                verse = {
                    'source': 'snskrt-ramayan',
                    'text': 'ramayana',
                    'kanda': entry.get('kanda', entry.get('book', '')),
                    'sarga': entry.get('sarga', entry.get('chapter', '')),
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
    
    log(f"  Loaded {len(all_verses)} verses from snskrt-ramayan")
    return all_verses

# ===========================
# MERGE & DEDUPLICATE
# ===========================

def merge_all_ramayana():
    """Merge all Ramayana sources"""
    log("=" * 60)
    log("MERGING ALL RAMAYANA SOURCES")
    log("=" * 60)
    
    sources = []
    sources.extend(load_dharmicdata_ramayana())
    sources.extend(load_valmiki_ramayan())
    sources.extend(load_snskrt_ramayan())
    
    log(f"\nTotal verses loaded: {len(sources)}")
    
    # Deduplicate
    seen = set()
    unique_verses = []
    duplicates = 0
    
    for verse in sources:
        key = f"{verse['kanda']}_{verse['sarga']}_{verse['verse']}_{verse['sanskrit'][:50]}"
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
    
    output_file = PROCESSED_DIR / "vedrishi_ramayana_clean.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')
    
    log(f"Saved {len(verses)} verses to {output_file}")
    
    # Statistics
    stats = {
        'total_verses': len(verses),
        'sources': list(set(v['source'] for v in verses)),
        'with_hindi': sum(1 for v in verses if v['hindi']),
        'with_english': sum(1 for v in verses if v['english']),
        'timestamp': datetime.now().isoformat()
    }
    
    stats_file = PROCESSED_DIR / "ramayana_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    log(f"Statistics: {stats}")
    return stats

# ===========================
# MAIN
# ===========================

def main():
    """Main function"""
    log("VEDRISHI AI - RAMAYANA DATA CLEANER")
    log("=" * 60)
    
    verses = merge_all_ramayana()
    valid_verses = quality_check(verses)
    stats = save_cleaned_data(valid_verses)
    
    log("\n" + "=" * 60)
    log("RAMAYANA CLEANING COMPLETE")
    log("=" * 60)
    
    return stats

if __name__ == "__main__":
    main()
