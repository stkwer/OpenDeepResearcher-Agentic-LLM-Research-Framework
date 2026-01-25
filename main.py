import os
import re
import time
import requests

# ---------------- CONFIG ----------------
BASE_URL = "http://127.0.0.1:1234/v1"
TAVILY_KEY = os.getenv("TAVILY_API_KEY")


# ---------------- MODEL ----------------
def get_model_id():
    try:
        resp = requests.get(f"{BASE_URL}/models", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("data"):
                return data["data"][0]["id"]
    except:
        pass
    return "local-model"


MODEL_NAME = get_model_id()


# ---------------- LLM CALL ----------------
def call_llm(system_msg: str, user_msg: str, max_tokens: int = 1000) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }

    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"


# ---------------- TAVILY SEARCH ----------------
def tavily_search(query: str) -> list:
    if not TAVILY_KEY:
        return []

    try:
        r = requests.post(
            "https://api.tavily.com/search",
            json={"query": query, "max_results": 2},
            headers={"Authorization": f"Bearer {TAVILY_KEY}"},
            timeout=15
        )
        if r.status_code == 200:
            return r.json().get("results", [])
    except:
        pass

    return []


# ================= AGENT 1: PLANNER =================
def planner_agent(topic: str) -> list:
    system = (
        "You are a Research Architect. Analyze the topic and generate research questions. "
        "Generate only as many questions as needed based on topic complexity."
    )

    user = (
        f"Topic: {topic}\n"
        "Generate research questions.\n"
        "Each question must be on a new line and end with a question mark.\n"
        "Questions:"
    )

    raw = call_llm(system, user, max_tokens=600)

    questions = []
    for line in raw.split("\n"):
        clean = re.sub(r"^[\d\-\.\)\*]+\s*", "", line).strip()
        if "?" in clean and len(clean) > 10:
            questions.append(clean)

    if not questions:
        questions = [f"What are the core concepts of {topic}?"]

    return questions


# ================= AGENT 2: SEARCHER (INTERNAL) =================
def searcher_agent(questions: list) -> dict:
    context_data = []
    sources = set()

    for q in questions:
        results = tavily_search(q)
        for r in results:
            content = r.get("content", "")
            if content:
                context_data.append(content[:600])
            if r.get("url"):
                sources.add(r["url"])
        time.sleep(0.5)

    return {
        "context": list(set(context_data))[:15],
        "sources": list(sources)
    }


# ================= AGENT 3: WRITER =================
def writer_agent(topic: str, questions: list, search_data: dict) -> str:
    facts_list = search_data.get("context", [])

    # -------- FORMAT PLANNER QUESTIONS --------
    formatted_questions = ""
    for i, q in enumerate(questions):
        formatted_questions += f"{i+1}. {q}\n"

    # -------- FORMAT SEARCH CONTEXT --------
    formatted_context = ""
    for i, fact in enumerate(facts_list):
        formatted_context += f"DATA POINT {i+1}: {fact}\n"

    if len(formatted_context) > 5500:
        formatted_context = formatted_context[:5500] + "..."

    system = (
        "You are a Senior AI Research Scientist and Technical Writer. "
        "Follow planner questions strictly while maintaining professional documentation quality."
    )

    # -------- USER PROMPT (YOUR ORIGINAL + EXTRA CONTEXT) --------
    user = (
        # -------- EXTRA (ADDED – DO NOT REMOVE) --------
        "MANDATORY ANALYTICAL CONTEXT:\n"
        "The Planner Agent has generated research questions.\n"
        "You MUST use them to guide and shape the technical analysis.\n"
        "All questions must be addressed implicitly or explicitly.\n\n"

        "PLANNER AGENT QUESTIONS:\n"
        f"{formatted_questions}\n"
        "----------------------------------------\n\n"

        # -------- ORIGINAL PROMPT (UNCHANGED) --------
        f"Generate a comprehensive technical documentation for the topic: '{topic}'.\n\n"
        f"STRUCTURE REQUIREMENTS:\n"
        f"1. TITLE: Professional and academic.\n"
        f"2. EXECUTIVE SUMMARY: A high-level overview (4-5 sentences).\n"
        f"3. TECHNICAL ANALYSIS: 7-9 detailed bullet points. Use bold text for key concepts. "
        f"Focus on the 'how' and 'why' based on the facts.\n"
        f"4. CHALLENGES & ETHICS: A specific section on implementation hurdles and ethical considerations.\n"
        f"5. STRATEGIC CONCLUSION: A forward-looking summary (6-9 sentences).\n\n"
        f"FACTS FROM WEB RESEARCH:\n"
        f"{formatted_context}\n\n"
        f"FORMATTING INSTRUCTIONS:\n"
        f"- Use H1 (#) for Title, H2 (##) for Sections.\n"
        f"- Use horizontal rules (---) to separate sections.\n"
        f"- Avoid empty filler phrases like 'In this report'.\n"
        f"- Ensure sentences are complete and professionally articulated.\n\n"
        f"FINAL REPORT:"
    )

    summary = call_llm(system, user, max_tokens=1500)

    if not summary or not summary.strip():
        return "❌ Report generation failed."

    return summary.replace("FINAL REPORT:", "").strip()


# ================= CLI MODE =================
def run_cli():
    print("### Local Agentic RAG System ###")

    while True:
        topic = input("You: ")
        if topic.lower() in ["exit", "quit"]:
            break

        questions = planner_agent(topic)
        data = searcher_agent(questions)
        report = writer_agent(topic, questions, data)

        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)


if __name__ == "__main__":
    run_cli()
