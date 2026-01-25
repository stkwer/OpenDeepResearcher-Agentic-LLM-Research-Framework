from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import List

llm = ChatOpenAI(
    openai_api_key="lm-studio",
    base_url="http://127.0.0.1:1234/v1",
    model="qwen2.5-7b-instruct"
)

def planner_agent(topic: str, num_subquestions: int = 8) -> List[str]:
    """
    Planner Agent:
    Generates exactly num_subquestions short, simple, professional sub-questions.
    Returns a Python list of sub-questions.
    """
    prompt = f"""
You are a Research Planner Agent.
Generate EXACTLY {num_subquestions} short, clear, simple sub-questions on the topic below.
Rules:
- One sentence per question
- Simple and professional tone
- No duplicates
- Cover multiple perspectives: technical, cost, security, risks, ethics, labor, future trends

Topic:
{topic}

Output: Numbered list only.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content.strip()

    sub_questions = [
        line.split(". ", 1)[1]
        for line in text.splitlines()
        if line.strip() and line[0].isdigit()
    ]

    return sub_questions
