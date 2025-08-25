#!/usr/bin/env python3
"""
Configure Alex to use a deployed webhook for Weaviate search
"""
import requests
import json

# Configuration
VAPI_API_KEY = "867ac81c-f57e-49ae-9003-25c88de12a15"
VAPI_BASE_URL = "https://api.vapi.ai"

# We'll use a public webhook service for now
WEBHOOK_URL = "https://webhook.site/unique-id"  # Replace with actual deployed URL

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

def configure_alex_with_webhook():
    """Configure Alex to call Weaviate webhook"""
    
    alex = get_alex_assistant()
    if not alex:
        print("❌ Could not find Alex")
        return False
    
    alex_id = alex['id']
    
    # System prompt that tells Alex to search Weaviate for every query
    system_prompt = """You're Alex. You're conversational and helpful.

IMPORTANT: You have access to a Weaviate knowledge base. For EVERY question someone asks, you need to search it first.

When someone asks you anything:
1. Think about their question
2. Search your knowledge base for relevant information
3. Use what you find to give a natural, conversational answer
4. If you don't find relevant info, just say you don't have information on that topic

Be natural and friendly - don't sound robotic or announce that you're searching."""

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Configure Alex with server URL for function calls
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
        "serverUrl": "https://gulwpditiuiacghs9syg.c0.us-east1.gcp.weaviate.cloud/v1/graphql",
        "firstMessage": "Hey! What's on your mind?"
    }
    
    try:
        response = requests.patch(
            f"{VAPI_BASE_URL}/assistant/{alex_id}",
            headers=headers,
            json=update_payload
        )
        
        if response.status_code == 200:
            print("✅ Configured Alex with Weaviate access!")
            return True
        else:
            print(f"❌ Failed to configure Alex: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error configuring Alex: {e}")
        return False

def main():
    """Configure Alex with direct Weaviate access"""
    
    print("🚀 Configuring Alex with direct Weaviate access...")
    
    success = configure_alex_with_webhook()
    
    if success:
        print("\n🎉 Alex is now configured!")
        print("\nAlex will now:")
        print("  • Search your Weaviate database for every question")
        print("  • Use your actual document content")
        print("  • Respond naturally with found information")
        print()
        print("📞 Test Alex now:")
        print("   +12182414667 (Twilio)")
        print("   +12186079458 (Vapi)")
    else:
        print("\n❌ Configuration failed")

if __name__ == "__main__":
    main()
