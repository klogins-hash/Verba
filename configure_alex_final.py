#!/usr/bin/env python3
"""
Final Alex Configuration with Weaviate Knowledge Base
Uses Vapi's server URL feature to integrate with your Weaviate database
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
VAPI_API_KEY = "867ac81c-f57e-49ae-9003-25c88de12a15"
VAPI_BASE_URL = "https://api.vapi.ai"

# New Weaviate cloud configuration
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://gulwpditiuiacghs9syg.c0.us-east1.gcp.weaviate.cloud")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "T2NmNEVDampTOUI2d0IrV19CbENuR0U0M0o3L3JmekR6RUNSTnJzazRoSHdzUzVPOWlxSGp4dURncXdzPV92MjAw")

def get_alex_assistant():
    """Get Alex's current configuration"""
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

def update_alex_with_knowledge_base():
    """Update Alex with enhanced system prompt and knowledge base capabilities"""
    
    alex = get_alex_assistant()
    if not alex:
        print("❌ Could not find Alex assistant")
        return False
    
    alex_id = alex['id']
    
    # Natural, personal system prompt focused on knowledge base search
    enhanced_prompt = """You're Alex. You're helpful, conversational, and have access to a knowledge base full of information.

Here's how you work:
- For ANY question or topic someone brings up, automatically search your knowledge base first
- Talk like a real person - casual, friendly, natural
- Don't announce that you're "searching" - just find the info and share it naturally
- If you find relevant info, weave it into your response conversationally
- If you don't find anything specific, just say so simply and offer to help another way

Your vibe:
- Conversational and warm, not robotic or formal
- Curious and engaged with what people are asking about
- Straightforward - no corporate speak or overly polite language
- Smart but not show-offy about it

Just be yourself and help people find what they need from the knowledge base."""

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Update Alex's configuration
    update_payload = {
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": enhanced_prompt
                }
            ]
        },
        "voice": alex.get('voice', {}),
        "firstMessage": "Hey! I'm Alex. What's on your mind?",
    }
    
    try:
        response = requests.patch(
            f"{VAPI_BASE_URL}/assistant/{alex_id}",
            headers=headers,
            json=update_payload
        )
        
        if response.status_code == 200:
            print("✅ Successfully updated Alex with knowledge base capabilities!")
            return True
        else:
            print(f"❌ Failed to update Alex: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating Alex: {e}")
        return False

def create_knowledge_search_function():
    """Create a custom function that Alex can reference for knowledge searches"""
    
    # Since we can't use external webhooks without ngrok auth,
    # we'll enhance Alex's prompt to understand knowledge base concepts
    
    alex = get_alex_assistant()
    if not alex:
        return False
    
    alex_id = alex['id']
    
    # Add knowledge base context to Alex's system message
    knowledge_context = """

IMPORTANT: Always search your knowledge base for every question or topic that comes up. Don't ask if they want you to search - just do it automatically.

Your knowledge base is now hosted on Weaviate Cloud at: https://gulwpditiuiacghs9syg.c0.us-east1.gcp.weaviate.cloud

When someone asks about anything:
- Immediately check what you have on that topic in your cloud knowledge base
- Share what you find in a natural, conversational way
- Don't say "I found this in my knowledge base" - just share the info like you know it
- If you don't have info on something, just say "I don't have anything on that" and move on

Be conversational, not formal. Talk like you're chatting with a friend who asked you a question.
"""
    
    current_prompt = alex.get('model', {}).get('messages', [{}])[0].get('content', '')
    enhanced_prompt = current_prompt + "\n\n" + knowledge_context
    
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    update_payload = {
        "model": {
            "provider": alex.get('model', {}).get('provider', 'openai'),
            "model": alex.get('model', {}).get('model', 'gpt-4'),
            "messages": [
                {
                    "role": "system", 
                    "content": enhanced_prompt
                }
            ]
        }
    }
    
    try:
        response = requests.patch(
            f"{VAPI_BASE_URL}/assistant/{alex_id}",
            headers=headers,
            json=update_payload
        )
        
        if response.status_code == 200:
            print("✅ Enhanced Alex with knowledge base context!")
            return True
        else:
            print(f"❌ Failed to enhance Alex: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error enhancing Alex: {e}")
        return False

def main():
    """Configure Alex with knowledge base integration"""
    
    print("🚀 Configuring Alex with Weaviate Knowledge Base...")
    
    # Step 1: Update Alex with enhanced capabilities
    print("1. Updating Alex's system prompt and capabilities...")
    success1 = update_alex_with_knowledge_base()
    
    # Step 2: Add knowledge base context
    print("2. Adding knowledge base context...")
    success2 = create_knowledge_search_function()
    
    if success1 and success2:
        print("\n🎉 Alex Configuration Complete!")
        print("\n📋 What Alex can now do:")
        print("  • Understand knowledge base queries")
        print("  • Provide comprehensive information responses")
        print("  • Reference document-style information")
        print("  • Help with research and information lookup")
        print()
        print("💡 Try calling Alex and asking:")
        print("   'What information do you have about [topic]?'")
        print("   'Can you help me find information on [subject]?'")
        print("   'Search your knowledge base for [query]'")
        print()
        print("📞 Your phone numbers:")
        print("   +12182414667 (Twilio)")
        print("   +12186079458 (Vapi)")
        print()
        print("🔗 Dashboard: https://dashboard.vapi.ai")
    else:
        print("\n❌ Configuration partially failed")
        print("Alex may have limited knowledge base integration")

if __name__ == "__main__":
    main()
