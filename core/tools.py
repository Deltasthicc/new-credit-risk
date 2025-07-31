# =====================================
# Importing Core Pipelines
# =====================================

# Importing the main pipeline functions from each AI agent module
import os  # For file path operations
import requests  # For making HTTP requests to external agents
from .credit_pipeline import credit_scoring_pipeline  # Generates credit risk score and limit recommendation
from core.fraud_pipeline import fraud_detection_pipeline  # Detects potentially fraudulent behavior
from core.explainability_pipeline import explainability_agent_pipeline  # Explains AI decisions using techniques like SHAP
from core.compliance_pipeline import compliance_agent_pipeline  # Validates decision against compliance/regulatory rules

# ============================
# MCP External Agent Endpoints
# ============================

EXTERNAL_FRAUD_AGENT_URL = os.getenv("EXTERNAL_FRAUD_AGENT_URL")
EXTERNAL_CREDIT_AGENT_URL = os.getenv("EXTERNAL_CREDIT_AGENT_URL")

# =======================
# Tool Runner Functions
# =======================

# Each function below is a wrapper that takes a single input (summary_text)
# and runs it through the appropriate pipeline (tool/agent).
# The input is expected to be a pre-summarized credit or transaction profile.
# The output is always a dictionary (usually containing scores, flags, or explanations).

def run_credit_tool(summary_text: str) -> dict:
    """
    Runs the Credit Scoring Agent, either external (if configured) or local.

    Parameters:
    - summary_text (str): Summarized customer or credit profile text.

    Returns:
    - dict: Credit scoring results.
    """
    if EXTERNAL_CREDIT_AGENT_URL:
        print(f"🔗 Forwarding credit scoring to {EXTERNAL_CREDIT_AGENT_URL}")
        try:
            response = requests.post(EXTERNAL_CREDIT_AGENT_URL, json={"summary": summary_text}, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️ External credit agent failed: {e}. Falling back to local agent.")
    return {
        "agentName": "Credit Scoring",
        "agentOrigin": "internal",
        **credit_scoring_pipeline(summary_text)  # Keep this as is for local agent
    }


def run_fraud_tool(summary_text: str) -> dict:
    """
    Runs the Fraud Detection Agent, either external (if configured) or local.

    Parameters:
    - summary_text (str): Summarized transaction or customer behavior text.

    Returns:
    - dict: Fraud analysis results.
    """
    if EXTERNAL_FRAUD_AGENT_URL:
        print(f"🔗 Forwarding fraud detection to {EXTERNAL_FRAUD_AGENT_URL}")
        try:
            response = requests.post(EXTERNAL_FRAUD_AGENT_URL, json={"summary": summary_text}, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️ External fraud agent failed: {e}. Falling back to local agent.")
    
    # For local agent (using MCP tool for fraud detection)
    from core.tools.fraud_detection_tool import FraudDetectionTool  # Import the custom fraud tool
    return {
        "agentName": "Fraud Detection",
        "agentOrigin": "internal",
        **fraud_detection_pipeline(summary_text)  # Use MCP fraud detection pipeline
    }


def run_explainability_tool(summary_text: str) -> dict:
    """
    Runs the Explainability Agent.

    Parameters:
    - summary_text (str): The input on which a decision was made (for explanation).

    Returns:
    - dict: Explanation of the decision (e.g., feature contributions, SHAP values).
    """
    return {
        "agentName": "Explainability",
        "agentOrigin": "internal",
        **explainability_agent_pipeline(summary_text)  # Assuming this is already handled
    }


def run_compliance_tool(summary_text: str) -> dict:
    """
    Runs the Compliance Agent.

    Parameters:
    - summary_text (str): Text summary of AI-generated decision or profile.

    Returns:
    - dict: Validation results against compliance rules or regulatory guidelines.
    """
    return {
        "agentName": "Compliance",
        "agentOrigin": "internal",
        **compliance_agent_pipeline(summary_text)  # Assuming this is already handled
    }
