---
project: QLM
status: active
area: Technology
energy: medium
deadline:
tags: [python, api, fastapi, github-pages, open-source, humor]
created: 2025-10-27
---

# QLM - Quack Language Model 🦆

**Status**: 🚧 Active Development
**Energy**: Medium
**Location**: [GitHub/Self/QLM](C:\GitHub\Self\QLM) (junctioned here)

## Project Overview

A humorous open-source project that brings the rubber duck back to debugging! QLM is a fake Large Language Model that responds to API requests with duck sounds instead of actual AI content.

### Why This Project?

- **Educational**: Demonstrates API compatibility and FastAPI usage
- **Humor**: Rubber duck debugging with a technical twist
- **Portfolio Piece**: Shows API design and frontend skills
- **Open Source**: Publicly available for others to enjoy

## Technical Implementation

### Core Features
- ✅ OpenAI API compatible endpoints (`/chat/completions`, `/completions`)
- ✅ FastAPI server with proper CORS support
- ✅ Cryptographically secure random duck sound generation
- ✅ Weighted probability system for realistic duck responses
- ✅ Hidden easter egg (0.001% chance) - base64 encoded in source

### Duck Sound Distribution
| Sound | Probability | Rarity |
|-------|-------------|---------|
| quack | 30% | Common |
| Quack | 30% | Common |
| Quack! | 10% | Uncommon |
| quack quack | 8% | Uncommon |
| Other variants | ~22% | Various |
| **Hidden Response** | **0.001%** | **Ultra Rare** |

### API Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /models` - List models
- `POST /chat/completions` - OpenAI-compatible chat
- `POST /completions` - Legacy completions

## Development Status

### ✅ Completed
- [x] FastAPI server with OpenAI compatibility
- [x] Duck sound generation algorithm
- [x] Hidden easter egg implementation
- [x] GitHub Pages frontend
- [x] README documentation
- [x] Vault junction setup

### 🔄 In Progress
- [ ] Git repository initialization
- [ ] GitHub Pages deployment
- [ ] Testing and validation

### 📋 Next Steps
- [ ] Push to GitHub repository
- [ ] Configure GitHub Pages
- [ ] Add comprehensive tests
- [ ] Create deployment scripts

## File Structure

```
QLM/
├── api/
│   └── main.py              # FastAPI server
├── frontend/
│   └── index.html           # GitHub Pages demo
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## GitHub Integration

**Repository**: `https://github.com/bearjcc/QLM`
**Frontend**: `https://bearjcc.github.io/QLM/`
**Status**: Public open source

## Usage Examples

### API Usage
```python
import openai

openai.api_base = "http://localhost:8000"
response = openai.ChatCompletion.create(
    model="quack-model",
    messages=[{"role": "user", "content": "Help debug this!"}]
)
print(response.choices[0].message.content)  # "Quack!"
```

### Local Development
```bash
cd C:\GitHub\Self\QLM
pip install -r requirements.txt
cd api && python main.py
# API available at http://localhost:8000
```

## Easter Egg Hunt

There's a hidden response that's extremely rare (0.001% chance). It's encoded in the source code in plain sight - can you find it? 🦆

## Links & References

- **Repo Junction**: [[C:\GitHub\Self\QLM]]
- **API Server**: [[api/main.py]]
- **Frontend Demo**: [[frontend/index.html]]
- **Documentation**: [[README.md]]

## Notes

This project combines humor with technical skills - perfect for demonstrating API design, random algorithms, and frontend deployment. The hidden easter egg adds an element of surprise for users who interact with it enough!
