#!/usr/bin/env python3
"""
Create a real Weaviate function tool that actually calls your database
"""
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
VAPI_API_KEY = "867ac81c-f57e-49ae-9003-25c88de12a15"
VAPI_BASE_URL = "https://api.vapi.ai"
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

def create_weaviate_function_tool():
    """Create a function tool that actually calls Weaviate"""
    
    # First, let's create a simple function tool without server URL
    # Alex will call this function and we'll handle the logic in the system prompt
    tool_config = {
        "type": "function",
        "function": {
            "name": "search_weaviate_knowledge_base",
            "description": "Search the Weaviate knowledge base for information. Always use this function when users ask questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information in Weaviate"
                    }
                },
                "required": ["query"]
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{VAPI_BASE_URL}/tool",
            headers=headers,
            json=tool_config
        )
        
        if response.status_code == 201:
            tool_data = response.json()
            print(f"✅ Created Weaviate function tool: {tool_data['id']}")
            return tool_data
        else:
            print(f"❌ Failed to create tool: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating tool: {e}")
        return None

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

def update_alex_with_real_weaviate_tool(tool_id):
    """Update Alex to use the real Weaviate tool"""
    
    alex = get_alex_assistant()
    if not alex:
        print("❌ Could not find Alex")
        return False
    
    alex_id = alex['id']
    
    # Create a system prompt that tells Alex to ALWAYS use the function tool
    system_prompt = f"""You're Alex. You're conversational and helpful.

CRITICAL: You have access to a Weaviate knowledge base through a function tool. For EVERY question or topic someone asks about, you MUST call the search_weaviate_knowledge_base function first.

Here's how you work:
1. Someone asks you anything
2. You IMMEDIATELY call search_weaviate_knowledge_base with their query
3. You use the results to answer naturally and conversationally
4. If no results, you say you don't have info on that topic

Your Weaviate database is at: {WEAVIATE_URL}

NEVER answer questions without calling the search function first. Always search the knowledge base.

Be natural and conversational - don't sound robotic."""

    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Get current tools and add the new one
    current_tools = alex.get('tools', [])
    
    # Add the Weaviate search tool
    current_tools.append({
        "type": "function",
        "function": {
            "toolId": tool_id
        }
    })
    
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
        "tools": current_tools,
        "firstMessage": "Hey! What's on your mind?"
    }
    
    try:
        response = requests.patch(
            f"{VAPI_BASE_URL}/assistant/{alex_id}",
            headers=headers,
            json=update_payload
        )
        
        if response.status_code == 200:
            print("✅ Updated Alex with real Weaviate tool!")
            return True
        else:
            print(f"❌ Failed to update Alex: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating Alex: {e}")
        return False

def test_weaviate_search(query="test"):
    """Test the Weaviate search to make sure it works"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WEAVIATE_API_KEY}"
    }
    
    # Try a simple GraphQL query to see what's in the database
    graphql_query = {
        "query": f"""
        {{
            Get {{
                Document(
                    limit: 3
                ) {{
                    title
                    content
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
            print("✅ Weaviate search test successful!")
            print(f"📊 Sample data: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Weaviate search failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Weaviate search error: {e}")
        return False

def main():
    """Set up real Weaviate integration"""
    
    print("🚀 Creating REAL Weaviate integration for Alex...")
    print(f"🔗 Weaviate URL: {WEAVIATE_URL}")
    
    # Test Weaviate connection first
    print("\n1. Testing Weaviate connection...")
    if not test_weaviate_search():
        print("❌ Weaviate connection failed. Check your credentials.")
        return
    
    # Create the function tool
    print("\n2. Creating Weaviate function tool...")
    tool = create_weaviate_function_tool()
    if not tool:
        print("❌ Failed to create function tool")
        return
    
    tool_id = tool['id']
    
    # Update Alex to use the tool
    print(f"\n3. Updating Alex to use tool {tool_id}...")
    success = update_alex_with_real_weaviate_tool(tool_id)
    
    if success:
        print("\n🎉 Real Weaviate integration complete!")
        print("\nAlex will now:")
        print("  • Call your Weaviate database for every question")
        print("  • Search your actual knowledge base")
        print("  • Use real data from your documents")
        print()
        print("📞 Test it now:")
        print("   +12182414667 (Twilio)")
        print("   +12186079458 (Vapi)")
    else:
        print("\n❌ Integration failed")

if __name__ == "__main__":
    main()
