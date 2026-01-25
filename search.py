from dotenv import load_dotenv
import os
from typing import List, Dict
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file.")

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def search_agent(
    sub_questions: List[str],
    max_results_per_query: int = 1
) -> Dict[str, List[Dict]]:
    """
    Search Agent (Fast Mode):
    - Only 1 result per question for speed
    - Short content snippets
    """

    results: Dict[str, List[Dict]] = {}

    for question in sub_questions:
        try:
            response = tavily.search(
                query=question,
                max_results=max_results_per_query,
                search_depth="basic",
                include_answer=False,
                include_raw_content=False,
                timeout=5
            )

            items = response.get("results", [])

            clean_items = []
            for item in items:
                clean_items.append({
                    "title": item.get("title", "Unknown Source"),
                    "url": item.get("url", ""),
                    "content": (item.get("content") or "")[:150]
                })

            results[question] = clean_items

        except Exception as e:
            results[question] = [{
                "title": "Search Error",
                "url": "",
                "content": str(e)
            }]

    return results
