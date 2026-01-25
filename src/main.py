from src.core.langgraph_pipeline import build_graph

def main():
    app = build_graph()
    print("LangGraph agent system ready. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        state = {"input": user_input}
        result = app.invoke(state)

        print("\n--- Planner Agent Output ---")
        for i, q in enumerate(result["sub_questions"], 1):
            print(f"{i}. {q}")

        print("\n--- Searcher Agent Output ---")
        for item in result["search_results"]:
            print(f"\nQuestion: {item['question']}")
            for i, src in enumerate(item["sources"], 1):
                print(f"Source {i}:")
                print(src["summary"])
                print(f"URL: {src['url']} (confidence: {src['confidence']})")

        print("\n--- Writer Agent Output ---\n")
        print(result["final_answer"])

if __name__ == "__main__":
    main()









































