from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

class SearcherAgent:
    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def run(self, query):
        results = self.client.search(query=query, max_results=3)
        return results["results"]
