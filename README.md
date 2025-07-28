# 🧠 Credit Risk & Fraud Prevention System (MCP-Compliant)

This project is a simulation of a **multi-agent AI credit risk and fraud prevention platform**, built using Microsoft Azure AI Agent Service, SHAP, Scikit-Learn, and Azure Cognitive Search. It follows the **Model Context Protocol (MCP)** specification to allow scalable, pluggable AI agent orchestration.

---

## 🏗️ Architecture Overview

```
                                 ┌────────────────────────┐
                                 │  External Bank Agent   │
                                 │ (Optional, MCP-Linked) │
                                 └────────────┬───────────┘
                                              │
                                              ▼
                           ┌──────────────────────────────┐
                           │ Bureau Summarizer Agent (BS) │
                           └────────────┬─────────────────┘
                                        │
                        ┌───────────────▼────────────────┐
                        │ Smart Controller Agent (Azure) │
                        └──────┬──────┬──────┬────────────┘
                               │      │      │
              ┌────────────────┘      │      └──────────────────┐
              ▼                       ▼                         ▼
     Credit Scoring Agent     Fraud Detection Agent     Explainability Agent
              │                       │                         │
              └────────────┬──────────┴────────────┬────────────┘
                           ▼                       ▼
                    Compliance Agent       Final Combined Report
```

---

## 🧰 Tech Stack

| Layer         | Tools & Frameworks                                                                 |
|---------------|-------------------------------------------------------------------------------------|
| **Platform**  | Microsoft Fabric (Lakehouse), Azure AI Agent Service                               |
| **AI Agents** | Azure OpenAI (GPT-4), SHAP, Scikit-learn, SentenceTransformers                      |
| **Search**    | Azure Cognitive Search with vector embeddings                                      |
| **Backend**   | Python 3.10, Flask, `joblib`, `pandas`, `re`, `json`, `datetime`, Azure SDKs       |
| **MCP**       | Model Context Protocol v1 (pluggable agent schema + validation)                    |

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.10+
- Azure Subscription (with OpenAI, AI Projects, Cognitive Search)
- Azure CLI (`az login`)
- VS Code recommended

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Agent Components

### 1. `Bureau Summariser Agent`
- Uses RAG (Retrieval-Augmented Generation) to generate summaries from financial documents.
- Inputs: `.docx`, `.xlsx` from Azure Blob
- Tools: Azure Search (Vector Index), GPT-4

### 2. `Credit Scoring Agent`
- Uses Azure LLM to return:
  - Credit rating (AAA–DDD)
  - Probability of Default (PD)
  - Financial strength scores

### 3. `Fraud Detection Agent`
- Uses a local ML model (`fraud_model.joblib`) to score fraud risk.
- GPT-4 explains why fraud was/wasn’t flagged.
- Output includes flagged anomalies, confidence, and authenticity scores.

### 4. `Explainability Agent`
- Uses SHAP + GPT to explain the credit risk decision.
- Outputs:
  - Top decision drivers
  - SHAP values
  - GPT-written summary

### 5. `Compliance Agent`
- Heuristically detects legal and regulatory compliance issues.
- Returns risk level and mitigation recommendations.

---

## 🧪 Running the System

### Run All Agents via Smart Controller

```bash
python -c "from core.smart_pipeline import run_smart_pipeline; import json; print(json.dumps(run_smart_pipeline(), indent=2))"
```

### Run Individual Agents

```bash
# Bureau
python core/bureau_pipeline.py

# Credit Score
python core/credit_pipeline.py

# Fraud Detection
python core/fraud_pipeline.py

# Explainability
python core/explainability_pipeline.py
```

---

## 🔌 External MCP Agent Plug-in (e.g. bank fraud model)

Supports connecting to external MCP agents via API (see `run_fraud_tool()` in `tools.py`).

```python
result["fraud_detection"] = run_fraud_tool(summary, external_endpoint="https://bank.com/mcp/fraud")
```

This allows banks or partners to inject their own prebuilt MCP-compliant agents, whose output is then merged into context.

---

## 📤 Output Format

Each agent returns MCP-compliant JSON:

```json
{
  "agentName": "Fraud Detection",
  "status": "AgentStatus.complete",
  "summary": "...",
  "confidenceScore": 0.92,
  "completedAt": "2025-07-27T18:08:10.460Z",
  "extractedData": { ... },
  "errorMessage": null
}
```

---

## 📁 Directory Structure

```
credit-risk/
├── core/
│   ├── smart_pipeline.py
│   ├── tools.py
│   ├── bureau_pipeline.py
│   ├── credit_pipeline.py
│   ├── fraud_pipeline.py
│   └── explainability_pipeline.py
├── agents/
│   └── [agent-specific models and pipelines]
├── output_data/
│   └── summary2.json, rag_summary.txt, final reports
├── .env
├── requirements.txt
└── README.md
```

---

## 📜 License

MIT License © 2025 Team CreditRisk

---

## 🙌 Authors

- **Shashwat Rajan** – MCP Integration, Agent Framework
- **Shiv Gupta** – Azure Deployment, Agent Flow Design
- **Divya Sharma** – Schema Validation, Compliance Agent

---

## 🔗 References

- [Azure AI Agent Service Docs](https://learn.microsoft.com/en-us/azure/ai-services/agent-service/)
- [Model Context Protocol (MCP)](https://aka.ms/mcp-spec)
- [SHAP Interpretability](https://shap.readthedocs.io/)