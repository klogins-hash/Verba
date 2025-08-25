#!/usr/bin/env python3
"""
Test Unstructured API with Prairiewood crawl data
"""
import requests
import json
import os
from typing import Dict, Any

# Unstructured API configuration
UNSTRUCTURED_API_URL = "https://api.unstructuredapp.io/general/v0/general"
UNSTRUCTURED_API_KEY = "wouLtcPhakuZxHqXGNaZatPlpWWHjY"

def test_unstructured_api():
    """Test basic connectivity to Unstructured API"""
    
    # Simple test with a small text sample
    test_text = "This is a test document to verify Unstructured API connectivity."
    
    headers = {
        "accept": "application/json",
        "unstructured-api-key": UNSTRUCTURED_API_KEY
    }
    
    # Test with text input
    files = {
        "files": ("test.txt", test_text, "text/plain")
    }
    
    data = {
        "strategy": "fast",
        "output_format": "application/json"
    }
    
    try:
        print("🧪 Testing Unstructured API connectivity...")
        response = requests.post(
            UNSTRUCTURED_API_URL,
            headers=headers,
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Unstructured API test successful!")
            print(f"📄 Processed {len(result)} elements")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def process_prairiewood_sample():
    """Process a small sample from Prairiewood data"""
    
    prairiewood_file = "/Users/franksimpson/Desktop/prairiewood_direct_crawl_20250825_112947.json"
    
    try:
        # Read just the first page from the crawl
        with open(prairiewood_file, 'r') as f:
            data = json.load(f)
        
        if 'pages' in data and len(data['pages']) > 0:
            first_page = data['pages'][0]
            content = first_page.get('content', '')
            title = first_page.get('title', '')
            url = first_page.get('url', '')
            
            # Create a sample document
            sample_doc = f"Title: {title}\nURL: {url}\n\nContent:\n{content[:2000]}..."  # First 2000 chars
            
            print(f"📝 Processing sample from: {url}")
            
            headers = {
                "accept": "application/json",
                "unstructured-api-key": UNSTRUCTURED_API_KEY
            }
            
            files = {
                "files": ("prairiewood_sample.txt", sample_doc, "text/plain")
            }
            
            data_payload = {
                "strategy": "hi_res",
                "output_format": "application/json",
                "chunking_strategy": "by_title"
            }
            
            response = requests.post(
                UNSTRUCTURED_API_URL,
                headers=headers,
                files=files,
                data=data_payload
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Processed Prairiewood sample!")
                print(f"📊 Generated {len(result)} structured elements")
                
                # Show sample of processed elements
                for i, element in enumerate(result[:3]):
                    print(f"\n🔸 Element {i+1}:")
                    print(f"   Type: {element.get('type', 'unknown')}")
                    print(f"   Text: {element.get('text', '')[:100]}...")
                
                return result
            else:
                print(f"❌ Processing failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
    except Exception as e:
        print(f"❌ Error processing sample: {e}")
        return None

def main():
    """Test Unstructured API with Prairiewood data"""
    
    print("🚀 Testing Unstructured API Account")
    print("=" * 50)
    
    # Test basic connectivity
    if test_unstructured_api():
        print("\n" + "=" * 50)
        print("🏨 Processing Prairiewood Sample")
        
        # Process sample from Prairiewood
        result = process_prairiewood_sample()
        
        if result:
            print(f"\n🎉 Success! Your Unstructured API account is working.")
            print(f"📈 Ready to process the full Prairiewood dataset.")
            print(f"💡 Next: Process all pages and import to Weaviate")
        else:
            print(f"\n❌ Sample processing failed")
    else:
        print(f"\n❌ API connectivity test failed")

if __name__ == "__main__":
    main()
