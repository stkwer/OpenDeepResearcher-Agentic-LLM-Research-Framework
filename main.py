from planner_agent import plan
from search_agent import get_evidence
from writer_agent import write_final_summary


def extract_sub_questions(plan_output):
    """
    Correctly reconstructs wrapped sub-questions
    and ensures exactly one question per number.
    """
    sub_questions = []
    current = ""

    for line in plan_output.split("\n"):
        line = line.strip()

        if line[:2] in {"1.", "2.", "3.", "4.", "5.", "6.", "7."}:
            if current:
                sub_questions.append(current.strip())
            current = line[3:].strip()
        elif current:
            current += " " + line

    if current:
        sub_questions.append(current.strip())

    # Deduplicate while preserving order
    return list(dict.fromkeys(sub_questions))


def deduplicate_evidence(evidence_blocks):
    """
    Removes repeated evidence from the same URL.
    """
    unique = {}
    for e in evidence_blocks:
        if e["url"] and e["url"] not in unique:
            unique[e["url"]] = e
    return list(unique.values())


def main():
    question = input("Enter your question: ").strip()

    print("\n--- PLANNER AGENT ---\n")
    plan_output = plan(question)
    print(plan_output)

    sub_questions = extract_sub_questions(plan_output)

    print("\n--- SEARCH AGENT ---\n")
    evidence_blocks = []

    for i, sq in enumerate(sub_questions, 1):
        print(f"Sub-question {i}: {sq}")

        evidence = get_evidence(sq)
        print("Content:", evidence["content"])
        print("Source:", evidence["url"], "\n")

        evidence_blocks.append(evidence)

    evidence_blocks = deduplicate_evidence(evidence_blocks)

    print("\n--- WRITER AGENT (FINAL SUMMARY) ---\n")
    final_summary = write_final_summary(question, evidence_blocks)
    print(final_summary)


if __name__ == "__main__":
    main()
