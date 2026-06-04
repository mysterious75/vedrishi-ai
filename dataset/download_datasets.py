import os
import json
import subprocess
import sys
from pathlib import Path

# Configuration
BASE_DIR = Path(r"D:\hacker\vedrishi\vedrishi-ai\dataset\raw")
SUMMARY_FILE = Path(r"D:\hacker\vedrishi\vedrishi-ai\dataset\download_summary.json")

# Dataset configurations
DATASETS = [
    {
        "id": "dataspoof/Puranas-dataset",
        "dir_name": "puranas-dataset",
        "description": "16 Puranas dataset",
        "hf_url": "https://huggingface.co/datasets/dataspoof/Puranas-dataset"
    },
    {
        "id": "Aharneish/spirit",
        "dir_name": "spirit-upanishads",
        "description": "108 Upanishads dataset",
        "hf_url": "https://huggingface.co/datasets/Aharneish/spirit"
    },
    {
        "id": "PyPranav/Bhagwat-Corpus-Data",
        "dir_name": "bhagwat-corpus-data",
        "description": "90K instruction examples",
        "hf_url": "https://huggingface.co/datasets/PyPranav/Bhagwat-Corpus-Data"
    },
    {
        "id": "SatyaSanatan/shrimad-bhagavad-gita-dataset-alpaca",
        "dir_name": "shrimad-bhagavad-gita-dataset-alpaca",
        "description": "703 QA rows",
        "hf_url": "https://huggingface.co/datasets/SatyaSanatan/shrimad-bhagavad-gita-dataset-alpaca"
    },
    {
        "id": "Saptak123/Bhagavad-Gita_Dataset",
        "dir_name": "bhagavad-gita-dataset-saptak",
        "description": "700 verses",
        "hf_url": "https://huggingface.co/datasets/Saptak123/Bhagavad-Gita_Dataset"
    }
]

def check_directory_exists(dir_path):
    """Check if directory exists and has content"""
    if not dir_path.exists():
        return False
    items = list(dir_path.iterdir())
    return len(items) > 0

def download_with_python(dataset_config):
    """Try downloading using Python datasets library"""
    dataset_id = dataset_config["id"]
    target_dir = BASE_DIR / dataset_config["dir_name"]
    
    print(f"\n{'='*60}")
    print(f"Dataset: {dataset_config['description']}")
    print(f"ID: {dataset_id}")
    print(f"Target: {target_dir}")
    print(f"{'='*60}")
    
    # Check if already downloaded
    if check_directory_exists(target_dir):
        print(f"[OK] Directory already exists and has content, skipping...")
        return {"status": "success", "method": "exists", "message": "Already downloaded"}
    
    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Import and load dataset
        from datasets import load_dataset
        print(f"Loading dataset {dataset_id}...")
        ds = load_dataset(dataset_id)
        
        # Save to disk
        print(f"Saving to {target_dir}...")
        ds.save_to_disk(str(target_dir))
        
        # Verify
        if check_directory_exists(target_dir):
            print(f"[OK] Successfully downloaded and saved!")
            return {"status": "success", "method": "python", "message": "Downloaded successfully"}
        else:
            return {"status": "failure", "method": "python", "message": "Download completed but directory is empty"}
            
    except Exception as e:
        print(f"[FAIL] Python download failed: {str(e)}")
        return {"status": "failure", "method": "python", "message": str(e)}

def download_with_git(dataset_config):
    """Try downloading using git clone from HuggingFace"""
    dataset_id = dataset_config["id"]
    target_dir = BASE_DIR / dataset_config["dir_name"]
    hf_url = dataset_config["hf_url"]
    
    print(f"\nTrying git clone from {hf_url}...")
    
    try:
        # Clone the repository
        result = subprocess.run(
            ["git", "clone", hf_url, str(target_dir)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            if check_directory_exists(target_dir):
                print(f"[OK] Successfully cloned!")
                return {"status": "success", "method": "git", "message": "Cloned successfully"}
            else:
                return {"status": "failure", "method": "git", "message": "Clone completed but directory is empty"}
        else:
            return {"status": "failure", "method": "git", "message": result.stderr}
            
    except subprocess.TimeoutExpired:
        return {"status": "failure", "method": "git", "message": "Clone timed out"}
    except Exception as e:
        return {"status": "failure", "method": "git", "message": str(e)}

def download_with_python_alternative(dataset_config):
    """Alternative Python approach using huggingface_hub"""
    dataset_id = dataset_config["id"]
    target_dir = BASE_DIR / dataset_config["dir_name"]
    
    try:
        from huggingface_hub import snapshot_download
        print(f"Trying snapshot download...")
        
        snapshot_download(
            repo_id=dataset_id,
            repo_type="dataset",
            local_dir=str(target_dir)
        )
        
        if check_directory_exists(target_dir):
            print(f"[OK] Successfully downloaded via snapshot!")
            return {"status": "success", "method": "snapshot", "message": "Downloaded successfully"}
        else:
            return {"status": "failure", "method": "snapshot", "message": "Download completed but directory is empty"}
            
    except Exception as e:
        print(f"[FAIL] Snapshot download failed: {str(e)}")
        return {"status": "failure", "method": "snapshot", "message": str(e)}

def download_dataset(dataset_config):
    """Download a dataset using multiple methods"""
    # First try Python
    result = download_with_python(dataset_config)
    
    # If Python fails, try git clone
    if result["status"] == "failure":
        print(f"Python method failed. Trying git clone...")
        result = download_with_git(dataset_config)
    
    # If both fail, try alternative Python approach
    if result["status"] == "failure":
        print(f"Git method also failed. Trying alternative Python approach...")
        result = download_with_python_alternative(dataset_config)
    
    return result

def main():
    """Main function to download all datasets"""
    print("="*60)
    print("VedRishi AI - Dataset Download Script")
    print("="*60)
    
    # Ensure base directory exists
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for dataset_config in DATASETS:
        result = download_dataset(dataset_config)
        result["dataset_id"] = dataset_config["id"]
        result["dir_name"] = dataset_config["dir_name"]
        result["description"] = dataset_config["description"]
        results.append(result)
    
    # Create summary
    summary = {
        "total_datasets": len(DATASETS),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] == "failure"),
        "datasets": results
    }
    
    # Save summary
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Total datasets: {summary['total_datasets']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"\nDetailed results saved to: {SUMMARY_FILE}")
    
    for result in results:
        status_symbol = "[OK]" if result["status"] == "success" else "[FAIL]"
        print(f"{status_symbol} {result['description']}: {result['status']}")
    
    return 0 if summary['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())