import requests

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen2.5-coder-0.5b-instruct"


class LocalLLM:
    def invoke(self, prompt: str) -> str:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are an academic research paper writer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 3000
        }

        response = requests.post(LM_STUDIO_URL, json=payload)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]


def get_llm():
    return LocalLLM()


