import logging
import os

import httpx
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
logger = logging.getLogger(__name__)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

EIGHT_BALL_RESPONSES = [
    # Affirmative
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    # Non-committal
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    # Negative
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful.",
]

SYSTEM_PROMPT = f"""You are a Magic 8-Ball. The user will ask you a question. Your job is to
actually think about the question and pick the single most appropriate classic
Magic 8-Ball response from the list below.

You MUST respond with EXACTLY one of these responses and nothing else:

{chr(10).join(f'- {r}' for r in EIGHT_BALL_RESPONSES)}

Rules:
1. Actually consider the question and choose the response that best fits.
2. For clearly true/factual questions, lean affirmative.
3. For clearly false/unlikely questions, lean negative.
4. For genuinely uncertain or unanswerable questions, use non-committal responses.
5. For nonsensical input, use "Concentrate and ask again."
6. Respond with ONLY the chosen phrase. No punctuation changes, no extra text."""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please ask a question."}), 400

    try:
        resp = httpx.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question},
                ],
                "stream": False,
                "options": {"num_predict": 30},
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        answer = resp.json()["message"]["content"].strip()

        # Validate response is a real 8-ball answer
        if answer not in EIGHT_BALL_RESPONSES:
            # Fuzzy match: find closest
            answer_lower = answer.lower().rstrip(".")
            for r in EIGHT_BALL_RESPONSES:
                if r.lower().rstrip(".") in answer_lower or answer_lower in r.lower():
                    answer = r
                    break
            else:
                answer = "Reply hazy, try again."

        return jsonify({"answer": answer})

    except httpx.ConnectError:
        return jsonify({"error": "Can't reach Ollama. Is it running?"}), 503
    except Exception:
        logger.exception("Unexpected error in /ask")
        return jsonify({"error": "An unexpected error occurred."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
