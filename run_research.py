import sys
import os
import re
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.planner import PlannerAgent
from agents.searcher import SearcherAgent
from agents.writer import WriterAgent
from agents.introducer import IntroductionAgent
from agents.concluder import ConclusionAgent
from core.memory import SessionMemory


# ----------------------------
# Helper functions
# ----------------------------
def clean_think(text: str) -> str:
    """Remove <think>...</think> blocks completely"""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def normalize_question(q: str) -> str:
    """Remove numbering like '1.' '2)' etc."""
    return re.sub(r"^\s*\d+[\.\)]\s*", "", q).strip()


def question_to_heading(question: str) -> str:
    """
    Convert a research question into a neutral academic heading
    (DOMAIN-INDEPENDENT, but academically valid)
    """
    q = question.lower()

    if "what is" in q or "theoretical" in q or "background" in q:
        return "Theoretical Background"
    if "how" in q and ("work" in q or "process" in q or "mechanism" in q):
        return "Underlying Mechanisms and Processes"
    if "evidence" in q or "study" in q or "experiment" in q:
        return "Empirical Evidence and Observations"
    if "impact" in q or "effect" in q:
        return "Impacts and Implications"
    if "challenge" in q or "limitation" in q or "risk" in q:
        return "Challenges and Limitations"
    if "future" in q or "direction" in q:
        return "Future Research Directions"

    return "Discussion"


# ----------------------------
# Initialize agents
# ----------------------------
planner = PlannerAgent()
searcher = SearcherAgent()
writer = WriterAgent()
intro_agent = IntroductionAgent()
conclusion_agent = ConclusionAgent()
memory = SessionMemory()


# ----------------------------
# User input
# ----------------------------
query = input("\nEnter your research topic:\n> ").strip()

print("\n📌 Planning research...")
plan = planner.plan(query)

if not isinstance(plan, list):
    raise TypeError("Planner must return a list of research questions")

print("✅ Research plan generated")
for i, q in enumerate(plan, 1):
    print(f"{i}. {q}")

sections = plan   # ✅ FIXED


# ----------------------------
# Report Header
# ----------------------------
final_report = f"""# {query.title()}

**Date:** {date.today().strftime('%B %d, %Y')}

---

## Abstract
This research report examines the topic of {query.lower()}, focusing on its theoretical foundations,
key mechanisms, empirical evidence, challenges, and future research directions based on existing
academic and professional literature.

---

## Introduction
{clean_think(intro_agent.write_intro(query))}

---
"""

session_sections = []
all_contents = []


# ----------------------------
# Main body
# ----------------------------
for raw_question in sections:
    question = normalize_question(raw_question)
    heading = question_to_heading(question)

    print(f"\n🔍 Searching literature: {question}")
    results = searcher.search(question)

    print("✍ Writing section...")
    content = clean_think(writer.write_section(question, results))

    final_report += f"## {heading}\n\n{content}\n\n### References\n"

    refs = []
    for i, res in enumerate(results, start=1):
        if res.get("url"):
            final_report += f"[{i}] {res['url']}\n"
            refs.append(res["url"])

    final_report += "\n"

    all_contents.append(content)
    session_sections.append({
        "question": question,
        "heading": heading,
        "content": content,
        "sources": refs
    })


# ----------------------------
# Conclusion
# ----------------------------
final_report += "## Conclusion\n\n"
final_report += clean_think(
    conclusion_agent.write_conclusion(query, all_contents)
)
final_report += "\n"


# ----------------------------
# Save output
# ----------------------------
with open("research_report.md", "w", encoding="utf-8") as f:
    f.write(final_report)

session_path = memory.save(query, {
    "topic": query,
    "plan": sections,
    "report": final_report,
    "sections": session_sections
})

print("\n✅ Research report generated: research_report.md")
print(f"🧠 Research session saved at: {session_path}")
