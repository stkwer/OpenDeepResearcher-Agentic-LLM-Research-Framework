import os
import json
import requests

class LocalLLM:
    def __init__(self, base_url=None, api_key=None, model=None):
        self.base_url = base_url or os.environ.get("LOCAL_API_BASE")
        self.api_key = api_key or os.environ.get("LOCAL_API_KEY", "local")
        self.model = model or os.environ.get("LOCAL_MODEL")

        if not self.base_url or not self.model:
            raise RuntimeError("Set LOCAL_API_BASE and LOCAL_MODEL before using LocalLLM.")

    def chat(self, system_prompt, user_prompt, temperature=0.0, max_tokens=300):
        url = self.base_url.rstrip("/") + "/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


class PlannerAgent:
    def __init__(self, llm=None):
        self.llm = llm or LocalLLM()

    def plan(self, query: str) -> dict:
        system = (
            "You are a Planner Agent.\n"
            "Your ONLY task is to generate 6-9 sub-questions.\n"
            "Do NOT answer the query.\n"
            "Do NOT provide explanations or facts.\n"
            "Each sub-question must be specific, clear, and independently answerable.\n\n"
            "Return ONLY valid JSON in this format:\n"
            "{\"steps\": [\"question1\", \"question2\", ...]}"
        )

        user = f"Generate sub-questions for the topic:\n{query}"

        response = self.llm.chat(system, user)

        start = response.find("{")
        end = response.rfind("}") + 1
        return json.loads(response[start:end])


if __name__ == "__main__":
    topic = input("\nEnter a topic: ").strip()
    if not topic:
        topic = "Explain any topic"

    planner = PlannerAgent()
    plan = planner.plan(topic)

    print("\n===== PLANNER OUTPUT =====\n")
    for i, step in enumerate(plan["steps"], start=1):
        print(f"{i}. {step}")
