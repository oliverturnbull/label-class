# Magic 8-Ball (LLM-powered)

A Magic 8-Ball web app that uses a local LLM via [Ollama](https://ollama.com) to actually understand your question and pick the most fitting classic 8-Ball response.

## Prerequisites

Install [Ollama](https://ollama.com) and pull a model:

```bash
ollama pull llama3.2
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
ollama serve    # if not already running
python app.py
```

Then open http://localhost:5000

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434/api/chat` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3.2` | Model to use for responses |

## How it works

Instead of picking a random response, the app sends your question to a local LLM (Llama 3.2 via Ollama) which considers the question and selects the most appropriate classic Magic 8-Ball answer from the original 20 responses. No API keys required.
