import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('D:/hacker/vedrishi/vedrishi-ai/dataset/final/vedrishi_complete_hindi.jsonl', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

total = len(lines)
has_sk = sum(1 for l in lines if json.loads(l).get('sanskrit',''))
has_en = sum(1 for l in lines if json.loads(l).get('english',''))
has_hi = sum(1 for l in lines if json.loads(l).get('hindi',''))
all3 = sum(1 for l in lines if all(json.loads(l).get(k,'') for k in ['sanskrit','english','hindi']))

print(f'Total: {total}')
print(f'Sanskrit: {has_sk}/{total} ({has_sk/total*100:.1f}%)')
print(f'English:  {has_en}/{total} ({has_en/total*100:.1f}%)')
print(f'Hindi:    {has_hi}/{total} ({has_hi/total*100:.1f}%)')
print(f'All 3:    {all3}/{total} ({all3/total*100:.1f}%)')

src_stats = {}
for line in lines:
    d = json.loads(line)
    tt = d.get('text_type', 'unknown')
    if tt not in src_stats:
        src_stats[tt] = {'total':0,'en':0,'hi':0,'all3':0}
    s = src_stats[tt]
    s['total'] += 1
    if d.get('english','').strip(): s['en'] += 1
    if d.get('hindi','').strip(): s['hi'] += 1
    if all(d.get(k,'').strip() for k in ['sanskrit','english','hindi']): s['all3'] += 1

for tt in sorted(src_stats):
    s = src_stats[tt]
    pct_en = s['en']/s['total']*100
    pct_hi = s['hi']/s['total']*100
    pct_all = s['all3']/s['total']*100
    print(f"\n{tt}: total={s['total']}")
    print(f"  English: {s['en']}/{s['total']} ({pct_en:.1f}%)")
    print(f"  Hindi:   {s['hi']}/{s['total']} ({pct_hi:.1f}%)")
    print(f"  All 3:   {s['all3']}/{s['total']} ({pct_all:.1f}%)")
