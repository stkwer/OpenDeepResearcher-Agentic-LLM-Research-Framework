import os
import requests
import json

from planner_agent import PlannerAgent


class SearcherAgent:
    def __init__(self):
        self.api_key = os.environ.get("TAVILY_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set TAVILY_API_KEY environment variable")
        
        self.base_url = "https://api.tavily.com/search"

    def answer(self, question: str):
        print(f"\n[SearcherAgent] Searching web for: {question}")

        try:
            payload = {
                "api_key": self.api_key,
                "query": question,
                "search_depth": "advanced",
                "max_results": 5
            }

            response = requests.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            answers = []
            
            for r in result.get("results", []):
                answers.append({
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "content": r.get("content")
                })

            return answers
        except requests.exceptions.RequestException as e:
            print(f"Error during Tavily search: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing Tavily response: {e}")
            return []


if __name__ == "__main__":
    topic = input("\nEnter a topic: ").strip()
    if not topic:
        topic = "Explain any topic"

    planner = PlannerAgent()
    searcher = SearcherAgent()

    plan = planner.plan(topic)

    print("\n===== ANSWERS (RAW WEB CONTENT) =====\n")

    for i, question in enumerate(plan["steps"], start=1):
        print(f"\nQ{i}: {question}")

        results = searcher.answer(question)

        if not results:
            print("No relevant web results found.")
            continue

        for res in results:
            print("\nTitle:", res["title"])
            print("URL:", res["url"])
            print("Content:", res["content"])
