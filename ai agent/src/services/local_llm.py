from openai import OpenAI

class LocalLLM:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"  # dummy key, required by SDK
        )

        self.model = "qwen2.5-coder-0.5b-instruct"

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an academic research paper writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        return response.choices[0].message.content.strip()
