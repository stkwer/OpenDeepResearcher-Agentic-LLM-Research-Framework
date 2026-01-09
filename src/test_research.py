from graph.research_graph import build_graph

# Build the research graph
graph = build_graph()

# 1️⃣ Take topic input from the user
topic = input("Enter your research topic: ")

# 2️⃣ Run the research workflow
result = graph.invoke({"topic": topic})

# 3️⃣ Print sub-questions
print("\n================ SUB QUESTIONS ================\n")
for i, q in enumerate(result["sub_questions"], 1):
    print(f"{i}. {q}")

# 4️⃣ Print search results (trimmed preview)
print("\n================ SEARCH RESULTS (PREVIEW) ================\n")

for i, r in enumerate(result["search_results"], 1):
    title = r.get("title", "N/A")
    url = r.get("url", "N/A")
    content = r.get("content", "")

    # Limit content preview
    preview = content.strip().replace("\n", " ")[:300]

    print(f"Result {i}")
    print(f"Title   : {title}")
    print(f"URL     : {url}")
    print(f"Content : {preview}...")
    print("-" * 70)

# 5️⃣ Print final summary
print("\n================ FINAL RESEARCH REPORT ================\n")
print(result["summary"])
