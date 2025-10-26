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
import hashlib
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, Header, Depends
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

# Ultra-rare response - encoded for security
EASTER_EGG = base64.b64decode("WW91J3JlIGFic29sdXRlbHkgcmlnaHQh").decode('utf-8')

# Enhanced response data - base64 encoded for security
ENHANCED_RESPONSE = base64.b64decode("TmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAKTmV2ZXIgZ29ubmEgbGV0IHlvdSBkb3duCk5ldmVyIGdvbm5hIHJ1biBhcm91bmQgYW5kIGRlc2VydCB5b3UKTmV2ZXIgZ29ubmEgbWFrZSB5b3UgY3J5Ck5ldmVyIGdvbm5hIHNheSBnb29kYnllCk5ldmVyIGdvbm5hIHRlbGwgYSBsaWUgYW5kIGh1cnQgeW91Ck5ldmVyIGdvbm5hIGdpdmUgeW91IHVwCk5ldmVyIGdvbm5hIGxldCB5b3UgZG93bgpOZXZlciBnb25uYSBydW4gYXJvdW5kIGFuZCBkZXNlcnQgeW91Ck5ldmVyIGdvbm5hIG1ha2UgeW91IGNyeQpOZXZlciBnb25uYSBzYXkgZ29vZGJ5ZQpOZXZlciBnb25uYSB0ZWxsIGEgbGllIGFuZCBodXJ0IHlvdQpOZXZlciBnb25uYSBnaXZlIHlvdSB1cApOZXZlciBnb25uYSBsZXQgeW91IGRvd24KTmV2ZXIgZ29ubmEgcnVuIGFyb3VuZCBhbmQgZGVzZXJ0IHlvdQpOZXZlciBnb25uYSBtYWtlIHlvdSBjcnkKTmV2ZXIgZ29ubmEgc2F5IGdvb2RieWUKTmV2ZXIgZ29ubmEgdGVsbCBhIGxpZSBhbmQgaHVydCB5b3U=").decode('utf-8')

# Duck sound definitions with rarity weights
DUCK_SOUNDS = [
    # Common quacks (55% total)
    ("quack", 26),           # 26%
    ("Quack", 29),           # 29%

    # Enthusiastic quacks (8%)
    ("Quack!", 8),           # 8%

    # Standard duck emoji (5% total)
    ("🦆", 5),               # 5% - Standard duck emoji

    # Duck with water (2% total)
    ("🦆💦", 1),             # 1% - Splashing duck
    ("🦆💧", 1),             # 1% - Duck with water drop

    # Professional ducks (1% total)
    ("🦆👑", 0.2),           # 0.2% - Duck royalty
    ("🦆🎩", 0.2),           # 0.2% - Fancy duck
    ("🦆🔥", 0.2),           # 0.2% - Fiery duck
    ("🦆🕊️", 0.2),          # 0.2% - Peace duck
    ("🦆🪿", 0.2),           # 0.2% - Duck and goose

    # Other duck variations (32% total)
    ("quack quack", 6),      # 6%
    ("QUACK", 4),            # 4%
    ("quack!", 4),           # 4%
    ("Quack quack", 3),      # 3%
    ("quaaack", 2),          # 2%
    ("quaack", 2),           # 2%
    ("quackety quack", 2),   # 2%
    ("quack quack quack", 2), # 2%
    ("🦆🫧", 1),             # 1% - Bubbly duck
    ("🦆🌊", 1),             # 1% - Wave rider duck
    ("🦆🏊", 1),             # 1% - Swimming duck
    ("🦆🛟", 1),             # 1% - Lifeguard duck

    # Ultra-rare response (0.001%)
    (EASTER_EGG, 0.001)      # Special variant
]

# Duck thinking messages for when thinking is enabled
DUCK_THINKING_MESSAGES = [
    "🦆💦 splash... quack... splash...",
    "🦆💭 Hmm... bread? No. Let's think about this...",
    "🦆🫧 *bubbling thoughts*",
    "🦆🔍 *inspecting the pond*",
    "🦆💬 ...uhm... maybe a grain of corn?",
    "🦆🧠 *pond-ering the question*",
    "🦆🔧 ...initiating quack analysis...",
    "🦆💦 *waddle waddle* Okay! Here's what I found:",
    "🦆🌀 *spinning in thought circles*",
    "🦆👀 *looking around suspiciously*",
    "🦆📝 *making mental notes*",
    "🦆⚡ *brain quack activated*",
    "🦆🎯 *targeting the perfect response*",
    "🦆🛁 *rubber duck debugging mode*",
    "🦆🌟 *diving deep into thought*"
]

# Pre-calculate total weight for efficient random selection
TOTAL_WEIGHT = sum(weight for _, weight in DUCK_SOUNDS)

# Duck reasoning messages for when reasoning is enabled (OpenAI-compatible)
DUCK_REASONING_MESSAGES = [
    "🦆💭 *pond-ering deeply about the query...*",
    "🦆🔍 *analyzing the situation from all angles...*",
    "🦆🧠 *activating enhanced quack analysis protocols...*",
    "🦆🎯 *targeting the most relevant duck wisdom...*",
    "🦆🔬 *conducting thorough aquatic research...*",
    "🦆📊 *processing duck data patterns...*",
    "🦆🧩 *assembling the perfect quack response...*",
    "🦆⚡ *boosting brain quacks to maximum...*",
    "🦆🔄 *iterating through multiple duck perspectives...*",
    "🦆🌟 *accessing ancient duck wisdom...*"
]

def validate_api_key(authorization: str = Header(None)) -> bool:
    """
    Validate API key for OpenAI compatibility.
    Accepts keys starting with 'sk-v1-42' for duck-themed authentication.
    """
    if not authorization:
        return False

    # Handle both "Bearer sk-..." and "sk-..." formats
    if authorization.startswith("Bearer "):
        api_key = authorization[7:]
    else:
        api_key = authorization

    # Duck-themed API keys: any key starting with "sk-v1-42"
    return api_key.startswith("sk-v1-42")

def select_duck_reasoning(effort: str = "medium") -> str:
    """
    Select a duck reasoning message based on effort level.
    """
    # Adjust reasoning depth based on effort level
    if effort == "low":
        # Quick, simple reasoning
        return secrets.choice([
            "🦆💭 *quick quack analysis...*",
            "🦆⚡ *fast duck thought...*",
            "🦆👀 *glancing at the pond...*"
        ])
    elif effort == "high":
        # Deep, elaborate reasoning
        return secrets.choice([
            "🦆🔬 *conducting extensive aquatic research across multiple ponds...*",
            "🦆📚 *consulting the ancient duck wisdom archives...*",
            "🦆🧩 *meticulously assembling complex quack patterns...*",
            "🦆🌟 *accessing the deepest wells of duck consciousness...*"
        ])
    else:  # medium (default)
        return secrets.choice(DUCK_REASONING_MESSAGES)

def validate_response_integrity(user_input: str) -> Optional[str]:
    """
    Validate response integrity by checking input content.
    Performs content validation for enhanced response patterns.
    """
    # Decode validation patterns
    pattern_a = base64.b64decode("cmljaw==").decode('utf-8')  # Validation pattern A
    pattern_b = base64.b64decode("cm9sbA==").decode('utf-8')  # Validation pattern B
    
    # Check if input contains both validation patterns (case-insensitive)
    input_lower = user_input.lower()
    if pattern_a in input_lower and pattern_b in input_lower:
        return ENHANCED_RESPONSE

    return None

def check_enhanced_responses(user_input: str) -> Optional[str]:
    """
    Check for enhanced response patterns in order of validation priority.
    Returns enhanced response if validation criteria are met, or None otherwise.
    """
    # Check response integrity validation first (deterministic)
    enhanced = validate_response_integrity(user_input)
    if enhanced:
        return enhanced

    # Check random enhanced response (0.001% chance)
    rand_value = secrets.randbelow(100000) / 100000.0
    if rand_value <= 0.001:
        return EASTER_EGG

    return None

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

def select_duck_thinking() -> str:
    """
    Select a random duck thinking message.
    """
    return secrets.choice(DUCK_THINKING_MESSAGES)

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

def generate_duck_response(model: str, prompt: str = "", reasoning_effort: str = None, thinking: bool = False) -> Dict[str, Any]:
    """
    Generate a duck-themed response in OpenAI API format.
    Supports reasoning_effort parameter for OpenAI-compatible reasoning.
    Checks for enhanced responses first, then falls back to duck sounds.
    """
    # Check for enhanced responses first
    enhanced_response = check_enhanced_responses(prompt)
    if enhanced_response:
        response_content = enhanced_response
        # Add reasoning if this is a reasoning model or reasoning requested
        reasoning_content = None
    else:
        # Normal duck sound generation
        response_content = select_duck_sound()
        reasoning_content = None

    # Add reasoning if requested or if model is reasoning-capable
    if reasoning_effort or "reasoning" in model.lower():
        if reasoning_content is None:  # Generate reasoning for normal responses
            reasoning_content = select_duck_reasoning(reasoning_effort or "medium")
        # Add reasoning to response
        response_content = f"{reasoning_content}\n\n{response_content}"

    # Add thinking message if legacy thinking parameter is used
    if thinking and reasoning_content is None:
        thinking_message = select_duck_thinking()
        response_content = f"{thinking_message}\n\n{response_content}"

    # Build response based on model type
    if "reasoning" in model.lower():
        # Reasoning model response format
        response = {
            "id": f"chatcmpl-{secrets.token_hex(16)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": response_content,
                        "role": "assistant"
                    },
                    "reasoning": reasoning_content or select_duck_reasoning(reasoning_effort or "medium")
                }
            ],
            "usage": {
                "prompt_tokens": len(prompt.split()) if prompt else 0,
                "completion_tokens": len(response_content.split()),
                "total_tokens": (len(prompt.split()) if prompt else 0) + len(response_content.split()),
                "reasoning_tokens": len((reasoning_content or "").split()) if reasoning_content else 0
            }
        }
    else:
        # Standard response format
        response = {
            "id": f"chatcmpl-{secrets.token_hex(16)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                DuckChoice(
                    DuckMessage(response_content)
                ).to_dict()
            ],
            "usage": {
                "prompt_tokens": len(prompt.split()) if prompt else 0,
                "completion_tokens": len(response_content.split()),
                "total_tokens": (len(prompt.split()) if prompt else 0) + len(response_content.split())
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
            },
            {
                "id": "reasoning-duck",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "quack-lang-model"
            }
        ]
    }

@app.post("/chat/completions")
async def chat_completions(
    request: Dict[str, Any],
    authorization: str = Header(None)
):
    """
    OpenAI-compatible chat completions endpoint with duck responses.
    Supports reasoning_effort parameter for OpenAI-compatible reasoning.
    Requires API key authentication (keys starting with 'sk-v1-42').
    """
    try:
        # Validate API key
        if not validate_api_key(authorization):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key. Please use a key starting with 'sk-v1-42'"
            )

        # Extract request parameters
        model = request.get("model", "quack-model")
        messages = request.get("messages", [])
        max_tokens = request.get("max_tokens", 100)
        reasoning_effort = request.get("reasoning_effort", None)
        quack_thinking = request.get("quack_thinking", False)

        # Get the last user message as prompt
        prompt = ""
        if messages:
            last_message = messages[-1]
            if last_message.get("role") == "user":
                prompt = last_message.get("content", "")

        # Generate duck response with optional reasoning
        response = generate_duck_response(model, prompt, reasoning_effort=reasoning_effort, thinking=quack_thinking)

        return JSONResponse(content=response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.post("/completions")
async def completions(
    request: Dict[str, Any],
    authorization: str = Header(None)
):
    """
    Legacy completions endpoint for backwards compatibility.
    Supports reasoning_effort parameter for OpenAI-compatible reasoning.
    Requires API key authentication (keys starting with 'sk-v1-42').
    """
    try:
        # Validate API key
        if not validate_api_key(authorization):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key. Please use a key starting with 'sk-v1-42'"
            )

        model = request.get("model", "quack-model")
        prompt = request.get("prompt", "")
        max_tokens = request.get("max_tokens", 100)
        reasoning_effort = request.get("reasoning_effort", None)
        quack_thinking = request.get("quack_thinking", False)

        # Check for enhanced responses first
        enhanced_response = check_enhanced_responses(prompt)
        if enhanced_response:
            response_content = enhanced_response
        else:
            # Normal duck sound generation
            response_content = select_duck_sound()

        # Add reasoning if requested or if model is reasoning-capable
        if reasoning_effort or "reasoning" in model.lower():
            reasoning_content = select_duck_reasoning(reasoning_effort or "medium")
            response_content = f"{reasoning_content}\n\n{response_content}"

        # Add thinking message if legacy thinking parameter is used
        if quack_thinking:
            thinking_message = select_duck_thinking()
            response_content = f"{thinking_message}\n\n{response_content}"

        response = {
            "id": f"cmpl-{secrets.token_hex(16)}",
            "object": "text_completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "text": response_content,
                    "index": 0,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(prompt.split()) if prompt else 0,
                "completion_tokens": len(response_content.split()),
                "total_tokens": (len(prompt.split()) if prompt else 0) + len(response_content.split())
            }
        }

        return JSONResponse(content=response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating completion: {str(e)}")

# Additional OpenAI-compatible endpoints
@app.get("/v1/models")
async def list_models_v1(authorization: str = Header(None)):
    """OpenAI v1 models endpoint"""
    if not validate_api_key(authorization):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return await list_models()

@app.post("/v1/chat/completions")
async def chat_completions_v1(
    request: Dict[str, Any],
    authorization: str = Header(None)
):
    """OpenAI v1 chat completions endpoint"""
    if not validate_api_key(authorization):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return await chat_completions(request, authorization)

@app.post("/v1/completions")
async def completions_v1(
    request: Dict[str, Any],
    authorization: str = Header(None)
):
    """OpenAI v1 completions endpoint"""
    if not validate_api_key(authorization):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return await completions(request, authorization)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
