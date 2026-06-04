import json, sys, random
sys.stdout.reconfigure(encoding='utf-8')

with open('D:/hacker/vedrishi/vedrishi-ai/dataset/instruction-pairs/vedrishi_instruction_pairs.jsonl', 'r', encoding='utf-8') as f:
    pairs = [json.loads(l) for l in f if l.strip()]

# Sample 1 from each text_type
for tt in ['gita', 'ramayana', 'mahabharata']:
    samples = [p for p in pairs if p.get('metadata',{}).get('text_type') == tt]
    if not samples:
        continue
    s = samples[0]
    print(f'\n=== {tt.upper()} ===')
    print(f'Instruction: {s["instruction"]}')
    print(f'Output (first 200): {s["output"][:200]}...')
    # Check if output contains Hindi/English
    has_dev = any('\u0900' <= c <= '\u097f' for c in s["output"])
    has_en = any(c.isascii() and c.isalpha() and c.islower() for c in s["output"])
    print(f'Has Devanagari: {has_dev}, Has English: {has_en}')

# Count outputs with Hindi/English
total = len(pairs)
with_hindi = sum(1 for p in pairs if any('\u0900' <= c <= '\u097f' for c in p["output"]) and len(p["output"]) > 50)
with_english = sum(1 for p in pairs if any(c.isascii() and c.isalpha() and c.islower() for c in p["output"]) and len(p["output"]) > 50)
both = sum(1 for p in pairs if any('\u0900' <= c <= '\u097f' for c in p["output"]) and any(c.isascii() and c.isalpha() and c.islower() for c in p["output"]) and len(p["output"]) > 50)

print(f'\nTotal: {total}')
print(f'With Hindi in output: {with_hindi} ({with_hindi/total*100:.1f}%)')
print(f'With English in output: {with_english} ({with_english/total*100:.1f}%)')
print(f'With both: {both} ({both/total*100:.1f}%)')
