import json, sys, random
sys.stdout.reconfigure(encoding='utf-8')
from collections import Counter

random.seed(42)

with open('D:/hacker/vedrishi/vedrishi-ai/dataset/instruction-pairs/vedrishi_instruction_pairs.jsonl', 'r', encoding='utf-8') as f:
    pairs = [json.loads(l) for l in f if l.strip()]

print(f'Total pairs: {len(pairs)}')

d = pairs[0]
print(f'Keys: {list(d.keys())}')
print(f'Instruction: {d["instruction"][:80]}...')
print(f'Output: {d["output"][:120]}...')

tt = Counter(p.get('metadata',{}).get('text_type','?') for p in pairs)
print(f'By text_type: {dict(tt)}')

random.shuffle(pairs)
split = int(len(pairs) * 0.9)
train = pairs[:split]
val = pairs[split:]

print(f'Train: {len(train)}, Val: {len(val)}')

out_dir = 'D:/hacker/vedrishi/vedrishi-ai/training/outputs/'
with open(out_dir + 'vedrishi_train.jsonl', 'w', encoding='utf-8') as f:
    for p in train:
        f.write(json.dumps(p, ensure_ascii=False) + '\n')

with open(out_dir + 'vedrishi_val.jsonl', 'w', encoding='utf-8') as f:
    for p in val:
        f.write(json.dumps(p, ensure_ascii=False) + '\n')

print('Saved train/val splits')
