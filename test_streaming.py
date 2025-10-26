#!/usr/bin/env python3
"""
Test streaming support for QLM API
"""

import requests
import json

# Test streaming response
print("Test: Streaming response")
print("=" * 60)

url = "http://localhost:8000/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-v1-42test"
}

# Test with multimodal content (like Roo sends)
data = {
    "model": "quack-model",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello duck!"
                }
            ]
        }
    ],
    "stream": True,
    "stream_options": {
        "include_usage": True
    }
}

try:
    response = requests.post(url, headers=headers, json=data, stream=True)
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    print("\nStreaming chunks:")
    
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith('data: '):
                data_str = decoded[6:]  # Remove 'data: ' prefix
                if data_str != '[DONE]':
                    chunk = json.loads(data_str)
                    if 'choices' in chunk and chunk['choices']:
                        delta = chunk['choices'][0].get('delta', {})
                        if 'content' in delta:
                            print(delta['content'], end='', flush=True)
                        if chunk['choices'][0].get('finish_reason'):
                            print(f"\n\nFinish reason: {chunk['choices'][0]['finish_reason']}")
                        if 'usage' in chunk:
                            print(f"Usage: {chunk['usage']}")
                else:
                    print("\n[DONE]")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

