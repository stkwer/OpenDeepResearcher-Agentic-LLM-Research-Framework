class WriterAgent:
    def __init__(self, llm):
        self.llm = llm

    def _section(self, title: str, topic: str, min_words: int):
        prompt = f"""
You are writing an academic research paper.

Write the section titled:
{title}

Research topic:
{topic}

Rules:
- Formal academic writing
- Paragraph-based (no bullets unless necessary)
- Minimum {min_words} words
- Do NOT write conclusion
- Do NOT write references
"""
        return self.llm.invoke(prompt)

    def _conclusion(self, topic: str):
        prompt = f"""
Write the FINAL CONCLUSION section for an academic research paper.

Topic:
{topic}

Rules:
- Summarize key insights
- Discuss implications
- Mention future scope
- 300–400 words
"""
        return self.llm.invoke(prompt)

    def run(self, state: dict):
        topic = state["input"]

        paper = []

        # Title
        paper.append(f"# {topic}\n")

        # Abstract
        paper.append("## Abstract\n" + self._section("Abstract", topic, 200))

        # Keywords
        paper.append(
            "## Keywords\n"
            "Artificial Intelligence, Machine Learning, Data Analytics, Automation, Ethics, Sustainability\n"
        )

        # Main body sections
        paper.append("## 1. Introduction\n" + self._section("Introduction", topic, 400))
        paper.append("## 2. Literature Review\n" + self._section("Literature Review", topic, 500))
        paper.append("## 3. Methodology\n" + self._section("Methodology", topic, 400))
        paper.append("## 4. Applications\n" + self._section("Applications", topic, 500))
        paper.append("## 5. Challenges and Limitations\n" + self._section("Challenges and Limitations", topic, 400))
        paper.append("## 6. Future Trends\n" + self._section("Future Trends", topic, 400))

        # ONE final conclusion
        paper.append("## 7. Conclusion\n" + self._conclusion(topic))

        # ONE references section
        paper.append(
            "## References\n"
            "[1] https://www.ajournals.org/ijai/article/details/1006-2538/79\n"
            "[2] https://www.sciencedirect.com/topics/artificial-intelligence\n"
            "[3] https://ieeexplore.ieee.org/Xplore/home.jsp\n"
        )

        state["final_answer"] = "\n\n".join(paper)
        return state











































