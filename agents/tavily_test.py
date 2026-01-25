import os
import requests

url = "https://api.tavily.com/search"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['TAVILY_API_KEY']}"
}

payload = {
    "query": "What is cloud computing?",
    "search_depth": "basic",
    "max_results": 3
}

response = requests.post(url, headers=headers, json=payload)
print("Status:", response.status_code)
print(response.json())
