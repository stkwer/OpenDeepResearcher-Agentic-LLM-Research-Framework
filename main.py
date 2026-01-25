from planner import planner_agent
from search import search_agent
from writer import writer_agent

def main():
    
    topic = input("Enter your research topic: ")

    
    sub_questions = planner_agent(topic, num_subquestions=8)
    print("\n--- Research Sub-Questions ---\n")
    for i, q in enumerate(sub_questions, 1):
        print(f"{i}. {q}")

    
    search_results = search_agent(sub_questions, max_results_per_query=2)
    print("\n--- Retrieved Content ---\n")
    for question, items in search_results.items():
        print(f"\nSub-Question:\n{question}\n")
        for item in items:
            print(f"- {item.get('title', 'No title')}")
            print(f"  URL: {item.get('url', 'No URL')}")
            print(f"  Content snippet: {item.get('content', '')[:300]}...\n")

    
    research_content = ""
    for results in search_results.values():
        for item in results:
            research_content += f"{item.get('title','')}: {item.get('content','')}\n\n"

    print("\n--- Final Summary ---\n")
    summary = writer_agent(topic, research_content)
    print(summary)

if __name__ == "__main__":
    main()
