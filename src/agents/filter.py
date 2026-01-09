from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

class FilterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=os.getenv("LLM_API_URL"),
            api_key=os.getenv("LLM_API_KEY"),
            model=os.getenv("MODEL_NAME"),
            temperature=0.1
        )

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a research quality evaluator.\n"
                "You will receive a list of web search results.\n"
                "Your task is to keep ONLY high-quality, relevant, non-duplicate sources.\n\n"
                "Rules:\n"
                "- Remove duplicates\n"
                "- Remove irrelevant or low-information sources\n"
                "- Keep the best 4–6 sources max\n\n"
                "Return the filtered list as JSON array."
            ),
            ("user", "{data}")
        ])

    def run(self, results):
        chain = self.prompt | self.llm | JsonOutputParser()
        return chain.invoke({"data": results})
