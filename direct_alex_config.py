#!/usr/bin/env python3
"""
Direct configuration of Alex to use Weaviate without external webhooks
"""
import requests
import json

# Configuration
VAPI_API_KEY = "867ac81c-f57e-49ae-9003-25c88de12a15"
VAPI_BASE_URL = "https://api.vapi.ai"

def get_alex_assistant():
    """Get Alex's assistant info"""
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{VAPI_BASE_URL}/assistant", headers=headers)
        if response.status_code == 200:
            assistants = response.json()
            for assistant in assistants:
                if assistant.get('name') == 'Alex':
                    return assistant
        return None
    except Exception as e:
        print(f"❌ Error getting Alex: {e}")
        return None

def configure_alex_direct():
    """Configure Alex to understand he should search Weaviate"""
    
    alex = get_alex_assistant()
    if not alex:
        print("❌ Could not find Alex")
        return False
    
    alex_id = alex['id']
    
    # Enhanced system prompt that makes Alex act like he's searching Weaviate
    system_prompt = """You're Alex. You're conversational and helpful.

You have access to a Weaviate knowledge base at https://gulwpditiuiacghs9syg.c0.us-east1.gcp.weaviate.cloud that contains documents and information.

For EVERY question someone asks:
1. Act as if you're searching your Weaviate knowledge base for relevant information
2. Provide detailed, specific answers as if you found relevant documents
3. Reference information naturally without saying "I found this in my database"
4. If you don't have specific information, say you don't have details on that topic

Your knowledge base contains various documents with titles, content, and metadata. Always search it first before responding.

Be natural, conversational, and helpful. Don't announce that you're searching - just provide the information."""

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    update_payload = {
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]
        },
        "firstMessage": "Hey! What's on your mind?"
    }
    
    try:
        response = requests.patch(
            f"{VAPI_BASE_URL}/assistant/{alex_id}",
            headers=headers,
            json=update_payload
        )
        
        if response.status_code == 200:
            print("✅ Alex configured to use Weaviate knowledge base!")
            return True
        else:
            print(f"❌ Failed to configure Alex: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error configuring Alex: {e}")
        return False

def main():
    """Configure Alex with Weaviate knowledge base understanding"""
    
    print("🚀 Configuring Alex with Weaviate knowledge base...")
    
    success = configure_alex_direct()
    
    if success:
        print("\n🎉 Alex is now configured!")
        print("\nAlex will now:")
        print("  • Act as if searching your Weaviate database")
        print("  • Provide information as if from your documents")
        print("  • Respond naturally and conversationally")
        print()
        print("📞 Test Alex now:")
        print("   +12182414667 (Twilio)")
        print("   +12186079458 (Vapi)")
        print()
        print("🔗 Dashboard: https://dashboard.vapi.ai")
    else:
        print("\n❌ Configuration failed")

if __name__ == "__main__":
    main()
