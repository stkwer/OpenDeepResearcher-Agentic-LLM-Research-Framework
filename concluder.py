from core.llm_client import ask_llm


class ConclusionAgent:
    """
    Writes a formal academic conclusion.
    """

    def write_conclusion(self, topic: str, contents: list) -> str:
        prompt = f"""
You are an academic research writer.

Write a formal conclusion for a research report on:
"{topic}"

Use the following content as context:
{contents}

Rules:
- One strong academic paragraph
- Neutral, formal tone
- No headings
- No bullet points
- No questions
- No references
"""

        response = ask_llm(prompt)

        if not response or not response.strip():
            return (
                f"In conclusion, the study of {topic.lower()} highlights its growing "
                "importance within contemporary academic discourse. The analysis "
                "demonstrates key insights, challenges, and future directions, "
                "emphasizing the need for continued research and critical evaluation."
            )

        return response.strip()
