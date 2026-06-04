#!/usr/bin/env python3
"""
VEDRISHI AI - Language Merge Script
Fills in missing Hindi and English translations for the VedRishi AI dataset
using the Valmiki Ramayan Dataset and Itihasa Dataset as sources.
"""

import json
import re
import unicodedata
import sys
import time
from pathlib import Path
from collections import defaultdict
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
FINAL_DIR = BASE_DIR / "dataset" / "final"
RAW_DIR = BASE_DIR / "dataset" / "raw"

VALMIKI_PATH = RAW_DIR / "Valmiki_Ramayan_Dataset" / "data" / "Valmiki_Ramayan_Shlokas.json"
ITIHASA_DIR = RAW_DIR / "itihasa" / "data"
MAIN_DATASET_PATH = FINAL_DIR / "vedrishi_complete_hindi.jsonl"
OUTPUT_PATH = FINAL_DIR / "vedrishi_complete_hindi.jsonl"

DEVANAGARI_RE = re.compile(r'[\u0900-\u097F]+')
VERSE_REF_RE = re.compile(r'[।॥]*(\d+)[-\.](\d+)[-\.](\d+)[।॥]*')

KANDA_NAME_TO_NUM = {
    "bala kanda": 1, "bala": 1,
    "ayodhya kanda": 2, "ayodhya": 2,
    "aranya kanda": 3, "aranya": 3,
    "kishkindha kanda": 4, "kishkindha": 4,
    "sundara kanda": 5, "sundara": 5,
    "yuddha kanda": 6, "yuddha": 6,
    "uttara kanda": 7, "uttara": 7,
}


def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")
    sys.stdout.flush()


def normalize(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'[।॥][\s]*[\d\-\.]+[\s]*[।॥]', '', text)
    text = re.sub(r'[।॥][\d\-\.]+', '', text)
    text = re.sub(r'[\d\-\.]+[\s]*[।॥]', '', text)
    text = re.sub(r'\s+', '', text)
    text = text.replace('।', '').replace('॥', '').replace(',', '').replace('.', '')
    text = text.replace('"', '').replace("'", "").replace(';', '').replace(':', '')
    text = text.replace('(', '').replace(')', '').replace('!', '').replace('?', '')
    text = text.replace('ॐ', '').replace('ऽ', '').replace('॰', '')
    text = text.replace('ॊ', 'ो').replace('ॆ', 'े').replace('ॢ', 'ृ')
    text = text.replace('ँ', '')
    return text.strip()


def normalize_aggressive(text):
    t = normalize(text)
    t = t.replace('ः', '')
    t = t.replace('्', '')
    t = t.replace('ं', '')
    return t.strip()


def extract_verse_ref(text):
    if not text:
        return None
    m = VERSE_REF_RE.search(text)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def extract_devanagari_words(text):
    if not text:
        return ""
    return " ".join(DEVANAGARI_RE.findall(text))


def extract_english_from_gloss(text):
    if not text:
        return ""
    result = DEVANAGARI_RE.sub('', text)
    result = result.replace('  ', ' ').replace(', ,', ',').strip()
    result = re.sub(r'^[\s,;:.!?]+', '', result)
    result = re.sub(r'[\s,;:.!?]+$', '', result)
    result = re.sub(r'\s+', ' ', result)
    return result


def has_content(val):
    if val is None:
        return False
    return isinstance(val, str) and bool(val.strip())


# =========================================================================
# LOAD MAIN DATASET
# =========================================================================

def load_main_dataset(path):
    log(f"Loading main dataset from {path}...")
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    log(f"  Loaded {len(entries)} entries")
    return entries


# =========================================================================
# LOAD VALMIKI RAMAYAN DATASET
# =========================================================================

def load_valmiki_dataset(path):
    log(f"Loading Valmiki dataset from {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    log(f"  Loaded {len(data)} entries")

    shloka_index = {}
    shloka_aggr_index = {}
    ref_index = {}
    sarga_groups = defaultdict(list)

    for entry in data:
        kanda = entry.get("kanda", "")
        sarga = entry.get("sarga", 0)
        shloka = entry.get("shloka", 0)
        shloka_text = entry.get("shloka_text") or ""
        translation = entry.get("translation") or ""
        explanation = entry.get("explanation") or ""

        if not shloka_text:
            continue

        norm = normalize(shloka_text)
        aggr = normalize_aggressive(shloka_text)

        val = {
            "explanation": explanation,
            "translation": translation,
            "kanda": kanda,
            "sarga": sarga,
            "shloka": shloka,
            "shloka_text": shloka_text,
        }

        if norm:
            shloka_index[norm] = val
        if aggr:
            if aggr not in shloka_aggr_index:
                shloka_aggr_index[aggr] = []
            shloka_aggr_index[aggr].append(val)

        kanda_num = KANDA_NAME_TO_NUM.get(kanda.strip().lower(), 0)
        if kanda_num and sarga and shloka:
            ref_index[(kanda_num, int(sarga), int(shloka))] = val
            sarga_groups[(kanda_num, int(sarga))].append(val)

    log(f"  Devanagari index: {len(shloka_index)} keys")
    log(f"  Aggressive index: {len(shloka_aggr_index)} keys")
    log(f"  Chapter/verse index: {len(ref_index)} keys")

    with_expl = sum(1 for v in data if has_content(v.get('explanation')))
    with_trans = sum(1 for v in data if has_content(v.get('translation')))
    log(f"  With explanation: {with_expl}/{len(data)}")
    log(f"  With translation: {with_trans}/{len(data)}")

    return {
        "shloka_index": shloka_index,
        "shloka_aggr_index": shloka_aggr_index,
        "ref_index": ref_index,
        "sarga_groups": dict(sarga_groups),
        "raw_count": len(data),
    }


# =========================================================================
# LOAD ITIHASA DATASET
# =========================================================================

def load_itihasa_dataset(itihasa_dir):
    log(f"Loading Itihasa dataset from {itihasa_dir}...")

    files_to_load = [
        ("train.sn", "train.en"),
        ("dev.sn", "dev.en"),
        ("test.sn", "test.en"),
    ]

    itihasa_norm_index = {}
    itihasa_aggr_index = {}
    total_pairs = 0

    for sn_file, en_file in files_to_load:
        sn_path = itihasa_dir / sn_file
        en_path = itihasa_dir / en_file
        if not sn_path.exists() or not en_path.exists():
            log(f"  WARNING: Missing {sn_file} or {en_file}, skipping")
            continue

        with open(sn_path, 'r', encoding='utf-8') as f_sn, \
             open(en_path, 'r', encoding='utf-8') as f_en:
            sn_lines = f_sn.readlines()
            en_lines = f_en.readlines()

        count = min(len(sn_lines), len(en_lines))
        pair_count = 0
        for i in range(count):
            sn = sn_lines[i].strip()
            en = en_lines[i].strip()
            if sn and en:
                norm = normalize(sn)
                aggr = normalize_aggressive(sn)
                if norm and len(norm) > 10:
                    if norm not in itihasa_norm_index:
                        itihasa_norm_index[norm] = en
                if aggr and len(aggr) > 10:
                    if aggr not in itihasa_aggr_index:
                        itihasa_aggr_index[aggr] = en
                pair_count += 1

        total_pairs += pair_count
        log(f"  {sn_file}: {pair_count} pairs")

    log(f"  Total pairs: {total_pairs}")
    log(f"  Norm index keys: {len(itihasa_norm_index)}")
    log(f"  Aggr index keys: {len(itihasa_aggr_index)}")
    return {
        "norm_index": itihasa_norm_index,
        "aggr_index": itihasa_aggr_index,
        "total_pairs": total_pairs,
    }


# =========================================================================
# COMPUTE COVERAGE
# =========================================================================

def compute_coverage(entries):
    total = len(entries)
    sanskrit = sum(1 for e in entries if has_content(e.get('sanskrit')))
    english = sum(1 for e in entries if has_content(e.get('english')))
    hindi = sum(1 for e in entries if has_content(e.get('hindi')))
    all_three = sum(1 for e in entries if has_content(e.get('sanskrit'))
                     and has_content(e.get('english'))
                     and has_content(e.get('hindi')))

    sources = defaultdict(lambda: {"total": 0, "english": 0, "hindi": 0, "all_three": 0})
    for e in entries:
        src = e.get('text_type', 'unknown')
        s = sources[src]
        s["total"] += 1
        if has_content(e.get('english')):
            s["english"] += 1
        if has_content(e.get('hindi')):
            s["hindi"] += 1
        if has_content(e.get('sanskrit')) and has_content(e.get('english')) and has_content(e.get('hindi')):
            s["all_three"] += 1

    return {
        "total": total,
        "sanskrit": sanskrit,
        "english": english,
        "hindi": hindi,
        "all_three": all_three,
        "sources": dict(sources),
    }


def print_coverage_report(stats, label="Coverage"):
    log("")
    log("=" * 70)
    log(f"  {label}")
    log("=" * 70)
    t = stats["total"]
    if t == 0:
        log("  (empty)")
        return
    log(f"  Total:   {t}")
    log(f"  Sanskrit: {stats['sanskrit']:>6}/{t} ({stats['sanskrit']/t*100:6.1f}%)")
    log(f"  English:  {stats['english']:>6}/{t} ({stats['english']/t*100:6.1f}%)")
    log(f"  Hindi:    {stats['hindi']:>6}/{t} ({stats['hindi']/t*100:6.1f}%)")
    log(f"  All 3:    {stats['all_three']:>6}/{t} ({stats['all_three']/t*100:6.1f}%)")
    log("  ")
    for src in sorted(stats["sources"]):
        s = stats["sources"][src]
        st = s["total"]
        log(f"  {src:15s}: eng={s['english']:>5}/{st} ({s['english']/st*100:5.1f}%)  "
            f"hin={s['hindi']:>5}/{st} ({s['hindi']/st*100:5.1f}%)  "
            f"all3={s['all_three']:>5}/{st} ({s['all_three']/st*100:5.1f}%)")
    log("=" * 70)


# =========================================================================
# UPDATE ENTRIES
# =========================================================================

def update_entries(entries, valmiki_data, itihasa_data):
    log("Updating entries with missing translations...")

    shloka_index = valmiki_data["shloka_index"]
    shloka_aggr_index = valmiki_data["shloka_aggr_index"]
    ref_index = valmiki_data["ref_index"]
    itihasa_norm = itihasa_data["norm_index"]
    itihasa_aggr = itihasa_data["aggr_index"]

    english_filled = 0
    english_valmiki = 0
    english_valmiki_aggr = 0
    english_valmiki_gloss = 0
    english_itihasa = 0
    hindi_filled = 0
    hindi_valmiki_exact = 0
    hindi_valmiki_aggr = 0

    total = len(entries)
    last_pct = 0

    for idx, entry in enumerate(entries):
        pct = 100 * (idx + 1) // total
        if pct > last_pct and pct % 5 == 0:
            log(f"  Progress: {idx + 1}/{total} ({pct}%)")
            last_pct = pct

        sanskrit = entry.get("sanskrit", "")
        text_type = entry.get("text_type", "")
        english = entry.get("english") or ""
        hindi = entry.get("hindi") or ""

        has_english = bool(english.strip())
        has_hindi = bool(hindi.strip())

        if has_english and has_hindi:
            continue

        norm = normalize(sanskrit)
        aggr = normalize_aggressive(sanskrit)

        # ------ FILL ENGLISH ------
        if not has_english:
            found_eng = None
            eng_source = ""

            # Priority 1: Valmiki explanation (exact norm match)
            if text_type == "ramayana" and norm:
                val = shloka_index.get(norm)
                if val and has_content(val.get("explanation")):
                    found_eng = val["explanation"].strip()
                    eng_source = "valmiki_expl"

            # Priority 2: Valmiki explanation (aggressive norm match)
            if not found_eng and text_type == "ramayana" and aggr:
                vals = shloka_aggr_index.get(aggr, [])
                for v in vals:
                    if has_content(v.get("explanation")):
                        found_eng = v["explanation"].strip()
                        eng_source = "valmiki_expl_aggr"
                        break

            # Priority 3: Valmiki translation (English gloss) via norm
            if not found_eng and text_type == "ramayana" and norm:
                val = shloka_index.get(norm)
                if val and has_content(val.get("translation")):
                    gloss = extract_english_from_gloss(val["translation"])
                    if gloss and len(gloss) > 20:
                        found_eng = gloss
                        eng_source = "valmiki_gloss"

            # Priority 4: Valmiki translation (English gloss) via aggr
            if not found_eng and text_type == "ramayana" and aggr:
                vals = shloka_aggr_index.get(aggr, [])
                for v in vals:
                    if has_content(v.get("translation")):
                        gloss = extract_english_from_gloss(v["translation"])
                        if gloss and len(gloss) > 20:
                            found_eng = gloss
                            eng_source = "valmiki_gloss_aggr"
                            break

            # Priority 5: Valmiki explanation via verse ref
            if not found_eng and text_type == "ramayana":
                verse_ref = extract_verse_ref(sanskrit)
                if verse_ref:
                    val = ref_index.get(verse_ref)
                    if val and has_content(val.get("explanation")):
                        found_eng = val["explanation"].strip()
                        eng_source = "valmiki_ref"

            # Priority 6: Valmiki translation via verse ref
            if not found_eng and text_type == "ramayana":
                verse_ref = extract_verse_ref(sanskrit)
                if verse_ref:
                    val = ref_index.get(verse_ref)
                    if val and has_content(val.get("translation")):
                        gloss = extract_english_from_gloss(val["translation"])
                        if gloss and len(gloss) > 20:
                            found_eng = gloss
                            eng_source = "valmiki_ref_gloss"

            # Priority 7: Itihasa exact norm match
            if not found_eng and norm:
                en_text = itihasa_norm.get(norm)
                if en_text:
                    found_eng = en_text.strip()
                    eng_source = "itihasa"

            # Priority 8: Itihasa aggressive norm match
            if not found_eng and aggr:
                en_text = itihasa_aggr.get(aggr)
                if en_text:
                    found_eng = en_text.strip()
                    eng_source = "itihasa_aggr"

            if found_eng:
                entry["english"] = found_eng
                english_filled += 1
                has_english = True
                if "valmiki_expl" in eng_source:
                    english_valmiki += 1
                elif "valmiki_aggr" in eng_source:
                    english_valmiki_aggr += 1
                elif "gloss" in eng_source:
                    english_valmiki_gloss += 1
                elif "itihasa" in eng_source:
                    english_itihasa += 1

        # ------ FILL HINDI ------
        if not has_hindi and text_type == "ramayana":
            found_hi = None
            hi_source = ""

            # Priority 1: Devanagari words from translation (norm)
            if norm:
                val = shloka_index.get(norm)
                if val and has_content(val.get("translation")):
                    hi = extract_devanagari_words(val["translation"])
                    if hi and len(hi) > 20:
                        found_hi = hi
                        hi_source = "valmiki_exact"

            # Priority 2: Devanagari words from translation (aggressive)
            if not found_hi and aggr:
                vals = shloka_aggr_index.get(aggr, [])
                for v in vals:
                    if has_content(v.get("translation")):
                        hi = extract_devanagari_words(v["translation"])
                        if hi and len(hi) > 20:
                            found_hi = hi
                            hi_source = "valmiki_aggr"
                            break

            # Priority 3: Devanagari words from translation (verse ref)
            if not found_hi:
                verse_ref = extract_verse_ref(sanskrit)
                if verse_ref:
                    val = ref_index.get(verse_ref)
                    if val and has_content(val.get("translation")):
                        hi = extract_devanagari_words(val["translation"])
                        if hi and len(hi) > 20:
                            found_hi = hi
                            hi_source = "valmiki_ref"

            # Priority 4: Valmiki explanation as Hindi fallback
            if not found_hi and norm:
                val = shloka_index.get(norm)
                if val and has_content(val.get("explanation")):
                    found_hi = val["explanation"].strip()
                    hi_source = "valmiki_expl_fallback"
            if not found_hi and aggr:
                vals = shloka_aggr_index.get(aggr, [])
                for v in vals:
                    if has_content(v.get("explanation")):
                        found_hi = v["explanation"].strip()
                        hi_source = "valmiki_expl_fallback_aggr"
                        break
            if not found_hi:
                verse_ref = extract_verse_ref(sanskrit)
                if verse_ref:
                    val = ref_index.get(verse_ref)
                    if val and has_content(val.get("explanation")):
                        found_hi = val["explanation"].strip()
                        hi_source = "valmiki_expl_ref"

            if found_hi:
                entry["hindi"] = found_hi
                hindi_filled += 1
                has_hindi = True
                if "exact" in hi_source:
                    hindi_valmiki_exact += 1
                elif "aggr" in hi_source:
                    hindi_valmiki_aggr += 1

        if "metadata" in entry:
            entry["metadata"]["has_english"] = has_english
            entry["metadata"]["has_hindi"] = has_hindi

    log(f"  English filled: {english_filled} "
        f"(Valmiki expl: {english_valmiki}, Valmiki expl aggr: {english_valmiki_aggr}, "
        f"Valmiki gloss: {english_valmiki_gloss}, Itihasa: {english_itihasa})")
    log(f"  Hindi filled:   {hindi_filled} "
        f"(Valmiki exact: {hindi_valmiki_exact}, Valmiki aggr: {hindi_valmiki_aggr})")
    return entries, {
        "english_filled": english_filled,
        "english_valmiki": english_valmiki,
        "english_valmiki_aggr": english_valmiki_aggr,
        "english_valmiki_gloss": english_valmiki_gloss,
        "english_itihasa": english_itihasa,
        "hindi_filled": hindi_filled,
        "hindi_valmiki_exact": hindi_valmiki_exact,
        "hindi_valmiki_aggr": hindi_valmiki_aggr,
    }


# =========================================================================
# SAVE DATASET
# =========================================================================

def save_dataset(entries, path):
    log(f"Saving updated dataset to {path}...")
    with open(path, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    log(f"  Saved {len(entries)} entries")


# =========================================================================
# MAIN
# =========================================================================

def main():
    log("=" * 70)
    log("VEDRISHI AI - LANGUAGE MERGE SCRIPT")
    log("=" * 70)

    start_time = time.time()

    log("\n[Step 1] Loading main dataset...")
    entries = load_main_dataset(MAIN_DATASET_PATH)

    before = compute_coverage(entries)
    print_coverage_report(before, "Coverage BEFORE merge")

    log("\n[Step 2] Loading Valmiki Ramayan Dataset...")
    valmiki_data = load_valmiki_dataset(VALMIKI_PATH)

    log("\n[Step 3] Loading Itihasa Dataset...")
    itihasa_data = load_itihasa_dataset(ITIHASA_DIR)

    log("\n[Step 4] Merging translations...")
    entries, update_stats = update_entries(entries, valmiki_data, itihasa_data)

    log("\n[Step 5] Saving updated dataset...")
    save_dataset(entries, OUTPUT_PATH)

    after = compute_coverage(entries)
    print_coverage_report(after, "Coverage AFTER merge")

    elapsed = time.time() - start_time
    log("")
    log("=" * 70)
    log("  MERGE SUMMARY")
    log("=" * 70)
    log(f"  Entries: {len(entries)}")
    log(f"  English added: {update_stats['english_filled']}")
    log(f"    Valmiki explanation:       {update_stats['english_valmiki']}")
    log(f"    Valmiki explanation aggr:  {update_stats['english_valmiki_aggr']}")
    log(f"    Valmiki gloss:             {update_stats['english_valmiki_gloss']}")
    log(f"    Itihasa:                   {update_stats['english_itihasa']}")
    log(f"  Hindi added:   {update_stats['hindi_filled']}")
    log(f"    Valmiki exact:             {update_stats['hindi_valmiki_exact']}")
    log(f"    Valmiki aggr:              {update_stats['hindi_valmiki_aggr']}")
    log(f"  Time: {elapsed:.1f}s")
    log("")
    bc, ac = before, after
    log(f"  English: {bc['english']:>6} -> {ac['english']:>6}  "
        f"({bc['english']/bc['total']*100:5.1f}% -> {ac['english']/ac['total']*100:5.1f}%)")
    log(f"  Hindi:   {bc['hindi']:>6} -> {ac['hindi']:>6}  "
        f"({bc['hindi']/bc['total']*100:5.1f}% -> {ac['hindi']/ac['total']*100:5.1f}%)")
    log(f"  All 3:   {bc['all_three']:>6} -> {ac['all_three']:>6}  "
        f"({bc['all_three']/bc['total']*100:5.1f}% -> {ac['all_three']/ac['total']*100:5.1f}%)")
    log("=" * 70)

    return entries, update_stats, before, after


if __name__ == "__main__":
    main()
