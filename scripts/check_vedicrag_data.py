import json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/hacker/vedrishi/vedrishi-ai/dataset/raw/VedicRAG_AI/dharmaganj/ratnaranjaka/mahabharatam'

# Check mahabharatam1.json
with open(f'{BASE}/mahabharatam1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, list) and len(data) > 0:
    print(f'Total entries in mahabharatam1: {len(data)}')
    print(f'Keys: {list(data[0].keys())}')
    for k in data[0]:
        val = str(data[0][k])
        print(f'  {k}: {val[:120]}')
    
    for k in data[0]:
        cnt = sum(1 for d in data if d.get(k) and len(str(d[k])) > 20)
        if cnt > 0:
            print(f'  {k} (non-empty): {cnt}/{len(data)}')

# Check all mahabharatam files
print('\n--- All mahabharatam files ---')
total_entries = 0
for i in range(1, 9):
    try:
        with open(f'{BASE}/mahabharatam{i}.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
        if isinstance(d, list):
            total_entries += len(d)
            print(f'  mahabharatam{i}.json: {len(d)} entries')
        elif isinstance(d, dict):
            print(f'  mahabharatam{i}.json: dict with keys {list(d.keys())[:5]}')
    except Exception as e:
        print(f'  mahabharatam{i}.json: Error - {e}')

print(f'\nTotal entries across all files: {total_entries}')
