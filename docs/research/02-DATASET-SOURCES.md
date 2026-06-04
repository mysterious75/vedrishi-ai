# RESEARCH: DATASET SOURCES FOR VEDRISHI AI

## PRIMARY SOURCES (FREE)

### 1. Bhagavad Gita
- **Source**: github.com/gita/BhagavadGita
- **Format**: REST API + JSON
- **Content**: 700 verses, 18 chapters
- **Languages**: Sanskrit, Hindi, English
- **Download**: Direct API calls
- **Use**: Core training data

### 2. Upanishads (108)
- **Source**: GitHub search "Upanishads JSON"
- **Alternative**: Archive.org (public domain texts)
- **Format**: Need to extract from PDFs
- **Use**: Philosophical depth

### 3. Valmiki Ramayana
- **Source**: techie-jai/VedicRAG_AI
- **Format**: Structured JSON
- **Content**: 24,000+ verses
- **Use**: Story-based training

### 4. Vidur Niti
- **Source**: GitHub search "Vidur Niti dataset"
- **Format**: Need manual extraction
- **Use**: Practical wisdom

### 5. Chanakya Niti
- **Source**: GitHub search "Chanakya Niti"
- **Format**: Available in some repos
- **Use**: Strategic thinking

## SECONDARY SOURCES

### 6. Yoga Sutras of Patanjali
- **Source**: atmabodha/Vedanta_Datasets
- **Format**: Structured data
- **Use**: Meditation guidance

### 7. Dhammapada (Buddhist, for comparison)
- **Source**: GitHub public datasets
- **Format**: JSON
- **Use**: Cross-tradition understanding

## DATA COLLECTION PROCESS

### Step 1: Download Raw Data
```bash
# Bhagavad Gita
curl -o gita.json "https://api.github.com/repos/gita/BhagavadGita/contents/gita"

# Other sources - manual download from GitHub
```

### Step 2: Convert to JSONL
```python
# Template for each verse
{
  "id": "gita_ch2_verse47",
  "source": "Bhagavad Gita, Chapter 2, Verse 47",
  "language": "hindi",
  "verse_sanskrit": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन...",
  "verse_transliteration": "karmaṇy-evādhikāras te mā phaleṣu kadācana...",
  "verse_hindi": "तेरा कर्म करने में ही अधिकार है, फल में कभी नहीं...",
  "verse_english": "You have a right to perform your duties, but never to the fruits...",
  "commentary": "Focus on action, detach from outcome...",
  "theme": ["karma_yoga", "detachment", "duty"],
  "difficulty": "beginner"
}
```

### Step 3: Generate Instruction Pairs
```
Prompt to AI:
"For this Gita verse, generate 5 realistic user questions in Hindi 
and Guru-style responses that are compassionate, non-dogmatic, and practical."
```

### Step 4: Filter Content
- Remove caste hierarchy glorification
- Remove gender-based restrictions
- Remove miracle-cure claims
- Remove political manipulation

## DATA QUALITY CHECKLIST
- [ ] Sanskrit verse accurate
- [ ] Hindi translation correct
- [ ] English translation faithful
- [ ] Theme tags relevant
- [ ] No toxic content
- [ ] No fake verses
- [ ] Commercial use license OK

## ESTIMATED DATA SIZES
| Source | Verses | Estimated Pairs |
|--------|--------|-----------------|
| Bhagavad Gita | 700 | 3,500 |
| Upanishads | 108 | 540 |
| Ramayana | 24,000 | 5,000 |
| Vidur Niti | 500 | 2,500 |
| Chanakya Niti | 400 | 2,000 |
| Yoga Sutras | 196 | 980 |
| **TOTAL** | **~26,000** | **~14,500** |
