#!/usr/bin/env python3
"""
Import Prairiewood data to Weaviate with correct API key
"""
import requests
import json
import os
from typing import Dict, Any, List
import time
from datetime import datetime

# Configuration
UNSTRUCTURED_API_URL = "https://api.unstructuredapp.io/general/v0/general"
UNSTRUCTURED_API_KEY = "wouLtcPhakuZxHqXGNaZatPlpWWHjY"
WEAVIATE_URL = "https://gulwpditiuiacghs9syg.c0.us-east1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "T2NmNEVDampTOUI2d0IrV19CbENuR0U0M0o3L3JmekR6RUNSTnJzazRoSHdzUzVPOWlxSGp4dURncXdzPV92MjAw"

def process_page_with_unstructured(page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process a single page through Unstructured API"""
    
    url = page_data.get('url', '')
    title = page_data.get('title', '')
    content = page_data.get('content', '')
    
    if not content.strip() or len(content) < 50:
        return []
    
    # Skip image files and other non-text content
    if any(ext in url.lower() for ext in ['.jpg', '.png', '.gif', '.pdf', '.css', '.js']):
        return []
    
    # Create document for processing
    doc_text = f"Title: {title}\nURL: {url}\n\nContent:\n{content}"
    
    headers = {
        "accept": "application/json",
        "unstructured-api-key": UNSTRUCTURED_API_KEY
    }
    
    files = {
        "files": (f"page_{hash(url)}.txt", doc_text, "text/plain")
    }
    
    data = {
        "strategy": "fast",
        "output_format": "application/json",
        "chunking_strategy": "by_title",
        "max_characters": 1000,
        "new_after_n_chars": 800
    }
    
    try:
        response = requests.post(
            UNSTRUCTURED_API_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            elements = response.json()
            
            # Add metadata to each element
            for element in elements:
                element['source_url'] = url
                element['source_title'] = title
                element['processed_at'] = datetime.now().isoformat()
            
            return elements
        else:
            print(f"⚠️  API error for {url}: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"⚠️  Error processing {url}: {e}")
        return []

def import_to_weaviate_simple(documents: List[Dict[str, Any]]) -> bool:
    """Import documents to Weaviate using simple REST API"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WEAVIATE_API_KEY}"
    }
    
    success_count = 0
    
    for doc in documents:
        # Use REST API instead of GraphQL
        weaviate_doc = {
            "class": "VERBA_DOCUMENTS",
            "properties": {
                "title": doc.get('title', ''),
                "text": doc.get('text', ''),
                "doc_name": doc.get('doc_name', ''),
                "doc_type": "webpage",
                "doc_link": doc.get('source_url', ''),
                "chunk_id": str(hash(doc.get('text', ''))),
                "chunk_index": 0,
                "type": doc.get('type', 'text'),
                "source": "Prairiewood Website"
            }
        }
        
        try:
            response = requests.post(
                f"{WEAVIATE_URL}/v1/objects",
                headers=headers,
                json=weaviate_doc,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                success_count += 1
            else:
                print(f"⚠️  Import failed: {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"⚠️  Error importing: {e}")
    
    print(f"✅ Imported {success_count}/{len(documents)} documents")
    return success_count > 0

def main():
    """Process and import Prairiewood data"""
    
    print("🚀 Importing Prairiewood to Weaviate")
    print("=" * 50)
    
    # Load crawl data
    prairiewood_file = "/Users/franksimpson/Desktop/prairiewood_direct_crawl_20250825_112947.json"
    
    try:
        with open(prairiewood_file, 'r') as f:
            data = json.load(f)
        pages = data.get('pages', [])
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return
    
    print(f"📄 Processing {len(pages)} pages...")
    
    all_documents = []
    processed_count = 0
    
    # Process first 20 pages as a test
    for i, page in enumerate(pages[:20]):
        url = page.get('url', f'page_{i}')
        print(f"🔄 {i+1}/20: {url}")
        
        # Process through Unstructured
        elements = process_page_with_unstructured(page)
        
        if elements:
            for element in elements:
                doc = {
                    'title': f"Prairiewood - {element.get('source_title', '')}",
                    'text': element.get('text', ''),
                    'doc_name': f"prairiewood_{hash(element.get('source_url', ''))}",
                    'source_url': element.get('source_url', ''),
                    'type': element.get('type', 'text')
                }
                all_documents.append(doc)
            
            processed_count += 1
            print(f"   ✅ {len(elements)} chunks")
        
        # Import in batches of 10
        if len(all_documents) >= 10:
            print(f"📤 Importing batch...")
            import_to_weaviate_simple(all_documents)
            all_documents = []
            time.sleep(1)
    
    # Import remaining
    if all_documents:
        print(f"📤 Final import...")
        import_to_weaviate_simple(all_documents)
    
    print(f"\n🎉 Complete! Processed {processed_count} pages")
    print(f"🤖 Alex now knows about Prairiewood!")

if __name__ == "__main__":
    main()
