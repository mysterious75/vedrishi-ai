#!/usr/bin/env python3
"""
VEDRISHI AI - Hindi Translation Merger
Parses Mahabharata Hindi files (1.utf8-18.utf8), attempts Ramayana Hindi,
merges Hindi translations into the existing cleaned dataset.
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict, OrderedDict

# Configuration
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
RAW_DIR = BASE_DIR / "dataset" / "raw"
PROCESSED_DIR = BASE_DIR / "dataset" / "processed"
FINAL_DIR = BASE_DIR / "dataset" / "final"
HINDI_MB_DIR = RAW_DIR / "mahabharata-hindi"
LOG_FILE = PROCESSED_DIR / "hindi_merge_log.txt"

FINAL_DIR.mkdir(parents=True, exist_ok=True)

# Parva name mapping (1-based)
PARVA_NAMES = {
    1: "Adi Parva", 2: "Sabha Parva", 3: "Vana Parva", 4: "Virata Parva",
    5: "Udyoga Parva", 6: "Bhishma Parva", 7: "Drona Parva", 8: "Karna Parva",
    9: "Shalya Parva", 10: "Sauptika Parva", 11: "Stri Parva", 12: "Shanti Parva",
    13: "Anushasana Parva", 14: "Ashvamedhika Parva", 15: "Ashramavasika Parva",
    16: "Mausala Parva", 17: "Mahaprasthanika Parva", 18: "Svargarohana Parva"
}

# Company/developer names to sanitize (from 10-sanitize-datasets.py)
COMPANY_NAMES = [
    "DharmicData", "VedicRAG_AI", "AI4Bharat", "Sangraha", "IndicAlign",
    "GRETIL", "DCS", "Sanskrit NLP", "SanskritDep", "ITX", "itc",
    "monier-williams", "Spokensanskrit", "spokensanskrit", "sanskrit-lexicon",
    "University of the West", "Dhamma", "dharmacentral", "Himalayan Academy",
    "gitasupersite", "Gitapress", "Gita Press", "WebSites", "Sanskrit Documents",
    "sanskritdocuments.org",
]

DEVELOPER_NAMES = [
    "DharmicData", "VedicRAG_AI", "AI4Bharat", "monier", "Monier-Williams", "ITX",
]

PATTERNS_TO_REMOVE = [
    (r"(?i)from\s+(DharmicData|VedicRAG_AI|AI4Bharat|GRETIL|DCS)", "[REDACTED]"),
    (r"(?i)by\s+(DharmicData|VedicRAG_AI|AI4Bharat)", "[REDACTED]"),
    (r"(?i)source[:\s]+(DharmicData|VedicRAG_AI|AI4Bharat|GRETIL|DCS)", "[REDACTED]"),
    (r"(?i)author[:\s]+(DharmicData|VedicRAG_AI|AI4Bharat)", "[REDACTED]"),
    (r"(?i)dataset[:\s]+(DharmicData|VedicRAG_AI|AI4Bharat|GRETIL|DCS)", "[REDACTED]"),
    (r"(?i)credit[:\s]+(DharmicData|VedicRAG_AI|AI4Bharat)", "[REDACTED]"),
    (r"(?i)license[:\s]+(ODbL|CC-BY|Creative Commons)", "[REDACTED]"),
    (r"(?i)\(c\)\s*\d{4}", ""),
    (r"(?i)copyright\s+\d{4}", ""),
]


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")
    print(log_msg)


def sanitize_text(text):
    if not isinstance(text, str) or not text:
        return text
    for name in COMPANY_NAMES:
        text = text.replace(name, "[DATASET]")
    for name in DEVELOPER_NAMES:
        text = text.replace(name, "[CONTRIBUTOR]")
    for pattern, replacement in PATTERNS_TO_REMOVE:
        text = re.sub(pattern, replacement, text)
    text = re.sub(r"https?://\S+", "[URL]", text)
    text = re.sub(r"www\.\S+", "[URL]", text)
    text = re.sub(r"\S+@\S+", "[EMAIL]", text)
    return text


def normalize_sanskrit(text):
    """Normalize Sanskrit text for comparison matching."""
    if not text:
        return ""
    text = " ".join(text.split())
    text = re.sub(r"[।॥\.\,\-\s]", "", text)
    text = text.replace("ॊ", "ो").replace("ॆ", "े")
    text = text.replace("त्त", "त").replace("ॢ", "ृ")
    return text.strip()


# ============================================================
# PHASE 1: Parse Mahabharata Hindi files
# ============================================================

PARVA_CHAPTER_PATTERN = re.compile(r"(\d+)\.(\d+)\.\s*अध्यायः")
VERSE_ID_PATTERN = re.compile(r"(\d+)-(\d+)-(\d+)\s*(?:\((\d+)\))?")
CHAPTER_END_PATTERN = re.compile(r"इति\s*श्रीम")
COMMENTARY_START_PATTERN = re.compile(r"^(\d+-\d+-\d+)\s+")


def parse_mahabharata_hindi():
    """Parse all 18 Mahabharata Hindi files.
    
    Each file contains Sanskrit verses with verse IDs (parva-chapter-verse)
    followed by Hindi commentary/glosses per chapter.
    Returns a dict: (parva, chapter) -> {sanskrit_verses: dict, hindi_commentary: str}
    """
    log("=" * 60)
    log("PHASE 1: Parsing Mahabharata Hindi files")
    log("=" * 60)

    chapter_data = {}
    total_verses_found = 0

    if not HINDI_MB_DIR.exists():
        log(f"ERROR: Mahabharata Hindi directory not found: {HINDI_MB_DIR}")
        return chapter_data, total_verses_found

    # Process files in order
    hindi_files = sorted(
        [f for f in os.listdir(HINDI_MB_DIR) if f.endswith(".utf8")],
        key=lambda x: int(x.split(".")[0])
    )
    log(f"Found {len(hindi_files)} Hindi files: {hindi_files}")

    for fname in hindi_files:
        file_path = HINDI_MB_DIR / fname
        parva_num = int(fname.split(".")[0])
        parva_name = PARVA_NAMES.get(parva_num, f"Parva {parva_num}")
        log(f"  Processing {fname} (Parva {parva_num}: {parva_name})")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        chapter_records = _parse_single_file(lines, parva_num)
        
        for (p, c), record in chapter_records.items():
            key = (p, c)
            if key not in chapter_data:
                chapter_data[key] = {"sanskrit_verses": OrderedDict(), "hindi_commentary": ""}
            
            # Merge sanskrit verses
            ch_sans = chapter_data[key]["sanskrit_verses"]
            for vref, stext in record.get("sanskrit_verses", {}).items():
                if vref not in ch_sans:
                    ch_sans[vref] = stext
                    
            # Merge Hindi commentary - prefer longer one
            existing_hindi = chapter_data[key]["hindi_commentary"]
            new_hindi = record.get("hindi_commentary", "")
            if len(new_hindi) > len(existing_hindi):
                chapter_data[key]["hindi_commentary"] = new_hindi

        for record in chapter_records.values():
            total_verses_found += len(record.get("sanskrit_verses", {}))

    log(f"\n  Total chapters with data: {len(chapter_data)}")
    log(f"  Total verse references found: {total_verses_found}")
    
    # Stats per parva
    parva_stats = defaultdict(lambda: {"chapters": set(), "verses": 0})
    for (p, c), rec in chapter_data.items():
        parva_stats[p]["chapters"].add(c)
        parva_stats[p]["verses"] += len(rec["sanskrit_verses"])
    for p in sorted(parva_stats.keys()):
        ps = parva_stats[p]
        log(f"    Parva {p} ({PARVA_NAMES.get(p,'?')}): {len(ps['chapters'])} chapters, {ps['verses']} verses")

    return chapter_data, total_verses_found


def _parse_single_file(lines, parva_num):
    """Parse a single mahabharata-hindi file.
    
    Structure:
    - Chapter starts with: 'X.Y. अध्यायः ZZZ' or 'पर्वनाम - अध्याय NNN'
    - Sanskrit verses with verse IDs like 'parva-chapter-verse (seq)'
    - Chapter ends with: 'इति श्रीमन्महाभारते...'
    - After chapter end + separator, Hindi commentary/gloss lines
    
    Returns dict: (parva, chapter) -> {sanskrit_verses, hindi_commentary}
    """
    records = {}
    current_chapter = None
    collecting_sanskrit = False
    sanskrit_buffer_lines = []
    verse_found_in_buffer = False

    # Find all chapter start lines
    chapter_starts = []
    for i, line in enumerate(lines):
        m = PARVA_CHAPTER_PATTERN.search(line)
        if m:
            p, c = int(m.group(1)), int(m.group(2))
            chapter_starts.append((i, p, c))

    if not chapter_starts:
        log(f"    WARNING: No chapter headers found in file for parva {parva_num}")
        return records

    # Process each chapter segment
    for idx, (start_line, p, c) in enumerate(chapter_starts):
        end_line = chapter_starts[idx + 1][0] if idx + 1 < len(chapter_starts) else len(lines)
        
        chapter_lines = lines[start_line:end_line]
        chapter_key = (p, c)
        
        # Extract Sanskrit verses from this chapter
        sanskrit_verses = OrderedDict()
        current_verse_id = None
        current_verse_lines = []
        
        for line in chapter_lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Check if line contains a verse-ending marker (verse ID somewhere in the line)
            verse_matches = list(VERSE_ID_PATTERN.finditer(stripped))
            
            if verse_matches:
                # This line has verse markers - extract the last one as the current verse end
                last_match = verse_matches[-1]
                vp, vc, vv = int(last_match.group(1)), int(last_match.group(2)), int(last_match.group(3))
                
                if current_verse_id and current_verse_lines:
                    # Save previous verse
                    verse_text = " ".join(current_verse_lines)
                    vkey = (current_verse_id[0], current_verse_id[1], current_verse_id[2])
                    if vkey not in sanskrit_verses:
                        sanskrit_verses[vkey] = verse_text
                
                # Get text before the last verse marker (Sanskrit text)
                text_before_marker = stripped[:last_match.start()].strip()
                # Remove any speaker tags or metadata at start
                text_before_marker = re.sub(r"^[`\'\"\s]*", "", text_before_marker)
                
                if text_before_marker and len(text_before_marker) > 5:
                    current_verse_lines = [text_before_marker]
                else:
                    current_verse_lines = []
                
                current_verse_id = (vp, vc, vv)
            else:
                # Non-verse line - could be continuation of Sanskrit or chapter metadata
                if not sanskrit_buffer_lines:
                    # Check for chapter/sub-chapter title lines
                    if re.match(r"^[आ-ौ]", stripped) and not re.search(r"[॥]", stripped):
                        if len(stripped) < 100:
                            # Chapter metadata, skip
                            continue
                
                if current_verse_id and stripped and len(stripped) > 10:
                    current_verse_lines.append(stripped)
        
        # Save last verse
        if current_verse_id and current_verse_lines:
            verse_text = " ".join(current_verse_lines)
            vkey = (current_verse_id[0], current_verse_id[1], current_verse_id[2])
            if vkey not in sanskrit_verses:
                sanskrit_verses[vkey] = verse_text
        
        # Extract Hindi commentary - appears after the chapter-end marker (इति श्रीम)
        # within the same chapter segment as the Sanskrit verses.
        # Commentaries are lines starting with a verse ID (like "1-1-1") containing word glosses.
        hindi_commentary = ""
        commentary_parts = []
        found_end_marker = False
        
        for line in chapter_lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Detect chapter-end marker
            if "इति श्रीम" in stripped or "समाप्त" in stripped:
                found_end_marker = True
                continue
            
            if not found_end_marker:
                continue
            
            # Skip headers/separators
            if stripped.startswith("॥ श्रीः") or stripped.startswith("-   -") or stripped.startswith("(अथ"):
                continue
            if PARVA_CHAPTER_PATTERN.search(stripped):
                continue
            
            # A commentary line starts with a verse ID (e.g., "1-71-1") and contains gloss text
            is_commentary = COMMENTARY_START_PATTERN.match(stripped) and len(stripped) > 80
            is_continuation = commentary_parts and len(stripped) > 40
            
            if is_commentary or is_continuation:
                commentary_parts.append(stripped)
        
        if commentary_parts:
            hindi_commentary = "\n".join(commentary_parts)
        
        if sanskrit_verses or hindi_commentary:
            records[chapter_key] = {
                "sanskrit_verses": sanskrit_verses,
                "hindi_commentary": hindi_commentary
            }

    return records


# ============================================================
# PHASE 2: Parse Ramayana Hindi (attempt)
# ============================================================

def find_ramayana_hindi():
    """Search for Ramayana Hindi translation resources locally.
    
    Checks: Valmiki_Ramayan_Dataset, snskrt-ramayan, any hindi-tagged files.
    Returns dict of (kanda, sarga, shloka) -> hindi_text or None if not found.
    """
    log("\n" + "=" * 60)
    log("PHASE 2: Searching for Ramayana Hindi resources")
    log("=" * 60)

    ramayana_hindi = OrderedDict()
    
    # Check 1: Valmiki_Ramayan_Dataset - has 'translation' field with Devanagari but it's Sanskrit→English glossary
    valmiki_path = RAW_DIR / "Valmiki_Ramayan_Dataset" / "data" / "Valmiki_Ramayan_Shlokas.json"
    if valmiki_path.exists():
        log("  Found Valmiki_Ramayan_Dataset - checking for Hindi translations...")
        try:
            with open(valmiki_path, "r", encoding="utf-8") as f:
                valmiki_data = json.load(f)
            log(f"  Loaded {len(valmiki_data)} entries from Valmiki dataset")
            
            # Check if translation is Hindi (contains Hindi postpositions)
            sample_translations = []
            for d in valmiki_data[:100]:
                t = d.get("translation", "") or ""
                sample_translations.append(t)
            
            # Check for Hindi markers in translation field
            hindi_markers = ["है", "का", "के", "की", "को", "में", "से", "था", "थी", "होता"]
            hindi_count = 0
            for t in sample_translations:
                if any(m in t for m in hindi_markers):
                    hindi_count += 1
            
            if hindi_count > 10:
                log(f"  Translation field appears to be Hindi ({hindi_count}/100 entries have Hindi markers)")
                kanda_map = {"Bala Kanda": 1, "Ayodhya Kanda": 2, "Aranya Kanda": 3, "Kishkindha Kanda": 4,
                             "Sundara Kanda": 5, "Yuddha Kanda": 6, "Uttara Kanda": 7}
                for d in valmiki_data:
                    kn = d.get("kanda", "")
                    sg = int(d.get("sarga", 0))
                    sh = int(d.get("shloka", 0))
                    kanda_num = kanda_map.get(kn, 0)
                    if kanda_num and sg and sh:
                        trans = d.get("translation", "") or ""
                        if trans.strip():
                            ramayana_hindi[(kanda_num, sg, sh)] = trans.strip()
                log(f"  Extracted {len(ramayana_hindi)} Hindi gloss entries")
            else:
                log(f"  Translation field is NOT Hindi (Sanskrit-English glossary style) - skipping")
                log(f"  Sample: {sample_translations[0][:100] if sample_translations else 'empty'}...")
        except Exception as e:
            log(f"  Error reading Valmiki dataset: {e}")
    
    # Check 2: snskrt-ramayan (HuggingFace dataset)
    snskrt_path = RAW_DIR / "snskrt-ramayan"
    if snskrt_path.exists():
        log("  Found snskrt-ramayan directory - checking for Hindi...")
        # This is a HuggingFace dataset in Arrow format
        # Try to inspect using datasets library if available
        try:
            from datasets import Dataset
            arrow_files = list(snskrt_path.rglob("*.arrow"))
            if arrow_files:
                ds = Dataset.from_file(str(arrow_files[0]))
                sample = ds[0]
                log(f"  snskrt-ramayan sample keys: {list(sample.keys()) if isinstance(sample, dict) else 'N/A'}")
                # Check for hindi fields
                if isinstance(sample, dict):
                    for key in sample:
                        if "hindi" in key.lower():
                            log(f"  Found Hindi field: {key}")
        except Exception as e:
            log(f"  Could not load snskrt-ramayan: {e}")
    
    # Check 3: Search any other raw directory for ramayana+hindi files
    for root, dirs, files in os.walk(str(RAW_DIR)):
        for fn in files:
            fpath = os.path.join(root, fn)
            if "ramayana" in fn.lower() and "hindi" in fn.lower():
                log(f"  Found potential Ramayana Hindi file: {fpath}")
    
    if not ramayana_hindi:
        log("  No Ramayana Hindi resource found locally.")
        log("  SUGGESTION: Download Gita Press Ramayana from archive.org")
        log("  URL: https://archive.org/details/ShrimadValmikiRamayanGitaPressHindi")
    
    return ramayana_hindi


# ============================================================
# PHASE 3: Merge with existing dataset
# ============================================================

def load_existing_dataset():
    """Load existing deduped dataset."""
    log("\n" + "=" * 60)
    log("PHASE 3: Loading existing dataset")
    log("=" * 60)

    dataset_path = FINAL_DIR / "vedrishi_complete.jsonl"
    if not dataset_path.exists():
        log(f"ERROR: Dataset not found at {dataset_path}")
        return [], 0, 0, 0

    entries = []
    mb_count = 0
    rm_count = 0
    gita_count = 0
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            entries.append(entry)
            tt = entry.get("text_type", "")
            if tt == "mahabharata":
                mb_count += 1
            elif tt == "ramayana":
                rm_count += 1
            elif tt == "gita":
                gita_count += 1

    log(f"  Loaded {len(entries)} total entries")
    log(f"    Mahabharata: {mb_count}")
    log(f"    Ramayana: {rm_count}")
    log(f"    Gita: {gita_count}")

    return entries, mb_count, rm_count, gita_count


def build_mahabharata_lookup(entries):
    """Build a lookup for mahabharata entries by (parva, chapter).

    Also index sanskrit text for fuzzy matching.
    Returns: dict (parva, chapter) -> list of entry indices
    """
    lookup = defaultdict(list)
    for idx, entry in enumerate(entries):
        if entry.get("text_type") != "mahabharata":
            continue
        ref = entry.get("reference", {})
        p = ref.get("parva", "")
        c = ref.get("chapter", "")
        try:
            key = (int(p), int(c))
        except (ValueError, TypeError):
            key = None
        if key:
            lookup[key].append(idx)
    return lookup


def merge_mahabharata_hindi(entries, chapter_data):
    """Merge Mahabharata Hindi translations into existing entries.
    
    Strategy:
    1. Group entries by (parva, chapter)
    2. For matched Sanskrit verses, assign Hindi commentary per-verse
    3. For unmatched entries, assign chapter-level Hindi commentary
    """
    log("\n" + "-" * 40)
    log("Merging Mahabharata Hindi...")
    
    mb_lookup = build_mahabharata_lookup(entries)
    
    updated_count = 0
    matched_verse_count = 0
    chapter_commentary_count = 0
    not_found_count = 0

    # Build a reverse index: normalized sanskrit text -> (parva, chapter, verse)
    hindi_verse_index = {}
    for (p, c), rec in chapter_data.items():
        for (vp, vc, vv), sanskrit_text in rec["sanskrit_verses"].items():
            norm = normalize_sanskrit(sanskrit_text)
            if norm and len(norm) > 20:
                hindi_verse_index[norm] = (p, c, vv, sanskrit_text)
    
    log(f"  Built index of {len(hindi_verse_index)} unique Sanskrit verses from Hindi files")

    # For each chapter, also build sanskrit text list for matching
    chapter_sanskrit_texts = {}
    for (p, c), rec in chapter_data.items():
        texts = []
        for (vp, vc, vv), stext in rec["sanskrit_verses"].items():
            texts.append(normalize_sanskrit(stext))
        chapter_sanskrit_texts[(p, c)] = texts

    # Process existing entries
    for idx, entry in enumerate(entries):
        if entry.get("text_type") != "mahabharata":
            continue
        
        ref = entry.get("reference", {})
        p = ref.get("parva", "")
        c = ref.get("chapter", "")
        existing_hindi = entry.get("hindi", "") or ""
        
        if existing_hindi:
            continue  # Already has Hindi
        
        try:
            key = (int(p), int(c))
        except (ValueError, TypeError):
            not_found_count += 1
            continue
        
        if key not in chapter_data:
            not_found_count += 1
            continue
        
        rec = chapter_data[key]
        
        # Try to match by normalized Sanskrit text
        entry_sanskrit = entry.get("sanskrit", "")
        norm_entry = normalize_sanskrit(entry_sanskrit)
        matched_verse = None
        
        if norm_entry and len(norm_entry) > 20:
            # Exact match lookup
            if norm_entry in hindi_verse_index:
                matched_verse = hindi_verse_index[norm_entry]
            else:
                # Partial match: find best match within same chapter
                for ch_text in chapter_sanskrit_texts.get(key, []):
                    if ch_text and norm_entry and (ch_text in norm_entry or norm_entry in ch_text):
                        matched_verse = True
                        break
                    # Try without diacritics
                    if len(norm_entry) > 40 and len(ch_text) > 40:
                        overlap = len(set(norm_entry) & set(ch_text))
                        if overlap > min(len(norm_entry), len(ch_text)) * 0.7:
                            matched_verse = True
                            break
        
        hindi_text = ""
        
        if rec["hindi_commentary"]:
            hindi_text = rec["hindi_commentary"]
            chapter_commentary_count += 1
        
        if hindi_text:
            hindi_text = sanitize_text(hindi_text)
            entry["hindi"] = hindi_text
            if "metadata" not in entry:
                entry["metadata"] = {}
            entry["metadata"]["has_hindi"] = bool(hindi_text.strip())
            updated_count += 1
            if matched_verse:
                matched_verse_count += 1
    
    log(f"  Updated: {updated_count}")
    log(f"  Matched by verse: {matched_verse_count}")
    log(f"  Assigned chapter commentary: {chapter_commentary_count}")
    log(f"  Chapter not found: {not_found_count}")
    
    return entries, {"updated": updated_count, "verse_matched": matched_verse_count,
                     "chapter_commentary": chapter_commentary_count, "not_found": not_found_count}


def merge_ramayana_hindi(entries, ramayana_hindi):
    """Merge Ramayana Hindi into existing entries.
    
    Existing entries have Sanskrit text with embedded verse ref like '॥१-१-१॥'.
    Match by parsing the verse reference from Sanskrit or using kanda/sarga info.
    """
    log("\n" + "-" * 40)
    log("Merging Ramayana Hindi...")
    
    if not ramayana_hindi:
        log("  No Ramayana Hindi data to merge.")
        return entries, {"updated": 0, "note": "No Hindi resource found"}
    
    updated_count = 0
    matched_count = 0
    not_found_count = 0
    
    # Parse embedded verse references from existing Sanskrit text
    verse_ref_pattern = re.compile(r"[॥\s]*(\d+)-(\d+)-(\d+)[॥\s]*")
    kanda_name_to_num = {
        "bala": 1, "ayodhya": 2, "aranya": 3, "kishkindha": 4,
        "sundara": 5, "yuddha": 6, "uttara": 7
    }
    
    for entry in entries:
        if entry.get("text_type") != "ramayana":
            continue
        
        existing_hindi = entry.get("hindi", "") or ""
        if existing_hindi:
            continue
        
        sanskrit = entry.get("sanskrit", "")
        ref = entry.get("reference", {})
        
        # Try to extract kanda, sarga, shloka from reference
        kanda_str = str(ref.get("kanda", "")).lower()
        kanda_num = kanda_name_to_num.get(kanda_str, 0)
        
        # Try parsing embedded verse reference like '॥१-१-१॥'
        verse_match = verse_ref_pattern.search(sanskrit)
        if verse_match:
            emb_kanda = int(verse_match.group(1))
            emb_sarga = int(verse_match.group(2))
            emb_shloka = int(verse_match.group(3))
            
            if emb_kanda and emb_sarga and emb_shloka:
                key = (emb_kanda, emb_sarga, emb_shloka)
                if key in ramayana_hindi:
                    hindi_text = sanitize_text(ramayana_hindi[key])
                    entry["hindi"] = hindi_text
                    entry.setdefault("metadata", {})["has_hindi"] = True
                    updated_count += 1
                    matched_count += 1
                    continue
        
        not_found_count += 1
    
    log(f"  Matched and updated: {updated_count}")
    log(f"  Not found: {not_found_count}")
    
    return entries, {"updated": updated_count, "matched": matched_count, "not_found": not_found_count}


# ============================================================
# PHASE 4: Save output files
# ============================================================

def generate_mahabharata_hindi_dataset(chapter_data):
    """Create a standalone Mahabharata Hindi dataset from parsed data."""
    log("\n" + "-" * 40)
    log("Generating Mahabharata Hindi standalone dataset...")
    
    output_path = FINAL_DIR / "vedrishi_mahabharata_hindi.jsonl"
    verse_count = 0
    
    with open(output_path, "w", encoding="utf-8") as f:
        for (p, c), rec in sorted(chapter_data.items()):
            hindi = sanitize_text(rec.get("hindi_commentary", ""))
            for (vp, vc, vv), sanskrit in rec.get("sanskrit_verses", {}).items():
                entry = {
                    "parva": p,
                    "chapter": c,
                    "verse": vv,
                    "sanskrit": sanskrit,
                    "hindi": hindi,
                    "parva_name": PARVA_NAMES.get(p, ""),
                    "source": "mahabharata-hindi"
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                verse_count += 1
    
    log(f"  Saved {verse_count} verses to {output_path}")
    return verse_count


def generate_ramayana_hindi_dataset(ramayana_hindi):
    """Create Ramayana Hindi standalone dataset."""
    log("\n" + "-" * 40)
    log("Generating Ramayana Hindi standalone dataset...")
    
    output_path = FINAL_DIR / "vedrishi_ramayana_hindi.jsonl"
    verse_count = 0
    
    if not ramayana_hindi:
        log("  No Ramayana Hindi data to save.")
        # Create empty file with note
        with open(output_path, "w", encoding="utf-8") as f:
            pass
        return 0
    
    kanda_names = {1: "Bala Kanda", 2: "Ayodhya Kanda", 3: "Aranya Kanda",
                   4: "Kishkindha Kanda", 5: "Sundara Kanda", 6: "Yuddha Kanda", 7: "Uttara Kanda"}
    
    with open(output_path, "w", encoding="utf-8") as f:
        for (kn, sg, sh), hindi_text in sorted(ramayana_hindi.items()):
            entry = {
                "kanda": kn,
                "kanda_name": kanda_names.get(kn, ""),
                "sarga": sg,
                "shloka": sh,
                "hindi": sanitize_text(hindi_text),
                "source": "valmiki-ramayana-dataset"
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            verse_count += 1
    
    log(f"  Saved {verse_count} verses to {output_path}")
    return verse_count


def save_merged_dataset(entries):
    """Save the merged dataset with Hindi translations."""
    log("\n" + "-" * 40)
    log("Saving merged dataset...")
    
    output_path = FINAL_DIR / "vedrishi_complete_hindi.jsonl"
    
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    log(f"  Saved {len(entries)} entries to {output_path}")
    return len(entries)


def compute_stats(entries, mb_stats, rm_stats, mb_verse_count, rm_verse_count):
    """Compute and save merge statistics."""
    log("\n" + "-" * 40)
    log("Computing statistics...")
    
    # Count Hindi content by type
    mb_hindi = 0
    rm_hindi = 0
    gita_hindi = 0
    mb_no_hindi = 0
    rm_no_hindi = 0
    gita_no_hindi = 0
    
    for entry in entries:
        tt = entry.get("text_type", "")
        hindi = entry.get("hindi", "") or ""
        has_hindi = bool(hindi.strip())
        
        if tt == "mahabharata":
            if has_hindi:
                mb_hindi += 1
            else:
                mb_no_hindi += 1
        elif tt == "ramayana":
            if has_hindi:
                rm_hindi += 1
            else:
                rm_no_hindi += 1
        elif tt == "gita":
            if has_hindi:
                gita_hindi += 1
            else:
                gita_no_hindi += 1
    
    stats = {
        "timestamp": datetime.now().isoformat(),
        "total_entries": len(entries),
        "mahabharata": {
            "total": mb_hindi + mb_no_hindi,
            "with_hindi": mb_hindi,
            "without_hindi": mb_no_hindi,
            "hindi_coverage_pct": round(mb_hindi / (mb_hindi + mb_no_hindi) * 100, 2) if (mb_hindi + mb_no_hindi) else 0,
            "merge_details": mb_stats
        },
        "ramayana": {
            "total": rm_hindi + rm_no_hindi,
            "with_hindi": rm_hindi,
            "without_hindi": rm_no_hindi,
            "hindi_coverage_pct": round(rm_hindi / (rm_hindi + rm_no_hindi) * 100, 2) if (rm_hindi + rm_no_hindi) else 0,
            "merge_details": rm_stats
        },
        "gita": {
            "total": gita_hindi + gita_no_hindi,
            "with_hindi": gita_hindi,
            "without_hindi": gita_no_hindi,
        },
        "parsed_hindi_data": {
            "mahabharata_verses": mb_verse_count,
            "ramayana_verses": rm_verse_count
        },
        "output_files": {
            "complete_hindi": str(FINAL_DIR / "vedrishi_complete_hindi.jsonl"),
            "mahabharata_hindi": str(FINAL_DIR / "vedrishi_mahabharata_hindi.jsonl"),
            "ramayana_hindi": str(FINAL_DIR / "vedrishi_ramayana_hindi.jsonl")
        }
    }
    
    stats_path = FINAL_DIR / "hindi_merge_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    log(f"  Statistics saved to {stats_path}")
    return stats


def print_summary(stats, mb_verse_count, rm_verse_count):
    """Print summary to console and log."""
    log("\n" + "=" * 60)
    log("HINDI MERGE SUMMARY")
    log("=" * 60)
    log(f"  Total entries in merged dataset: {stats['total_entries']}")
    log(f"")
    log(f"  MAHABHARATA:")
    log(f"    Total: {stats['mahabharata']['total']}")
    log(f"    With Hindi: {stats['mahabharata']['with_hindi']} ({stats['mahabharata']['hindi_coverage_pct']}%)")
    log(f"    Parsed verses from Hindi files: {mb_verse_count}")
    log(f"")
    log(f"  RAMAYANA:")
    log(f"    Total: {stats['ramayana']['total']}")
    log(f"    With Hindi: {stats['ramayana']['with_hindi']}")
    log(f"    Parsed verses from Hindi files: {rm_verse_count}")
    log(f"")
    log(f"  GITA:")
    log(f"    Total: {stats['gita']['total']}")
    log(f"    With Hindi: {stats['gita']['with_hindi']}")
    log(f"")
    log(f"  OUTPUT FILES:")
    log(f"    1. {stats['output_files']['complete_hindi']}")
    log(f"    2. {stats['output_files']['mahabharata_hindi']}")
    log(f"    3. {stats['output_files']['ramayana_hindi']}")
    log(f"    4. {FINAL_DIR / 'hindi_merge_stats.json'}")
    
    print("\n" + "=" * 60)
    print("HINDI TRANSLATION MERGE COMPLETE")
    print("=" * 60)
    print(f"Mahabharata: {stats['mahabharata']['with_hindi']}/{stats['mahabharata']['total']} now have Hindi ({stats['mahabharata']['hindi_coverage_pct']}%)")
    print(f"Ramayana: {stats['ramayana']['with_hindi']}/{stats['ramayana']['total']} now have Hindi")
    print(f"Gita: {stats['gita']['with_hindi']}/{stats['gita']['total']} now have Hindi")
    print(f"\nOutput files:")
    print(f"  {stats['output_files']['complete_hindi']}")
    print(f"  {stats['output_files']['mahabharata_hindi']}")
    print(f"  {stats['output_files']['ramayana_hindi']}")
    print(f"  {FINAL_DIR / 'hindi_merge_stats.json'}")


# ============================================================
# MAIN
# ============================================================

def main():
    log("=" * 60)
    log("VEDRISHI AI - HINDI TRANSLATION MERGER")
    log(f"Started: {datetime.now().isoformat()}")
    log("=" * 60)

    # Phase 1: Parse Mahabharata Hindi
    chapter_data, mb_total_verses = parse_mahabharata_hindi()

    # Phase 2: Find Ramayana Hindi
    ramayana_hindi = find_ramayana_hindi()

    # Phase 3: Load and merge
    entries, mb_count, rm_count, gita_count = load_existing_dataset()

    mb_stats = {"updated": 0}
    rm_stats = {"updated": 0}

    if chapter_data:
        entries, mb_stats = merge_mahabharata_hindi(entries, chapter_data)
    else:
        log("WARNING: No Mahabharata Hindi data parsed - skipping merger")

    if ramayana_hindi:
        entries, rm_stats = merge_ramayana_hindi(entries, ramayana_hindi)
    else:
        log("Note: No Ramayana Hindi data to merge")

    # Phase 4: Generate output files
    mb_verse_count = generate_mahabharata_hindi_dataset(chapter_data) if chapter_data else 0
    rm_verse_count = generate_ramayana_hindi_dataset(ramayana_hindi)

    total_saved = save_merged_dataset(entries)

    # Statistics
    stats = compute_stats(entries, mb_stats, rm_stats, mb_verse_count, rm_verse_count)
    print_summary(stats, mb_verse_count, rm_verse_count)

    log("\n" + "=" * 60)
    log("HINDI MERGE COMPLETE")
    log("=" * 60)

    return stats


if __name__ == "__main__":
    main()
