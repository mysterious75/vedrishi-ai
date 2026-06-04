#!/usr/bin/env python3
"""
Upload VedRishi dataset to Unsloth Cloud
Run this script after setting up Unsloth Cloud account
"""

import json
import requests
from pathlib import Path

# Configuration
UNSLOTH_API_KEY = "YOUR_UNSLOTH_API_KEY"  # Get from https://unsloth.ai
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
    
    print("\nDataset ready for upload!")
    print("Please upload manually via Unsloth Cloud interface:")
    print("1. Go to https://cloud.unsloth.ai")
    print("2. Create new project: vedrishi-ai")
    print("3. Upload vedrishi_train.jsonl and vedrishi_val.jsonl")
    print("4. Configure QLoRA settings")
    print("5. Start training")

if __name__ == "__main__":
    upload_to_unsloth()
