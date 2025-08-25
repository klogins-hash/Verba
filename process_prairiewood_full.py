#!/usr/bin/env python3
"""
Process full Prairiewood crawl data through Unstructured API and import to Weaviate
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

def load_prairiewood_data():
    """Load the Prairiewood crawl data"""
    prairiewood_file = "/Users/franksimpson/Desktop/prairiewood_direct_crawl_20250825_112947.json"
    
    try:
        print("📂 Loading Prairiewood crawl data...")
        with open(prairiewood_file, 'r') as f:
            data = json.load(f)
        
        pages = data.get('pages', [])
        print(f"📄 Found {len(pages)} pages to process")
        return pages
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []

def process_page_with_unstructured(page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process a single page through Unstructured API"""
    
    url = page_data.get('url', '')
    title = page_data.get('title', '')
    content = page_data.get('content', '')
    
    if not content.strip():
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
        "strategy": "hi_res",
        "output_format": "application/json",
        "chunking_strategy": "by_title",
        "max_characters": 1500,
        "new_after_n_chars": 1200,
        "overlap": 100
    }
    
    try:
        response = requests.post(
            UNSTRUCTURED_API_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=60
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
            print(f"⚠️  Failed to process {url}: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"⚠️  Error processing {url}: {e}")
        return []

def create_weaviate_document(element: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Unstructured element to Weaviate document format"""
    
    text = element.get('text', '')
    element_type = element.get('type', 'unknown')
    source_url = element.get('source_url', '')
    source_title = element.get('source_title', '')
    
    return {
        "title": f"Prairiewood - {source_title}",
        "text": text,
        "doc_name": f"prairiewood_{hash(source_url)}_{element.get('element_id', '')}",
        "doc_type": "webpage",
        "doc_link": source_url,
        "chunk_id": element.get('element_id', ''),
        "chunk_index": 0,
        "type": element_type,
        "source": "Prairiewood Website"
    }

def import_to_weaviate(documents: List[Dict[str, Any]]) -> bool:
    """Import documents to Weaviate"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WEAVIATE_API_KEY}"
    }
    
    success_count = 0
    
    for doc in documents:
        # Create GraphQL mutation
        mutation = """
        mutation {
            Add(class: "VERBA_DOCUMENTS", object: {
                title: "%s"
                text: "%s"
                doc_name: "%s"
                doc_type: "%s"
                doc_link: "%s"
                chunk_id: "%s"
                chunk_index: %d
                type: "%s"
                source: "%s"
            }) {
                title
                _additional {
                    id
                }
            }
        }
        """ % (
            doc['title'].replace('"', '\\"'),
            doc['text'].replace('"', '\\"').replace('\n', '\\n'),
            doc['doc_name'],
            doc['doc_type'],
            doc['doc_link'],
            doc['chunk_id'],
            doc['chunk_index'],
            doc['type'],
            doc['source']
        )
        
        try:
            response = requests.post(
                f"{WEAVIATE_URL}/v1/graphql",
                headers=headers,
                json={"query": mutation},
                timeout=30
            )
            
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"⚠️  Failed to import document: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️  Error importing document: {e}")
    
    print(f"✅ Imported {success_count}/{len(documents)} documents to Weaviate")
    return success_count > 0

def main():
    """Process full Prairiewood dataset"""
    
    print("🚀 Processing Full Prairiewood Dataset")
    print("=" * 60)
    
    # Load data
    pages = load_prairiewood_data()
    if not pages:
        print("❌ No pages to process")
        return
    
    all_documents = []
    processed_count = 0
    
    print(f"\n📊 Processing {len(pages)} pages through Unstructured API...")
    
    for i, page in enumerate(pages):
        url = page.get('url', f'page_{i}')
        print(f"🔄 Processing {i+1}/{len(pages)}: {url}")
        
        # Process through Unstructured
        elements = process_page_with_unstructured(page)
        
        if elements:
            # Convert to Weaviate format
            for element in elements:
                doc = create_weaviate_document(element)
                all_documents.append(doc)
            
            processed_count += 1
            print(f"   ✅ Generated {len(elements)} chunks")
        else:
            print(f"   ⚠️  No content extracted")
        
        # Rate limiting - be nice to the API
        time.sleep(1)
        
        # Process in batches to avoid memory issues
        if len(all_documents) >= 50:
            print(f"\n📤 Importing batch of {len(all_documents)} documents...")
            import_to_weaviate(all_documents)
            all_documents = []
    
    # Import remaining documents
    if all_documents:
        print(f"\n📤 Importing final batch of {len(all_documents)} documents...")
        import_to_weaviate(all_documents)
    
    print(f"\n🎉 Processing Complete!")
    print(f"📊 Processed {processed_count}/{len(pages)} pages")
    print(f"🗄️  Prairiewood knowledge now available in Weaviate")
    print(f"🤖 Alex can now answer questions about Prairiewood!")

if __name__ == "__main__":
    main()
