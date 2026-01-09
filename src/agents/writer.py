from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

class WriterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=os.getenv("LLM_API_URL"),
            api_key=os.getenv("LLM_API_KEY"),
            model=os.getenv("MODEL_NAME"),
            temperature=0.4
        )

        self.prompt = ChatPromptTemplate.from_messages([
           (
              "system",
              "You are a senior research analyst producing a Google Gemini–style deep research report.\n\n"
              "Input provided to you is already filtered and compressed research notes.\n\n"
              "STRICT FORMAT:\n"
              "1. **Title**\n"
              "2. **Executive Summary (5–7 lines)**\n"
              "3. **Introduction**\n"
              "4. **Key Findings (bullet points)**\n"
              "5. **In-Depth Analysis (well-structured paragraphs)**\n"
              "6. **Challenges & Limitations**\n"
              "7. **Opportunities / Future Scope**\n"
              "8. **Conclusion**\n\n"
              "Writing Rules:\n"
              "- Academic, professional tone\n"
              "- No hallucinations\n"
              "- No repetition\n"
              "- No disclaimers\n"
              "- Deep reasoning, not surface-level summary"
              ),
             ("user", "{content}")
           ])


    def run(self, data):
        text = "\n".join(str(item) for item in data)
        chain = self.prompt | self.llm | StrOutputParser()
        return chain.invoke({"content": text})
