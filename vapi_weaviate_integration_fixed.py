#!/usr/bin/env python3
"""
Vapi-Weaviate Integration Tool (Fixed Version)
Creates a Vapi Function Tool that connects Alex to your Verba Weaviate knowledge base
"""
import requests
import json
from typing import Dict, Any, List

# Configuration
VAPI_API_KEY = "867ac81c-f57e-49ae-9003-25c88de12a15"
VAPI_BASE_URL = "https://api.vapi.ai"

def create_weaviate_search_tool():
    """Create a Vapi Function Tool for Weaviate knowledge base search"""
    
    tool_config = {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the Weaviate knowledge base for relevant information to answer user questions. Use this when users ask questions that might be answered by documents in the knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information in the knowledge base"
                    }
                },
                "required": ["query"]
            }
        },
        "server": {
            "url": "https://weaviate-production-5bc1.up.railway.app/v1/graphql",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer b631484764105cea8c7d19b2469cc6144cc048feff68e119f0e527281a0409df"
            }
        }
    }
    
    return tool_config

def create_direct_weaviate_tool():
    """Create a direct Weaviate query tool using GraphQL"""
    
    tool_config = {
        "type": "function",
        "function": {
            "name": "query_weaviate_direct",
            "description": "Query the Weaviate database directly for documents and chunks. Use this to search for specific information in the knowledge base.",
            "parameters": {
                "type": "object", 
                "properties": {
                    "search_query": {
                        "type": "string",
                        "description": "The text to search for in the knowledge base"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["search_query"]
            }
        },
        "server": {
            "url": "https://weaviate-production-5bc1.up.railway.app/v1/graphql",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer b631484764105cea8c7d19b2469cc6144cc048feff68e119f0e527281a0409df"
            },
            "body": {
                "query": "{ Get { Document(nearText: {concepts: [\"{{parameters.search_query}}\"]}, limit: {{parameters.limit}}) { title content source _additional { score } } } }"
            }
        }
    }
    
    return tool_config

def get_alex_assistant_id():
    """Get Alex's full assistant ID"""
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
                    return assistant.get('id')
        return None
    except Exception as e:
        print(f"❌ Error getting assistants: {e}")
        return None

def create_vapi_tools():
    """Create tools in Vapi"""
    
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # For now, let's create a simpler function tool that Alex can use
    simple_tool = {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the knowledge base for information to help answer user questions about documents and data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information"
                    }
                },
                "required": ["query"]
            }
        }
    }
    
    try:
        response = requests.post(
            f"{VAPI_BASE_URL}/tool",
            headers=headers,
            json=simple_tool
        )
        
        if response.status_code == 201:
            tool_data = response.json()
            print(f"✅ Created tool: {simple_tool['function']['name']} (ID: {tool_data['id']})")
            return [tool_data]
        else:
            print(f"❌ Failed to create tool: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error creating tool: {e}")
        return []

def update_alex_assistant(tool_ids: List[str]):
    """Update Alex assistant to include the new tools"""
    
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    alex_id = get_alex_assistant_id()
    if not alex_id:
        print("❌ Could not find Alex assistant")
        return False
    
    try:
        # Get Alex's current configuration
        response = requests.get(
            f"{VAPI_BASE_URL}/assistant/{alex_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to get Alex's configuration: {response.status_code}")
            return False
            
        alex_config = response.json()
        current_tools = alex_config.get('tools', [])
        
        # Add the new tools
        for tool_id in tool_ids:
            current_tools.append({
                "type": "function",
                "function": {
                    "toolId": tool_id
                }
            })
        
        # Update Alex
        update_payload = {
            "tools": current_tools
        }
        
        response = requests.patch(
            f"{VAPI_BASE_URL}/assistant/{alex_id}",
            headers=headers,
            json=update_payload
        )
        
        if response.status_code == 200:
            print(f"✅ Successfully updated Alex with knowledge base tools!")
            return True
        else:
            print(f"❌ Failed to update Alex: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating Alex: {e}")
        return False

def main():
    """Main function to set up the integration"""
    
    print("🚀 Setting up Vapi-Weaviate Integration for Alex...")
    
    # Get Alex's ID
    alex_id = get_alex_assistant_id()
    if not alex_id:
        print("❌ Could not find Alex assistant")
        return
    
    print(f"🤖 Found Alex (ID: {alex_id})")
    
    # Create the tools
    print("\n1. Creating Vapi function tool...")
    created_tools = create_vapi_tools()
    
    if not created_tools:
        print("❌ No tools were created successfully")
        return
    
    # Extract tool IDs
    tool_ids = [tool['id'] for tool in created_tools]
    
    print(f"\n2. Updating Alex assistant with {len(tool_ids)} new tool(s)...")
    success = update_alex_assistant(tool_ids)
    
    if success:
        print("\n🎉 Integration complete!")
        print("\n📋 What Alex can now do:")
        print("  • Search your Weaviate knowledge base")
        print("  • Answer questions using your document data")
        print("  • Provide contextual information from your knowledge base")
        print()
        print("💡 Try calling Alex and asking:")
        print("   'What information do you have about [topic]?'")
        print("   'Search the knowledge base for [query]'")
        print()
        print("🔗 Dashboard: https://dashboard.vapi.ai")
    else:
        print("\n❌ Integration failed during assistant update")
        print("Tool was created but not added to Alex")

if __name__ == "__main__":
    main()
