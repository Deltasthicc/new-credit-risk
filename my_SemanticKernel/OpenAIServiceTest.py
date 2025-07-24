import openai
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://my-sk-orchestrator.openai.azure.com/",
    api_key="2xTlXYrRx9nTbvwfYLxi4isHOUSYwgK3ueGWektK9j1M2uA7HvReJQQJ99BGACHYHv6XJ3w3AAABACOGSBIC",
    api_version="2024-06-01"
)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use your actual deployment name
        messages=[{"role": "user", "content": "Hello, test connection"}],
        max_tokens=10
    )
    print("Connection successful!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Connection failed: {e}")