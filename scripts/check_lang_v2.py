import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

RAW = Path('D:/hacker/vedrishi/vedrishi-ai/dataset/raw')

# ============================================================
# 1. VALMIKI RAMAYAN DATASET - English check
# ============================================================
print("=" * 70)
print("1. VALMIKI RAMAYAN DATASET - has English?")
print("=" * 70)
with open(str(RAW / 'Valmiki_Ramayan_Dataset/data/Valmiki_Ramayan_Shlokas.json'), 'r', encoding='utf-8') as f:
    vrd = json.load(f)
print(f"Total entries: {len(vrd)}")
keys = list(vrd[0].keys())
print(f"Keys: {keys}")
with_en = sum(1 for d in vrd if d.get('translation') and len(str(d['translation'])) > 10)
print(f"With 'translation' (likely English): {with_en}")
if with_en > 0:
    s = [d for d in vrd if d.get('translation') and len(str(d['translation'])) > 10][0]
    print(f"Sample translation: {s['translation'][:200]}")

# ============================================================
# 2. ITIHASA - may have English Mahabharata
# ============================================================
print("\n" + "=" * 70)
print("2. ITIHASA DATASET")
print("=" * 70)
itihasa = RAW / 'itihasa'
for f in itihasa.rglob('*.json'):
    try:
        with open(str(f), 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        if isinstance(data, list) and len(data) > 0:
            print(f"File: {f.name}")
            print(f"Entries: {len(data)}")
            print(f"Keys: {list(data[0].keys())}")
            # Check for English
            for k in data[0]:
                v = str(data[0][k])[:100]
                if any(c.isascii() and c.isalpha() for c in v) and not all(ord(c) < 128 and c.isascii() for c in v if c.isalpha()):
                    print(f"  {k}: [mixed/potentially English] {v[:100]}")
            break
    except:
        continue

# ============================================================
# 3. VEDICRAG_AI MAHABHARATA
# ============================================================
print("\n" + "=" * 70)
print("3. VEDICRAG_AI MAHABHARATA")
print("=" * 70)
vrag = RAW / 'VedicRAG_AI'
for f in sorted(vrag.rglob('*.json')):
    if 'mahabharat' not in f.name.lower() and 'mbh' not in f.name.lower():
        continue
    try:
        with open(str(f), 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        if isinstance(data, list) and len(data) > 0:
            print(f"File: {f.name}")
            print(f"Entries: {len(data)}")
            print(f"Keys: {list(data[0].keys())}")
            for k in data[0]:
                print(f"  {k}: {str(data[0][k])[:120]}")
        break
    except Exception as e:
        print(f"  Error: {e}")
        continue

# ============================================================
# 4. DHARMICDATA MAHABHARATA
# ============================================================
print("\n" + "=" * 70)
print("4. DHARMICDATA MAHABHARATA")
print("=" * 70)
for f in sorted((RAW / 'DharmicData/Mahabharata').rglob('*.json'))[:1]:
    with open(str(f), 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    if isinstance(data, list) and len(data) > 0:
        print(f"File: {f.name}")
        print(f"Entries: {len(data)}")
        print(f"Keys: {list(data[0].keys())}")
        for k in data[0]:
            print(f"  {k}: {str(data[0][k])[:120]}")

# ============================================================
# 5. GITA PRESS HINDI MAHABHARATA
# ============================================================
print("\n" + "=" * 70)
print("5. GITA PRESS HINDI MAHABHARATA (mahabharata-hindi)")
print("=" * 70)
gp = RAW / 'mahabharata-hindi'
utf8s = sorted(gp.rglob('*.utf8'))
print(f"UTF8 files: {len(utf8s)}")
total_lines = 0
for f in utf8s:
    with open(str(f), 'r', encoding='utf-8') as fh:
        lines = [l.strip() for l in fh if l.strip()]
        total_lines += len(lines)
print(f"Total non-empty lines across all files: {total_lines}")

# ============================================================
# 6. SUMMARY OF CURRENT DATASET COVERAGE
# ============================================================
print("\n" + "=" * 70)
print("6. CURRENT COVERAGE SUMMARY")
print("=" * 70)

file = RAW.parent / 'final/vedrishi_complete_hindi.jsonl'
if not file.exists():
    file = RAW.parent / 'final/vedrishi_complete.jsonl'

with open(str(file), 'r', encoding='utf-8') as f:
    verses = [json.loads(line) for line in f if line.strip()]

total = len(verses)
with_sans = sum(1 for v in verses if v.get('sanskrit') and len(str(v.get('sanskrit', ''))) > 10)
with_eng = sum(1 for v in verses if v.get('english') and len(str(v.get('english', ''))) > 10)
with_hin = sum(1 for v in verses if v.get('hindi') and len(str(v.get('hindi', ''))) > 10)
all3 = sum(1 for v in verses if (v.get('sanskrit') and len(str(v.get('sanskrit','')))>10) and (v.get('english') and len(str(v.get('english','')))>10) and (v.get('hindi') and len(str(v.get('hindi','')))>10))

print(f"Total: {total}")
print(f"Sanskrit: {with_sans} ({100*with_sans/total:.1f}%)")
print(f"English:  {with_eng} ({100*with_eng/total:.1f}%)")
print(f"Hindi:    {with_hin} ({100*with_hin/total:.1f}%)")
print(f"All 3:    {all3} ({100*all3/total:.1f}%)")

for tt in ['gita', 'ramayana', 'mahabharata']:
    sub = [v for v in verses if v.get('text_type') == tt]
    if not sub:
        continue
    n = len(sub)
    ws = sum(1 for v in sub if v.get('sanskrit') and len(str(v.get('sanskrit','')))>10)
    we = sum(1 for v in sub if v.get('english') and len(str(v.get('english','')))>10)
    wh = sum(1 for v in sub if v.get('hindi') and len(str(v.get('hindi','')))>10)
    wa = sum(1 for v in sub if ws and we and wh and 
             len(str(v.get('sanskrit','')))>10 and 
             len(str(v.get('english','')))>10 and 
             len(str(v.get('hindi','')))>10)
    print(f"\n  {tt.upper()} ({n}):")
    print(f"    S: {ws} ({100*ws/n:.1f}%)  E: {we} ({100*we/n:.1f}%)  H: {wh} ({100*wh/n:.1f}%)  All3: {wa}")
