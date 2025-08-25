#!/usr/bin/env python3
"""
Working webhook that searches your actual Weaviate documents
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
def search_documents():
    """Search VERBA_DOCUMENTS for actual content"""
    
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "No query provided"})
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WEAVIATE_API_KEY}"
        }
        
        # Search documents with actual content
        graphql_query = {
            "query": f"""
            {{
                Get {{
                    VERBA_DOCUMENTS(
                        limit: 5
                        where: {{
                            operator: Like
                            path: ["text"]
                            valueText: "*{query}*"
                        }}
                    ) {{
                        text
                        doc_name
                        doc_type
                        doc_uuid
                        chunk_count
                        _additional {{
                            id
                            score
                        }}
                    }}
                }}
            }}
            """
        }
        
        response = requests.post(
            f"{WEAVIATE_URL}/v1/graphql",
            headers=headers,
            json=graphql_query,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if 'errors' in result:
                # Try a simpler query if the complex one fails
                simple_query = {
                    "query": f"""
                    {{
                        Get {{
                            VERBA_DOCUMENTS(limit: 3) {{
                                text
                                doc_name
                                doc_type
                                _additional {{
                                    id
                                }}
                            }}
                        }}
                    }}
                    """
                }
                
                response = requests.post(
                    f"{WEAVIATE_URL}/v1/graphql",
                    headers=headers,
                    json=simple_query,
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                
            documents = result.get('data', {}).get('Get', {}).get('VERBA_DOCUMENTS', [])
            
            if documents:
                formatted_results = []
                for doc in documents:
                    text = doc.get('text', 'No content')[:300] + "..." if len(doc.get('text', '')) > 300 else doc.get('text', 'No content')
                    formatted_results.append({
                        "name": doc.get('doc_name', 'Unknown'),
                        "type": doc.get('doc_type', 'Unknown'),
                        "content": text,
                        "relevance": doc.get('_additional', {}).get('score', 'N/A')
                    })
                
                return jsonify({
                    "query": query,
                    "found": len(documents),
                    "results": formatted_results,
                    "status": "success"
                })
            else:
                return jsonify({
                    "query": query,
                    "found": 0,
                    "results": "No documents found matching your query.",
                    "status": "success"
                })
                
        else:
            return jsonify({
                "query": query,
                "results": f"Search failed: {response.status_code} - {response.text}",
                "status": "error"
            })
            
    except Exception as e:
        return jsonify({
            "query": query if 'query' in locals() else "unknown",
            "results": f"Error: {str(e)}",
            "status": "error"
        })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "weaviate": WEAVIATE_URL})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    print("🚀 Starting working Weaviate webhook...")
    print(f"🔗 Weaviate: {WEAVIATE_URL}")
    print("📡 Endpoint: /search")
    app.run(host='0.0.0.0', port=port, debug=False)
