#!/usr/bin/env python3
"""
VEDRISHI AI - Kaggle Dataset Upload Script
Uploads training data to Kaggle for easy access during training
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
TRAINING_DIR = Path(__file__).parent.parent / "training"
DATASET_DIR = TRAINING_DIR.parent / "dataset" / "instruction-pairs"
KAGGLE_DIR = Path(__file__).parent.parent / "kaggle-dataset"
KAGGLE_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = KAGGLE_DIR / "upload_log.txt"

def log(message):
    """Log message to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ===========================
# PREPARE KAGGLE DATASET
# ===========================

def prepare_kaggle_dataset():
    """Prepare dataset for Kaggle upload"""
    print("=" * 60)
    print("VEDRISHI AI - PREPARING KAGGLE DATASET")
    print("=" * 60)
    
    # Copy training files
    train_file = Path(__file__).parent.parent / "training" / "outputs" / "vedrishi_train.jsonl"
    val_file = Path(__file__).parent.parent / "training" / "outputs" / "vedrishi_val.jsonl"
    
    # Copy to kaggle-dataset
    import shutil
    
    if train_file.exists():
        shutil.copy(train_file, KAGGLE_DIR / "vedrishi_train.jsonl")
        print(f"Copied: {train_file.name}")
    
    if val_file.exists():
        shutil.copy(val_file, KAGGLE_DIR / "vedrishi_val.jsonl")
        print(f"Copied: {val_file.name}")
    
    # Create metadata
    metadata = {
        "title": "VedRishi AI Training Dataset",
        "id": "vedrishi-ai/training-dataset",
        "licenses": [
            {
                "name": "CC0-1.0"
            }
        ]
    }
    
    metadata_file = KAGGLE_DIR / "dataset-metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Created: {metadata_file.name}")
    
    return KAGGLE_DIR

# ===========================
# KAGGLE API UPLOAD
# ===========================

def upload_to_kaggle():
    """Upload dataset to Kaggle using API"""
    print("\n" + "=" * 60)
    print("UPLOADING TO KAGGLE")
    print("=" * 60)
    
    # Check if kaggle CLI is available
    import subprocess
    
    try:
        result = subprocess.run(["kaggle", "--version"], capture_output=True, text=True)
        print("Kaggle CLI found")
    except FileNotFoundError:
        print("Kaggle CLI not found")
        print("Please install: pip install kaggle")
        return False
    
    # Check if credentials exist
    kaggle_dir = Path.home() / ".kaggle"
    if not (kaggle_dir / "kaggle.json").exists():
        print("\nKaggle credentials not found!")
        print("Please:")
        print("1. Go to https://www.kaggle.com/settings")
        print("2. Create new API token")
        print("3. Save kaggle.json to ~/.kaggle/kaggle.json")
        return False
    
    # Upload dataset
    print("\nUploading dataset to Kaggle...")
    
    # Create dataset
    cmd = f"kaggle datasets create -p {KAGGLE_DIR}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Dataset uploaded successfully!")
        print("URL: https://www.kaggle.com/datasets/vedrishi-ai/training-dataset")
        return True
    else:
        print(f"Upload failed: {result.stderr}")
        return False

# ===========================
# MANUAL UPLOAD INSTRUCTIONS
# ===========================

def print_manual_instructions():
    """Print manual upload instructions"""
    print("\n" + "=" * 60)
    print("MANUAL UPLOAD INSTRUCTIONS")
    print("=" * 60)
    
    print("\nIf automatic upload fails, follow these steps:")
    print("\n1. Go to: https://www.kaggle.com/datasets/new")
    print("2. Fill in:")
    print("   - Dataset name: vedrishi-training-dataset")
    print("   - Title: VedRishi AI Training Dataset")
    print("   - License: CC0-1.0")
    print(f"3. Upload files from: {KAGGLE_DIR}")
    print("4. Click 'Create Dataset'")
    print("5. Copy the dataset URL")
    print("6. Update notebook with your dataset URL")

# ===========================
# MAIN
# ===========================

def main():
    """Main function"""
    log("VEDRISHI AI - KAGGLE DATASET UPLOAD")
    log("=" * 60)
    
    # Prepare dataset
    kaggle_dir = prepare_kaggle_dataset()
    
    # Try to upload
    upload_success = upload_to_kaggle()
    
    if not upload_success:
        print_manual_instructions()
    
    log("\n" + "=" * 60)
    log("DATASET PREPARATION COMPLETE")
    log("=" * 60)
    log(f"Dataset directory: {kaggle_dir}")
    
    print("\n" + "=" * 60)
    print("KAGGLE DATASET READY")
    print("=" * 60)
    print(f"\nDataset files: {kaggle_dir}")
    print("\nNext steps:")
    print("1. Upload dataset to Kaggle (manual or automatic)")
    print("2. Update notebook with your dataset URL")
    print("3. Run training on Kaggle")
    
    return {
        'kaggle_dir': str(kaggle_dir),
        'upload_success': upload_success
    }

if __name__ == "__main__":
    main()
