import requests
import re
import json
from requests.exceptions import ReadTimeout
from concurrent.futures import ThreadPoolExecutor
import os




# =========================
# CONFIGURATION
# =========================
API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL = "qwen2.5-3b-instruct"

TAVILY_API_KEY = "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"
TAVILY_URL = "https://api.tavily.com/search"

# =========================
# PROMPTS
# =========================
CLASSIFIER_PROMPT = """
Classify the user's message into one category:
PLAN, CALCULATE, NORMAL
Return only one word.
"""

PLANNER_PROMPT ="""
You are a Research Planner Agent.

IMPORTANT:
- Respond in the SAME language as the user's question.

STRICT RULES:
- Output ONLY valid JSON
- Do NOT add explanations
- Do NOT use markdown
- Generate 6 to 7 clear, research-focused sub-questions

Format EXACTLY like this:

{
  "sub_questions": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5",
    "Question 6",
    "Question 7"
  ]
}
"""


WRITER_PROMPT = """
You are a Research Writer Agent.

IMPORTANT:
- Write ALL content in the SAME language as the user's question.

Write a structured research report based on the planner questions.

RULES:
- Create ONE section per planner question
- Use the planner questions as section titles
- For EACH section, write:
  - Either 3–4 concise bullet points
  - OR one short paragraph (max 4–5 lines)
- Be informative but concise
- Do NOT repeat ideas across sections
- Do NOT include references or URLs
- Do NOT add a References section

The goal is clarity and coverage, not length.
"""



# =========================
# AGENTS
# =========================
def classify_intent(message):
    keywords = [
    "research", "study", "analysis", "impact", "future", "overview",
    "how to", "use", "applications", "role", "benefits", "challenges",
    "strategy", "guide", "approach"
]

    if any(k in message.lower() for k in keywords):
        return "PLAN"

    response = requests.post(
        API_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ]
        },
        timeout=120
    )
    return response.json()["choices"][0]["message"]["content"].strip().upper()


def planner_agent(query):
    try:
        response = requests.post(
            API_URL,
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": PLANNER_PROMPT},
                    {"role": "user", "content": query}
                ]
            },
            timeout=120
        )

        content = response.json()["choices"][0]["message"]["content"].strip()

        # Try direct JSON parse
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # Try extracting JSON block
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(content[start:end])

        # Final fallback
        raise ValueError("Planner did not return valid JSON")

    except Exception:
        # SAFE fallback — app never crashes
        return {
            "sub_questions": [
                "Key aspects of the topic",
                "Current trends and developments",
                "Benefits and opportunities",
                "Challenges and risks",
                "Future outlook"
            ]
        }



def searcher_agent(sub_questions, max_results=3):
    def single_search(q):
        if isinstance(q, dict):
            q = q.get("question", str(q))

        response = requests.post(
            TAVILY_URL,
            headers={
                "Authorization": f"Bearer {TAVILY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "query": q,
                "max_results": max_results,
                "search_depth": "basic"
            },
            timeout=10
        )

        data = response.json()
        return q, [
            {"url": r.get("url"), "content": r.get("content")}
            for r in data.get("results", [])
        ]

    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(single_search, q) for q in sub_questions]
        for f in futures:
            q, res = f.result()
            results[q] = res

    return results

def write_single_section(question, evidence):
    try:
        response = requests.post(
            API_URL,
            json={
                "model": MODEL,
                "max_tokens": 600,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a research writer. "
                            "Answer ONLY the given question IN DEPTH. "
                            "Write 2–3 short paragraphs (6–10 lines total). "
                            "Explain concepts clearly and logically. "
                            "Use concrete examples where relevant. "
                            "Do NOT include references or URLs. "
                            "Do NOT be generic."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Question:\n{question}\n\n"
                            f"Evidence:\n{json.dumps(evidence)[:1200]}"
                        )
                    }
                ]
            },
            timeout=60
        )

        data = response.json()
        if "choices" not in data:
            return "⚠️ Unable to generate this section."

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Error generating section: {str(e)}"



def writer_agent(search_data, progress_callback=None):
    sections = []

    # limit to 3 questions (performance fix)
    items = list(search_data.items())[:3]
    total = len(items)

    for idx, (question, evidence) in enumerate(items, 1):
        if progress_callback:
            progress_callback(f"✍️ Writing section {idx}/{total}...")

        section_text = write_single_section(question, evidence)
        sections.append(section_text)

    return sections



def synthesize_final_report(section_answers):
    """
    Creates a detailed research report with timeout safety.
    """

    # Combine section answers, but cap input size (VERY IMPORTANT)
    notes = "\n\n".join(section_answers)
    notes = notes[:3000]  # reduce input, NOT output quality

    try:
        response = requests.post(
            API_URL,
            json={
                "model": MODEL,
                "max_tokens": 900,  # slightly reduced, still long
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a senior research analyst.\n\n"
                            "IMPORTANT:\n"
                            "Write the ENTIRE report in the SAME language as the user's question.\n\n"
                            "Write a DETAILED academic-style research report using the structure below.\n\n"
                            "STRUCTURE:\n"
                            "1. Introduction – explain the context and importance of the topic\n"
                            "2. Key Findings – integrate ALL provided notes into a multi-paragraph analysis\n"
                            "3. Implications and Challenges – discuss ethical, technical, and practical issues in depth\n"
                            "4. Conclusion – summarize insights and future outlook\n\n"
                            "RULES:\n"
                            "- Do NOT aggressively summarize\n"
                            "- Expand ideas clearly\n"
                            "- Maintain academic but readable tone\n"
                            "- Do NOT include references or URLs"
                        )
                    },
                    {
                        "role": "user",
                        "content": notes
                    }
                ]
            },
            timeout=120  # ⏱ give the model time
        )

        data = response.json()
        if "choices" not in data:
            raise ValueError("No choices returned")

        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.ReadTimeout:
        # 🔁 SAFE FALLBACK (NEVER FAILS)
        return (
            "## Introduction\n"
            "This report examines the topic using synthesized research findings derived from multiple analytical sections.\n\n"
            "## Key Findings\n"
            f"{notes}\n\n"
            "## Implications and Challenges\n"
            "The findings reveal significant opportunities alongside ethical, technical, and practical challenges that must be addressed.\n\n"
            "## Conclusion\n"
            "Overall, the analysis highlights meaningful impact while emphasizing the need for responsible and well-governed adoption."
        )

    except Exception as e:
        return f"⚠️ Error synthesizing report: {str(e)}"

def stream_synthesize_final_report(section_answers, stream_callback):
    import json
    import requests

    notes = "\n\n".join(section_answers)
    notes = notes[:3000]

    payload = {
        "model": MODEL,
        "stream": True,
        "max_tokens": 900,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a senior research analyst.\n\n"
                    "Write a structured research report with:\n"
                    "1. Introduction\n"
                    "2. Key Findings\n"
                    "3. Implications and Challenges\n"
                    "4. Conclusion\n\n"
                    "Write clearly and academically."
                )
            },
            {
                "role": "user",
                "content": notes
            }
        ]
    }

    response = requests.post(
        API_URL,
        json=payload,
        stream=True,
        timeout=300
    )

    full_text = ""

    for line in response.iter_lines():
        if not line:
            continue

        decoded = line.decode("utf-8").replace("data: ", "").strip()

        if decoded == "[DONE]":
            break

        try:
            data = json.loads(decoded)
            delta = data["choices"][0]["delta"].get("content", "")
            if delta:
                full_text += delta
                stream_callback(full_text)
        except Exception:
            continue

    return full_text




def looks_like_math(text):
    return bool(re.search(r"\d+\s*[\+\-\*/]", text))

def calculator(expr):
    cleaned = re.sub(r"[^0-9+\-*/().]", "", expr)

    # 🔒 SAFETY CHECK
    if cleaned.strip() == "":
        return "⚠️ This does not look like a mathematical expression."

    try:
        return str(eval(cleaned))
    except Exception as e:
        return f"⚠️ Calculation error: {str(e)}"



def normal_chat(query):
    response = requests.post(
        API_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": query}]
        },
        timeout=30
    )
    return response.json()["choices"][0]["message"]["content"].strip()

# =========================
# PIPELINE
# =========================
def run_research_pipeline(user_query, progress_callback=None):

    def update(msg):
        if progress_callback:
            progress_callback(msg)

    update("🧠 Planning research...")
    intent = classify_intent(user_query)

    if intent == "PLAN":
        plan = planner_agent(user_query)
        if "error" in plan:
            return "", [], []

        planner_questions = plan.get("sub_questions")
        if not planner_questions or not isinstance(planner_questions, list):
            planner_questions = [
                "Key aspects of the topic",
                "Current trends and developments",
                "Benefits and opportunities",
                "Challenges and limitations",
                "Future outlook"
                ]

        planner_questions = planner_questions[:6]


        update("🔎 Searching the web...")
        search_data = searcher_agent(planner_questions)

        section_answers = writer_agent(search_data, progress_callback=update)
        update("🧩 Synthesizing final report...")
        final_answer = synthesize_final_report(section_answers)



        sources = []
        for items in search_data.values():
            for item in items:
                if item.get("url"):
                    sources.append(item["url"])

        update("✅ Done")
        return final_answer, list(set(sources)), planner_questions

    elif intent == "CALCULATE" and looks_like_math(user_query):
        return calculator(user_query), [], []
    else:
     return normal_chat(user_query), [], []
