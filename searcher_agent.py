import requests
import json
from typing import List, Dict, Any
from planner_agent import PlannerAgent

class SearcherAgent:
    """
    Searcher Agent: Uses Tavily API to retrieve relevant, up-to-date content for each subquestion.
    """

    def __init__(self, api_key: str = "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"):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com/search"

    def search_subquestion(self, subquestion: str) -> List[Dict[str, Any]]:
        """
        Search for relevant sources using Tavily API for a single subquestion.
        Returns a list of source dictionaries with title, url, content (snippet), and score.
        """
        payload = {
            "api_key": self.api_key,
            "query": subquestion,
            "search_depth": "advanced",
            "include_images": False,
            "include_answer": False,
            "include_raw_content": False,
            "max_results": 5,
            "include_domains": [],
            "exclude_domains": []
        }

        try:
            response = requests.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            sources = []
            for result in results:
                sources.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0.0)
                })
            return sources
        except requests.RequestException as e:
            print(f"Error searching for '{subquestion}': {e}")
            return []

    def search_all(self, subquestions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for sources for all subquestions.
        Handles both dict and string types in subquestions list.
        Returns a dict where keys are subquestion IDs and values are lists of sources.
        Enhanced to display detailed source information in terminal.
        """
        results = {}
        print("\n" + "="*80)
        print("SEARCH AGENT RESULTS - DETAILED SOURCE INFORMATION")
        print("="*80)
        
        for subq in subquestions:
            qid = subq["id"]
            text = subq["text"]
            print(f"\n🔍 Searching for subquestion {qid}: {text}")
            sources = self.search_subquestion(text)
            results[qid] = sources
            
            print(f"\n📚 Found {len(sources)} sources for {qid}:")
            print("-" * 60)
            
            for i, source in enumerate(sources, 1):
                print(f"\n📄 Source {i}:")
                print(f"   Title: {source['title']}")
                print(f"   URL: {source['url']}")
                print(f"   Content: {source['content'][:300]}{'...' if len(source['content']) > 300 else ''}")
                print(f"   Score: {source['score']}")
                print(f"   {'─' * 50}")
            
        print(f"\n✅ Search completed for {len(subquestions)} subquestions")
        print("="*80)
        return results

if __name__ == "__main__":
    # First, run the planner agent to get subquestions
    print("Enter your research question:")
    research_question = input("> ").strip()
    if not research_question:
        print("No question provided.")
        exit(1)

    print("[system] Running planner agent...")
    planner = PlannerAgent()
    result = planner.plan(research_question)
    subquestions = result.get("subquestions", [])
    print(f"[system] Planner generated {len(subquestions)} subquestions.")

    print("Subquestions:")
    for i, subq in enumerate(subquestions):
        if isinstance(subq, dict):
            qid = subq.get("id", f"q{i+1}")
            qtype = subq.get("type", "unknown")
            text = subq.get("text", str(subq))
            print(f"  {i+1}. [{qid} - {qtype}] {text}")
        else:
            print(f"  {i+1}. {subq}")
    print()

    # Now, run the searcher agent on those subquestions
    print("[system] Running searcher agent...")
    agent = SearcherAgent()  # Uses default API key

    results = agent.search_all(subquestions)
    print("\nSearch Results:")
    for qid, sources in results.items():
        print(f"\n{qid}:")
        for source in sources:
            print(f"  Title: {source['title']}")
            print(f"  URL: {source['url']}")
            print(f"  Content: {source['content'][:500]}{'...' if len(source['content']) > 500 else ''}")
            print(f"  Score: {source['score']}")
            print("  ---")