import os
from google import genai

class WriterAgent:
    def __init__(self):
        # Pulls the Gemini key from your .env file
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"

    def run(self, topic, research_log):
        prompt = f"""
        You are a Professional Technical Writer.
        
        TOPIC: {topic}
        
        RESEARCH DATA GATHERED:
        {research_log}
        
        TASK:
        Write a comprehensive, highly structured research report based on the data above.
        1. Use clear Markdown headings (##, ###).
        2. Include an Introduction and Conclusion.
        3. Use bullet points for key facts.
        4. Cite the sources provided in the research data.
        5. Use a professional and analytical tone.
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text