import os
from google.genai import Client

MODEL_ID = "gemini-2.5-flash"

class WriterAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = Client(api_key=self.api_key)

    def run(self, topic, research_log):
        prompt = f"""
        You are a Senior Technical Research Analyst.
        
        Topic: {topic}
        
        Your task is to write a high-level, comprehensive Research Report based ONLY on the provided research data. 
        The report must be structured professionally and should NOT look like a simple list of answers.

        Follow this exact structure:
        1. **Title**: A professional title for the research.
        2. **Executive Summary**: A brief overview of the key findings.
        3. **Introduction**: Setting the context of the research topic.
        4. **Key Research Findings**: 
           - Organize the 8 sub-questions' data into logical sections with clear headings.
           - Use a narrative flow to connect the points.
           - Use bullet points only where necessary for clarity.
        5. **Analysis**: Synthesize how these findings impact the industry or the field.
        6. **Conclusion**: Final thoughts and future outlook.
        7. **References**: List the sources/URLs provided in the research data.

        RESEARCH DATA:
        {research_log}

        Important: Maintain a formal, academic tone. Cite the sources inline where possible.
        """

        response = self.client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )

        return response.text