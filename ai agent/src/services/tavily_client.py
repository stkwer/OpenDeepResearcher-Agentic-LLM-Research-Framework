import os
import requests


class TavilyClient:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise RuntimeError("TAVILY_API_KEY not set")

        self.url = "https://api.tavily.com/search"

    def search(self, query: str, max_results: int = 3, search_depth: str = "basic"):
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
        }

        response = requests.post(self.url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()














