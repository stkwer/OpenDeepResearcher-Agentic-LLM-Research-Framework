from dotenv import load_dotenv
load_dotenv()

from src.services.tavily_client import TavilySearchService

t = TavilySearchService()

results = t.search("What is cyber security")

print("\n=== TAVILY TEST OUTPUT ===\n")

for r in results:
    print("Title:", r["title"])
    print("URL:", r["url"])
    print("Content:", r["content"][:200])  # first 200 chars
    print("-" * 40)
