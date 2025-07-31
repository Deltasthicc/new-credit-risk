# Credit Risk MCP Server with AI Agents

This backend project provides a complete credit risk and fraud detection pipeline using Flask and multiple AI agents. It supports integration with Azure AI Agents and local ML models to simulate real-world financial risk evaluation.

## 🚀 Features

- ✅ Flask server with ngrok support for public API testing
- 🤖 AI Agent support for:
  - Fraud Detection (ML + GPT Explanation)
  - Credit Scoring
  - Compliance Verification
  - Multi-Agent Risk Assessment
- 🧠 Azure AI Agent integration for LLM-based summaries
- 📂 Modular code: `core/`, `agents/`, and `mcp_server.py`

## 📦 Endpoints

### `POST /`
Run all agents and return a full risk assessment.

### `POST /fraud`
Run only the fraud detection agent.

### `POST /credit`
Run only the credit scoring agent.

### `POST /compliance`
Run only the compliance agent.

### `POST /risk`
Run a combined multi-agent risk assessment.

### `GET /info`
Returns server metadata and endpoint descriptions.

### `GET /health`
Returns server health and agent load status.

## 🔧 Example `curl` Test

```powershell
curl.exe -X POST "https://<your-ngrok-url>/" `
  -H "Content-Type: application/json" `
  -H "ngrok-skip-browser-warning: true" `
  -d '{ "summary": "ABC Corp with ₹5B Revenue, ₹0.5B Net Income, ₹8B Total Assets. Industry: Manufacturing. Country: India." }'
```

## 🧠 Local Agent Example (Fraud Detection)

Fraud detection uses a joblib-trained binary classifier and includes an explanation generated via Azure AI Assistant.

## 📁 Directory Structure

```
credit-risk/
├── agents/
│   └── fraud_detection/
│       └── fraud_model.joblib
├── core/
│   ├── fraud_pipeline.py
│   ├── credit_pipeline.py
│   └── compliance_pipeline.py
├── mcp_server.py
└── output_data/
```

## 📌 Requirements

- Python 3.10+
- Azure Developer Account with AI Agent Service
- `requirements.txt` with:
  - flask
  - pandas
  - joblib
  - azure-identity
  - azure-ai-projects

## 🧪 Run Server

```bash
python mcp_server.py
```

Then open:
- `http://localhost:5000` or
- your `https://<ngrok-url>` for public access

