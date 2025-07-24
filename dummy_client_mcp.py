# dummy_client_mcp.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/fraud-evaluator", methods=["POST"])
def dummy_fraud():
    print("[DUMMY FRAUD] Received:", request.json)
    return jsonify({
        "fraud_score": 0.92,
        "reasons": ["Velocity trigger", "Geo mismatch"]
    })

@app.route("/credit-score", methods=["POST"])
def dummy_credit():
    print("[DUMMY CREDIT] Received:", request.json)
    return jsonify({
        "credit_score": 745,
        "recommendation": "Eligible for ₹5,00,000 personal loan"
    })

if __name__ == "__main__":
    app.run(port=5055)
