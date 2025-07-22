# =====================================
# Azure Cognitive Search — Vector Query Example
# =====================================
# This script performs a semantic search query using a sentence embedding
# vector and Azure AI Search's vector index API.

import requests
import json
from sentence_transformers import SentenceTransformer

# =====================================
# Configuration Parameters
# =====================================

# Azure Search endpoint (change only the subdomain if deploying elsewhere)
endpoint = "https://bureau-agent.search.windows.net"

# The name of the vector index deployed in Azure Cognitive Search
index_name = "bureau-vector-index"

# Azure Search API Key (⚠️ In production, move to environment variables)
api_key = "ChGGOA90c0DUSuFp3VQFqIuh2hUrTAODxez4oubIp6AzSeDcQrf8"

# Your query/question to be semantically matched
query_text = "What are the total assets and liabilities for the company?"

# =====================================
# Generate Query Vector using SentenceTransformer
# =====================================

# Load a pretrained transformer model for sentence embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert query to vector format compatible with Azure vector search
query_vector = model.encode(query_text).tolist()

# =====================================
# Construct Azure Search Request
# =====================================

# API endpoint for search requests (2023-07-01-preview supports vector search)
url = f"{endpoint}/indexes/{index_name}/docs/search?api-version=2023-07-01-preview"

# Required headers for the API call
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Search body includes vector query + fallback text search
payload = {
    "search": query_text,  # Fallback keyword search if needed
    "vector": {
        "value": query_vector,
        "fields": "content_vector",  # Field containing stored document vectors
        "k": 3                       # Return top 3 results
    },
    "top": 3  # Top 3 documents (combined with vector + text relevance)
}

# =====================================
# Send the Search Request
# =====================================

response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()  # Raise error if request failed
results = response.json()

# =====================================
# Display Top Results
# =====================================

print("\n🔎 Top Results:\n")
for doc in results.get("value", []):
    print(f"Filename: {doc.get('filename')}")
    print(f"Score: {doc.get('@search.score'):.4f}")
    print(f"Snippet: {doc.get('content', '')[:300].strip()}...")
    print("-" * 60)
