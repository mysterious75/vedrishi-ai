import json, sys
from pathlib import Path

# 1. Check Valmiki Ramayan Dataset for English
print("=" * 60)
print("CHECKING VALMIKI RAMAYAN DATASET")
print("=" * 60)
with open('D:/hacker/vedrishi/vedrishi-ai/dataset/raw/Valmiki_Ramayan_Dataset/data/Valmiki_Ramayan_Shlokas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f'Total entries: {len(data)}')
print(f'Keys: {list(data[0].keys())}')
print(f'shloka_text: {data[0]["shloka_text"][:100]}')
print(f'translation: {data[0]["translation"][:100]}')
print(f'explanation: {data[0]["explanation"][:100]}')
with_trans = sum(1 for d in data if d.get('translation') and len(d['translation']) > 10)
print(f'With translation (English): {with_trans}')
with_expl = sum(1 for d in data if d.get('explanation') and len(d['explanation']) > 10)
print(f'With explanation: {with_expl}')

# 2. Check VedicRAG_AI for Mahabharata English
print("\n" + "=" * 60)
print("CHECKING VEDICRAG_AI MAHABHARATA")
print("=" * 60)
vrag = Path('D:/hacker/vedrishi/vedrishi-ai/dataset/raw/VedicRAG_AI')
for f in vrag.rglob('*.json'):
    if 'mahabharat' in f.name.lower() or 'mbh' in f.name.lower():
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        if isinstance(data, list):
            print(f'File: {f.name}')
            print(f'Entries: {len(data)}')
            print(f'Keys: {list(data[0].keys())}')
            for k in data[0]:
                print(f'  {k}: {str(data[0][k])[:100]}')
            break
        elif isinstance(data, dict):
            print(f'File: {f.name}')
            print(f'Keys: {list(data.keys())[:20]}')
            break

# 3. Check DharmicData Mahabharata structure
print("\n" + "=" * 60)
print("CHECKING DHARMICDATA MAHABHARATA")
print("=" * 60)
mbh_dir = Path('D:/hacker/vedrishi/vedrishi-ai/dataset/raw/DharmicData/Mahabharata')
files = sorted(mbh_dir.rglob('*.json'))[:3]
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    if isinstance(data, list):
        print(f'File: {f.name}')
        print(f'Entries: {len(data)}')
        print(f'Keys: {list(data[0].keys())}')
        for k in data[0]:
            print(f'  {k}: {str(data[0][k])[:100]}')
        break

# 4. Check itihasa data
print("\n" + "=" * 60)
print("CHECKING ITIHASA DATA")
print("=" * 60)
itihasa = Path('D:/hacker/vedrishi/vedrishi-ai/dataset/raw/itihasa')
for f in itihasa.rglob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    if isinstance(data, list) and len(data) > 0:
        print(f'File: {f.name}')
        print(f'Entries: {len(data)}')
        print(f'Keys: {list(data[0].keys())}')
        for k in data[0]:
            print(f'  {k}: {str(data[0][k])[:100]}')
        break

# 5. Check Gita Press Mahabharata Hindi files
print("\n" + "=" * 60)
print("CHECKING GITA PRESS MAHABHARATA HINDI")
print("=" * 60)
gita_press = Path('D:/hacker/vedrishi/vedrishi-ai/dataset/raw/mahabharata-hindi')
files = list(gita_press.rglob('*.utf8'))[:3]
print(f'UTF8 files: {len(list(gita_press.rglob("*.utf8")))}')
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    print(f'File: {f.name}, Lines: {len(lines)}')
    if len(lines) > 0:
        print(f'First line: {lines[0][:100]}')
    break

print("\n" + "=" * 60)
print("CHECKING oliver-hellwig-sanskrit")
print("=" * 60)
oh = Path('D:/hacker/vedrishi/vedrishi-ai/dataset/raw/oliver-hellwig-sanskrit')
for f in oh.rglob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    if isinstance(data, list) and len(data) > 0:
        print(f'File: {f.name}')
        print(f'Entries: {len(data)}')
        print(f'Keys: {list(data[0].keys())}')
        for k in data[0]:
            print(f'  {k}: {str(data[0][k])[:100]}')
        break
