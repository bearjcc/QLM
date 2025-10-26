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
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import secrets
import random
import asyncio

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

# Track last responses to avoid duplicates (stores last N responses)
from collections import deque
RECENT_RESPONSES = deque(maxlen=5)  # Remember last 5 responses

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
    Avoids returning the same sound as the last few responses.
    """
    max_attempts = 20  # Prevent infinite loop
    attempts = 0
    
    while attempts < max_attempts:
        # Generate random float between 0 and 1 using secrets for crypto-strength randomness
        rand_value = secrets.randbelow(100000) / 100000.0

        current_weight = 0.0
        for sound, weight in DUCK_SOUNDS:
            current_weight += weight
            if rand_value <= current_weight:
                # Check if this sound was recently used
                if sound not in RECENT_RESPONSES:
                    RECENT_RESPONSES.append(sound)
                    return sound
                # If it was recent, try again
                attempts += 1
                break

    # Fallback: return any sound not in recent history
    for sound, _ in DUCK_SOUNDS:
        if sound not in RECENT_RESPONSES:
            RECENT_RESPONSES.append(sound)
            return sound
    
    # Last resort (all sounds were recent, just return a random one)
    rand_value = secrets.randbelow(100000) / 100000.0
    current_weight = 0.0
    for sound, weight in DUCK_SOUNDS:
        current_weight += weight
        if rand_value <= current_weight:
            RECENT_RESPONSES.append(sound)
            return sound
    
    # Ultimate fallback (should never happen)
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
    """Root endpoint - serves HTML landing page"""
    from fastapi.responses import HTMLResponse
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QLM - Quack Language Model</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        h1 { text-align: center; font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
        .subtitle { text-align: center; font-size: 1.2em; opacity: 0.9; margin-bottom: 30px; }
        .duck-emoji { font-size: 4em; text-align: center; margin: 20px 0; }
        .info { background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 20px; margin: 20px 0; }
        code { background: rgba(0, 0, 0, 0.3); padding: 2px 8px; border-radius: 4px; }
        .endpoint { margin: 10px 0; padding: 10px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; }
        a { color: #ffd700; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦆 QLM</h1>
        <p class="subtitle">Quack Language Model API</p>
        <div class="duck-emoji">🦆</div>
        
        <div class="info">
            <h2>API Information</h2>
            <p><strong>Version:</strong> 1.0.0</p>
            <p><strong>Status:</strong> Running</p>
            <p><strong>Description:</strong> OpenAI-compatible API that responds with duck sounds</p>
        </div>
        
        <div class="info">
            <h2>Available Endpoints</h2>
            <div class="endpoint"><code>POST /chat/completions</code> - OpenAI-compatible chat</div>
            <div class="endpoint"><code>GET /models</code> - List available models</div>
            <div class="endpoint"><code>GET /health</code> - Health check</div>
        </div>
        
        <div class="info">
            <h2>Quick Start</h2>
            <p>Use with any OpenAI-compatible client:</p>
            <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto;">
curl -X POST http://localhost:8000/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer sk-v1-42test" \\
  -d '{
    "model": "quack-model",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'</pre>
        </div>
        
        <div class="info">
            <h2>Links</h2>
            <p><a href="https://github.com/bearjcc/QLM" target="_blank">📦 GitHub Repository</a></p>
            <p><a href="https://bearjcc.github.io/QLM/" target="_blank">🌐 Interactive Demo</a></p>
            <p><a href="/health">🏥 Health Check</a></p>
            <p><a href="/models">📋 Available Models</a></p>
        </div>
        
        <p style="text-align: center; margin-top: 30px; opacity: 0.8;">
            <em>"Rubber Duckie, you're the one..." — Inspired by Ernie's timeless wisdom</em>
        </p>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

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
    request: Request,
    authorization: str = Header(None)
):
    """
    OpenAI-compatible chat completions endpoint with duck responses.
    Supports reasoning_effort parameter for OpenAI-compatible reasoning.
    Requires API key authentication (keys starting with 'sk-v1-42').
    """
    try:
        # Parse request body
        body = await request.json()
        
        # Log request for debugging
        print(f"=== INCOMING REQUEST ===")
        print(f"Model: {body.get('model', 'unknown')}")
        print(f"Stream: {body.get('stream', False)}")
        print(f"Authorization: {authorization[:20]}..." if authorization else "None")
        
        # Validate API key
        if not validate_api_key(authorization):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key. Please use a key starting with 'sk-v1-42'"
            )

        # Extract request parameters
        model = body.get("model", "quack-model")
        messages = body.get("messages", [])
        max_tokens = body.get("max_tokens", 100)
        reasoning_effort = body.get("reasoning_effort", None)
        quack_thinking = body.get("quack_thinking", False)

        # Get the last user message as prompt
        prompt = ""
        if messages:
            last_message = messages[-1]
            if last_message.get("role") == "user":
                content = last_message.get("content", "")
                
                # Handle multimodal content (Roo sends content as list)
                if isinstance(content, list):
                    # Extract text from multimodal content
                    text_parts = []
                    for part in content:
                        if isinstance(part, dict) and part.get("type") == "text":
                            text_parts.append(part.get("text", ""))
                    prompt = " ".join(text_parts)
                else:
                    prompt = content

        # Check if streaming is requested
        stream = body.get("stream", False)
        
        if stream:
            # Return streaming response
            async def generate_stream():
                # Generate the duck response
                response_data = generate_duck_response(model, prompt, reasoning_effort=reasoning_effort, thinking=quack_thinking)
                content = response_data["choices"][0]["message"]["content"]
                
                # Stream the response in chunks (character by character for effect)
                chunk_id = f"chatcmpl-{secrets.token_hex(16)}"
                
                # Send initial chunk
                yield f"data: {json.dumps({'id': chunk_id, 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': model, 'choices': [{'index': 0, 'delta': {'role': 'assistant', 'content': ''}, 'finish_reason': None}]})}\n\n"
                
                # Stream content
                for char in content:
                    chunk = {
                        "id": chunk_id,
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [{
                            "index": 0,
                            "delta": {"content": char},
                            "finish_reason": None
                        }]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
                    await asyncio.sleep(0.01)  # Small delay for streaming effect
                
                # Send final chunk with usage info (if requested)
                final_chunk = {
                    "id": chunk_id,
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop"
                    }]
                }
                
                # Include usage if stream_options.include_usage is true
                if body.get("stream_options", {}).get("include_usage", False):
                    final_chunk["usage"] = response_data["usage"]
                
                yield f"data: {json.dumps(final_chunk)}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            # Non-streaming response
            response = generate_duck_response(model, prompt, reasoning_effort=reasoning_effort, thinking=quack_thinking)
            return JSONResponse(content=response)

    except HTTPException:
        raise
    except Exception as e:
        # Log the error for debugging
        import traceback
        print(f"ERROR in chat_completions: {str(e)}")
        print(f"Model: {body.get('model', 'unknown') if 'body' in locals() else 'unknown'}")
        traceback.print_exc()
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
