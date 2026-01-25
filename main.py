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












# # main.py
# from planner import planner_agent
# from search import search_agent
# from writer import writer_agent

# def main():
#     # Step 0: Input topic
#     topic = input("Enter your research topic: ")

#     # Step 1: Generate sub-questions using planner agent
#     sub_questions = planner_agent(topic, num_subquestions=8)
#     print("\n--- Research Sub-Questions ---\n")
#     for i, q in enumerate(sub_questions, 1):
#         print(f"{i}. {q}")

#     # Step 2: Retrieve content for each sub-question using search agent
#     search_results = search_agent(sub_questions, max_results_per_query=2)
#     print("\n--- Retrieved Content ---\n")
#     for question, items in search_results.items():
#         print(f"\nSub-Question:\n{question}\n")
#         for item in items:
#             print(f"- {item.get('title','No title')}")
#             print(f"  URL: {item.get('url','No URL')}")
#             print(f"  Content snippet: {item.get('content','')[:300]}...\n")

#     # Step 3: Combine all retrieved content into one string
#     research_content = ""
#     for results in search_results.values():
#         for item in results:
#             research_content += f"{item.get('title','')}: {item.get('content','')}\n\n"

#     # Step 4: Generate final summary using writer agent
#     print("\n--- Final Summary ---\n")
#     summary = writer_agent(topic, research_content)
#     print(summary)

# if __name__ == "__main__":
#     main()









# from planner import planner_agent
# from search import search_agent
# from writer import writer_agent

# def main():
#     topic = input("Enter your research topic: ")

#     # Step 1: Planner
#     sub_questions = planner_agent(topic, num_subquestions=8)
#     print("\n--- Research Sub-Questions ---\n")
#     for i, q in enumerate(sub_questions, 1):
#         print(f"{i}. {q}")

#     # Step 2: Search
#     print("\n--- Retrieved Content ---\n")
#     search_results = search_agent(sub_questions, max_results_per_query=2)
#     for question, results in search_results.items():
#         print(f"\nSub-Question:\n{question}\n")
#         for item in results:
#             print(f"- {item.get('title','No title')}")
#             print(f"  {item.get('url','No URL')}")
#             print(f"  {item.get('content','')}\n")

#     # Step 3: Combine all retrieved content into one string for Writer Agent
#     research_content = ""
#     for results in search_results.values():
#         for item in results:
#             research_content += f"{item.get('title','')}: {item.get('content','')}\n\n"

#     # Step 4: Writer
#     print("\n--- Final Summaries ---\n")
#     summary = writer_agent(topic, research_content)
#     print(summary)

# if __name__ == "__main__":
#     main()



# # main.py
# from planner import planner_agent
# from search import search_agent
# from writer import writer_agent

# def main():
#     topic = input("Enter your research topic: ")

#     # Step 1: Generate sub-questions (optional)
#     sub_questions = planner_agent(topic, num_subquestions=8)
#     print("\n--- Research Sub-Questions ---\n")
#     for i, q in enumerate(sub_questions, 1):
#         print(f"{i}. {q}")

#     # Step 2: Retrieve content for each sub-question
#     search_results = search_agent(sub_questions, max_results_per_query=2)

#     print("\n--- Retrieved Content ---\n")
#     for question, items in search_results.items():
#         print(f"\nSub-Question:\n{question}\n")
#         for item in items:
#             print(f"- {item.get('title','No title')}")
#             print(f"  URL: {item.get('url','No URL')}")
#             print(f"  Content snippet: {item.get('content','')[:200]}...\n")

#     # Step 3: Combine all retrieved content into one string
#     research_content = ""
#     for results in search_results.values():
#         for item in results:
#             research_content += f"{item.get('title','')}: {item.get('content','')}\n\n"

#     # Step 4: Generate a structured summary with dynamic headings
#     print("\n--- Final Summary ---\n")
#     summary = writer_agent(topic, research_content)
#     print(summary)

# if __name__ == "__main__":
#     main()









# from planner import planner_agent
# from search import search_agent
# from writer import writer_agent

# def main():
#     topic = input("Enter your research topic: ")

#     # Step 1: Planner
#     sub_questions = planner_agent(topic, num_subquestions=8)
#     print("\n--- Research Sub-Questions ---\n")
#     for i, q in enumerate(sub_questions, 1):
#         print(f"{i}. {q}")

#     # Step 2: Search
#     print("\n--- Retrieved Content ---\n")
#     search_results = search_agent(sub_questions, max_results_per_query=2)
#     for question, results in search_results.items():
#         print(f"\nSub-Question:\n{question}\n")
#         for item in results:
#             print(f"- {item.get('title','No title')}")
#             print(f"  {item.get('url','No URL')}")
#             print(f"  {item.get('content','')}\n")

#     # Step 3: Writer
#     print("\n--- Final Summaries ---\n")
#     summaries = writer_agent(topic,search_results)
#     for question, summary in summaries.items():
#         print(f"\n{question}\n{summary}")

# if __name__ == "__main__":
#     main()




































# # # # # from planner import planner_agent
# # # # # from search import search_agent

# # # # # # Step 1: Input your research topic
# # # # # topic = input("Enter your research topic: ")

# # # # # # Step 2: Generate sub-questions using Planner Agent
# # # # # sub_questions = planner_agent(topic, num_subquestions=5)

# # # # # print("\n--- Generated Sub-Questions ---")
# # # # # for i, q in enumerate(sub_questions, 1):
# # # # #     print(f"{i}. {q}")

# # # # # # Step 3: Fetch search results using Search Agent
# # # # # search_results = search_agent(sub_questions)

# # # # # # Step 4: Display search results
# # # # # for question, items in search_results.items():
# # # # #     print(f"\n=== {question} ===")
# # # # #     for item in items:
# # # # #         title = item.get("title", "No title")
# # # # #         url = item.get("url", "No URL")
# # # # #         score = item.get("score", "N/A")
# # # # #         print(f"- {title} | {url} | Score: {score}")
# # # # from planner import planner_agent
# # # # from search import search_agent
# # # # from writer import writer_agent

# # # # # Step 1: Topic input
# # # # topic = input("Enter your research topic: ")

# # # # # Step 2: Generate sub-questions
# # # # sub_questions = planner_agent(topic, num_subquestions=5)

# # # # # Step 3: Fetch search results
# # # # search_results = search_agent(sub_questions)

# # # # # Step 4: Generate summaries
# # # # summaries = writer_agent(search_results)

# # # # # Step 5: Display summaries
# # # # for question, summary in summaries.items():
# # # #     print(f"\n=== {question} ===")
# # # #     print(summary)



# # from planner import planner_agent
# # from search import search_agent
# # from writer import writer_agent

# # def main():
# #     topic = input("Enter your research topic: ")

# #     # Step 1: Planner
# #     sub_questions = planner_agent(topic, num_subquestions=8)
# #     print("\n--- Research Sub-Questions ---\n")
# #     for i, q in enumerate(sub_questions, 1):
# #         print(f"{i}. {q}")

# #     # Step 2: Search
# #     print("\n--- Retrieved Content ---\n")
# #     search_results = search_agent(sub_questions, max_results_per_query=2)
# #     for question, results in search_results.items():
# #         print(f"\nSub-Question:\n{question}\n")
# #         for item in results:
# #             print(f"- {item.get('title','No title')}")
# #             print(f"  {item.get('url','No URL')}")
# #             print(f"  {item.get('content','')[:300]}\n")

# #     # Step 3: Writer
# #     print("\n--- Final Summaries ---\n")
# #     summaries = writer_agent(search_results)
# #     for question, summary in summaries.items():
# #         print(f"\n{question}\n{summary}")

# # if __name__ == "__main__":
# #     main()





# # # main.py
# # from planner import planner_agent
# # from search import search_agent
# # from writer import writer_agent

# # def main():
# #     topic = input("Enter your research topic: ")

# #     # Step 1: Generate sub-questions
# #     print("\n--- Research Sub-Questions ---\n")
# #     sub_questions = planner_agent(topic, num_subquestions=8)
# #     for i, q in enumerate(sub_questions, 1):
# #         print(f"{i}. {q}")

# #     # Step 2: Retrieve content for each sub-question
# #     print("\n--- Retrieved Content ---\n")
# #     search_results = search_agent(sub_questions, max_results_per_query=1)
# #     for question, items in search_results.items():
# #         print(f"\nSub-Question:\n{question}\n")
# #         for item in items:
# #             print(f"- {item.get('title','No title')}")
# #             print(f"  URL: {item.get('url','No URL')}")
# #             print(f"  Content snippet: {item.get('content','')[:200]}...\n")

# #     # Step 3: Generate summaries using Writer Agent
# #     print("\n--- Final Summaries ---\n")
# #     summaries = writer_agent(search_results)
# #     for question, bullets in summaries.items():
# #         print(f"\n{question}\n{bullets}")

# # if __name__ == "__main__":
# #     main()






# # main.py
# from planner import planner_agent
# from search import search_agent
# from writer import writer_agent

# def main():
#     topic = input("Enter your research topic: ")

#     # Step 1: Generate sub-questions
#     print("\n--- Research Sub-Questions ---\n")
#     sub_questions = planner_agent(topic, num_subquestions=8)
#     for i, q in enumerate(sub_questions, 1):
#         print(f"{i}. {q}")

#     # Step 2: Retrieve content for each sub-question
#     print("\n--- Retrieved Content ---\n")
#     search_results = search_agent(sub_questions, max_results_per_query=1)
#     for question, items in search_results.items():
#         print(f"\nSub-Question:\n{question}\n")
#         for item in items:
#             print(f"- {item.get('title','No title')}")
#             print(f"  URL: {item.get('url','No URL')}")
#             print(f"  Content snippet: {item.get('content','')[:200]}...\n")

#     # Step 3: Generate summaries using Writer Agent
#     print("\n--- Final Summaries ---\n")
#     summaries = writer_agent(search_results)
#     for question, bullets in summaries.items():
#         print(f"\n{question}\n{bullets}")

# if __name__ == "__main__":
#     main()
