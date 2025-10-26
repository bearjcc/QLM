# QLM - Quack Language Model 🦆

A humorous open-source project that brings the rubber duck back to debugging! QLM is a fake Large Language Model that responds to API requests with duck sounds instead of actual AI content.

[![GitHub Pages Demo](https://img.shields.io/badge/demo-GitHub%20Pages-green)](https://bearjcc.github.io/QLM/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

## What is QLM?

QLM (Quack Language Model) is an API-compatible service that mimics OpenAI's API format but responds exclusively with duck onomatopoeia. It's designed for:

- **Educational purposes**: Understanding API compatibility
- **Humor**: Bringing joy to debugging sessions
- **Testing**: Mock API responses for development
- **Easter eggs**: Hidden surprises for dedicated users

## Features

- ✅ **OpenAI API Compatible**: Drop-in replacement for testing
- ✅ **Fast & Secure**: Cryptographically secure random generation
- ✅ **Varied Responses**: 13+ different duck sounds with realistic probabilities
- ✅ **Hidden Easter Egg**: Ultra-rare response (0.001% chance)
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

3. **Test the API:**
```bash
curl -X POST http://localhost:8000/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "quack-model",
    "messages": [{"role": "user", "content": "Hello!"}]
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
| quack | 30% | Standard duck sound |
| Quack | 30% | Capitalized variant |
| Quack! | 10% | Enthusiastic quack |
| quack quack | 8% | Double quack |
| QUACK | 5% | Loud quack |
| quack! | 5% | Excited quack |
| Quack quack | 4% | Polite double |
| Other variants | ~8% | Various creative combinations |

**Hidden Response (< 0.001%)**: There's an ultra-rare easter egg that might surprise you!

## API Endpoints

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
  ]
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

**Note**: The easter egg is intentionally undocumented - discover it yourself! 🦆

## License

MIT License - feel free to use in your projects!

## Acknowledgments

- Inspired by rubber duck debugging methodology
- Built with FastAPI for speed and compatibility
- Deployed via GitHub Pages for universal access

---

**Made with 🦆 and lots of quacks by BearJCC**

*Sometimes the best debugging tool is a duck that agrees with everything you say...*
