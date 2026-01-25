import requests

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

def ask_llm(prompt: str, timeout: int = 120) -> str | None:
    payload = {
        "model": "local-model",  # REQUIRED by LM Studio
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }

    try:
        response = requests.post(
            LM_STUDIO_URL,
            json=payload,
            timeout=timeout
        )

        if response.status_code != 200:
            print("❌ LLM Error:", response.text)
            return None

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        print("❌ LLM Error: request timed out")
        return None

    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return None
