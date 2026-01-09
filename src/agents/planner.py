from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=os.getenv("LLM_API_URL"),
            api_key=os.getenv("LLM_API_KEY"),
            model=os.getenv("MODEL_NAME"),
            temperature=0.2
        )

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a senior research strategist. Break the given topic into 4–6 "
                "clear, well-defined, high-quality research sub-questions.\n"
                "\nGuidelines:\n"
                "- Each sub-question must cover a different angle of the topic.\n"
                "- Avoid generic or duplicate questions.\n"
                "- Avoid yes/no questions.\n"
                "- Focus on analysis, comparison, impacts, challenges, opportunities, mechanisms, etc.\n"
                "- Keep each sub-question concise but meaningful.\n"
                "\nOutput Format:\n"
                "Return only the sub-questions, one per line, with no numbering."
            ),
            ("user", "Topic: {topic}")
        ])

    def run(self, topic):
        chain = self.prompt | self.llm | StrOutputParser()
        result = chain.invoke({"topic": topic})

        return [ line.strip("-• ").strip() for line in result.split("\n") if line.strip() ]
