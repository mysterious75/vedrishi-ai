#!/usr/bin/env python3
"""
VEDRISHI AI - Bhagavad Gita Data Downloader
Downloads all 700 verses from BhagavadGita API
"""

import json
import os
import requests
from pathlib import Path

# Configuration
BASE_URL = "https://api.github.com/repos/gita/BhagavadGita/contents/gita"
OUTPUT_DIR = Path(__file__).parent.parent / "dataset" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "bhagavad_gita.json"

def download_gita():
    """Download all chapters and verses from Bhagavad Gita API"""
    
    print("🕉️  VEDRISHI AI - Bhagavad Gita Downloader")
    print("=" * 50)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Store all data
    all_data = {
        "metadata": {
            "source": "BhagavadGita API",
            "total_chapters": 18,
            "total_verses": 700,
            "languages": ["sanskrit", "hindi", "english"]
        },
        "chapters": []
    }
    
    # Download each chapter
    for chapter_num in range(1, 19):
        print(f"\n📖 Downloading Chapter {chapter_num}...")
        
        chapter_url = f"{BASE_URL}/{chapter_num}"
        response = requests.get(chapter_url)
        
        if response.status_code != 200:
            print(f"  ❌ Failed to download chapter {chapter_num}")
            continue
        
        chapter_data = response.json()
        chapter_info = {
            "chapter_number": chapter_num,
            "verses": []
        }
        
        # Download each verse in chapter
        for verse_file in chapter_data:
            if verse_file["name"].endswith(".json"):
                verse_url = verse_file["download_url"]
                verse_response = requests.get(verse_url)
                
                if verse_response.status_code == 200:
                    verse_data = verse_response.json()
                    chapter_info["verses"].append(verse_data)
                    print(f"  ✅ Verse {verse_data.get('verse_number', '?')} downloaded")
                else:
                    print(f"  ❌ Failed to download verse")
        
        all_data["chapters"].append(chapter_info)
        print(f"  📊 Chapter {chapter_num}: {len(chapter_info['verses'])} verses")
    
    # Save to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    # Summary
    total_verses = sum(len(ch['verses']) for ch in all_data['chapters'])
    print("\n" + "=" * 50)
    print(f"✅ Download Complete!")
    print(f"📊 Total Chapters: {len(all_data['chapters'])}")
    print(f"📊 Total Verses: {total_verses}")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    
    return all_data

if __name__ == "__main__":
    download_gita()
