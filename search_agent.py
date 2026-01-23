import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_evidence(sub_question, main_question=None):
    """
    Context-aware search to avoid acronym ambiguity
    """
    if main_question:
        query = f"{sub_question} (context: {main_question}, artificial intelligence, machine learning)"
    else:
        query = sub_question

    results = client.search(
        query=query,
        search_depth="advanced",
        max_results=1,
        include_raw_content=True
    )

    if not results["results"]:
        return {
            "sub_question": sub_question,
            "content": "",
            "url": ""
        }

    r = results["results"][0]
    return {
        "sub_question": sub_question,
        "content": r.get("content", "")[:350].strip(),
        "url": r.get("url", "")
    }