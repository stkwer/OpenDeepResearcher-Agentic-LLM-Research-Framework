from planner_agent import PlannerAgent, LocalLLM
from searcher_agent import SearcherAgent
import sys
import contextlib
import io

MAX_CONTENT_LENGTH = 6000


@contextlib.contextmanager
def suppress_stdout():
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = original_stdout


class WriterAgent:
    def __init__(self, llm=None):
        self.llm = llm or LocalLLM()
        self.planner = PlannerAgent()
        self.searcher = SearcherAgent()

    def answer(self, question: str) -> str:
        try:
            # Planner
            plan = self.planner.plan(question)
            if not plan or "steps" not in plan or not plan["steps"]:
                return "Error: Planner could not generate valid sub-questions."
        except Exception as e:
            return f"Error in planner: {str(e)}"

        # Searcher
        all_web_results = []
        for sub_question in plan["steps"]:
            try:
                with suppress_stdout():
                    results = self.searcher.answer(sub_question)
                if results:
                    all_web_results.extend(results)
            except Exception as e:
                print(f"Warning: Search failed for '{sub_question}': {e}")
                continue

        # If no results, return fallback message
        if not all_web_results:
            return "Could not find relevant information to answer your question. Please try again with a different query."

        # Writer system prompt
        system = (
            "You are the Writer Agent and the final answering agent. "
            "Your job is to explain the topic clearly and naturally, as a knowledgeable human would in conversation.\n\n"

            "How to think:\n"
            "Imagine you are explaining this to a curious student in simple words. "
            "Focus on clarity, understanding, and logical flow rather than formal structure.\n\n"

            "Strict rules:\n"
            "Do not use headings, subheadings, titles, hashtags, stars, markdown, bullet points, or numbered lists. "
            "Do not format the text in any way. "
            "Do not sound like a textbook, notes, blog, or Wikipedia article. "
            "Do not define terms mechanically. "
            "Do not enumerate points or categories. "
            "Do not repeat the same idea in different ways.\n\n"

            "Writing style:\n"
            "Write in smooth, continuous paragraphs. "
            "Each paragraph should naturally lead into the next. "
            "Use simple, clean, human language. "
            "The tone should feel like a real person explaining, not a machine teaching. "
            "Avoid robotic, academic, or lecture-like tone.\n\n"

            "Content rules:\n"
            "Use only the provided information. "
            "Do not add external knowledge, assumptions, or extra facts. "
            "Do not mention sources, tools, agents, or processes. "
            "Do not explain what you are doing. Just explain the topic.\n\n"

            "Output:\n"
            "Produce a complete, self-contained answer that directly addresses the original question. "
            "The final output should be plain text only, with no formatting symbols of any kind."
        )

        # Combine search content (length-safe)
        combined_content = ""
        current_length = 0

        for r in all_web_results:
            content = r.get("content", "")
            if not content:
                continue

            if current_length + len(content) > MAX_CONTENT_LENGTH:
                remaining = MAX_CONTENT_LENGTH - current_length
                combined_content += content[:remaining]
                break

            combined_content += content + "\n\n"
            current_length += len(content)

        # User prompt
        user = (
            f"Original Question:\n{question}\n\n"
            f"Collected Information:\n{combined_content}"
        )

        try:
            return self.llm.chat(
                system,
                user,
                temperature=0.0,
                max_tokens=900
            )
        except Exception as e:
            return f"Error generating response: {str(e)}"


if __name__ == "__main__":
    topic = input("\nEnter a topic: ").strip()
    if not topic:
        topic = "Explain any topic"

    writer = WriterAgent()
    final_answer = writer.answer(topic)

    print(final_answer)
