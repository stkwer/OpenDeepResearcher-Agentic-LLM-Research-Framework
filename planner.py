import re
from core.llm_client import ask_llm


class PlannerAgent:
    def plan(self, query: str) -> list[str]:
        prompt = f"""
You are an expert academic research planner.

Generate 5–7 high-quality academic research questions
for a research paper on the topic below.

TOPIC:
"{query}"

RULES:
- Each item must be a full academic question
- Minimum 10 words per question
- Output ONLY a numbered list
- No explanations
"""

        response = ask_llm(prompt)

        if not response:
            return self._fallback()

        response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)

        questions = []
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                continue
            cleaned = re.sub(r"^\d+[\.\)]\s*", "", line)
            if len(cleaned.split()) >= 8:
                questions.append(cleaned)

        return questions if len(questions) >= 3 else self._fallback()

    def _fallback(self):
        return [
            "What theoretical frameworks explain the core concepts of the topic?",
            "What key mechanisms influence outcomes in this domain?",
            "What empirical evidence supports current academic understanding?",
            "What limitations affect existing approaches?",
            "What future research directions are most promising?"
        ]
