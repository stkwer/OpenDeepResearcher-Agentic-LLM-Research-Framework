from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

class CompressorAgent:
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
                "You are a research compression agent.\n"
                "Condense the provided content into dense, high-signal research notes.\n\n"
                "Rules:\n"
                "- Extract only factual, important information\n"
                "- Remove fluff, repetition, and navigation text\n"
                "- Preserve technical accuracy\n"
                "- Write concise bullet-style research notes\n"
                "- Do NOT invent information\n"
            ),
            ("user", "{content}")
        ])

    def run(self, results):
        combined = ""

        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            content = r.get("content") or ""

            # Skip results with no usable content
            if not content.strip():
                continue

            combined += (
                f"Title: {title}\n"
                f"Source: {url}\n"
                f"Content: {content[:800]}\n\n"
            )

        if not combined.strip():
            return "No high-quality content available to compress."

        chain = self.prompt | self.llm | StrOutputParser()
        return chain.invoke({"content": combined})
