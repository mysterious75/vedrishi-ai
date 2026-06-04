import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('D:/hacker/vedrishi/vedrishi-ai/dataset/raw/Valmiki_Ramayan_Dataset/data/Valmiki_Ramayan_Shlokas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total = len(data)
with_trans = sum(1 for d in data if d.get('translation') and len(str(d['translation'])) > 10)
with_expl = sum(1 for d in data if d.get('explanation') and len(str(d['explanation'])) > 10)
print(f'Total: {total}')
print(f'With translation: {with_trans}')
print(f'With explanation: {with_expl}')

# Check if explanation is proper English
for d in data:
    if d.get('explanation') and len(str(d['explanation'])) > 50:
        print(f'\nExplanation sample:')
        print(f'  {str(d["explanation"])[:300]}')
        break

for d in data:
    if d.get('translation') and len(str(d['translation'])) > 50:
        print(f'\nTranslation sample:')
        print(f'  {str(d["translation"])[:300]}')
        break

# Check explanation quality - is it English?
en_count = 0
for d in data:
    if d.get('explanation') and len(str(d['explanation'])) > 50:
        t = str(d['explanation'])
        ascii_letters = sum(1 for c in t if c.isascii() and c.isalpha())
        total_letters = sum(1 for c in t if c.isalpha())
        if total_letters > 0 and ascii_letters / total_letters > 0.5:
            en_count += 1

print(f'\nExplanations that are mostly English: {en_count}/{with_expl}')
