import requests
import json
import os

# Load the static registry of external agent URLs
with open("config/client_registry.json") as f:
    CLIENT_REGISTRY = json.load(f)

def call_external_agent(url, payload, timeout=5):
    """
    Calls an external MCP agent via HTTP POST and returns the JSON response.
    Returns None on failure (timeouts, HTTP errors, bad JSON, etc.).
    """
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[MCP WARNING] External call to {url} failed: {e}")
        return None

def transform_external_output(agent_type, output):
    """
    Maps external output to a consistent internal format based on agent type.
    This allows merging external data into our summarizer context.
    """
    transformed = {}
    
    if agent_type == "fraud":
        # Normalize fraud-related keys
        score = output.get("fraud_score") or output.get("score")
        flags = output.get("flags") or output.get("reasons")
        if score is not None:
            transformed["fraud_score"] = score
        if flags:
            transformed["fraud_flags"] = flags
    
    elif agent_type == "credit":
        # Normalize credit-related keys
        score = output.get("credit_score") or output.get("score")
        recommendation = output.get("recommendation") or output.get("summary")
        if score is not None:
            transformed["credit_score_external"] = score
        if recommendation:
            transformed["credit_recommendation_external"] = recommendation

    else:
        # Default: return output as-is
        transformed = output.copy()

    return transformed

def format_external_summary(agent_type, data):
    """
    Returns a short text snippet describing the external agent result,
    to be appended to the summary text seen by internal agents.
    """
    if agent_type == "fraud" and "fraud_score" in data:
        return f"External fraud model score = {data['fraud_score']}"
    if agent_type == "credit" and "credit_score_external" in data:
        return f"External credit model score = {data['credit_score_external']}"
    
    # Fallback: dump JSON string
    return json.dumps(data)
