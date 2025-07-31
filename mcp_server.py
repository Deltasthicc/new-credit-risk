from flask import Flask, request, jsonify
from fastmcp import FastMCP
import asyncio
from threading import Thread
import subprocess
import time
import os
import requests
import json
from datetime import datetime

# Import your actual agent pipelines
from core.fraud_pipeline import fraud_detection_pipeline
from core.credit_pipeline import credit_scoring_pipeline
from core.compliance_pipeline import compliance_agent_pipeline

# Initialize Flask app with ngrok-friendly configuration
app = Flask(__name__)
app.config['SERVER_NAME'] = None  # Allow external access

# Initialize FastMCP server
mcp_server = FastMCP("credit_risk_mcp_server")
# Set this dynamically if possible, else override manually
NGROK_URL = "https://be2c4e1372e8.ngrok-free.app"

# ==========================
# Core Agent Pipeline Functions (calling your actual agents)
# ==========================

def fraud_detection_logic(data):
    """Call the actual fraud detection agent pipeline"""
    try:
        # Extract summary or create one from the data
        if "summary" in data:
            summary = data["summary"]
        else:
            # Create summary from financial data
            revenue = data.get("Revenue", 0)
            net_income = data.get("Net_Income", 0)
            total_assets = data.get("Total_Assets", 0)
            total_liabilities = data.get("Total_Liabilities", 0)
            equity = data.get("Equity", 0)
            industry = data.get("Industry", "Unknown")
            country = data.get("Country", "Unknown")
            
            summary = f"Company with ₹{revenue/1000000000:.1f}B Revenue, ₹{net_income/1000000000:.1f}B Net Income, ₹{total_assets/1000000000:.1f}B Total Assets"
            if total_liabilities > 0:
                summary += f", ₹{total_liabilities/1000000000:.1f}B Total Liabilities"
            if equity > 0:
                summary += f", ₹{equity/1000000000:.1f}B Equity"
            summary += f". Industry: {industry}. Country: {country}."
        
        print(f"🔍 Calling fraud detection agent with summary: {summary}")
        
        # Call your actual fraud detection agent
        result = fraud_detection_pipeline(summary)
        
        print(f"✅ Fraud detection agent result: {result}")
        return result
    
    except Exception as e:
        print(f"❌ Error in fraud detection agent: {str(e)}")
        return {"error": f"Fraud detection agent failed: {str(e)}"}

def credit_scoring_logic(data):
    """Call the actual credit scoring agent pipeline"""
    try:
        # Extract summary or create one from the data
        if "summary" in data:
            summary = data["summary"]
        else:
            # Create summary from financial data
            revenue = data.get("Revenue", 0)
            net_income = data.get("Net_Income", 0)
            total_assets = data.get("Total_Assets", 0)
            total_liabilities = data.get("Total_Liabilities", 0)
            equity = data.get("Equity", 0)
            industry = data.get("Industry", "Unknown")
            country = data.get("Country", "Unknown")
            
            summary = f"Company with ₹{revenue/1000000000:.1f}B Revenue, ₹{net_income/1000000000:.1f}B Net Income, ₹{total_assets/1000000000:.1f}B Total Assets"
            if total_liabilities > 0:
                summary += f", ₹{total_liabilities/1000000000:.1f}B Total Liabilities"
            if equity > 0:
                summary += f", ₹{equity/1000000000:.1f}B Equity"
            summary += f". Industry: {industry}. Country: {country}."
        
        print(f"📊 Calling credit scoring agent with summary: {summary}")
        
        # Call your actual credit scoring agent
        result = credit_scoring_pipeline(summary)
        
        print(f"✅ Credit scoring agent result: {result}")
        return result
    
    except Exception as e:
        print(f"❌ Error in credit scoring agent: {str(e)}")
        return {"error": f"Credit scoring agent failed: {str(e)}"}

def compliance_logic(data):
    """Call the actual compliance agent pipeline"""
    try:
        # Extract summary or create one from the data
        if "summary" in data:
            summary = data["summary"]
        else:
            # Create summary from financial data
            revenue = data.get("Revenue", 0)
            net_income = data.get("Net_Income", 0)
            total_assets = data.get("Total_Assets", 0)
            total_liabilities = data.get("Total_Liabilities", 0)
            equity = data.get("Equity", 0)
            industry = data.get("Industry", "Unknown")
            country = data.get("Country", "Unknown")
            
            summary = f"Company with ₹{revenue/1000000000:.1f}B Revenue, ₹{net_income/1000000000:.1f}B Net Income, ₹{total_assets/1000000000:.1f}B Total Assets"
            if total_liabilities > 0:
                summary += f", ₹{total_liabilities/1000000000:.1f}B Total Liabilities"
            if equity > 0:
                summary += f", ₹{equity/1000000000:.1f}B Equity"
            summary += f". Industry: {industry}. Country: {country}."
        
        print(f"⚖️ Calling compliance agent with summary: {summary}")
        
        # Call your actual compliance agent
        result = compliance_agent_pipeline(summary)
        
        print(f"✅ Compliance agent result: {result}")
        return result
    
    except Exception as e:
        print(f"❌ Error in compliance agent: {str(e)}")
        return {"error": f"Compliance agent failed: {str(e)}"}

# ==========================
# MCP Tools (these call the agent pipelines)
# ==========================

@mcp_server.tool
def get_fraud_detection_result(data):
    """MCP tool for fraud detection using agent pipeline"""
    return fraud_detection_logic(data)

@mcp_server.tool
def get_credit_score_result(data):
    """MCP tool for credit scoring using agent pipeline"""
    return credit_scoring_logic(data)

@mcp_server.tool
def get_compliance_result(data):
    """MCP tool for compliance checking using agent pipeline"""
    return compliance_logic(data)

# ==========================
# Middleware to handle ngrok headers
# ==========================
@app.before_request
def handle_ngrok_headers():
    """Handle ngrok-specific headers and CORS for external access"""
    if request.headers.get('ngrok-skip-browser-warning'):
        pass
    
    if request.is_json or request.method in ['POST', 'PUT', 'PATCH']:
        request.environ['HTTP_NGROK_SKIP_BROWSER_WARNING'] = 'true'

@app.after_request
def after_request(response):
    """Add CORS headers and ngrok-friendly headers"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,ngrok-skip-browser-warning')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('ngrok-skip-browser-warning', 'true')
    return response

# Handle OPTIONS requests for CORS
@app.route('/', methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path=None):
    """Handle preflight OPTIONS requests"""
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,ngrok-skip-browser-warning')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ==========================
# GET Routes
# ==========================

@app.route("/", methods=["GET"])
def root_get():
    """Root endpoint for browser access via ngrok"""
    ngrok_url = NGROK_URL
    return jsonify({
        "message": "🏦 Credit Risk MCP Server with AI Agents",
        "status": "online",
        "ngrok_url": ngrok_url,
        "description": "AI-powered financial analysis using specialized agents",
        "agents": {
            "fraud_detection": "AI agent for fraud risk analysis",
            "credit_scoring": "AI agent for credit assessment",
            "compliance": "AI agent for regulatory compliance",
        },
        "endpoints": {
            "POST /": "Comprehensive AI agent analysis",
            "POST /credit": "Credit scoring agent only",
            "POST /fraud": "Fraud detection agent only", 
            "POST /compliance": "Compliance agent only",
            "GET /info": "Server information",
            "GET /health": "Health check"
        },
        "sample_data": {
            "summary": "XYZ Ltd. is a fintech company with ₹2.5B Revenue, ₹0.2B Net Income, ₹3B Total Assets. Industry: IT Services. Country: India.",
            "or_structured": {
                "Revenue": 2500000000,
                "Net_Income": 200000000,
                "Total_Assets": 3000000000,
                "Industry": "IT Services",
                "Country": "India"
            }
        },
        "test_command": f"curl -X POST {ngrok_url} -H 'Content-Type: application/json' -H 'ngrok-skip-browser-warning: true' -d '{{\"summary\": \"XYZ Ltd. is a fintech company with ₹2.5B Revenue, ₹0.2B Net Income, ₹3B Total Assets. Industry: IT Services. Country: India.\"}}'"
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint accessible via ngrok"""
    ngrok_url = NGROK_URL
    return jsonify({
        "status": "healthy", 
        "service": "credit_risk_mcp_server_with_agents",
        "ngrok_url": ngrok_url,
        "local_url": "http://localhost:5000",
        "accessible_via_ngrok": True,
        "agents_loaded": True,
        "pipelines": ["fraud_detection", "credit_scoring", "compliance"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route("/info", methods=["GET"])
def server_info():
    """Get server information including ngrok URL"""
    ngrok_url = NGROK_URL
    return jsonify({
        "service": "Credit Risk MCP Server with AI Agents",
        "version": "2.0.0",
        "status": "online",
        "ngrok_enabled": True,
        "ai_agents": {
            "fraud_detection_pipeline": "Active",
            "credit_scoring_pipeline": "Active",
            "compliance_agent_pipeline": "Active",
        },
        "endpoints": {
            "comprehensive_analysis": "/",
            "fraud_detection": "/fraud",
            "credit_scoring": "/credit", 
            "compliance_check": "/compliance",
            "health_check": "/health",
            "server_info": "/info"
        },
        "urls": {
            "local": "http://localhost:5000",
            "ngrok": ngrok_url,
            "ngrok_dashboard": "http://localhost:4040"
        },
        "sample_requests": {
            "with_summary": {
                "url": ngrok_url,
                "method": "POST",
                "body": {
                    "summary": "XYZ Ltd. is a fintech company with ₹2.5B Revenue, ₹0.2B Net Income, ₹3B Total Assets. Industry: IT Services. Country: India."
                }
            },
            "with_structured_data": {
                "url": ngrok_url,
                "method": "POST", 
                "body": {
                    "Revenue": 2500000000,
                    "Net_Income": 200000000,
                    "Total_Assets": 3000000000,
                    "Industry": "IT Services",
                    "Country": "India"
                }
            }
        }
    })

@app.route('/favicon.ico', methods=["GET"])
def favicon():
    """Handle favicon requests"""
    return '', 204

# ==========================
# POST Routes (calling actual agent pipelines)
# ==========================

@app.route("/", methods=["POST"])
def handle_request():
    """Main route that processes financial data through AI agents"""
    try:
        if not request.is_json:
            return jsonify({
                "message": "Credit Risk MCP Server with AI Agents",
                "status": "ready",
                "ngrok_url": NGROK_URL,
                "usage": "Send POST request with JSON data (summary or structured financial data)",
                "sample_curl": f"curl -X POST {NGROK_URL} -H 'Content-Type: application/json' -H 'ngrok-skip-browser-warning: true' -d '{{\"summary\": \"Company with ₹2.5B Revenue, ₹0.2B Net Income, ₹3B Total Assets. Industry: IT Services. Country: India.\"}}'"
            }), 200
        
        data = request.get_json()
        print(f"🤖 Processing data through AI agents: {data}")
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Process through all AI agent pipelines
        print("🚀 Starting AI agent processing...")
        
        results = {
            "fraud_detection": fraud_detection_logic(data),
            "credit_scoring": credit_scoring_logic(data),
            "compliance": compliance_logic(data),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "processed_via": "ai_agents_via_ngrok",
            "ngrok_url": NGROK_URL,
            "processing_method": "agent_pipelines",
            "input_data": data
        }
        
        print(f"✅ All AI agents completed processing")
        return jsonify(results)
        
    except Exception as e:
        print(f"❌ Error processing request through AI agents: {str(e)}")
        return jsonify({"error": str(e), "processed_via": "ai_agents_via_ngrok"}), 500

@app.route("/fraud", methods=["POST"])
def fraud_only():
    """Route for fraud detection agent only"""
    try:
        data = request.get_json()
        print(f"🔍 Running fraud detection agent only...")
        result = fraud_detection_logic(data)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Fraud detection agent error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/credit", methods=["POST"])
def credit_only():
    """Route for credit scoring agent only"""
    try:
        data = request.get_json()
        print(f"📊 Running credit scoring agent only...")
        result = credit_scoring_logic(data)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Credit scoring agent error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/compliance", methods=["POST"])
def compliance_only():
    """Route for compliance agent only"""
    try:
        data = request.get_json()
        print(f"⚖️ Running compliance agent only...")
        result = compliance_logic(data)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Compliance agent error: {str(e)}")
        return jsonify({"error": str(e)}), 500
# ==========================
# Ngrok Integration
# ==========================

def check_existing_ngrok():
    """Check if ngrok is already running and get the public URL"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=3)
        tunnels = response.json()
        
        if tunnels.get("tunnels"):
            for tunnel in tunnels["tunnels"]:
                if tunnel.get("proto") == "https":
                    public_url = tunnel["public_url"]
                    print(f"🌐 Found existing ngrok tunnel!")
                    print(f"📡 Public URL: {public_url}")
                    print(f"🔗 Your AI agents are accessible at: {public_url}")
                    print(f"📊 Ngrok dashboard: http://localhost:4040")
                    return public_url
        
        print("⚠️  Ngrok is running but no HTTPS tunnels found")
        return None
        
    except requests.exceptions.RequestException:
        print("ℹ️  Ngrok dashboard not accessible - ngrok may not be running")
        print("💡 Start ngrok manually with: ngrok http 5000")
        return None
    except Exception as e:
        print(f"❌ Error checking ngrok status: {e}")
        return None

# ==========================
# Running MCP Server in a Background Thread
# ==========================

def run_mcp_server():
    """Run the FastMCP server asynchronously in a background thread"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(mcp_server.run_async())
    except Exception as e:
        print(f"MCP Server error: {e}")

# ==========================
# Main Entry Point
# ==========================

if __name__ == "__main__":
    print("🚀 Starting Credit Risk MCP Server with AI Agents...")
    print("🤖 Loading AI agent pipelines...")
    
    # Start the MCP server in a separate background thread
    mcp_thread = Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()
    print("✅ MCP server with AI agents started in background thread")
    
    # Check for existing ngrok tunnel
    print("🔍 Checking for existing ngrok tunnel...")
    ngrok_url = check_existing_ngrok()
    
    print("\n" + "="*70)
    print("🏦 CREDIT RISK MCP SERVER WITH AI AGENTS READY")
    print("="*70)
    print(f"🏠 Local URL:       http://localhost:5000")
    print(f"🌐 Ngrok URL:       {NGROK_URL}")
    print(f"📊 Ngrok Dashboard: http://localhost:4040")
    print(f"🤖 AI Agents:       fraud_detection, credit_scoring, compliance")
    
    print(f"\n🌍 YOUR AI AGENTS ARE NOW ACCESSIBLE WORLDWIDE VIA NGROK!")
    print(f"🔗 Direct browser access: {NGROK_URL}")
    print(f"📋 Test API endpoint:     {NGROK_URL}/info")
    
    print(f"\n📋 Test your AI agents with these commands:")
    print(f"# Test with summary format (recommended):")
    print(f"curl -X POST {NGROK_URL} \\")
    print(f"  -H 'Content-Type: application/json' \\")
    print(f"  -H 'ngrok-skip-browser-warning: true' \\")
    print(f"  -d '{{\"summary\": \"XYZ Ltd. is a fintech company with ₹2.5B Revenue, ₹0.2B Net Income, ₹3B Total Assets. Industry: IT Services. Country: India.\"}}'")
    
    print(f"\n# Test with structured data:")
    print(f"curl -X POST {NGROK_URL} \\")
    print(f"  -H 'Content-Type: application/json' \\")
    print(f"  -H 'ngrok-skip-browser-warning: true' \\")
    print(f"  -d '{{\"Revenue\": 2500000000, \"Net_Income\": 200000000, \"Total_Assets\": 3000000000, \"Industry\": \"IT Services\", \"Country\": \"India\"}}'")
    
    print(f"\n🎯 Test individual AI agents:")
    print(f"curl -X POST {NGROK_URL}/fraud -H 'Content-Type: application/json' -H 'ngrok-skip-browser-warning: true' -d '{{\"summary\": \"Company summary here\"}}'")
    print(f"curl -X POST {NGROK_URL}/credit -H 'Content-Type: application/json' -H 'ngrok-skip-browser-warning: true' -d '{{\"summary\": \"Company summary here\"}}'")
    print(f"curl -X POST {NGROK_URL}/compliance -H 'Content-Type: application/json' -H 'ngrok-skip-browser-warning: true' -d '{{\"summary\": \"Company summary here\"}}'")
    
    print(f"\n🔍 Available endpoints:")
    print(f"  POST /           - All AI agents (comprehensive analysis)")
    print(f"  POST /fraud      - Fraud detection AI agent only")
    print(f"  POST /credit     - Credit scoring AI agent only")
    print(f"  POST /compliance - Compliance AI agent only")
    print(f"  GET  /health     - Health check with agent status")
    print(f"  GET  /info       - Complete server and agent information")
    print("="*70)
    
    # Start Flask app
    try:
        print("🚀 Starting Flask server with AI agents on port 5000...")
        app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Shutting down AI agent server gracefully...")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        print("✅ AI agent server stopped")