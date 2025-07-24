# === app.py ===
# This is the main entry point for the Credit Risk Assessment backend API.
# It uses Flask to expose HTTP endpoints for running various AI/ML pipelines,
# including bureau summarization, credit scoring, fraud detection, compliance checking,
# explainability, and a smart controller that orchestrates all the tools.
# It also supports Model Context Protocol (MCP) for schema-based validation of agent inputs/outputs.

<<<<<<< HEAD
from flask import Flask, request, jsonify  # Flask web framework for HTTP APIs
from core.bureau_pipeline import bureau_agent_pipeline  # Agent to summarize credit bureau data
from core.credit_pipeline import credit_scoring_pipeline  # Agent to calculate credit score
from core.fraud_pipeline import fraud_detection_pipeline  # Agent to detect fraud patterns
from core.compliance_pipeline import compliance_agent_pipeline  # Agent to check policy violations
from core.explainability_pipeline import explainability_agent_pipeline  # Agent to generate model explanations
from core.smart_pipeline import run_smart_pipeline  # Orchestrated pipeline to run all agents together
import traceback  # To capture detailed error logs
from core.blob_utils import upload_file_to_blob  # Function to upload files to Azure Blob Storage
from mcp.validator import validate_input_against_schema, validate_output_against_schema  # Schema validation utilities
import json  # JSON parsing for MCP schema files
import os  # For file and path operations
import requests  # HTTP client for making external API calls
import pandas as pd  # Data manipulation library for handling dataframes
from core.agent_registry import AGENT_PIPELINES  # Dictionary mapping agent names to their functions
from utils.external_mcp_utils import (
    CLIENT_REGISTRY,
    call_external_agent,
    transform_external_output,
    format_external_summary
)
=======
from flask import Flask, request, jsonify  # Flask web framework for API endpoints
from core.bureau_pipeline import bureau_agent_pipeline  # Bureau summary pipeline
from core.credit_pipeline import credit_scoring_pipeline  # Credit scoring pipeline
from core.fraud_pipeline import fraud_detection_pipeline  # Fraud detection pipeline
from core.compliance_pipeline import compliance_agent_pipeline  # Compliance checking pipeline
from core.explainability_pipeline import explainability_agent_pipeline  # Explainability pipeline
from core.smart_pipeline import run_smart_pipeline  # Smart controller pipeline (orchestrates all tools)
import traceback  # For printing detailed error tracebacks in case of exceptions
from core.blob_utils import upload_file_to_blob  # Utility for uploading files to Azure Blob Storage
from mcp.validator import validate_input_against_schema, validate_output_against_schema  # Input/output schema validators
import json  # For JSON serialization/deserialization
import os  # For file path operations
from core.agent_registry import AGENT_PIPELINES  # Central registry for all agent pipelines
import asyncio  # For running asynchronous tasks
from my_SemanticKernel.my_sk_orchestrator import SemanticKernelOrchestrator
>>>>>>> 04aff6f12177b60313af99738de0c7fb554ecc3c

# === Flask App Initialization ===
app = Flask(__name__)


#Initialize SK orchestrator 
sk_orchestrator = SemanticKernelOrchestrator()

# === Health Check Endpoint ===
@app.route("/", methods=["GET"])
def index():
    """
    Basic GET route for checking if the API is live.
    """
    return "API is up and running!"

# === Fraud Detection Endpoint ===
@app.route("/run-fraud", methods=["POST"])
def run_fraud():
    """
    Runs the fraud detection agent on the latest summary text from disk.
    Returns the fraud detection results.
    """
    try:
        summary_text = open("output_data/rag_summary.txt", encoding="utf-8").read()
        fraud_result = fraud_detection_pipeline(summary_text)
        return jsonify(fraud_result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Compliance Checking Endpoint ===
@app.route("/run-compliance", methods=["POST"])
def run_compliance():
    """
    Runs the compliance check agent on the summary.
    Returns whether the input violates any compliance rules.
    """
    try:
        summary_text = open("output_data/rag_summary.txt", encoding="utf-8").read()
        compliance_result = compliance_agent_pipeline(summary_text)
        return jsonify(compliance_result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Explainability Endpoint ===
@app.route("/run-explainability", methods=["POST"])
def run_explainability():
    """
    Runs the explainability agent to explain AI decisions based on the summary.
    Useful for transparency and auditing.
    """
    try:
        summary_text = open("output_data/rag_summary.txt", encoding="utf-8").read()
        explain_result = explainability_agent_pipeline(summary_text)
        return jsonify(explain_result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/run-smart-controller", methods=["POST"])
def run_smart_controller():
    """
    Smart controller endpoint:
    - Calls external client MCP agents if available (fraud, credit)
    - Injects their results as context into internal agents
    - Then runs your full Azure AI-based smart pipeline
    """
    try:
        # =======================
        # STEP 1: Extract request
        # =======================
        data = request.get_json()
        client_id = data.get("client_id", "default")  # fallback to 'default'
        external_text_segments = []

        # Clone context for summarizer (optional if Azure agents use summaries)
        context = data.copy()

        # ============================
        # STEP 2: External agent calls
        # ============================
        client_conf = CLIENT_REGISTRY.get(client_id, {})

        # --- External fraud ---
        if "fraud_agent_url" in client_conf:
            fraud_result = call_external_agent(client_conf["fraud_agent_url"], context)
            if fraud_result:
                fraud_transformed = transform_external_output("fraud", fraud_result)
                context.update(fraud_transformed)
                external_text_segments.append(format_external_summary("fraud", fraud_transformed))

        # --- External credit ---
        if "credit_agent_url" in client_conf:
            credit_result = call_external_agent(client_conf["credit_agent_url"], context)
            if credit_result:
                credit_transformed = transform_external_output("credit", credit_result)
                context.update(credit_transformed)
                external_text_segments.append(format_external_summary("credit", credit_transformed))

        # ======================================
        # STEP 3: Inject context into summary?
        # ======================================
        if external_text_segments:
            if "context" not in data:
                data["context"] = ""
            data["context"] += "\n\nExternal MCP Agent Context:\n" + "\n".join(external_text_segments)

        # ===================================
        # STEP 4: Run your original pipeline
        # ===================================
        final_result = run_smart_pipeline()

        # Append MCP summary section if it exists
        if external_text_segments and "bureau_summary" in final_result:
            existing_summary = final_result["bureau_summary"].get("summary", "")
            new_summary = existing_summary + "\n\nExternal MCP Agent Context:\n" + "\n".join(external_text_segments)
            final_result["bureau_summary"]["summary"] = new_summary

        return jsonify(final_result), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


<<<<<<< HEAD
# === MCP-Compliant Dynamic Agent Endpoint ===
@app.route("/run-agent/<agent_name>", methods=["POST"])
def run_agent(agent_name):
    """
    Dynamically runs any registered agent using its MCP schema.
    Input and output are validated against corresponding schemas.
    """
    try:
        mcp_path = os.path.join("mcp", f"{agent_name}.json")

        # Ensure the agent's MCP schema exists
        if not os.path.exists(mcp_path):
            return jsonify({"error": f"Schema file not found for agent '{agent_name}'"}), 404

        # Load MCP input/output schema from file
        with open(mcp_path, "r", encoding="utf-8") as f:
            mcp = json.load(f)

        # Extract JSON input from request
        data = request.get_json()

        # Validate request input using MCP schema
        is_valid, errors = validate_input_against_schema(data, mcp["input_schema"])
        if not is_valid:
            return jsonify({"error": "Invalid input", "details": errors}), 400

        # Fetch the corresponding pipeline function
        pipeline_fn = AGENT_PIPELINES.get(agent_name)
        if not pipeline_fn:
            return jsonify({"error": f"No pipeline function registered for agent: {agent_name}"}), 500

        # Run the agent pipeline
        result = pipeline_fn(data.get("summary") or data)

        # Validate agent output using MCP schema
        valid_output, output_errors = validate_output_against_schema(result, mcp["output_schema"])
        if not valid_output:
            return jsonify({
                "warning": "Output doesn't match schema",
                "errors": output_errors,
                "result": result
            }), 200

        return jsonify(result), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# === Multi-Agent Orchestration Endpoint ===
@app.route("/run-all-agents", methods=["POST"])
def run_all_agents():
    """
    Runs all agents listed in AGENT_PIPELINES on the latest summary text.
    Validates each agent's input and output using its respective MCP schema.
    Returns a dictionary of results or validation warnings.
    """
    try:
        summary_text = open("output_data/rag_summary.txt", encoding="utf-8").read()
        combined_results = {}

        for agent_name, pipeline_fn in AGENT_PIPELINES.items():
            mcp_path = os.path.join("mcp", f"{agent_name}.json")

            # Skip agents with missing MCP definitions
            if not os.path.exists(mcp_path):
                combined_results[agent_name] = {"error": "MCP schema not found"}
                continue

            # Load MCP file
            with open(mcp_path, "r", encoding="utf-8") as f:
                mcp = json.load(f)

            # Validate input
            input_data = {"summary": summary_text}
            is_valid, input_errors = validate_input_against_schema(input_data, mcp["input_schema"])
            if not is_valid:
                combined_results[agent_name] = {"error": "Invalid input", "details": input_errors}
                continue

            # Run pipeline
            result = pipeline_fn(summary_text)

            # Validate output
            is_valid_output, output_errors = validate_output_against_schema(result, mcp["output_schema"])
            if not is_valid_output:
                combined_results[agent_name] = {
                    "warning": "Output doesn't match schema",
                    "errors": output_errors,
                    "result": result
                }
            else:
                combined_results[agent_name] = result

        return jsonify(combined_results), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# === Flask Entrypoint ===
=======


## Semantic Kernel Endpoints
@app.route("/run-sk-smart-controller", methods=["POST"])
def run_sk_smart_controller():
    try:
        # Handle case where request.json is None
        requirements = []
        if request.json and "requirements" in request.json:
            requirements = request.json["requirements"]
        
        print(f"Processing requirements: {requirements}")
        
        #Run async orchestrator
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(sk_orchestrator.run_smart_analysis(requirements))
        loop.close()

        return jsonify(result), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/run-sk-credit-analysis", methods=["POST"])
def run_sk_credit_analysis():
    """Full credit analysis using SK orchestration."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            sk_orchestrator.run_credit_analysis()
        )
        loop.close()
        
        return jsonify({"analysis": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === Main Entrypoint ===
# This block runs the Flask app when the script is executed directly.
# The app listens on all interfaces (0.0.0.0) at port 5000.
>>>>>>> 04aff6f12177b60313af99738de0c7fb554ecc3c
if __name__ == "__main__":
    # Launch the app on all available IPs, port 5000
    app.run(host="0.0.0.0", port=5000, debug=False)
# This allows the API to be accessible from any network interface.