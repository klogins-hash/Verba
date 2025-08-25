#!/usr/bin/env python3
"""
Vapi-Weaviate Integration Tool
Creates a Vapi Function Tool that connects Alex to your Verba Weaviate knowledge base
"""
import requests
import json
from typing import Dict, Any, List

# Configuration
VAPI_API_KEY = "867ac81c-f57e-49ae-9003-25c88de12a15"
VAPI_BASE_URL = "https://api.vapi.ai"
ALEX_ASSISTANT_ID = "6cfeaaa0-8b5a-4f8e-9c3d-2a1b4c5d6e7f"  # Your Alex assistant ID (full ID)

# Your Verba API configuration (using your Railway deployment)
VERBA_BASE_URL = "http://localhost:8000"  # Local Verba API
VERBA_CREDENTIALS = {
    "url": "https://weaviate-production-5bc1.up.railway.app/",
    "api_key": "b631484764105cea8c7d19b2469cc6144cc048feff68e119f0e527281a0409df",
}

def create_weaviate_search_tool():
    """Create a Vapi Function Tool for Weaviate knowledge base search"""
    
    tool_config = {
        "type": "function",
        "name": "search_knowledge_base",
        "description": "Search the Weaviate knowledge base for relevant information to answer user questions. Use this when users ask questions that might be answered by documents in the knowledge base.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant information in the knowledge base"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        },
        "server": {
            "url": f"{VERBA_BASE_URL}/api/query",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {
                "query": "{{parameters.query}}",
                "credentials": VERBA_CREDENTIALS,
                "RAG": {
                    "chunker": "WordChunker",
                    "embedder": "OpenAIEmbedder",
                    "retriever": "WindowRetriever",
                    "generator": "OpenAIGenerator"
                },
                "labels": [],
                "documentFilter": []
            }
        }
    }
    
    return tool_config

def create_document_search_tool():
    """Create a tool to search for specific documents"""
    
    tool_config = {
        "type": "function", 
        "name": "search_documents",
        "description": "Search for specific documents in the knowledge base by title or content",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find documents by title or content"
                },
                "page_size": {
                    "type": "integer",
                    "description": "Number of documents to return (default: 10)",
                    "default": 10
                }
            },
            "required": ["query"]
        },
        "server": {
            "url": f"{VERBA_BASE_URL}/api/get_all_documents",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {
                "query": "{{parameters.query}}",
                "credentials": VERBA_CREDENTIALS,
                "pageSize": "{{parameters.page_size}}",
                "page": 1,
                "labels": []
            }
        }
    }
    
    return tool_config

def create_vapi_tools():
    """Create both tools in Vapi"""
    
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    tools = [
        create_weaviate_search_tool(),
        create_document_search_tool()
    ]
    
    created_tools = []
    
    for tool in tools:
        try:
            response = requests.post(
                f"{VAPI_BASE_URL}/tool",
                headers=headers,
                json=tool
            )
            
            if response.status_code == 201:
                tool_data = response.json()
                created_tools.append(tool_data)
                print(f"✅ Created tool: {tool['name']} (ID: {tool_data['id']})")
            else:
                print(f"❌ Failed to create tool {tool['name']}: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error creating tool {tool['name']}: {e}")
    
    return created_tools

def update_alex_assistant(tool_ids: List[str]):
    """Update Alex assistant to include the new tools"""
    
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # First, get Alex's current configuration
    try:
        response = requests.get(
            f"{VAPI_BASE_URL}/assistant/{ALEX_ASSISTANT_ID}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to get Alex's configuration: {response.status_code}")
            return False
            
        alex_config = response.json()
        
        # Add the new tools to Alex's configuration
        current_tools = alex_config.get('tools', [])
        
        # Add tool references
        for tool_id in tool_ids:
            current_tools.append({"type": "function", "function": {"toolId": tool_id}})
        
        # Update Alex's configuration
        update_payload = {
            "tools": current_tools
        }
        
        response = requests.patch(
            f"{VAPI_BASE_URL}/assistant/{ALEX_ASSISTANT_ID}",
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

def main():
    """Main function to set up the integration"""
    
    print("🚀 Setting up Vapi-Weaviate Integration for Alex...")
    print(f"📊 Verba API: {VERBA_BASE_URL}")
    
    # Get Alex's correct ID
    print("0. Getting Alex's assistant ID...")
    alex_id = get_alex_assistant_id()
    if not alex_id:
        print("❌ Could not find Alex assistant")
        return
    
    global ALEX_ASSISTANT_ID
    ALEX_ASSISTANT_ID = alex_id
    print(f"🤖 Assistant: Alex (ID: {ALEX_ASSISTANT_ID})")
    print()
    
    # Create the tools
    print("1. Creating Vapi tools...")
    created_tools = create_vapi_tools()
    
    if not created_tools:
        print("❌ No tools were created successfully")
        return
    
    # Extract tool IDs
    tool_ids = [tool['id'] for tool in created_tools]
    
    print(f"\n2. Updating Alex assistant with {len(tool_ids)} new tools...")
    success = update_alex_assistant(tool_ids)
    
    if success:
        print("\n🎉 Integration complete!")
        print("\n📋 What Alex can now do:")
        print("  • Search your Weaviate knowledge base")
        print("  • Find specific documents")
        print("  • Answer questions using your data")
        print("  • Provide contextual information from your documents")
        print()
        print("💡 Try asking Alex questions about your documents!")
        print("   Example: 'What information do you have about [topic]?'")
    else:
        print("\n❌ Integration failed during assistant update")
        print("Tools were created but not added to Alex")
        print("You can manually add them in the Vapi dashboard")

if __name__ == "__main__":
    main()
