#!/usr/bin/env python3
"""
VEDRISHI AI - RAG Pipeline with ChromaDB
Retrieval-Augmented Generation for verse accuracy
"""

import json
import chromadb
from pathlib import Path
from datetime import datetime
import hashlib

# Configuration
RAG_DIR = Path(__file__).parent.parent / "rag"
RAG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = RAG_DIR / "rag_log.txt"

def log(message):
    """Log message to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ===========================
# CHROMADB SETUP
# ===========================

def setup_chromadb():
    """Setup ChromaDB for verse storage"""
    log("Setting up ChromaDB...")
    
    # Create ChromaDB client
    client = chromadb.PersistentClient(path=str(RAG_DIR / "chroma_db"))
    
    # Create collection for verses
    collection = client.get_or_create_collection(
        name="vedrishi_verses",
        metadata={"description": "VedRishi AI - Sacred verses collection"}
    )
    
    log(f"ChromaDB setup complete: {RAG_DIR / 'chroma_db'}")
    return client, collection

# ===========================
# LOAD VERSES
# ===========================

def load_verses():
    """Load all verses from final dataset"""
    log("Loading verses from final dataset...")
    
    final_file = Path(__file__).parent.parent / "dataset" / "final" / "vedrishi_complete.jsonl"
    verses = []
    
    with open(final_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    
    log(f"Loaded {len(verses)} verses")
    return verses

# ===========================
# INDEX VERSES
# ===========================

def index_verses(collection, verses):
    """Index verses in ChromaDB"""
    log("Indexing verses in ChromaDB...")
    
    batch_size = 100
    total_indexed = 0
    
    for i in range(0, len(verses), batch_size):
        batch = verses[i:i + batch_size]
        
        ids = []
        documents = []
        metadatas = []
        
        for verse in batch:
            # Create unique ID
            verse_id = hashlib.md5(
                json.dumps(verse, sort_keys=True).encode()
            ).hexdigest()
            
            # Create document text
            doc_text = f"{verse.get('sanskrit', '')} {verse.get('hindi', '')} {verse.get('english', '')}"
            
            # Create metadata
            metadata = {
                'text_type': verse.get('text_type', ''),
                'reference': json.dumps(verse.get('reference', {})),
                'has_hindi': verse.get('has_hindi', False),
                'has_english': verse.get('has_english', False),
                'has_commentaries': verse.get('has_commentaries', False)
            }
            
            ids.append(verse_id)
            documents.append(doc_text)
            metadatas.append(metadata)
        
        # Add batch to collection
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        
        total_indexed += len(batch)
        log(f"  Indexed {total_indexed}/{len(verses)} verses")
    
    log(f"Total verses indexed: {total_indexed}")
    return total_indexed

# ===========================
# SEARCH VERSES
# ===========================

def search_verses(collection, query, n_results=5):
    """Search for relevant verses"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    return results

# ===========================
# RAG PIPELINE
# ===========================

def rag_query(collection, query):
    """Perform RAG query"""
    log(f"\nRAG Query: {query}")
    
    # Search for relevant verses
    results = search_verses(collection, query, n_results=3)
    
    # Extract relevant verses
    relevant_verses = []
    for i, doc in enumerate(results['documents'][0]):
        verse_data = {
            'text': doc,
            'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
            'distance': results['distances'][0][i] if results['distances'] else 0
        }
        relevant_verses.append(verse_data)
    
    # Generate response with context
    context = "\n\n".join([v['text'][:500] for v in relevant_verses])
    
    response = f"आपके प्रश्न के लिए प्रासंगिक श्लोक:\n\n{context}\n\n"
    response += "ये श्लोक भगवद गीता, रामायण और महाभारत से लिए गए हैं।"
    response += "\n\n[नोट: यह एक AI मार्गदर्शक है। यह किसी योग्य पंडित या गुरु की सलाह का विकल्प नहीं है।]"
    
    log(f"  Found {len(relevant_verses)} relevant verses")
    log(f"  Response length: {len(response)}")
    
    return response, relevant_verses

# ===========================
# MAIN
# ===========================

def main():
    """Main function"""
    log("VEDRISHI AI - RAG PIPELINE")
    log("=" * 60)
    
    # Setup ChromaDB
    client, collection = setup_chromadb()
    
    # Load verses
    verses = load_verses()
    
    # Index verses
    indexed_count = index_verses(collection, verses)
    
    # Test RAG query
    test_query = "गीता में कर्मयोग क्या है?"
    response, relevant_verses = rag_query(collection, test_query)
    
    log("\n" + "=" * 60)
    log("RAG PIPELINE SETUP COMPLETE")
    log("=" * 60)
    log(f"\nIndexed {indexed_count} verses")
    log(f"ChromaDB location: {RAG_DIR / 'chroma_db'}")
    log(f"\nTest Query: {test_query}")
    log(f"Response: {response[:200]}...")
    
    print("\n" + "=" * 60)
    print("RAG PIPELINE SETUP COMPLETE")
    print("=" * 60)
    print(f"\nIndexed {indexed_count} verses")
    print(f"ChromaDB location: {RAG_DIR / 'chroma_db'}")
    
    return {
        'indexed_count': indexed_count,
        'chromadb_path': str(RAG_DIR / 'chroma_db')
    }

if __name__ == "__main__":
    main()
