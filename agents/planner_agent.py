import os
from google.genai import Client
from google.genai import types

MODEL_ID = "gemini-2.5-flash"

class PlannerAgent:
    def __init__(self, api_key=None):
        # Agar key nahi di to .env se uthayega
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = Client(api_key=self.api_key)

    def run(self, topic):
        prompt = f"""
        You are a Research Planner. Topic: "{topic}"
        Generate exactly 8 specific sub-questions required to write a report.
        Return ONLY the questions, one per line.
        """
        response = self.client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        return [q.strip() for q in response.text.split("\n") if q.strip()][:8]