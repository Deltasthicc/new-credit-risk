from azure.ai.agents.models import Tool
import json

class FraudDetectionTool(Tool):
    def __init__(self, server_label, server_url):
        # Initialize the tool with server details
        self.server_label = server_label
        self.server_url = server_url
    
    @property
    def definitions(self):
        """
        Return the definitions for this tool. 
        This will be a list of the available tool definitions.
        """
        return [{
            "tool_name": self.server_label,
            "server_url": self.server_url,
            "description": "This tool detects fraud in financial summaries.",
            "parameters": ["Revenue", "Net_Income", "Equity", "Industry_Sector", "Country"]
        }]
    
    def execute(self, tool_call):
        """
        Executes the tool using the input from the tool call. This will perform the fraud detection logic.
        """
        # Simulated tool execution logic (you would replace this with actual fraud detection logic)
        data = tool_call["data"]
        fraud_risk_score = data.get("Revenue", 0) * 0.00001  # Example fraud detection logic
        result = {
            "fraud_detected": "Yes" if fraud_risk_score > 0.5 else "No",
            "confidence": fraud_risk_score
        }
        return result
    
    @property
    def resources(self):
        """
        Return the resources required for this tool.
        """
        return {"resource_type": "fraud_detection_model", "version": "1.0"}

# =====================================
# Get MCP Tool (Custom Fraud Detection Tool)
# =====================================

def get_mcp_tool():
    """
    Initialize the custom MCP fraud detection tool client.
    """
    # Initialize the custom Fraud Detection tool with the server label and URL
    mcp_tool = FraudDetectionTool(
        server_label="fraud_detection_tool",
        server_url=" https://9bf5ebef422b.ngrok-free.app"  # Replace with your ngrok public URL
    )
    return mcp_tool
