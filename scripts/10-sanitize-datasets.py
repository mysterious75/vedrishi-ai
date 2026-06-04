#!/usr/bin/env python3
"""
VEDRISHI AI - Dataset Sanitizer
Removes company/developer names from datasets for production safety
"""

import json
import re
from pathlib import Path
from datetime import datetime

# Configuration
RAW_DIR = Path(__file__).parent.parent / "dataset" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "dataset" / "processed"
FINAL_DIR = Path(__file__).parent.parent / "dataset" / "final"
LOG_FILE = FINAL_DIR / "sanitization_log.txt"

def log(message):
    """Log message to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ===========================
# NAMES TO REMOVE
# ===========================

COMPANY_NAMES = [
    "DharmicData",
    "VedicRAG_AI",
    "AI4Bharat",
    "Sangraha",
    "IndicAlign",
    "GRETIL",
    "DCS",
    "Sanskrit NLP",
    "SanskritDep",
    "ITX",
    "itc",
    "monier-williams",
    "Spokensanskrit",
    "spokensanskrit",
    "sanskrit-lexicon",
    "University of the West",
    "Dhamma",
    "dharmacentral",
    "Himalayan Academy",
    "gitasupersite",
    "Gitapress",
    "Gita Press",
    "WebSites",
    "Sanskrit Documents",
    "sanskritdocuments.org",
]

DEVELOPER_NAMES = [
    "DharmicData",
    "VedicRAG_AI",
    "AI4Bharat",
    "monier",
    "Monier-Williams",
    "ITX",
]

# Patterns to remove
PATTERNS_TO_REMOVE = [
    r"(?i)from\s+(DharmicData|VedicRAG_AI|AI4Bharat|GRETIL|DCS)",
    r"(?i)by\s+(DharmicData|VedicRAG_AI|AI4Bharat)",
    r"(?i)source[:\s]+(DharmicData|VedicRAG_AI|AI4Bharat|GRETIL|DCS)",
    r"(?i)author[:\s]+(DharmicData|VedicRAG_AI|AI4Bharat)",
    r"(?i)dataset[:\s]+(DharmicData|VedicRAG_AI|AI4Bharat|GRETIL|DCS)",
    r"(?i)credit[:\s]+(DharmicData|VedicRAG_AI|AI4Bharat)",
    r"(?i)license[:\s]+(ODbL|CC-BY|Creative Commons)",
    r"(?i)\(c\)\s*\d{4}",
    r"(?i)copyright\s+\d{4}",
]

# ===========================
# SANITIZE FUNCTIONS
# ===========================

def sanitize_text(text):
    """Remove company/developer names from text"""
    if not isinstance(text, str):
        return text
    
    # Remove company names
    for name in COMPANY_NAMES:
        text = text.replace(name, "[DATASET]")
    
    # Remove developer names
    for name in DEVELOPER_NAMES:
        text = text.replace(name, "[CONTRIBUTOR]")
    
    # Remove patterns
    for pattern in PATTERNS_TO_REMOVE:
        text = re.sub(pattern, "[REDACTED]", text)
    
    # Remove URLs
    text = re.sub(r'https?://\S+', '[URL]', text)
    text = re.sub(r'www\.\S+', '[URL]', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    
    return text

def sanitize_metadata(metadata):
    """Remove company/developer names from metadata"""
    if not isinstance(metadata, dict):
        return metadata
    
    sanitized = {}
    for key, value in metadata.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_text(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_metadata(value)
        else:
            sanitized[key] = value
    
    return sanitized

# ===========================
# SANITIZE FILES
# ===========================

def sanitize_jsonl_file(input_file, output_file):
    """Sanitize a JSONL file"""
    log(f"Sanitizing: {input_file}")
    
    sanitized_count = 0
    total_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            if not line.strip():
                continue
            
            total_count += 1
            entry = json.loads(line)
            
            # Sanitize text fields
            if 'sanskrit' in entry:
                entry['sanskrit'] = sanitize_text(entry['sanskrit'])
            if 'hindi' in entry:
                entry['hindi'] = sanitize_text(entry['hindi'])
            if 'english' in entry:
                entry['english'] = sanitize_text(entry['english'])
            if 'commentaries' in entry:
                entry['commentaries'] = [sanitize_text(c) for c in entry['commentaries']]
            
            # Sanitize metadata
            if 'metadata' in entry:
                entry['metadata'] = sanitize_metadata(entry['metadata'])
            if 'reference' in entry:
                entry['reference'] = sanitize_metadata(entry['reference'])
            
            f_out.write(json.dumps(entry, ensure_ascii=False) + '\n')
            sanitized_count += 1
    
    log(f"  Sanitized {sanitized_count}/{total_count} entries")
    return sanitized_count

def main():
    """Main function"""
    log("=" * 60)
    log("VEDRISHI AI - DATASET SANITIZATION")
    log("=" * 60)
    
    # Sanitize processed files
    processed_files = [
        "vedrishi_gita_clean.jsonl",
        "vedrishi_ramayana_clean.jsonl",
        "vedrishi_mahabharata_clean.jsonl"
    ]
    
    for filename in processed_files:
        input_file = PROCESSED_DIR / filename
        output_file = PROCESSED_DIR / filename.replace("_clean.jsonl", "_sanitized.jsonl")
        
        if input_file.exists():
            sanitize_jsonl_file(input_file, output_file)
    
    # Sanitize final file
    final_input = FINAL_DIR / "vedrishi_complete.jsonl"
    final_output = FINAL_DIR / "vedrishi_complete_sanitized.jsonl"
    
    if final_input.exists():
        sanitize_jsonl_file(final_input, final_output)
    
    # Sanitize instruction pairs
    instruction_input = Path(__file__).parent.parent / "dataset" / "instruction-pairs" / "vedrishi_instruction_pairs.jsonl"
    instruction_output = Path(__file__).parent.parent / "dataset" / "instruction-pairs" / "vedrishi_instruction_pairs_sanitized.jsonl"
    
    if instruction_input.exists():
        sanitize_jsonl_file(instruction_input, instruction_output)
    
    log("\n" + "=" * 60)
    log("SANITIZATION COMPLETE")
    log("=" * 60)
    log(f"Files sanitized: {len(processed_files) + 2}")
    log(f"Output directory: {FINAL_DIR}")
    
    print("\n" + "=" * 60)
    print("DATASET SANITIZATION COMPLETE")
    print("=" * 60)
    print("All company/developer names removed for production safety")

if __name__ == "__main__":
    main()
