#!/usr/bin/env python3
"""
Tests for QLM API functionality
"""

import pytest
import json
from fastapi.testclient import TestClient
from api.main import app, select_duck_sound, DUCK_SOUNDS, EASTER_EGG

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint returns correct information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "QLM" in data["name"]
    assert "endpoints" in data

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_models_endpoint():
    """Test models list endpoint"""
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "list"
    assert len(data["data"]) > 0
    assert data["data"][0]["id"] == "quack-model"

def test_chat_completions():
    """Test chat completions endpoint"""
    request_data = {
        "model": "quack-model",
        "messages": [{"role": "user", "content": "Hello duck!"}]
    }

    response = client.post("/chat/completions", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["object"] == "chat.completion"
    assert data["model"] == "quack-model"
    assert len(data["choices"]) == 1
    assert "message" in data["choices"][0]
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert "content" in data["choices"][0]["message"]

    # Verify the response is a duck sound
    duck_response = data["choices"][0]["message"]["content"]
    assert duck_response in [sound for sound, _ in DUCK_SOUNDS]

def test_completions():
    """Test legacy completions endpoint"""
    request_data = {
        "model": "quack-model",
        "prompt": "Test prompt"
    }

    response = client.post("/completions", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["object"] == "text_completion"
    assert data["model"] == "quack-model"
    assert len(data["choices"]) == 1
    assert "text" in data["choices"][0]

    # Verify the response is a duck sound
    duck_response = data["choices"][0]["text"]
    assert duck_response in [sound for sound, _ in DUCK_SOUNDS]

def test_duck_sound_selection():
    """Test that duck sound selection works correctly"""
    # Test that we can call the function
    sound = select_duck_sound()
    assert isinstance(sound, str)
    assert len(sound) > 0

    # Test that it's one of our defined sounds
    assert sound in [s for s, _ in DUCK_SOUNDS]

def test_easter_egg_hidden():
    """Test that easter egg is properly hidden in code"""
    # The easter egg should be base64 encoded in the DUCK_SOUNDS
    easter_sounds = [sound for sound, weight in DUCK_SOUNDS if weight < 0.01]
    assert len(easter_sounds) == 1

    # The easter egg should be decodable
    import base64
    decoded = base64.b64decode("WW91J3JlIGFic29sdXRlbHkgcmlnaHQh").decode('utf-8')
    assert easter_sounds[0] == decoded

def test_cors_headers():
    """Test CORS headers are present"""
    response = client.get("/")
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"

def test_usage_tokens():
    """Test that usage tokens are calculated correctly"""
    request_data = {
        "model": "quack-model",
        "messages": [{"role": "user", "content": "Hello world test"}]
    }

    response = client.post("/chat/completions", json=request_data)
    data = response.json()

    # Should have 2 tokens in prompt
    assert data["usage"]["prompt_tokens"] == 2
    # Should have some tokens in completion
    assert data["usage"]["completion_tokens"] > 0
    # Total should be sum
    assert data["usage"]["total_tokens"] == data["usage"]["prompt_tokens"] + data["usage"]["completion_tokens"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
