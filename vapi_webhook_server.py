#!/usr/bin/env python3
"""
Vapi Webhook Server for Weaviate Knowledge Base Integration
This creates a webhook endpoint that Alex can call to search your Weaviate database
"""
from flask import Flask, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Weaviate configuration from your .env
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://gulwpditiuiacghs9syg.c0.us-east1.gcp.weaviate.cloud")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "T2NmNEVDampTOUI2d0IrV19CbENuR0U0M0o3L3JmekR6RUNSTnJzazRoSHdzUzVPOWlxSGp4dURncXdzPV92MjAw")

@app.route('/webhook/search-knowledge-base', methods=['POST'])
def search_knowledge_base():
    """Webhook endpoint for Alex to search the Weaviate knowledge base"""
    
    try:
        # Get the function call data from Vapi
        data = request.json
        
        # Extract the search query from the function parameters
        function_call = data.get('message', {}).get('functionCall', {})
        parameters = function_call.get('parameters', {})
        query = parameters.get('query', '')
        
        if not query:
            return jsonify({
                "result": "No search query provided. Please provide a query to search the knowledge base."
            })
        
        # Search Weaviate using GraphQL
        search_result = search_weaviate(query)
        
        if search_result:
            # Format the results for Alex
            response_text = format_search_results(search_result, query)
        else:
            response_text = f"I couldn't find any relevant information for '{query}' in the knowledge base."
        
        return jsonify({
            "result": response_text
        })
        
    except Exception as e:
        return jsonify({
            "result": f"Sorry, I encountered an error while searching the knowledge base: {str(e)}"
        })

def search_weaviate(query: str, limit: int = 5):
    """Search Weaviate database using GraphQL"""
    
    graphql_query = {
        "query": f"""
        {{
            Get {{
                Document(
                    nearText: {{
                        concepts: ["{query}"]
                    }}
                    limit: {limit}
                ) {{
                    title
                    content
                    source
                    _additional {{
                        score
                        id
                    }}
                }}
            }}
        }}
        """
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WEAVIATE_API_KEY}"
    }
    
    try:
        response = requests.post(
            f"{WEAVIATE_URL}v1/graphql",
            headers=headers,
            json=graphql_query,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('data', {}).get('Get', {}).get('Document', [])
        else:
            print(f"Weaviate query failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error querying Weaviate: {e}")
        return None

def format_search_results(results, query):
    """Format search results for Alex to present to the user"""
    
    if not results:
        return f"I couldn't find any information about '{query}' in the knowledge base."
    
    response = f"I found {len(results)} relevant document(s) about '{query}':\n\n"
    
    for i, doc in enumerate(results[:3], 1):  # Show top 3 results
        title = doc.get('title', 'Untitled Document')
        content = doc.get('content', '')
        source = doc.get('source', 'Unknown source')
        score = doc.get('_additional', {}).get('score', 0)
        
        # Truncate content to first 200 characters
        content_preview = content[:200] + "..." if len(content) > 200 else content
        
        response += f"{i}. **{title}**\n"
        response += f"   Source: {source}\n"
        response += f"   Content: {content_preview}\n"
        response += f"   Relevance: {score:.2f}\n\n"
    
    if len(results) > 3:
        response += f"...and {len(results) - 3} more documents found."
    
    return response

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "vapi-weaviate-webhook"})

if __name__ == '__main__':
    print("🚀 Starting Vapi-Weaviate Webhook Server...")
    print(f"📊 Weaviate URL: {WEAVIATE_URL}")
    print("🔗 Webhook endpoint: /webhook/search-knowledge-base")
    print("💡 Use ngrok to expose this server for Vapi integration")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
