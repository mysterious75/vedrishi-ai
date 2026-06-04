#!/usr/bin/env python3
"""
VEDRISHI AI - Fine-tuning Script for Unsloth Cloud
Prepares data and configuration for QLoRA training on Qwen 2.5 7B
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
TRAINING_DIR = Path(__file__).parent.parent
DATASET_DIR = TRAINING_DIR.parent / "dataset" / "instruction-pairs"
OUTPUT_DIR = TRAINING_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ===========================
# DATA PREPARATION
# ===========================

def prepare_dataset_for_unsloth():
    """Prepare instruction pairs in Unsloth format"""
    print("=" * 60)
    print("VEDRISHI AI - PREPARING DATASET FOR UNSLOTH CLOUD")
    print("=" * 60)
    
    # Load instruction pairs
    input_file = DATASET_DIR / "vedrishi_instruction_pairs.jsonl"
    pairs = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                pairs.append(json.loads(line))
    
    print(f"Loaded {len(pairs)} instruction pairs")
    
    # Convert to Unsloth/Alpaca format
    unsloth_data = []
    
    for pair in pairs:
        # Alpaca format: instruction, input, output
        unsloth_entry = {
            "instruction": pair['instruction'],
            "input": pair.get('input', ''),
            "output": pair['output']
        }
        unsloth_data.append(unsloth_entry)
    
    # Save in Unsloth format
    output_file = OUTPUT_DIR / "vedrishi_unsloth_format.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in unsloth_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Saved {len(unsloth_data)} entries in Unsloth format")
    print(f"Output: {output_file}")
    
    # Split into train/val (90/10)
    split_idx = int(len(unsloth_data) * 0.9)
    train_data = unsloth_data[:split_idx]
    val_data = unsloth_data[split_idx:]
    
    train_file = OUTPUT_DIR / "vedrishi_train.jsonl"
    val_file = OUTPUT_DIR / "vedrishi_val.jsonl"
    
    with open(train_file, 'w', encoding='utf-8') as f:
        for entry in train_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    with open(val_file, 'w', encoding='utf-8') as f:
        for entry in val_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Train: {len(train_data)}, Val: {len(val_data)}")
    
    return train_file, val_file

# ===========================
# UNSLOTH CLOUD CONFIG
# ===========================

def create_unsloth_config():
    """Create configuration for Unsloth Cloud"""
    print("\n" + "=" * 60)
    print("CREATING UNSLOTH CLOUD CONFIGURATION")
    print("=" * 60)
    
    config = {
        "project_name": "vedrishi-ai",
        "base_model": "unsloth/Qwen2.5-7B-Instruct",
        "training_method": "qlora",
        "dataset": {
            "train_file": "vedrishi_train.jsonl",
            "val_file": "vedrishi_val.jsonl",
            "format": "alpaca",
            "total_pairs": 31647
        },
        "hyperparameters": {
            "learning_rate": 2e-4,
            "num_epochs": 3,
            "batch_size": 4,
            "gradient_accumulation_steps": 4,
            "warmup_steps": 100,
            "max_seq_length": 2048,
            "lora_r": 16,
            "lora_alpha": 32,
            "lora_dropout": 0.05,
            "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            "quantization": "4bit",
            "bf16": True,
            "fp16": False,
            "optimizer": "adamw_8bit",
            "lr_scheduler": "cosine",
            "weight_decay": 0.01,
            "max_grad_norm": 1.0
        },
        "safety_config": {
            "disclaimer_required": True,
            "topic_filters": ["medical_advice", "legal_advice", "financial_advice", "political", "controversial"],
            "crisis_helplines": {
                "iCall": "9152987821",
                "VandrevalaFoundation": "1860-2662-345"
            }
        },
        "output_dir": "vedrishi-qlora-output",
        "wandb_project": "vedrishi-ai-training",
        "created_at": datetime.now().isoformat()
    }
    
    config_file = TRAINING_DIR / "configs" / "unsloth_config.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"Configuration saved: {config_file}")
    print(f"\nKey Settings:")
    print(f"  Base Model: {config['base_model']}")
    print(f"  Training Method: {config['training_method']}")
    print(f"  Total Pairs: {config['dataset']['total_pairs']}")
    print(f"  Epochs: {config['hyperparameters']['num_epochs']}")
    print(f"  Learning Rate: {config['hyperparameters']['learning_rate']}")
    
    return config

# ===========================
# UNSLOTH UPLOAD SCRIPT
# ===========================

def create_upload_script():
    """Create script to upload dataset to Unsloth Cloud"""
    print("\n" + "=" * 60)
    print("CREATING UNSLOTH CLOUD UPLOAD SCRIPT")
    print("=" * 60)
    
    upload_script = '''#!/usr/bin/env python3
"""
Upload VedRishi dataset to Unsloth Cloud
Run this script after setting up Unsloth Cloud account
"""

import json
import os
import requests
from pathlib import Path

# Configuration
UNSLOTH_API_KEY = os.environ.get("UNSLOTH_API_KEY", "")  # Get from https://unsloth.ai
PROJECT_NAME = "vedrishi-ai"
DATASET_DIR = Path(__file__).parent.parent / "dataset" / "instruction-pairs"

def upload_to_unsloth():
    """Upload dataset to Unsloth Cloud"""
    print("Uploading dataset to Unsloth Cloud...")
    
    # Load dataset
    train_file = DATASET_DIR / "vedrishi_train.jsonl"
    val_file = DATASET_DIR / "vedrishi_val.jsonl"
    
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = [json.loads(line) for line in f if line.strip()]
    
    with open(val_file, 'r', encoding='utf-8') as f:
        val_data = [json.loads(line) for line in f if line.strip()]
    
    print(f"Train: {len(train_data)}, Val: {len(val_data)}")
    
    # TODO: Implement Unsloth Cloud API upload
    # This will be updated when Unsloth Cloud provides API access
    
    print("\\nDataset ready for upload!")
    print("Please upload manually via Unsloth Cloud interface:")
    print("1. Go to https://cloud.unsloth.ai")
    print("2. Create new project: vedrishi-ai")
    print("3. Upload vedrishi_train.jsonl and vedrishi_val.jsonl")
    print("4. Configure QLoRA settings")
    print("5. Start training")

if __name__ == "__main__":
    upload_to_unsloth()
'''
    
    upload_file = TRAINING_DIR / "scripts" / "upload_to_unsloth.py"
    with open(upload_file, 'w', encoding='utf-8') as f:
        f.write(upload_script)
    
    print(f"Upload script saved: {upload_file}")
    return upload_file

# ===========================
# MAIN
# ===========================

def main():
    """Main function"""
    # Prepare dataset
    train_file, val_file = prepare_dataset_for_unsloth()
    
    # Create Unsloth config
    config = create_unsloth_config()
    
    # Create upload script
    upload_script = create_upload_script()
    
    print("\n" + "=" * 60)
    print("UNSLOTH CLOUD PREPARATION COMPLETE!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Sign up at https://unsloth.ai")
    print("2. Create new project: vedrishi-ai")
    print("3. Upload dataset files:")
    print(f"   - {train_file}")
    print(f"   - {val_file}")
    print("4. Configure QLoRA settings")
    print("5. Start training (estimated: 2-4 hours)")
    print("6. Download fine-tuned model")
    
    return {
        'train_file': str(train_file),
        'val_file': str(val_file),
        'config': str(TRAINING_DIR / "configs" / "unsloth_config.json"),
        'upload_script': str(upload_script)
    }

if __name__ == "__main__":
    main()
