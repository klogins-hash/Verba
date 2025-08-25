#!/usr/bin/env python3
"""
Check what's actually in your Weaviate database
"""
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

def check_schema():
    """Check what classes exist in Weaviate"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WEAVIATE_API_KEY}"
    }
    
    try:
        # Get schema
        response = requests.get(f"{WEAVIATE_URL}/v1/schema", headers=headers)
        
        if response.status_code == 200:
            schema = response.json()
            print("✅ Schema retrieved!")
            print(f"📊 Classes found: {json.dumps(schema, indent=2)}")
            
            # Extract class names
            classes = [cls['class'] for cls in schema.get('classes', [])]
            print(f"\n📋 Available classes: {classes}")
            return classes
        else:
            print(f"❌ Schema request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        return []

def test_search_with_classes(classes):
    """Test search with actual classes"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WEAVIATE_API_KEY}"
    }
    
    for class_name in classes:
        print(f"\n🔍 Testing class: {class_name}")
        
        # Try to get some objects from this class
        graphql_query = {
            "query": f"""
            {{
                Get {{
                    {class_name}(limit: 2) {{
                        _additional {{
                            id
                        }}
                    }}
                }}
            }}
            """
        }
        
        try:
            response = requests.post(
                f"{WEAVIATE_URL}/v1/graphql",
                headers=headers,
                json=graphql_query,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'errors' not in result:
                    print(f"✅ {class_name} works!")
                    print(f"📊 Sample: {json.dumps(result, indent=2)}")
                else:
                    print(f"❌ {class_name} has errors: {result['errors']}")
            else:
                print(f"❌ {class_name} request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing {class_name}: {e}")

if __name__ == "__main__":
    print("🔍 Checking your Weaviate database schema...")
    print(f"🔗 URL: {WEAVIATE_URL}")
    
    classes = check_schema()
    
    if classes:
        test_search_with_classes(classes)
    else:
        print("❌ No classes found or schema check failed")
