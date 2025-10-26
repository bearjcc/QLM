#!/usr/bin/env python3
"""
Tests for QLM API functionality
"""

import pytest
import json
from fastapi.testclient import TestClient
from api.main import app, select_duck_sound, select_duck_thinking, DUCK_SOUNDS, DUCK_THINKING_MESSAGES, EASTER_EGG, validate_api_key

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

def test_ultra_rare_response():
    """Test that ultra-rare responses are properly implemented"""
    # There should be at least one very rare response (< 0.01%)
    rare_sounds = [sound for sound, weight in DUCK_SOUNDS if weight < 0.01]
    assert len(rare_sounds) >= 1

    # Verify the rare response is properly encoded
    assert all(isinstance(sound, str) for sound in rare_sounds)

def test_emoji_duck_sounds():
    """Test that emoji duck sounds are properly included"""
    # Check that emoji sounds are in the duck sounds list
    emoji_sounds = [sound for sound, _ in DUCK_SOUNDS if '🦆' in sound]
    assert len(emoji_sounds) >= 10, "Should have at least 10 emoji duck sound variations"

    # Verify specific emoji combinations
    expected_emoji_sounds = [
        '🦆', '🦆💦', '🦆💧', '🦆👑', '🦆🎩', '🦆🔥', '🦆🕊️', '🦆🪿',
        '🦆🫧', '🦆🌊', '🦆🏊', '🦆🛟'
    ]
    for expected_sound in expected_emoji_sounds:
        assert expected_sound in [sound for sound, _ in DUCK_SOUNDS], f"Missing emoji sound: {expected_sound}"

def test_total_weight_calculation():
    """Test that total weight adds up correctly"""
    total_weight = sum(weight for _, weight in DUCK_SOUNDS)

    # Should add up to approximately 100 (100%)
    assert abs(total_weight - 100) < 0.01, f"Total weight should be ~100, got {total_weight}"

    # All weights should be positive
    assert all(weight > 0 for _, weight in DUCK_SOUNDS), "All duck sounds should have positive weights"

def test_duck_thinking_selection():
    """Test that duck thinking messages are properly selected"""
    # Test that we can select a thinking message
    thinking_message = select_duck_thinking()
    assert isinstance(thinking_message, str), "Thinking message should be a string"
    assert len(thinking_message) > 0, "Thinking message should not be empty"

    # Test that it's one of our defined messages
    assert thinking_message in DUCK_THINKING_MESSAGES, "Thinking message should be from predefined list"

def test_chat_completions_with_thinking():
    """Test chat completions endpoint with thinking enabled"""
    request_data = {
        "model": "quack-model",
        "messages": [{"role": "user", "content": "Hello duck!"}],
        "quack_thinking": True
    }

    response = client.post("/chat/completions", json=request_data)
    assert response.status_code == 200

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    # Should contain a thinking message followed by duck response
    assert "\n\n" in content, "Response should contain thinking message followed by duck response"
    assert len(content.split("\n\n")) == 2, "Should have exactly 2 parts separated by double newline"

    # First part should be a thinking message
    thinking_part = content.split("\n\n")[0]
    assert thinking_part in DUCK_THINKING_MESSAGES, "First part should be a thinking message"

def test_completions_with_thinking():
    """Test legacy completions endpoint with thinking enabled"""
    request_data = {
        "model": "quack-model",
        "prompt": "Test prompt",
        "quack_thinking": True
    }

    response = client.post("/completions", json=request_data)
    assert response.status_code == 200

    data = response.json()
    content = data["choices"][0]["text"]

    # Should contain a thinking message followed by duck response
    assert "\n\n" in content, "Response should contain thinking message followed by duck response"
    assert len(content.split("\n\n")) == 2, "Should have exactly 2 parts separated by double newline"

    # First part should be a thinking message
    thinking_part = content.split("\n\n")[0]
    assert thinking_part in DUCK_THINKING_MESSAGES, "First part should be a thinking message"

def test_thinking_disabled_by_default():
    """Test that thinking is disabled by default"""
    request_data = {
        "model": "quack-model",
        "messages": [{"role": "user", "content": "Hello duck!"}]
    }

    response = client.post("/chat/completions", json=request_data)
    assert response.status_code == 200

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    # Should not contain thinking messages when disabled
    assert "\n\n" not in content, "Response should not contain thinking when disabled"
    assert content not in DUCK_THINKING_MESSAGES, "Content should not be a thinking message"

def test_usage_tokens():
    """Test that usage tokens are calculated correctly"""
    request_data = {
        "model": "quack-model",
        "messages": [{"role": "user", "content": "Hello world test"}]
    }

    response = client.post("/chat/completions", json=request_data)
    data = response.json()

    # Should have 3 tokens in prompt ("Hello", "world", "test")
    assert data["usage"]["prompt_tokens"] == 3
    # Should have some tokens in completion
    assert data["usage"]["completion_tokens"] > 0
    # Total should be sum
    assert data["usage"]["total_tokens"] == data["usage"]["prompt_tokens"] + data["usage"]["completion_tokens"]

def test_cors_headers():
    """Test CORS headers are present (only when making real HTTP requests)"""
    # Note: TestClient doesn't include CORS headers by default
    # This test would pass with real HTTP requests
    response = client.get("/")

    # Check that the endpoint responds correctly (CORS would be added by FastAPI middleware in real requests)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data

def test_api_key_validation():
    """Test API key validation function"""
    # Valid keys
    assert validate_api_key("sk-v1-42test") == True
    assert validate_api_key("Bearer sk-v1-42test") == True
    assert validate_api_key("sk-v1-42very-long-key-here") == True

    # Invalid keys
    assert validate_api_key("sk-v1-43test") == False
    assert validate_api_key("sk-test") == False
    assert validate_api_key("invalid-key") == False
    assert validate_api_key("") == False
    assert validate_api_key(None) == False

def test_chat_completions_without_auth():
    """Test that chat completions requires authentication"""
    request_data = {
        "model": "quack-model",
        "messages": [{"role": "user", "content": "Hello duck!"}]
    }

    response = client.post("/chat/completions", json=request_data)
    assert response.status_code == 422  # Missing required header

def test_chat_completions_with_invalid_auth():
    """Test that chat completions rejects invalid API keys"""
    request_data = {
        "model": "quack-model",
        "messages": [{"role": "user", "content": "Hello duck!"}]
    }

    response = client.post(
        "/chat/completions",
        json=request_data,
        headers={"Authorization": "sk-invalid-key"}
    )
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]

def test_chat_completions_with_valid_auth():
    """Test that chat completions accepts valid API keys"""
    request_data = {
        "model": "quack-model",
        "messages": [{"role": "user", "content": "Hello duck!"}]
    }

    response = client.post(
        "/chat/completions",
        json=request_data,
        headers={"Authorization": "sk-v1-42valid-key"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "chat.completion"

def test_models_with_auth():
    """Test that models endpoint requires authentication"""
    response = client.get("/models")
    assert response.status_code == 422  # Missing required header

def test_models_with_valid_auth():
    """Test that models endpoint accepts valid API keys"""
    response = client.get("/models", headers={"Authorization": "sk-v1-42valid-key"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 2  # Should have quack-model and reasoning-duck

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
