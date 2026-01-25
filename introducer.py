from core.llm_client import ask_llm


class IntroductionAgent:
    """
    Writes a formal academic introduction section.
    """

    def write_intro(self, topic: str) -> str:
        prompt = f"""
You are an academic research writer.

Write a formal introduction for a research report on:
"{topic}"

Rules:
- 1–2 short academic paragraphs
- Neutral, formal tone
- No questions
- No bullet points
- No headings
- No references
"""

        response = ask_llm(prompt)

        if not response or not response.strip():
            return (
                f"The topic of {topic.lower()} has gained increasing attention due to its "
                "significant influence on modern academic and professional discourse. "
                "This report examines its key concepts, challenges, and future implications "
                "through a structured and evidence-based approach."
            )

        return response.strip()
