import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Check Valmiki Ramayan for translation and explanation quality
with open('D:/hacker/vedrishi/vedrishi-ai/dataset/raw/Valmiki_Ramayan_Dataset/data/Valmiki_Ramayan_Shlokas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total = len(data)
print(f'Total entries: {total}')

# Check translation quality
with_trans = sum(1 for d in data if d.get('translation') and len(str(d['translation'])) > 10)
with_expl = sum(1 for d in data if d.get('explanation') and len(str(d['explanation'])) > 10)
with_both = sum(1 for d in data if d.get('translation') and len(str(d['translation'])) > 10 
                and d.get('explanation') and len(str(d['explanation'])) > 10)

print(f'With translation: {with_trans}')
print(f'With explanation: {with_expl}')
print(f'With both: {with_both}')

# Sample entries
print('\n--- Sample translations (first 3) ---')
count = 0
for d in data:
    if d.get('translation') and len(str(d['translation'])) > 10:
        print(f"\nEntry {d['kanda']} {d['sarga']}.{d['shloka']}:")
        print(f"  translation: {str(d['translation'])[:200]}")
        if d.get('explanation') and len(str(d['explanation'])) > 10:
            print(f"  explanation: {str(d['explanation'])[:200]}")
        count += 1
        if count >= 3:
            break

# Check if translation is actually English or mixed
print('\n--- Checking if translation is proper English ---')
en_count = 0
non_en_count = 0
for d in data:
    if d.get('translation') and len(str(d['translation'])) > 10:
        t = str(d['translation'])
        # If it has mostly ASCII letters (English), count it
        ascii_letters = sum(1 for c in t if c.isascii() and c.isalpha())
        total_letters = sum(1 for c in t if c.isalpha())
        if total_letters > 0 and ascii_letters / total_letters > 0.5:
            en_count += 1
        else:
            non_en_count += 1

print(f'Translation is mostly English: {en_count}')
print(f'Translation is mostly non-English: {non_en_count}')
