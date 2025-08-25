#!/usr/bin/env python3
"""
Test the new Weaviate cloud instance connection
"""
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

WEAVIATE_URL = "https://gulwpditiuiacghs9syg.c0.us-east1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "T2NmNEVDampTOUI2d0IrV19CbENuR0U0M0o3L3JmekR6RUNSTnJzazRoSHdzUzVPOWlxSGp4dURncXdzPV92MjAw"

def test_weaviate_connection():
    """Test connection to new Weaviate cloud instance"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WEAVIATE_API_KEY}"
    }
    
    # Test basic connection
    try:
        print("🔍 Testing Weaviate cloud connection...")
        response = requests.get(f"{WEAVIATE_URL}/v1/meta", headers=headers, timeout=10)
        
        if response.status_code == 200:
            meta = response.json()
            print("✅ Connection successful!")
            print(f"📊 Weaviate version: {meta.get('version', 'Unknown')}")
            print(f"🏠 Hostname: {meta.get('hostname', 'Unknown')}")
        else:
            print(f"❌ Connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # Test GraphQL endpoint
    try:
        print("\n🔍 Testing GraphQL endpoint...")
        
        # Simple schema query
        graphql_query = {
            "query": "{ Get { _Meta { count } } }"
        }
        
        response = requests.post(
            f"{WEAVIATE_URL}/v1/graphql",
            headers=headers,
            json=graphql_query,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ GraphQL endpoint working!")
            print(f"📈 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ GraphQL failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ GraphQL error: {e}")
    
    return True

if __name__ == "__main__":
    print("🚀 Testing new Weaviate cloud instance...")
    print(f"🔗 URL: {WEAVIATE_URL}")
    print()
    
    success = test_weaviate_connection()
    
    if success:
        print("\n🎉 New Weaviate instance is ready!")
        print("Alex can now connect to your cloud Weaviate database.")
    else:
        print("\n❌ Connection issues detected.")
        print("Please check your credentials and network connection.")
