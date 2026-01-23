import os, requests
from dotenv import load_dotenv

load_dotenv()

LMSTUDIO_URL = os.getenv("LMSTUDIO_URL")
MODEL = os.getenv("LOCAL_MODEL_NAME")
TIMEOUT = int(os.getenv("TIMEOUT", 180))

PROMPT = """
You are a STRICT research planning agent.

ABSOLUTE RULES:
- DO NOT rewrite the question
- DO NOT rephrase
- DO NOT correct grammar
- DO NOT add new meaning

The MAIN QUESTION must be EXACTLY the same text as the user input.

Task:
Generate 5–7 meaningful sub-questions that help deeply research the topic.

FORMAT (FOLLOW EXACTLY):

MAIN QUESTION:
{question}

SUB-QUESTIONS:
1. ...
2. ...
3. ...
4. ...
5. ...
"""

def plan(question):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": PROMPT.format(question=question)}
        ],
        "temperature": 0,
        "max_tokens": 400
    }

    r = requests.post(
        f"{LMSTUDIO_URL}/v1/chat/completions",
        json=payload,
        timeout=TIMEOUT
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]