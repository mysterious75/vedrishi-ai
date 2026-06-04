#!/usr/bin/env python3
"""
VEDRISHI AI - Master Data Cleaner & Merger
Merges all Gita sources into one clean dataset
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

# Log file
LOG_FILE = PROCESSED_DIR / "cleaning_log.txt"

def log(message):
    """Log message to file and print"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    # Write to file only (avoid console encoding issues)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def normalize_text(text):
    """Normalize text - fix encoding, remove extra spaces"""
    if not text:
        return ""
    
    # Handle dict objects
    if isinstance(text, dict):
        # Try to get a string value from dict
        for key in ['text', 'sanskrit', 'hindi', 'english', 'meaning']:
            if key in text and isinstance(text[key], str):
                text = text[key]
                break
        else:
            return ""
    
    if not isinstance(text, str):
        return str(text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Normalize Unicode
    text = text.strip()
    
    return text

def extract_verse_id(text):
    """Extract verse ID from text for deduplication"""
    # Create hash of verse content
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# ===========================
# SOURCE 1: DharmicData
# ===========================

def load_dharmicdata_gita():
    """Load Gita from DharmicData"""
    log("Loading DharmicData Gita...")
    
    gita_dir = RAW_DIR / "DharmicData" / "SrimadBhagvadGita"
    all_verses = []
    
    for chapter_num in range(1, 19):
        file_path = gita_dir / f"bhagavad_gita_chapter_{chapter_num}.json"
        
        if not file_path.exists():
            log(f"  Warning: Chapter {chapter_num} not found")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for entry in data.get('BhagavadGitaChapter', []):
            verse = {
                'source': 'DharmicData',
                'text': 'gita',
                'chapter': chapter_num,
                'verse': entry.get('verse', 0),
                'sanskrit': normalize_text(entry.get('text', '')),
                'hindi': '',
                'english': '',
                'commentaries': {}
            }
            
            # Extract translations
            translations = entry.get('translations', {})
            if 'swami ramsukhdas' in translations:
                verse['hindi'] = normalize_text(translations['swami ramsukhdas'])
            if 'swami sivananda' in translations:
                verse['english'] = normalize_text(translations['swami sivananda'])
            
            # Extract commentaries
            commentaries = entry.get('commentaries', {})
            for author, text in commentaries.items():
                verse['commentaries'][author] = normalize_text(text)
            
            all_verses.append(verse)
    
    log(f"  Loaded {len(all_verses)} verses from DharmicData")
    return all_verses

# ===========================
# SOURCE 2: bhagavad-gita-dataset
# ===========================

def load_bhagavad_gita_dataset():
    """Load Gita from bhagavad-gita-dataset"""
    log("Loading bhagavad-gita-dataset...")
    
    dataset_dir = RAW_DIR / "bhagavad-gita-dataset" / "dataset"
    all_verses = []
    
    for chapter_num in range(1, 19):
        file_path = dataset_dir / f"chapter_{chapter_num:02d}.json"
        
        if not file_path.exists():
            log(f"  Warning: Chapter {chapter_num} not found")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # This dataset has chapters with verses
        chapter_data = data if isinstance(data, list) else data.get('verses', [])
        
        for entry in chapter_data:
            verse = {
                'source': 'bhagavad-gita-dataset',
                'text': 'gita',
                'chapter': chapter_num,
                'verse': entry.get('verse_number', entry.get('verse', 0)),
                'sanskrit': normalize_text(entry.get('sanskrit', entry.get('text', ''))),
                'hindi': normalize_text(entry.get('hindi', '')),
                'english': normalize_text(entry.get('english', '')),
                'commentaries': {}
            }
            
            all_verses.append(verse)
    
    log(f"  Loaded {len(all_verses)} verses from bhagavad-gita-dataset")
    return all_verses

# ===========================
# SOURCE 3: gita/gita
# ===========================

def load_gita_gita():
    """Load Gita from gita/gita"""
    log("Loading gita/gita...")
    
    gita_dir = RAW_DIR / "gita" / "data"
    all_verses = []
    
    if not gita_dir.exists():
        log("  Warning: gita/data directory not found")
        return all_verses
    
    # Load verse data
    verse_file = gita_dir / "verse.json"
    if verse_file.exists():
        with open(verse_file, 'r', encoding='utf-8') as f:
            verses = json.load(f)
        
        for entry in verses:
            verse = {
                'source': 'gita/gita',
                'text': 'gita',
                'chapter': entry.get('chapter', 0),
                'verse': entry.get('verse', 0),
                'sanskrit': normalize_text(entry.get('text', '')),
                'hindi': normalize_text(entry.get('hindi_meaning', '')),
                'english': normalize_text(entry.get('english_meaning', '')),
                'commentaries': {}
            }
            all_verses.append(verse)
    
    log(f"  Loaded {len(all_verses)} verses from gita/gita")
    return all_verses

# ===========================
# MERGE & DEDUPLICATE
# ===========================

def merge_all_gita():
    """Merge all Gita sources and remove duplicates"""
    log("=" * 60)
    log("MERGING ALL GITA SOURCES")
    log("=" * 60)
    
    # Load all sources
    sources = []
    sources.extend(load_dharmicdata_gita())
    sources.extend(load_bhagavad_gita_dataset())
    sources.extend(load_gita_gita())
    
    log(f"\nTotal verses loaded: {len(sources)}")
    
    # Deduplicate based on verse content
    seen = set()
    unique_verses = []
    duplicates = 0
    
    for verse in sources:
        # Create unique key from chapter + verse + sanskrit text
        key = f"{verse['chapter']}_{verse['verse']}_{verse['sanskrit'][:50]}"
        key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
        
        if key_hash not in seen:
            seen.add(key_hash)
            unique_verses.append(verse)
        else:
            duplicates += 1
    
    log(f"Unique verses: {len(unique_verses)}")
    log(f"Duplicates removed: {duplicates}")
    
    # Sort by chapter and verse
    unique_verses.sort(key=lambda x: (x['chapter'], x['verse']))
    
    return unique_verses

# ===========================
# QUALITY CHECK
# ===========================

def quality_check(verses):
    """Quality check - remove invalid entries"""
    log("\n" + "=" * 60)
    log("QUALITY CHECK")
    log("=" * 60)
    
    valid_verses = []
    issues = {
        'no_sanskrit': 0,
        'no_chapter': 0,
        'no_verse': 0,
        'too_short': 0
    }
    
    for verse in verses:
        # Check Sanskrit text exists
        if not verse['sanskrit'] or len(verse['sanskrit']) < 10:
            issues['no_sanskrit'] += 1
            continue
        
        # Check chapter exists
        if not verse['chapter'] or verse['chapter'] < 1 or verse['chapter'] > 18:
            issues['no_chapter'] += 1
            continue
        
        # Check verse exists
        if not verse['verse'] or verse['verse'] < 1:
            issues['no_verse'] += 1
            continue
        
        # Check text is not too short
        if len(verse['sanskrit']) < 20:
            issues['too_short'] += 1
            continue
        
        valid_verses.append(verse)
    
    log(f"Valid verses: {len(valid_verses)}")
    log(f"Issues found:")
    for issue, count in issues.items():
        if count > 0:
            log(f"  - {issue}: {count}")
    
    return valid_verses

# ===========================
# SAVE CLEANED DATA
# ===========================

def save_cleaned_data(verses):
    """Save cleaned data in JSONL format"""
    log("\n" + "=" * 60)
    log("SAVING CLEANED DATA")
    log("=" * 60)
    
    # Save as JSONL
    output_file = PROCESSED_DIR / "vedrishi_gita_clean.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')
    
    log(f"Saved {len(verses)} verses to {output_file}")
    
    # Save as JSON (for readability)
    output_json = PROCESSED_DIR / "vedrishi_gita_clean.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
    
    log(f"Saved {len(verses)} verses to {output_json}")
    
    # Statistics
    stats = {
        'total_verses': len(verses),
        'chapters': len(set(v['chapter'] for v in verses)),
        'sources': list(set(v['source'] for v in verses)),
        'with_hindi': sum(1 for v in verses if v['hindi']),
        'with_english': sum(1 for v in verses if v['english']),
        'with_commentaries': sum(1 for v in verses if v['commentaries']),
        'timestamp': datetime.now().isoformat()
    }
    
    stats_file = PROCESSED_DIR / "gita_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    log(f"\nStatistics:")
    log(f"  Total verses: {stats['total_verses']}")
    log(f"  Chapters: {stats['chapters']}")
    log(f"  With Hindi: {stats['with_hindi']}")
    log(f"  With English: {stats['with_english']}")
    log(f"  With Commentaries: {stats['with_commentaries']}")
    
    return stats

# ===========================
# MAIN
# ===========================

def main():
    """Main function"""
    log("VEDRISHI AI - GITA DATA CLEANER")
    log("=" * 60)
    
    # Merge all sources
    verses = merge_all_gita()
    
    # Quality check
    valid_verses = quality_check(verses)
    
    # Save cleaned data
    stats = save_cleaned_data(valid_verses)
    
    log("\n" + "=" * 60)
    log("✅ GITA CLEANING COMPLETE")
    log("=" * 60)
    
    return stats

if __name__ == "__main__":
    main()
