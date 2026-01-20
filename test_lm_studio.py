"""Test script to verify LM Studio connection"""
import requests
import json

# Test 1: Check if server is running
print("Testing LM Studio connection...")
print("-" * 50)

try:
    response = requests.get("http://127.0.0.1:1234/v1/models")
    print("✅ Server is reachable")
    print(f"Available models: {response.json()}")
except Exception as e:
    print(f"❌ Server connection failed: {e}")
    exit(1)

# Test 2: Try a simple completion
print("\n" + "-" * 50)
print("Testing chat completion...")

try:
    response = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "qwen2.5-7b-instruct",
            "messages": [
                {"role": "user", "content": "Say hello in one word"}
            ],
            "temperature": 0.7,
            "max_tokens": 10
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Chat completion successful!")
        print(f"Response: {result['choices'][0]['message']['content']}")
    else:
        print(f"❌ Chat completion failed with status {response.status_code}")
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"❌ Request failed: {e}")

print("\n" + "-" * 50)
print("Test complete!")
