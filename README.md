# Magic 8-Ball (LLM-powered)

A Magic 8-Ball web app that uses Claude to actually understand your question and pick the most fitting classic 8-Ball response.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env
```

## Run

```bash
python app.py
```

Then open http://localhost:5000

## How it works

Instead of picking a random response, the app sends your question to Claude Haiku which considers the question and selects the most appropriate classic Magic 8-Ball answer from the original 20 responses.
