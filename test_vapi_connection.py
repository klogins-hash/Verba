#!/usr/bin/env python3
"""
Test script to verify Vapi API connection
"""
import requests
import json

# Your Vapi API key
API_KEY = "867ac81c-f57e-49ae-9003-25c88de12a15"
BASE_URL = "https://api.vapi.ai"

def test_vapi_connection():
    """Test the Vapi API connection by listing assistants"""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test connection by listing assistants
        print("🔍 Testing Vapi API connection...")
        response = requests.get(f"{BASE_URL}/assistant", headers=headers)
        
        if response.status_code == 200:
            print("✅ Connection successful!")
            assistants = response.json()
            print(f"📋 Found {len(assistants)} assistant(s) in your account")
            
            if assistants:
                print("\n🤖 Your assistants:")
                for i, assistant in enumerate(assistants[:5], 1):  # Show first 5
                    name = assistant.get('name', 'Unnamed')
                    id = assistant.get('id', 'No ID')
                    created = assistant.get('createdAt', 'Unknown')
                    print(f"  {i}. {name} (ID: {id[:8]}...)")
            else:
                print("   No assistants found. You can create one!")
                
        elif response.status_code == 401:
            print("❌ Authentication failed - Invalid API key")
            return False
        else:
            print(f"❌ Connection failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    
    # Test phone numbers endpoint
    try:
        print("\n📞 Checking phone numbers...")
        response = requests.get(f"{BASE_URL}/phone-number", headers=headers)
        
        if response.status_code == 200:
            phone_numbers = response.json()
            print(f"📱 Found {len(phone_numbers)} phone number(s)")
            
            if phone_numbers:
                print("\n📞 Your phone numbers:")
                for i, phone in enumerate(phone_numbers[:3], 1):  # Show first 3
                    number = phone.get('number', 'Unknown')
                    provider = phone.get('provider', 'Unknown')
                    print(f"  {i}. {number} ({provider})")
        else:
            print(f"⚠️  Could not fetch phone numbers (status: {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not fetch phone numbers: {e}")
    
    return True

if __name__ == "__main__":
    success = test_vapi_connection()
    
    if success:
        print("\n🎉 Vapi connection is working!")
        print("You can now:")
        print("  • Create voice assistants")
        print("  • Make/receive phone calls")
        print("  • Build voice workflows")
        print("\n🔗 Dashboard: https://dashboard.vapi.ai")
    else:
        print("\n❌ Connection failed. Please check your API key.")
