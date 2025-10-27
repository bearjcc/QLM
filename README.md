---
title: QLM - Quack Language Model
emoji: 🦆
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# QLM - Quack Language Model 🦆

A humorous open-source project that brings the rubber duck back to debugging! QLM is a fake Large Language Model that responds to API requests with duck sounds instead of actual AI content.

[![GitHub Pages Demo](https://img.shields.io/badge/demo-GitHub%20Pages-green)](https://bearjcc.github.io/QLM/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

## What is QLM?

While others chase AGI, we've achieved **ADI: Artificial Duck Intelligence**.

QLM (Quack Language Model) is an OpenAI-compatible API that responds exclusively with duck sounds. Some might be stuck on a high horse. We're not sure how to get down from a duck.

**Use Cases:**
- **Rubber Duck Debugging**: Now with actual ducks
- **API Testing**: Mock OpenAI-compatible responses
- **Humor**: Bringing joy back to development
- **Demonstrating API Compatibility**: Educational and entertaining

## Features

- ✅ **OpenAI API Compatible**: Full compatibility with `/v1/*` endpoints
- ✅ **API Key Authentication**: Secure authentication with duck-themed keys (`sk-v1-42...`)
- ✅ **Duck Reasoning**: `reasoning_effort` parameter for OpenAI-compatible reasoning
- ✅ **Multiple Models**: Standard (`quack-model`) and reasoning (`reasoning-duck`) models
- ✅ **Rich Duck Emojis**: 24+ different duck sounds, emojis, and combinations
- ✅ **Varied Responses**: No consecutive duplicates for more entertaining interactions
- ✅ **Web Interface**: Interactive demo via GitHub Pages
- ✅ **Production Ready**: CORS support, error handling, logging

## Quick Start

### Local Development

1. **Clone and setup:**
```bash
git clone https://github.com/bearjcc/QLM.git
cd QLM
pip install -r requirements.txt
```

2. **Run the API server:**
```bash
cd api
python main.py
```

3. **Test the API (requires authentication):**
```bash
curl -X POST http://localhost:8000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-v1-42your-api-key-here" \
  -d '{
    "model": "quack-model",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

**⚠️ Authentication Required:** All API endpoints require an API key starting with `sk-v1-42`. Requests without proper authentication will return a 401 error.

**With Reasoning:**
```bash
curl -X POST http://localhost:8000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-v1-42your-api-key-here" \
  -d '{
    "model": "reasoning-duck",
    "messages": [{"role": "user", "content": "Help debug this code!"}],
    "reasoning_effort": "high"
  }'
```

4. **Open the web interface:**
```bash
cd frontend
# Open index.html in your browser
```

### Using with OpenAI Client

QLM works as a drop-in replacement for OpenAI API:

```python
import openai

# Point to QLM instead of OpenAI
openai.api_base = "http://localhost:8000"
openai.api_key = "not-needed"

response = openai.ChatCompletion.create(
    model="quack-model",
    messages=[{"role": "user", "content": "Help me debug this code!"}]
)

print(response.choices[0].message.content)  # "Quack!" or similar
```

## Duck Sound Distribution

QLM generates responses based on realistic duck sound probabilities:

| Sound | Probability | Description |
|-------|-------------|-------------|
| quack | 26% | Standard duck sound |
| Quack | 29% | Capitalized variant |
| Quack! | 8% | Enthusiastic quack |
| 🦆 | 5% | Standard duck emoji |
| 🦆💦 | 1% | Splashing duck |
| 🦆💧 | 1% | Duck with water drop |
| 🦆👑 | 0.2% | Duck royalty |
| 🦆🎩 | 0.2% | Fancy duck |
| 🦆🔥 | 0.2% | Fiery duck |
| 🦆🕊️ | 0.2% | Peace duck |
| 🦆🪿 | 0.2% | Duck and goose |
| 🦆🫧 | 1% | Bubbly duck |
| 🦆🌊 | 1% | Wave rider duck |
| 🦆🏊 | 1% | Swimming duck |
| 🦆🛟 | 1% | Lifeguard duck |
| quack quack | 6% | Double quack |
| QUACK | 4% | Loud quack |
| quack! | 4% | Excited quack |
| Quack quack | 3% | Polite double |
| Other variants | 8% | Various creative combinations |

### Duck Thinking Feature

Enable duck-themed thinking messages by setting `quack_thinking: true` in your request:

**Example Response with Thinking:**
```json
{
  "choices": [{
    "message": {
      "content": "🦆💦 splash... quack... splash...\n\n🦆🫧",
      "role": "assistant"
    }
  }]
}
```

**Available Thinking Messages:**
- `🦆💦 splash... quack... splash...`
- `🦆💭 Hmm... bread? No. Let's think about this...`
- `🦆🫧 *bubbling thoughts*`
- `🦆🔍 *inspecting the pond*`
- And 11 more silly duck-themed thinking variations!

The system uses cryptographically secure random generation to ensure fair distribution of all duck sounds.

## Available Models

- **`quack-model`**: Standard duck responses with basic functionality
- **`reasoning-duck`**: Advanced model with reasoning capabilities and enhanced responses

## API Endpoints

All endpoints require authentication with an API key starting with `sk-v1-42`.

### Chat Completions (OpenAI Compatible)
```
POST /chat/completions
```
Standard OpenAI chat completion format with duck responses.

**Request:**
```json
{
  "model": "quack-model",
  "messages": [
    {"role": "user", "content": "Your message here"}
  ],
  "reasoning_effort": "medium",  // Optional: "low", "medium", "high"
  "quack_thinking": true         // Optional: Enable duck-themed thinking messages
}
```

**Authentication:**
```
Authorization: Bearer sk-v1-42your-api-key-here
```

**Response (Reasoning Model):**
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "reasoning-duck",
  "choices": [{
    "message": {
      "content": "🦆🔬 *conducting aquatic research...*\n\n🦆",
      "role": "assistant"
    },
    "reasoning": "🦆🔬 *conducting aquatic research...*",
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 3,
    "completion_tokens": 5,
    "reasoning_tokens": 4,
    "total_tokens": 12
  }
}
```

**Response:**
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1699123456,
  "model": "quack-model",
  "choices": [{
    "message": {
      "content": "Quack!",
      "role": "assistant"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 4,
    "completion_tokens": 1,
    "total_tokens": 5
  }
}
```

### Legacy Completions
```
POST /completions
```
Backwards compatible with older OpenAI API format.

**Request:**
```json
{
  "model": "quack-model",
  "prompt": "Your message here",
  "reasoning_effort": "high",  // Optional: "low", "medium", "high"
  "quack_thinking": true       // Optional: Enable duck-themed thinking messages
}
```

**Authentication:**
```
Authorization: Bearer sk-v1-42your-api-key-here
```

### Health Check
```
GET /health
```
Returns API health status.

### Models List
```
GET /models
```
Lists available models (currently just "quack-model").

## Deployment

### GitHub Pages (Frontend Only)

1. **Enable GitHub Pages:**
   - Go to repository Settings > Pages
   - Set source to "Deploy from a branch"
   - Select "main" branch and "/frontend" folder

2. **Access the demo:**
   - Frontend: `https://bearjcc.github.io/QLM/`
   - Note: GitHub Pages doesn't support server-side APIs

### Production Server

For full API functionality, deploy to a server with Python support:

```bash
# Using gunicorn
pip install gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

Or use Docker:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY api/ ./api/
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Configuration

Environment variables:
- `PORT`: Server port (default: 8000)
- No authentication required (intentionally public)

## Testing

Run the included tests:
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - feel free to use in your projects!

## Why QLM?

**State-of-the-art ADI Technology**: While competitors focus on billions of parameters, we've mastered the most important one: quack.

**Unparalleled Accuracy**: 100% of our responses are duck sounds. Other models can only dream of such consistency.

**Ethical AI**: Our ducks never hallucinate. They're just ducks.

**Energy Efficient**: Trained on a single pond. Carbon footprint: one bread crumb.

## Acknowledgments

- Inspired by rubber duck debugging methodology
- Powered by ADI (Artificial Duck Intelligence)
- Built with FastAPI for maximum quackability
- Hosted on Hugging Face Spaces

---

**Made with 🦆 and ADI by BearJCC**

*"Rubber Duckie, you're the one..." — Inspired by Ernie's timeless wisdom*
