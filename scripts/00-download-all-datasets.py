#!/usr/bin/env python3
"""
VEDRISHI AI - Master Dataset Downloader
Downloads ALL datasets from all sources
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "dataset" / "raw"
LOG_FILE = BASE_DIR / "dataset" / "download_log.txt"

# Create directories
RAW_DIR.mkdir(parents=True, exist_ok=True)

def log(message):
    """Log message to file and print"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def run_command(cmd, cwd=None):
    """Run shell command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)

def download_github_repo(url, name):
    """Clone a GitHub repository"""
    target_dir = RAW_DIR / name
    
    if target_dir.exists():
        log(f"⏭️  {name} already exists, skipping...")
        return True
    
    log(f"📥 Downloading {name}...")
    success, output = run_command(f"git clone {url} {target_dir}")
    
    if success:
        log(f"✅ {name} downloaded successfully")
    else:
        log(f"❌ Failed to download {name}: {output[:200]}")
    
    return success

def download_huggingface_dataset(dataset_id, name):
    """Download HuggingFace dataset"""
    target_dir = RAW_DIR / name
    
    if target_dir.exists():
        log(f"⏭️  {name} already exists, skipping...")
        return True
    
    log(f"📥 Downloading {name} from HuggingFace...")
    
    # Try huggingface-cli first
    success, output = run_command(
        f"huggingface-cli download {dataset_id} --repo-type dataset --local-dir {target_dir}"
    )
    
    if not success:
        # Fallback to git clone
        success, output = run_command(
            f"git clone https://huggingface.co/datasets/{dataset_id} {target_dir}"
        )
    
    if success:
        log(f"✅ {name} downloaded successfully")
    else:
        log(f"❌ Failed to download {name}: {output[:200]}")
    
    return success

def download_bhagavad_gita_api():
    """Download Bhagavad Gita via API"""
    target_file = RAW_DIR / "bhagavad_gita_api" / "verses.json"
    target_file.parent.mkdir(parents=True, exist_ok=True)
    
    if target_file.exists():
        log("⏭️  Bhagavad Gita API data already exists, skipping...")
        return True
    
    log("📥 Downloading Bhagavad Gita from API...")
    
    all_verses = []
    api_base = "https://api.bhagavadgita.io/v2"
    
    # Download all 18 chapters
    for chapter in range(1, 19):
        url = f"{api_base}/chapters/{chapter}/verses/"
        success, output = run_command(f'curl -s "{url}"')
        
        if success:
            try:
                verses = json.loads(output)
                all_verses.extend(verses)
                log(f"  ✅ Chapter {chapter}: {len(verses)} verses")
            except json.JSONDecodeError:
                log(f"  ❌ Chapter {chapter}: Invalid JSON")
        else:
            log(f"  ❌ Chapter {chapter}: {output[:100]}")
    
    # Save all verses
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(all_verses, f, ensure_ascii=False, indent=2)
    
    log(f"✅ Bhagavad Gita API: {len(all_verses)} verses downloaded")
    return True

def install_huggingface_hub():
    """Install huggingface_hub if not present"""
    log("📦 Installing huggingface_hub...")
    success, _ = run_command("pip install huggingface_hub datasets")
    if success:
        log("✅ huggingface_hub installed")
    else:
        log("⚠️  huggingface_hub installation failed, will try git clone")
    return success

# ===========================
# MAIN DOWNLOAD FUNCTION
# ===========================

def download_all():
    """Download all datasets"""
    
    log("=" * 60)
    log("🕉️  VEDRISHI AI - MASTER DATASET DOWNLOADER")
    log("=" * 60)
    
    # Install dependencies
    install_huggingface_hub()
    
    # Track results
    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }
    
    # ===========================
    # TIER 1: MUST DOWNLOAD
    # ===========================
    log("\n" + "=" * 60)
    log("TIER 1: MUST DOWNLOAD (Free, Commercial OK)")
    log("=" * 60)
    
    tier1_datasets = [
        # DharmicData - All-in-one scriptures
        ("https://github.com/bhavykhatri/DharmicData.git", "DharmicData"),
        
        # Bhagavad Gita - Structured dataset
        ("https://github.com/deepakrakshit/bhagavad-gita-dataset.git", "bhagavad-gita-dataset"),
        
        # Vedavani - Vedic audio
        (None, "Vedavani-Dataset"),  # HuggingFace
        
        # VedicRAG_AI - Extended scriptures
        ("https://github.com/techie-jai/VedicRAG_AI.git", "VedicRAG_AI"),
        
        # Valmiki Ramayana
        ("https://github.com/Ashutosh-Vijay/Valmiki_Ramayan_Dataset.git", "Valmiki_Ramayan_Dataset"),
    ]
    
    for url, name in tier1_datasets:
        if url:
            success = download_github_repo(url, name)
        else:
            success = download_huggingface_dataset("sanganaka/Vedavani-Dataset", name)
        
        if success:
            results["success"].append(name)
        else:
            results["failed"].append(name)
    
    # Bhagavad Gita API
    download_bhagavad_gita_api()
    results["success"].append("bhagavad_gita_api")
    
    # AI4Bharat datasets (large, optional)
    log("\n📥 AI4Bharat datasets (large, may take time)...")
    try:
        from datasets import load_dataset
        
        # Sangraha Hindi subset
        log("  Downloading Sangraha Hindi...")
        dataset = load_dataset("ai4bharat/sangraha", data_dir="verified/hin", 
                             cache_dir=str(RAW_DIR / "sangraha_hindi"))
        log("  ✅ Sangraha Hindi downloaded")
        results["success"].append("sangraha_hindi")
    except Exception as e:
        log(f"  ⚠️  Sangraha download skipped: {str(e)[:100]}")
    
    # ===========================
    # TIER 2: SHOULD DOWNLOAD
    # ===========================
    log("\n" + "=" * 60)
    log("TIER 2: SHOULD DOWNLOAD (Supplementary)")
    log("=" * 60)
    
    tier2_datasets = [
        # Vedanta Datasets
        ("https://github.com/atmabodha/Vedanta_Datasets.git", "Vedanta_Datasets"),
        
        # Itihasa Corpus
        ("https://github.com/rahular/itihasa.git", "itihasa"),
        
        # Chanakya Niti (HuggingFace)
        (None, "Chanakya-niti"),
        
        # 108 Upanishads (HuggingFace)
        (None, "108-Upanishads"),
        
        # Puranas (HuggingFace)
        (None, "Puranas-dataset"),
    ]
    
    for url, name in tier2_datasets:
        if url:
            success = download_github_repo(url, name)
        else:
            # Map names to HuggingFace IDs
            hf_map = {
                "Chanakya-niti": "Umang-Bansal/Chanakya-niti",
                "108-Upanishads": "Aharneish/spirit",
                "Puranas-dataset": "dataspoof/Puranas-dataset",
            }
            hf_id = hf_map.get(name, name)
            success = download_huggingface_dataset(hf_id, name)
        
        if success:
            results["success"].append(name)
        else:
            results["failed"].append(name)
    
    # ===========================
    # TIER 3: NICE TO HAVE
    # ===========================
    log("\n" + "=" * 60)
    log("TIER 3: NICE TO HAVE (Evaluation & Extras)")
    log("=" * 60)
    
    tier3_datasets = [
        # DharmaBench
        (None, "DharmaBench"),
        
        # Bhagavad Gita Q&A
        (None, "Bhagavad-Gita-QA"),
        
        # Bhagwat Gita Infinity
        (None, "Bhagwat-Gita-Infinity"),
    ]
    
    for url, name in tier3_datasets:
        if url:
            success = download_github_repo(url, name)
        else:
            hf_map = {
                "DharmaBench": "Intellexus/DharmaBench",
                "Bhagavad-Gita-QA": "JDhruv14/Bhagavad-Gita-QA",
                "Bhagwat-Gita-Infinity": "Modotte/Bhagwat-Gita-Infinity",
            }
            hf_id = hf_map.get(name, name)
            success = download_huggingface_dataset(hf_id, name)
        
        if success:
            results["success"].append(name)
        else:
            results["failed"].append(name)
    
    # ===========================
    # SUMMARY
    # ===========================
    log("\n" + "=" * 60)
    log("📊 DOWNLOAD SUMMARY")
    log("=" * 60)
    log(f"✅ Successful: {len(results['success'])}")
    log(f"❌ Failed: {len(results['failed'])}")
    log(f"📁 Total datasets: {len(results['success']) + len(results['failed'])}")
    
    if results['failed']:
        log(f"\n❌ Failed downloads:")
        for name in results['failed']:
            log(f"  - {name}")
    
    # Save summary
    summary_file = BASE_DIR / "dataset" / "download_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)
    
    log(f"\n📁 Summary saved to: {summary_file}")
    log("=" * 60)
    
    return results

# ===========================
# ENTRY POINT
# ===========================

if __name__ == "__main__":
    print("""
    🕉️  VEDRISHI AI - MASTER DATASET DOWNLOADER
    ============================================
    
    This will download ALL datasets for training.
    Total size: ~85 GB (depending on what you choose)
    
    Options:
    1. Download ALL (recommended)
    2. Download TIER 1 only (essential)
    3. Download TIER 1 + 2 (recommended)
    
    Press Enter to start, or Ctrl+C to cancel...
    """)
    
    input()
    
    results = download_all()
    
    print("\n🎉 Download complete!")
    print(f"✅ Success: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")
