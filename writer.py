from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(
    openai_api_key="lm-studio",
    base_url="http://127.0.0.1:1234/v1",
    model="qwen2.5-7b-instruct"
)

def writer_agent(topic: str, research_content: str) -> str:
    """
    Generates a clean, structured summary for the main topic.
    The agent automatically decides headings and subheadings based on the research content.
    Each section has 1–3 concise sentences.
    Subheadings are marked with '**' and a 'Conclusion' section is added at the end.
    """

    prompt = f"""
You are a professional writer.

Generate a structured, readable summary for the topic "{topic}" using the research content below.
- Create your own headings and subheadings to organize the content clearly.
- Mark all subheadings with '**' at the start and end.
- Include an introduction with 2 paragraphs.
- Each section or subheading should have 1–3 concise sentences.
- Include a 'Conclusion' heading at the end summarizing the topic.
- Keep the writing simple, clear, and readable.
- Do NOT include instructions, notes, or mentions of sub-questions.
- Output only the summary with headings, subheadings (marked with '**'), and paragraphs.

Research content:
{research_content}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()
