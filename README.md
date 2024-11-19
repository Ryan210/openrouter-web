# Open Router Web Interface

A web interface for OpenRouter AI API, supporting both chat and image generation capabilities.

## Features
- Chat with AI models
- Generate images from text descriptions

## Deployment Steps

1. Fork this repository
2. Create a new Web Service on Render.com
3. Connect your GitHub repository
4. Add environment variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key
5. Deploy the application

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
OPENROUTER_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python app.py
```
