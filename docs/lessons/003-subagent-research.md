# LESSON 003: SUB-AGENTS FOR RESEARCH
**Date**: 2026-06-04
**Phase**: Dataset Research

## WHAT HAPPENED
- Bhagavad Gita download script failed
- User ne kaha sub-agents use karo
- 7 parallel sub-agents launch kiye
- Sab ne comprehensive research ki

## KEY FINDINGS

### 1. Bhagavad Gita - Multiple Sources
- **deepakrakshit/bhagavad-gita-dataset** (MIT) - BEST for structured data
- **api.bhagavadgita.io/v2** (GPL-3.0) - 21 author translations
- **gita/gita** (Unlicense) - Raw JSON data
- **HuggingFace**: JDhruv14, Modotte, SatyaSanatan

### 2. All-In-One Source Found
- **bhavykhatri/DharmicData** (ODbL-1.0)
- 140K+ verses: Gita, Ramayana, Mahabharata, 3 Vedas
- Commercial use OK with attribution

### 3. AI4Bharat Datasets
- **Sangraha**: 251B tokens (Hindi 34.5B, Sanskrit 14.9B)
- **IndicAlign**: 74.7M instruction pairs
- **License**: CC-BY-4.0 (commercial OK)

### 4. Audio Data Available
- **Vedavani**: 30,779 Vedic verses with audio (Apache-2.0)
- **Bhagavad Gita Audio**: 701 shlokas on HuggingFace

### 5. Evaluation Benchmarks
- **DharmaBench**: 13 tasks for Sanskrit/Tibetan
- Published at IJCNLP-AACL 2025
- CC-BY-4.0 license

## LESSONS LEARNED

### 1. Sub-Agents Are Powerful
- 7 agents researched simultaneously
- Found 20+ datasets I would have missed
- Each agent went deep into its topic

### 2. Free Resources Abundant
- 140K+ verses available for free
- Multiple API options (no auth needed)
- HuggingFace datasets easy to use

### 3. Commercial Use Possible
- Most datasets have permissive licenses
- CC-BY-4.0, MIT, Apache-2.0 all allow commercial use
- Only need attribution

### 4. Download Strategy
- Start with DharmicData (all-in-one)
- Add AI4Bharat for Hindi/Sanskrit base
- Use APIs for specific queries
- Audio data for voice features

## WHAT TO DO NEXT
1. Run master download script
2. Verify downloaded data
3. Convert to training format
4. Start fine-tuning

## PREVENTION
- Always check license before using data
- Use sub-agents for parallel research
- Document all sources
- Keep download logs

---
> **Status**: Research complete, ready for download
