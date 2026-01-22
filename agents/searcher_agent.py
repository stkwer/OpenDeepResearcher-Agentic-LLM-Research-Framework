import os
from tavily import TavilyClient

class SearcherAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.client = TavilyClient(api_key=self.api_key)

    def run(self, questions):
        research_log = ""
        for q in questions:
            try:
                result = self.client.search(query=q, search_depth="basic", max_results=1)
                if result["results"]:
                    item = result["results"][0]
                    research_log += f"\n### Question: {q}\nFact: {item['content']}\nSource: {item['url']}\n"
            except:
                continue
        return research_log