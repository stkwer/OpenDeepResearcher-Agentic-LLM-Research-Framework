from src.services.tavily_client import TavilySearchService

t = TavilySearchService()
print(t.search("What is machine learning?"))
