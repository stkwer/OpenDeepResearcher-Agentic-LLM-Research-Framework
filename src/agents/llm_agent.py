from dataclasses import dataclass
from src.services.lmstudio_client import chat_with_lmstudio


@dataclass
class LLMAgent:
    name: str = "local_llm"

    def run(self, query: str, context: str | None = None) -> str:
        prompt = query
        if context:
            prompt = (
                "Use the following context to answer the question.\n\n"
                f"Context:\n{context}\n\nQuestion:\n{query}"
            )
        return chat_with_lmstudio(prompt)
