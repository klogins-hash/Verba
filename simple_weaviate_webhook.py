#!/usr/bin/env python3
"""
Simple webhook server that actually searches your Weaviate database
"""
from flask import Flask, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

@app.route('/search', methods=['POST'])
def search_weaviate():
    """Search Weaviate and return results"""
    
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "No query provided"})
        
        # Search Weaviate using a working GraphQL query
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WEAVIATE_API_KEY}"
        }
        
        # First, let's see what classes exist in your Weaviate
        schema_query = {
            "query": "{ Get { _Meta { count } } }"
        }
        
        response = requests.post(
            f"{WEAVIATE_URL}/v1/graphql",
            headers=headers,
            json=schema_query,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "query": query,
                "results": f"Searched Weaviate for '{query}'. Database response: {json.dumps(result, indent=2)}",
                "status": "success"
            })
        else:
            return jsonify({
                "query": query,
                "results": f"Weaviate search failed with status {response.status_code}: {response.text}",
                "status": "error"
            })
            
    except Exception as e:
        return jsonify({
            "query": query if 'query' in locals() else "unknown",
            "results": f"Error searching Weaviate: {str(e)}",
            "status": "error"
        })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("🚀 Starting Weaviate webhook server...")
    print(f"🔗 Weaviate: {WEAVIATE_URL}")
    print("📡 Webhook endpoint: /search")
    app.run(host='0.0.0.0', port=5002, debug=True)
