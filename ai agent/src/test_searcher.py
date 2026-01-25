from src.agents.searcher_agent import SearcherAgent

searcher = SearcherAgent()

query = "Explain machine learning"
result = searcher.run(query)

print("\n--- Tavily Research Output ---\n")
print(result)
