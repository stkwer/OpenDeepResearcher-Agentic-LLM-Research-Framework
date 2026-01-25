import os
import json
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.writer import WriterAgent
from agents.searcher import SearcherAgent

SESSIONS_DIR = "sessions"
OUTPUT_MD = "research_report.md"


def find_latest_session():
    files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]
    if not files:
        raise FileNotFoundError("No session files found.")
    files.sort(reverse=True)
    return os.path.join(SESSIONS_DIR, files[0])


def regenerate():
    session_path = find_latest_session()
    print(f"\n📂 Loading session: {session_path}")

    with open(session_path, "r", encoding="utf-8") as f:
        session = json.load(f)

    topic = session["topic"]
    plan = session["plan"]

    writer = WriterAgent()
    searcher = SearcherAgent()

    regenerated_sections = []

    print("\n🔁 Regenerating sections...\n")

    for i, question in enumerate(plan, start=1):
        print(f"✍️  Section {i}: {question}")

        results = searcher.search(question)
        content = writer.write_section(question, results)

        regenerated_sections.append((question, content))

    # ---------- REBUILD MARKDOWN ----------
    report = f"# {topic.title()}\n\n"

    for question, content in regenerated_sections:
        report += f"## {question}\n\n{content}\n\n"

    # ---------- SAVE ----------
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(report)

    session["report"] = report

    with open(session_path, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2)

    print("\n✅ Regeneration complete")
    print(f"📄 {OUTPUT_MD} updated")
    print(f"🧠 Session updated: {session_path}")


if __name__ == "__main__":
    regenerate()
