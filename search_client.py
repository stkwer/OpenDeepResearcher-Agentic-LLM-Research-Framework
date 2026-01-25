import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file")

client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query: str, max_results: int = 3) -> list:
    """
    Search the web using Tavily and return
    title, summary, and source URL.
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=False
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title", "No title"),
            "summary": item.get("content", "No summary available")[:600],
            "url": item.get("url", "")
        })

    return results
