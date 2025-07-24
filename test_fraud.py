import requests

resp = requests.post(
    "http://localhost:5055/fraud-evaluator",
    json={"test": "123"}
)

print(resp.status_code)
print(resp.json())