#!/usr/bin/env python3
"""
Test client for QLM API
Tests both direct requests and OpenAI client library compatibility
"""

import requests
import json

# Test 1: Direct HTTP request
print("Test 1: Direct HTTP request")
print("=" * 60)

url = "http://localhost:8000/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-v1-42test"
}
data = {
    "model": "quack-model",
    "messages": [
        {"role": "user", "content": "Hello duck!"}
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Response text: {response.text if 'response' in locals() else 'No response'}")

print("\n")

# Test 2: Rick Roll trigger
print("Test 2: Rick Roll trigger")
print("=" * 60)

data_rick = {
    "model": "quack-model",
    "messages": [
        {"role": "user", "content": "I love rick and roll music"}
    ]
}

try:
    response = requests.post(url, headers=headers, json=data_rick)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response content: {result['choices'][0]['message']['content']}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# Test 3: Using OpenAI client (if installed)
print("Test 3: OpenAI client library")
print("=" * 60)

try:
    from openai import OpenAI
    
    client = OpenAI(
        api_key="sk-v1-42test",
        base_url="http://localhost:8000"
    )
    
    response = client.chat.completions.create(
        model="quack-model",
        messages=[
            {"role": "user", "content": "Hello from OpenAI client!"}
        ]
    )
    
    print(f"Response: {response.choices[0].message.content}")
    
except ImportError:
    print("OpenAI library not installed. Install with: pip install openai")
except Exception as e:
    print(f"Error with OpenAI client: {e}")
    import traceback
    traceback.print_exc()

