# COMPLETE DATASET CATALOG - VEDRISHI AI
> All research compiled from 7 sub-agents

---

## TIER 1: MUST DOWNLOAD (Free, Commercial OK)

### 1. AI4Bharat Sangraha (251B tokens)
- **URL**: https://huggingface.co/datasets/ai4bharat/sangraha
- **License**: CC-BY-4.0 (commercial OK)
- **Format**: Parquet (JSONL)
- **Content**: Hindi (34.5B tokens) + Sanskrit (14.9B tokens)
- **Download**:
```python
from datasets import load_dataset
dataset = load_dataset("ai4bharat/sangraha", data_dir="verified/hin")
dataset = load_dataset("ai4bharat/sangraha", data_dir="verified/san")
```

### 2. AI4Bharat IndicAlign-Instruct (74.7M pairs)
- **URL**: https://huggingface.co/datasets/ai4bharat/indic-align
- **License**: CC-BY-4.0 (commercial OK)
- **Format**: Parquet
- **Content**: 74.7M prompt-response pairs
- **Download**:
```python
from datasets import load_dataset
dataset = load_dataset("ai4bharat/indic-align")
```

### 3. Bhagavad Gita (700 verses - BEST)
- **URL**: https://github.com/deepakrakshit/bhagavad-gita-dataset
- **License**: MIT
- **Format**: JSON (chapter_01.json to chapter_18.json)
- **Content**: Sanskrit + Hindi + English
- **Download**:
```bash
git clone https://github.com/deepakrakshit/bhagavad-gita-dataset.git
```

### 4. Bhagavad Gita API (v2 - No Auth)
- **URL**: https://api.bhagavadgita.io/v2
- **Docs**: https://api.bhagavadgita.io/docs
- **License**: GPL-3.0
- **Content**: 700 verses, 21 author translations
- **Endpoints**:
```
GET /v2/chapters/
GET /v2/chapters/{chapter_number}/verses/
GET /v2/chapters/{chapter_number}/verses/{verse_number}/
```

### 5. DharmicData (140K+ verses - BEST ALL-IN-ONE)
- **URL**: https://github.com/bhavykhatri/DharmicData
- **License**: ODbL-1.0 (commercial OK)
- **Format**: JSON
- **Content**:
  - Bhagavad Gita: ~700 verses
  - Ramcharitmanas: ~10,000 chaupais
  - Mahabharata: ~100,000 verses
  - Valmiki Ramayana: ~24,000 verses
  - Rigveda: 10,000+ hymns
  - Yajurveda: ~3,880 verses
  - Atharvaveda: ~6,000 verses
- **Download**:
```bash
git clone https://github.com/bhavykhatri/DharmicData.git
```

### 6. Vedavani Dataset (Vedic Audio)
- **URL**: https://huggingface.co/datasets/sanganaka/Vedavani-Dataset
- **License**: Apache-2.0
- **Format**: CSV + WAV (6.81 GB)
- **Content**: 30,779 Vedic verses with audio
- **Download**:
```bash
git clone https://huggingface.co/datasets/sanganaka/Vedavani-Dataset
```

### 7. DharmaBench (Evaluation)
- **URL**: https://huggingface.co/datasets/Intellexus/DharmaBench
- **License**: CC-BY-4.0
- **Format**: JSON
- **Content**: 13 Sanskrit/Tibetan tasks
- **Download**:
```python
from datasets import load_dataset
ds = load_dataset("Intellexus/DharmaBench")
```

---

## TIER 2: SHOULD DOWNLOAD (Supplementary)

### 8. VedicRAG_AI (85,895+ verses)
- **URL**: https://github.com/techie-jai/VedicRAG_AI
- **License**: MIT (README says, no LICENSE file)
- **Format**: TXT + XML + JSON
- **Content**: Ramayana (17K), Mahabharata (68K), Upanishads, Vedas
- **Download**:
```bash
git clone https://github.com/techie-jai/VedicRAG_AI.git
```

### 9. Vedanta_Datasets (Gita + Upanishads + Yoga Sutras)
- **URL**: https://github.com/atmabodha/Vedanta_Datasets
- **License**: None specified
- **Format**: CSV
- **Content**: Gita, Upanishads, Yoga Sutras
- **Download**:
```bash
git clone https://github.com/atmabodha/Vedanta_Datasets.git
```

### 10. Itihasa Corpus (93K shlokas)
- **URL**: https://github.com/rahular/itihasa
- **License**: Not specified
- **Format**: JSON/CSV
- **Content**: Ramayana + Mahabharata translations
- **Download**:
```bash
git clone https://github.com/rahular/itihasa.git
```

### 11. Valmiki Ramayana Dataset
- **URL**: https://github.com/Ashutosh-Vijay/Valmiki_Ramayan_Dataset
- **License**: MIT
- **Format**: Not specified
- **Content**: 24K verses
- **Download**:
```bash
git clone https://github.com/Ashutosh-Vijay/Valmiki_Ramayan_Dataset.git
```

### 12. Chanakya Niti
- **URL**: https://huggingface.co/datasets/Umang-Bansal/Chanakya-niti
- **License**: Apache-2.0
- **Format**: JSON (429 rows)
- **Download**:
```python
from datasets import load_dataset
ds = load_dataset("Umang-Bansal/Chanakya-niti")
```

### 13. 108 Upanishads
- **URL**: https://huggingface.co/datasets/Aharneish/spirit
- **Content**: 108 Upanishads with commentary
- **Download**:
```python
from datasets import load_dataset
ds = load_dataset("Aharneish/spirit")
```

### 14. Puranas (16 Puranas)
- **URL**: https://huggingface.co/datasets/dataspoof/Puranas-dataset
- **Format**: CSV
- **Content**: 16 cleaned Puranas
- **Download**:
```python
from datasets import load_dataset
ds = load_dataset("dataspoof/Puranas-dataset")
```

### 15. Bhagavad Gita Q&A
- **URL**: https://huggingface.co/datasets/JDhruv14/Bhagavad-Gita-QA
- **Format**: CSV
- **Content**: 10,500 Q&A pairs
- **Download**:
```python
from datasets import load_dataset
ds = load_dataset("JDhruv14/Bhagavad-Gita-QA")
```

### 16. Bhagwat Gita Infinity
- **URL**: https://huggingface.co/datasets/Modotte/Bhagwat-Gita-Infinity
- **Format**: JSON
- **Content**: 700 verses with commentaries
- **Download**:
```python
from datasets import load_dataset
ds = load_dataset("Modotte/Bhagwat-Gita-Infinity")
```

---

## TIER 3: NICE TO HAVE

### 17. Sanskrit Verses GRETiL (283K verses)
- **URL**: https://huggingface.co/datasets/paws/sanskrit-verses-gretil
- **Content**: 283,935 verses

### 18. RigVeda
- **URL**: https://huggingface.co/datasets/JDhruv14/RigVeda
- **Content**: 10.6K rows

### 19. Sanskrit NER (Naamah)
- **URL**: https://huggingface.co/datasets/akhil2808/Naamah
- **Content**: 100K-1M entities

### 20. Sanskrit Triplets
- **URL**: https://huggingface.co/datasets/indhic-ai/sanskrit-triplets
- **Content**: 57.1K semantic triplets

---

## DOWNLOAD PRIORITY ORDER

1. **DharmicData** (all-in-one, 140K+ verses, ODbL)
2. **Bhagavad Gita dataset** (deepakrakshit, MIT)
3. **AI4Bharat Sangraha** (Hindi/Sanskrit base)
4. **AI4Bharat IndicAlign** (instruction pairs)
5. **Vedavani** (audio data)
6. **VedicRAG_AI** (supplementary scriptures)
7. **Chanakya Niti** (practical wisdom)
8. **108 Upanishads** (philosophical depth)
9. **Puranas** (mythological context)
10. **DharmaBench** (evaluation benchmark)

---

## TOTAL ESTIMATED SIZE
| Source | Size |
|--------|------|
| DharmicData | ~500 MB |
| Bhagavad Gita | ~10 MB |
| AI4Bharat Sangraha | ~50 GB (Hindi subset) |
| AI4Bharat IndicAlign | ~28 GB |
| Vedavani | ~7 GB |
| VedicRAG_AI | ~163 MB |
| Others | ~1 GB |
| **TOTAL** | **~85 GB** |

> **Note**: Download Hindi/Sanskrit subsets only to save space
