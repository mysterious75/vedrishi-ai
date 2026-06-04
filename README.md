# VedRishi AI

AI-powered Hindu spiritual guide trained on sacred scriptures (Gita, Ramayana, Mahabharata).

## Features

- **Scripture-based AI**: Trained on 165,000+ verses from Gita, Ramayana, and Mahabharata
- **Multilingual**: Sanskrit, Hindi, and English support
- **Safety-first**: Built-in disclaimers, crisis helpline redirect, and content filters
- **RAG Pipeline**: ChromaDB for accurate verse retrieval

## Project Structure

```
vedrishi-ai/
├── dataset/           # Cleaned and processed datasets
├── training/          # Kaggle notebooks and training configs
├── rag/               # RAG pipeline with ChromaDB
├── evaluation/        # Model evaluation scripts
├── vendor/            # Third-party dependencies
│   └── mempalace/     # AI memory system (MIT License)
├── scripts/           # Data processing scripts
└── docs/              # Documentation
```

## Training

Training is done on Kaggle using QLoRA fine-tuning of Qwen 2.5 7B.

### Requirements
- GPU: NVIDIA T4 x2 (or better)
- RAM: 16GB+
- Internet: ON

### Steps
1. Clone this repository on Kaggle
2. Upload dataset from `training/outputs/`
3. Run `training/notebooks/vedrishi-kaggle-training.ipynb`
4. Download fine-tuned model

## Dataset Statistics

| Text Type | Verses |
|-----------|--------|
| Bhagavad Gita | 701 |
| Ramayana | 22,432 |
| Mahabharata | 142,432 |
| **Total** | **165,565** |

## Safety Features

- AI spiritual assistant disclaimer on every response
- Crisis helpline redirect (iCall: 9152987821)
- No medical/legal/financial advice
- No fake verses or false promises
- Zero tolerance for caste/gender discrimination

## License

MIT License - See [LICENSE](LICENSE) for details

## Acknowledgments

- Sacred texts from public domain sources
- MemePalace for AI memory system
- Kaggle for training infrastructure
