from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# WRITER LLM CONFIG
# ============================================================
writer_llm = ChatOpenAI(
    model="qwen2.5-7b-instruct",
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    temperature=0.2
)


# ============================================================
# RESEARCH-STYLE WRITER PROMPT
# ============================================================
writer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
You are an academic research writer.

Write in a formal research-report style.

Rules:
- Use clear sections with headings
- Do NOT add new information beyond given answers
- Do NOT mention sources or URLs
- Maintain neutral, academic tone
- Avoid repetition
- Ensure logical flow

Required structure:
1. Title
2. Introduction
3. Key Concepts and Findings
4. Applications and Implications
5. Limitations and Challenges
6. Conclusion
"""),
    ("human",
     """
Research Topic:
{main_topic}

Sub-question findings:
{sub_answers}

Write a structured research-style explanation.
""")
])


# ============================================================
# WRITER AGENT (LINKED TO SEARCHER OUTPUT)
# ============================================================
def writer_agent(research_results: dict) -> str:
    """
    Converts Searcher Agent output into a structured research-style report.
    """

    if "sub_questions" not in research_results:
        raise ValueError("Invalid input: missing sub_questions")

    main_topic = research_results.get("main_topic", "")

    # Collect findings from Searcher Agent
    findings = []
    for sub in research_results["sub_questions"]:
        if sub.get("short_answer"):
            findings.append(
                f"{sub['question']}: {sub['short_answer']}"
            )

    if not findings:
        raise ValueError("No searcher findings available for synthesis")

    combined_findings = "\n".join(findings)

    chain = writer_prompt | writer_llm
    research_output = chain.invoke({
        "main_topic": main_topic,
        "sub_answers": combined_findings
    }).content.strip()

    return research_output
