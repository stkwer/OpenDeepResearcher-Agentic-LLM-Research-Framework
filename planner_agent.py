import os
from google import genai
from google.genai import types

class PlannerAgent:
    def __init__(self):
        # Initializing the client inside the agent
        self.client = genai.Client(api_key=os.getenv("AIzaSyBcXgVLQUtwE2V_bRhHWtwvsc3UUxwxwXM"))
        self.model_id = "gemini-2.5-flash"

    def run(self, topic):
        prompt = f"Generate 8 research questions for the topic: {topic}. Return only the questions, one per line."
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        # Convert the text response into a list of strings
        return [q.strip() for q in response.text.strip().split('\n') if q.strip()]