import re
import time
from core.llm_client import ask_llm


class WriterAgent:
    """
    Writes clean academic content.
    - No references
    - No citations
    - No markdown
    - One coherent paragraph per section
    """

    def write_section(
        self,
        sub_question: str,
        search_results: list,
        retries: int = 3
    ) -> str:
        for attempt in range(retries):
            try:
                return self._generate(sub_question, search_results)
            except Exception:
                if attempt == retries - 1:
                    return self._fallback(sub_question)
                time.sleep(2)

    def _generate(self, sub_question: str, search_results: list) -> str:
        information = ""

        for r in search_results:
            summary = r.get("summary", "").strip()
            if summary:
                information += f"{summary}\n"

        if information:
            prompt = f"""
You are an academic research writer.

Write ONE well-structured academic paragraph that answers the
research question below using ONLY the provided information.

Research Question:
{sub_question}

Background Information:
{information}

Strict Rules:
- One paragraph only
- Formal academic tone
- No headings
- No citations
- No references
- No markdown
- No bullet points
- Neutral and objective style
"""
        else:
            prompt = f"""
You are an academic research writer.

Write ONE well-structured academic paragraph that answers the
research question below based on general academic knowledge.

Research Question:
{sub_question}

Strict Rules:
- One paragraph only
- Formal academic tone
- No headings
- No citations
- No references
- No markdown
- No bullet points
- Neutral and objective style
"""

        response = ask_llm(prompt)

        if not response or not response.strip():
            raise RuntimeError("Empty LLM response")

        # Remove any hidden chain-of-thought
        cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)

        return cleaned.strip()

    def _fallback(self, sub_question: str) -> str:
        return (
            f"This section discusses {sub_question.lower()} by examining its "
            "fundamental concepts, relevance, and implications within the "
            "broader academic and practical context."
        )
