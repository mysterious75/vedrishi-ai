import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "dataset" / "final"
INPUT_FILE = DATA_DIR / "vedrishi_complete.jsonl"
DEDUPED_FILE = DATA_DIR / "vedrishi_complete_deduped.jsonl"
STATS_FILE = DATA_DIR / "final_stats.json"

def main():
    seen_ids = set()
    deduped_lines = []
    total = 0
    duplicates = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            obj = json.loads(line)
            entry_id = obj.get("id")
            if entry_id in seen_ids:
                duplicates += 1
                continue
            seen_ids.add(entry_id)
            deduped_lines.append(line)

    with open(DEDUPED_FILE, "w", encoding="utf-8") as f:
        for line in deduped_lines:
            f.write(line + "\n")

    # Replace original with deduped
    INPUT_FILE.unlink()
    DEDUPED_FILE.rename(INPUT_FILE)

    # Count stats from deduped data
    by_text_type = {}
    by_source = {}
    with_hindi = 0
    with_english = 0
    with_commentaries = 0

    for line in deduped_lines:
        obj = json.loads(line)
        text_type = obj.get("text_type", "unknown")
        by_text_type[text_type] = by_text_type.get(text_type, 0) + 1

        source = obj.get("source", "unknown")
        by_source[source] = by_source.get(source, 0) + 1

        if obj.get("hindi"):
            with_hindi += 1
        if obj.get("english"):
            with_english += 1
        if obj.get("commentaries"):
            with_commentaries += 1

    stats = {
        "total_entries": len(deduped_lines),
        "by_text_type": by_text_type,
        "by_source": by_source,
        "with_hindi": with_hindi,
        "with_english": with_english,
        "with_commentaries": with_commentaries,
    }

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"Total entries processed: {total}")
    print(f"Duplicates removed: {duplicates}")
    print(f"Final count: {len(deduped_lines)}")

if __name__ == "__main__":
    main()
