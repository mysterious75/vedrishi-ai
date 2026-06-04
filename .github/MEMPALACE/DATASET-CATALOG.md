# VEDRISHI AI - MASTER DATASET CATALOG
> Sab kuch jo download karna hai - compiled from 7 sub-agents

---

## DOWNLOAD COMMANDS (Copy-Paste Ready)

### 1. DharmicData (BEST - All-in-One, 140K+ verses)
```bash
cd D:\hacker\vedrishi\vedrishi-ai\dataset\raw
git clone https://github.com/bhavykhatri/DharmicData.git
```
**Contains**: Gita, Ramayana, Mahabharata, Rigveda, Yajurveda, Atharvaveda
**License**: ODbL-1.0 (commercial OK)

### 2. Bhagavad Gita Dataset (700 verses, 3 languages)
```bash
git clone https://github.com/deepakrakshit/bhagavad-gita-dataset.git
```
**Contains**: Sanskrit + Hindi + English
**License**: MIT

### 3. Bhagavad Gita API (v2, no auth)
```bash
curl -s "https://api.bhagavadgita.io/v2/chapters/1/verses/" > chapter_1.json
curl -s "https://api.bhagavadgita.io/v2/chapters/2/verses/" > chapter_2.json
# ... repeat for all 18 chapters
```
**Contains**: 700 verses, 21 author translations
**License**: GPL-3.0

### 4. AI4Bharat Sangraha (251B tokens)
```python
from datasets import load_dataset
# Hindi subset
dataset = load_dataset("ai4bharat/sangraha", data_dir="verified/hin")
# Sanskrit subset
dataset = load_dataset("ai4bharat/sangraha", data_dir="verified/san")
```
**License**: CC-BY-4.0 (commercial OK)

### 5. AI4Bharat IndicAlign (74.7M instruction pairs)
```python
from datasets import load_dataset
dataset = load_dataset("ai4bharat/indic-align")
```
**License**: CC-BY-4.0 (commercial OK)

### 6. Vedavani Dataset (Vedic Audio)
```bash
git clone https://huggingface.co/datasets/sanganaka/Vedavani-Dataset
```
**Contains**: 30,779 verses with audio (6.81 GB)
**License**: Apache-2.0

### 7. VedicRAG_AI (85,895+ verses)
```bash
git clone https://github.com/techie-jai/VedicRAG_AI.git
```
**Contains**: Ramayana (17K), Mahabharata (68K), Upanishads, Vedas
**License**: MIT (check with author for commercial)

### 8. DharmaBench (Evaluation)
```python
from datasets import load_dataset
ds = load_dataset("Intellexus/DharmaBench")
```
**Contains**: 13 Sanskrit/Tibetan tasks
**License**: CC-BY-4.0

### 9. Chanakya Niti
```python
from datasets import load_dataset
ds = load_dataset("Umang-Bansal/Chanakya-niti")
```
**Contains**: 429 rows of practical wisdom
**License**: Apache-2.0

### 10. 108 Upanishads
```python
from datasets import load_dataset
ds = load_dataset("Aharneish/spirit")
```
**Contains**: 108 Upanishads with commentary

### 11. Puranas (16 Puranas)
```python
from datasets import load_dataset
ds = load_dataset("dataspoof/Puranas-dataset")
```
**Contains**: 16 cleaned Puranas

### 12. Bhagavad Gita Q&A
```python
from datasets import load_dataset
ds = load_dataset("JDhruv14/Bhagavad-Gita-QA")
```
**Contains**: 10,500 Q&A pairs

### 13. Bhagwat Gita Infinity
```python
from datasets import load_dataset
ds = load_dataset("Modotte/Bhagwat-Gita-Infinity")
```
**Contains**: 700 verses with commentaries

### 14. Vedanta Datasets
```bash
git clone https://github.com/atmabodha/Vedanta_Datasets.git
```
**Contains**: Gita, Upanishads, Yoga Sutras

### 15. Itihasa Corpus
```bash
git clone https://github.com/rahular/itihasa.git
```
**Contains**: 93K shlokas (Ramayana + Mahabharata)

### 16. Valmiki Ramayana
```bash
git clone https://github.com/Ashutosh-Vijay/Valmiki_Ramayan_Dataset.git
```
**Contains**: 24K verses
**License**: MIT

---

## QUICK DOWNLOAD (ALL AT ONCE)

Run this single script:
```bash
cd D:\hacker\vedrishi\vedrishi-ai
python scripts/00-download-all-datasets.py
```

---

## TOTAL SIZE ESTIMATE
| Source | Size |
|--------|------|
| DharmicData | ~500 MB |
| Bhagavad Gita datasets | ~50 MB |
| AI4Bharat Sangraha (Hindi) | ~50 GB |
| AI4Bharat IndicAlign | ~28 GB |
| Vedavani | ~7 GB |
| VedicRAG_AI | ~163 MB |
| Others | ~1 GB |
| **TOTAL** | **~85 GB** |

---

## COMMERCIAL USE SUMMARY
| Dataset | License | Commercial OK |
|---------|---------|---------------|
| DharmicData | ODbL-1.0 | ✅ YES |
| Bhagavad Gita (deepakrakshit) | MIT | ✅ YES |
| AI4Bharat Sangraha | CC-BY-4.0 | ✅ YES |
| AI4Bharat IndicAlign | CC-BY-4.0 | ✅ YES |
| Vedavani | Apache-2.0 | ✅ YES |
| DharmaBench | CC-BY-4.0 | ✅ YES |
| Chanakya Niti | Apache-2.0 | ✅ YES |
| Valmiki Ramayana | MIT | ✅ YES |
