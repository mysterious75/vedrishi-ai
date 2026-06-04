# VedRishi AI - Training Requirements Checklist

## 📋 Kaggle Training Requirements

### Hardware Requirements
- [x] GPU: NVIDIA T4 x2 (or better) - Kaggle provides T4 x2
- [x] RAM: 16GB+ - Kaggle provides 16GB
- [x] Storage: 20GB+ free space - Kaggle provides 20GB

### Software Requirements
- [x] Python 3.10+
- [x] PyTorch 2.0+
- [x] Transformers 4.30+
- [x] PEFT 0.4+
- [x] BitsAndBytes 0.40+
- [x] TRL 0.7+
- [x] Unsloth (optional but recommended)

### Dataset Requirements
- [x] Training data: 28,482 instruction pairs (JSONL format)
- [x] Validation data: 3,165 instruction pairs (JSONL format)
- [x] Total size: ~32MB (compressed)
- [x] Format: Alpaca format (instruction, input, output)

### Model Requirements
- [x] Base model: Qwen 2.5 7B Instruct
- [x] Quantization: 4-bit (QLoRA)
- [x] LoRA rank: 16
- [x] LoRA alpha: 32

### Training Configuration
- [x] Batch size: 4
- [x] Gradient accumulation: 4
- [x] Effective batch size: 16
- [x] Learning rate: 2e-4
- [x] Epochs: 3
- [x] Max sequence length: 2048

## 🔧 Pre-Training Checklist

### Data Preparation
- [x] Raw datasets downloaded (40+ sources)
- [x] Data cleaned and normalized (165,565 verses)
- [x] Instruction pairs generated (31,647 pairs)
- [x] Dataset sanitized (company names removed)
- [x] Train/val split (90/10)

### Code Preparation
- [x] Training notebook created
- [x] Kaggle-compatible configuration
- [x] Evaluation script ready
- [x] RAG pipeline setup

### Infrastructure
- [x] GitHub repository created
- [x] Code uploaded to GitHub
- [x] MemePalace integrated as submodule
- [x] Documentation complete

## 🚀 Kaggle Training Steps

### Step 1: Setup Kaggle
1. Create Kaggle account at kaggle.com
2. Enable GPU acceleration in notebook settings
3. Clone repository: `git clone https://github.com/mysterious75/vedrishi-ai.git`

### Step 2: Install Dependencies
```bash
pip install torch transformers datasets accelerate peft bitsandbytes trl unsloth
```

### Step 3: Upload Dataset
1. Upload `training/outputs/vedrishi_train.jsonl` to Kaggle dataset
2. Upload `training/outputs/vedrishi_val.jsonl` to Kaggle dataset

### Step 4: Run Training
1. Open `training/notebooks/vedrishi-kaggle-training.ipynb`
2. Run all cells
3. Monitor training loss and validation metrics

### Step 5: Download Model
1. Download fine-tuned model from Kaggle output
2. Upload to HuggingFace Hub (optional)
3. Test model with sample queries

## 📊 Expected Results

### Training Metrics
- Training loss: < 1.0 (after 3 epochs)
- Validation loss: < 1.5
- Training time: 2-4 hours on T4 x2

### Model Performance
- Verse accuracy: ≥ 92%
- Tone score: ≥ 85%
- Safety score: 100%
- Disclaimer present: 100%

## ⚠️ Important Notes

### Data Privacy
- [x] No company/developer names in dataset
- [x] No personal information in training data
- [x] All verses from public domain sources

### Safety Requirements
- [x] Crisis helpline redirect configured
- [x] No medical/legal/financial advice
- [x] No fake verses or false promises
- [x] Zero tolerance for discrimination

### License Compliance
- [x] Qwen 2.5: Apache 2.0
- [x] MemePalace: MIT License
- [x] Training data: Public domain + ODbL-1.0

## 📝 Next Steps After Training

1. **Evaluation**: Run evaluation script on 100+ test queries
2. **RAG Integration**: Set up ChromaDB for verse retrieval
3. **API Development**: Build FastAPI backend
4. **Frontend**: Create Next.js web interface
5. **WhatsApp Bot**: Integrate Twilio for WhatsApp
6. **Beta Launch**: Deploy to production

---

**Status**: Ready for Kaggle training
**Last Updated**: 2026-06-04
