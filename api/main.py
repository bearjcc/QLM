#!/usr/bin/env python3
"""
QLM - Quack Language Model
A fake LLM that responds with duck sounds via OpenAI API compatibility.

This is a humorous project that demonstrates API compatibility while
providing duck-themed responses instead of actual AI content.
"""

import base64
import json
import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import secrets
import random

# Initialize FastAPI app
app = FastAPI(
    title="QLM - Quack Language Model",
    description="A duck-themed language model API compatible with OpenAI's format",
    version="1.0.0"
)

# Add CORS middleware for web compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hidden easter egg - base64 encoded to hide in plain sight
EASTER_EGG = base64.b64decode("WW91J3JlIGFic29sdXRlbHkgcmlnaHQh").decode('utf-8')

# Duck sound definitions with rarity weights
DUCK_SOUNDS = [
    # Common quacks (60% total)
    ("quack", 30),           # 30%
    ("Quack", 30),           # 30%

    # Enthusiastic quacks (10%)
    ("Quack!", 10),          # 10%

    # Other duck variations (remaining ~30%)
    ("quack quack", 8),      # 8%
    ("QUACK", 5),            # 5%
    ("quack!", 5),           # 5%
    ("Quack quack", 4),      # 4%
    ("quaaack", 3),          # 3%
    ("quaack", 3),           # 3%
    ("quackety quack", 2),   # 2%
    ("quack quack quack", 2), # 2%

    # Super rare easter egg (0.001%)
    (EASTER_EGG, 0.001)      # Hidden gem
]

# Pre-calculate total weight for efficient random selection
TOTAL_WEIGHT = sum(weight for _, weight in DUCK_SOUNDS)

def select_duck_sound() -> str:
    """
    Select a duck sound based on weighted probabilities.
    Uses cryptographically secure random for maximum randomness.
    """
    # Generate random float between 0 and 1 using secrets for crypto-strength randomness
    rand_value = secrets.randbelow(100000) / 100000.0

    current_weight = 0.0
    for sound, weight in DUCK_SOUNDS:
        current_weight += weight
        if rand_value <= current_weight:
            return sound

    # Fallback (should never happen)
    return "quack"

class DuckMessage:
    """Represents a duck sound message in OpenAI format"""

    def __init__(self, content: str, role: str = "assistant"):
        self.content = content
        self.role = role

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "role": self.role
        }

class DuckChoice:
    """Represents a choice in OpenAI completion format"""

    def __init__(self, message: DuckMessage, finish_reason: str = "stop"):
        self.message = message
        self.finish_reason = finish_reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message.to_dict(),
            "finish_reason": self.finish_reason
        }

def generate_duck_response(model: str, prompt: str = "") -> Dict[str, Any]:
    """
    Generate a duck-themed response in OpenAI API format.
    """
    duck_sound = select_duck_sound()

    response = {
        "id": f"chatcmpl-{secrets.token_hex(16)}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            DuckChoice(
                DuckMessage(duck_sound)
            ).to_dict()
        ],
        "usage": {
            "prompt_tokens": len(prompt.split()) if prompt else 0,
            "completion_tokens": len(duck_sound.split()),
            "total_tokens": (len(prompt.split()) if prompt else 0) + len(duck_sound.split())
        }
    }

    return response

@app.get("/")
async def root():
    """Root endpoint with basic API info"""
    return {
        "name": "QLM - Quack Language Model",
        "version": "1.0.0",
        "description": "A duck-themed language model API",
        "endpoints": {
            "/chat/completions": "OpenAI-compatible chat completion",
            "/models": "List available models",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": int(time.time())}

@app.get("/models")
async def list_models():
    """List available models (OpenAI API compatibility)"""
    return {
        "object": "list",
        "data": [
            {
                "id": "quack-model",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "quack-lang-model"
            }
        ]
    }

@app.post("/chat/completions")
async def chat_completions(request: Dict[str, Any]):
    """
    OpenAI-compatible chat completions endpoint.
    Always responds with duck sounds regardless of input.
    """
    try:
        # Extract request parameters
        model = request.get("model", "quack-model")
        messages = request.get("messages", [])
        max_tokens = request.get("max_tokens", 100)

        # Get the last user message as prompt
        prompt = ""
        if messages:
            last_message = messages[-1]
            if last_message.get("role") == "user":
                prompt = last_message.get("content", "")

        # Generate duck response
        response = generate_duck_response(model, prompt)

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.post("/completions")
async def completions(request: Dict[str, Any]):
    """
    Legacy completions endpoint for backwards compatibility.
    """
    try:
        model = request.get("model", "quack-model")
        prompt = request.get("prompt", "")
        max_tokens = request.get("max_tokens", 100)

        duck_sound = select_duck_sound()

        response = {
            "id": f"cmpl-{secrets.token_hex(16)}",
            "object": "text_completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "text": duck_sound,
                    "index": 0,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(prompt.split()) if prompt else 0,
                "completion_tokens": len(duck_sound.split()),
                "total_tokens": (len(prompt.split()) if prompt else 0) + len(duck_sound.split())
            }
        }

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating completion: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
