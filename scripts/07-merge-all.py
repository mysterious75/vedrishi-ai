#!/usr/bin/env python3
"""
VEDRISHI AI - Master Dataset Merger
Combines all cleaned datasets into one unified format
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

# Configuration
PROCESSED_DIR = Path(__file__).parent.parent / "dataset" / "processed"
OUTPUT_DIR = Path(__file__).parent.parent / "dataset" / "final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / "merger_log.txt"

def log(message):
    """Log message to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ===========================
# LOAD CLEANED DATA
# ===========================

def load_jsonl(filename):
    """Load JSONL file"""
    filepath = PROCESSED_DIR / filename
    data = []
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
    return data

# ===========================
# UNIFIED FORMAT
# ===========================

def create_unified_entry(verse, text_type):
    """Create unified format entry"""
    return {
        'id': hashlib.md5(f"{text_type}_{verse.get('chapter', verse.get('kanda', verse.get('parva', '')))}_{verse.get('verse', 0)}_{verse.get('sanskrit', '')[:50]}".encode()).hexdigest(),
        'text_type': text_type,
        'source': verse.get('source', ''),
        'reference': {
            'chapter': verse.get('chapter', verse.get('sarga', verse.get('section', ''))),
            'verse': verse.get('verse', 0),
            'kanda': verse.get('kanda', ''),
            'parva': verse.get('parva', '')
        },
        'sanskrit': verse.get('sanskrit', ''),
        'hindi': verse.get('hindi', ''),
        'english': verse.get('english', ''),
        'commentaries': verse.get('commentaries', {}),
        'metadata': {
            'has_hindi': bool(verse.get('hindi')),
            'has_english': bool(verse.get('english')),
            'has_commentaries': bool(verse.get('commentaries')),
            'sanskrit_length': len(verse.get('sanskrit', ''))
        }
    }

# ===========================
# MERGE ALL
# ===========================

def merge_all():
    """Merge all cleaned datasets"""
    log("=" * 60)
    log("MERGING ALL CLEANED DATASETS")
    log("=" * 60)
    
    all_entries = []
    
    # Load Gita
    log("Loading Gita...")
    gita = load_jsonl("vedrishi_gita_clean.jsonl")
    for verse in gita:
        all_entries.append(create_unified_entry(verse, 'gita'))
    log(f"  Gita: {len(gita)} verses")
    
    # Load Ramayana
    log("Loading Ramayana...")
    ramayana = load_jsonl("vedrishi_ramayana_clean.jsonl")
    for verse in ramayana:
        all_entries.append(create_unified_entry(verse, 'ramayana'))
    log(f"  Ramayana: {len(ramayana)} verses")
    
    # Load Mahabharata
    log("Loading Mahabharata...")
    mahabharata = load_jsonl("vedrishi_mahabharata_clean.jsonl")
    for verse in mahabharata:
        all_entries.append(create_unified_entry(verse, 'mahabharata'))
    log(f"  Mahabharata: {len(mahabharata)} verses")
    
    log(f"\nTotal entries: {len(all_entries)}")
    
    # Deduplicate
    seen = set()
    unique_entries = []
    duplicates = 0
    
    for entry in all_entries:
        key = f"{entry['text_type']}_{entry['reference']['chapter']}_{entry['reference']['verse']}_{entry['sanskrit'][:50]}"
        key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
        
        if key_hash not in seen:
            seen.add(key_hash)
            unique_entries.append(entry)
        else:
            duplicates += 1
    
    log(f"Unique entries: {len(unique_entries)}")
    log(f"Duplicates removed: {duplicates}")
    
    return unique_entries

# ===========================
# SAVE FINAL DATASET
# ===========================

def save_final(entries):
    """Save final unified dataset"""
    log("\n" + "=" * 60)
    log("SAVING FINAL DATASET")
    log("=" * 60)
    
    # Save as JSONL
    output_jsonl = OUTPUT_DIR / "vedrishi_complete.jsonl"
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    log(f"Saved {len(entries)} entries to {output_jsonl}")
    
    # Save as JSON
    output_json = OUTPUT_DIR / "vedrishi_complete.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    
    log(f"Saved {len(entries)} entries to {output_json}")
    
    # Statistics
    stats = {
        'total_entries': len(entries),
        'by_text_type': {},
        'by_source': {},
        'with_hindi': sum(1 for e in entries if e['metadata']['has_hindi']),
        'with_english': sum(1 for e in entries if e['metadata']['has_english']),
        'with_commentaries': sum(1 for e in entries if e['metadata']['has_commentaries']),
        'timestamp': datetime.now().isoformat()
    }
    
    for entry in entries:
        text_type = entry['text_type']
        stats['by_text_type'][text_type] = stats['by_text_type'].get(text_type, 0) + 1
        
        source = entry['source']
        stats['by_source'][source] = stats['by_source'].get(source, 0) + 1
    
    stats_file = OUTPUT_DIR / "final_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    log(f"\nFinal Statistics:")
    log(f"  Total entries: {stats['total_entries']}")
    log(f"  By text type: {stats['by_text_type']}")
    log(f"  With Hindi: {stats['with_hindi']}")
    log(f"  With English: {stats['with_english']}")
    log(f"  With Commentaries: {stats['with_commentaries']}")
    
    return stats

# ===========================
# MAIN
# ===========================

def main():
    """Main function"""
    log("VEDRISHI AI - MASTER DATASET MERGER")
    log("=" * 60)
    
    entries = merge_all()
    stats = save_final(entries)
    
    log("\n" + "=" * 60)
    log("MASTER MERGER COMPLETE")
    log("=" * 60)
    
    return stats

if __name__ == "__main__":
    main()
