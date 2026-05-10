from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import os

# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192",
    temperature=0
)
def writer_agent(topic: str, research_content: str) -> str:
    """
    Generates a clean, structured summary for the main topic.
    The agent automatically decides headings and subheadings based on the research content.
    Each section has 1–3 concise sentences.
    Subheadings are marked with '**' and a 'Conclusion' section is added at the end.
    """

    prompt = f"""
You are a professional writer.

Generate a structured, readable summary for the topic "{topic}" using the research content below.
- Create your own headings and subheadings to organize the content clearly.
- Mark all subheadings with '**' at the start and end.
- Include an introduction with 2 paragraphs.
- Each section or subheading should have 1–3 concise sentences.
- Include a 'Conclusion' heading at the end summarizing the topic.
- Keep the writing simple, clear, and readable.
- Do NOT include instructions, notes, or mentions of sub-questions.
- Output only the summary with headings, subheadings (marked with '**'), and paragraphs.

Research content:
{research_content}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()


























































































































































































































































# # writer.py
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage

# # Initialize the LLM
# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )

# def writer_agent(topic: str, research_content: str) -> str:
#     """
#     Generates a clean, structured summary for the main topic.
#     The agent automatically decides headings and subheadings based on the research content.
#     Each section has 1–3 concise sentences.
#     """

#     prompt = f"""
# You are a professional writer.

# Generate a structured, readable summary for the topic "{topic}" using the research content below.
# - Create your own headings and subheadings to organize the content clearly.
# - Include an introduction with 2 paragraphs.
# - Each section or subheading should have 1–3 concise sentences.
# - Keep the writing simple, clear, and readable.
# - Do NOT include instructions, notes, or mentions of sub-questions.
# - Output only the summary with headings, subheadings, and paragraphs.

# Research content:
# {research_content}
# """

#     response = llm.invoke([HumanMessage(content=prompt)])
#     return response.content.strip()







# # writer.py
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage

# # Initialize the LLM
# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )

# def writer_agent(topic: str, research_content: str) -> str:
#     """
#     Generates a clean, structured summary for the main topic.
#     The agent itself decides headings like Introduction, Key Features, Importance,
#     Applications, and Ethical & Security Considerations.
#     The Introduction section has 2 paragraphs.
#     Each of the other sections has 1–3 concise sentences.
#     The LLM uses the research_content to guide the summary.
#     """
    
#     prompt = f"""
# You are a professional writer.

# Generate ONE concise summary for the topic "{topic}".
# - Create 4–6 sections with clear side headings.
# - The Introduction section should have 2 paragraphs of 2–3 sentences each.
# - Each of the other sections should have 1–3 sentences.
# - Side headings can include: Introduction, Key Features, Importance, Applications, Ethical & Security Considerations.
# - Keep the text simple, clear, and readable.
# - Do NOT mention sub-questions, bullet points, or instructions.

# Research content:
# {research_content}
# """
#     response = llm.invoke([HumanMessage(content=prompt)])
#     return response.content.strip()





# # writer.py
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage

# # Initialize the LLM
# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )

# def writer_agent(topic: str, research_content: str) -> str:
#     """
#     Generates a clean, structured summary for the main topic.
#     The agent itself decides headings like Introduction, Key Features, Importance,
#     Applications, and Ethical & Security Considerations.
#     Each section has 1–3 concise sentences.
#     """

#     prompt = f"""
# You are a professional writer.

# Generate ONE concise summary for the topic "{topic}".
# - Create 4–6 sections with clear side headings.
# - Include an introductory paragraph of 2–3 sentences.
# - Each section should have 1–3 sentences.
# - Side headings can include: Introduction, Key Features, Importance, Applications, Ethical & Security Considerations.
# - Keep the text simple, clear, and readable.
# - Do NOT mention sub-questions, bullet points, or instructions.
# - Use the research content below to guide your writing.

# Research content:
# {research_content}
# """

#     response = llm.invoke([HumanMessage(content=prompt)])
#     return response.content.strip()


















# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage
# from typing import Dict, List

# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )

# def writer_agent(search_results: Dict[str, List[Dict]]) -> Dict[str, str]:
#     """
#     Writer Agent (Paragraph Style):
#     - Generates 2–3 short paragraphs per sub-question
#     - Each paragraph is 2–3 sentences
#     - Synthesizes information from multiple sources
#     """

#     prompt_sections = []

#     for i, (question, items) in enumerate(search_results.items(), 1):
#         sources_text = ""
#         for item in items:
#             sources_text += f"""
# Source Title: {item.get('title', 'Unknown')}
# Content Snippet: {item.get('content', '')}
# """

#         prompt_sections.append(f"""
# QUESTION {i}: {question}
# {sources_text}
# """)

#     full_prompt = f"""
# You are a professional Research Writer Agent.

# Instructions:
# - For EACH question, write **2–3 short paragraphs**
# - Each paragraph should contain **2–3 sentences**
# - Use a clear, professional, academic tone
# - Synthesize ideas across all provided sources
# - Include explanations, implications, examples, or risks where relevant
# - Do NOT use bullet points
# - Do NOT repeat the question text inside paragraphs

# Research material:
# {chr(10).join(prompt_sections)}

# Output format (strict):
# Question 1:
# <paragraph>
# <paragraph>

# Question 2:
# <paragraph>
# <paragraph>
# """

#     response = llm.invoke([HumanMessage(content=full_prompt)])

#     # Parse response into dictionary
#     summaries = {}
#     blocks = response.content.split("Question ")[1:]
#     questions = list(search_results.keys())

#     for i, block in enumerate(blocks):
#         summaries[questions[i]] = block.strip()

#     return summaries










































































































































































































































# # # # # from langchain_openai import ChatOpenAI
# # # # # from langchain_core.messages import HumanMessage
# # # # # from typing import List, Dict

# # # # # # Initialize LM Studio Local LLM for writing
# # # # # llm = ChatOpenAI(
# # # # #     openai_api_key="lm-studio",
# # # # #     base_url="http://127.0.0.1:1234/v1",
# # # # #     model="qwen2.5-7b-instruct"
# # # # # )

# # # # # def writer_agent(search_results: Dict[str, List[Dict]]) -> Dict[str, str]:
# # # # #     """
# # # # #     Writer Agent:
# # # # #     - Takes search results from Search Agent
# # # # #     - Generates a structured summary for each sub-question
# # # # #     Returns a dictionary: {sub_question: summary}
# # # # #     """
# # # # #     summaries = {}

# # # # #     for question, results in search_results.items():
# # # # #         # Prepare a prompt including all results
# # # # #         content_text = ""
# # # # #         for i, item in enumerate(results, 1):
# # # # #             title = item.get("title", "No title")
# # # # #             url = item.get("url", "No URL")
# # # # #             snippet = item.get("content", "") or ""
# # # # #             content_text += f"{i}. {title}\nURL: {url}\nContent: {snippet}\n\n"

# # # # #         prompt = f"""
# # # # # You are a Research Writer Agent.

# # # # # Generate a clear and concise summary for the following sub-question based on the search results.
# # # # # Make it professional, structured, and easy to understand.
# # # # # Include key points and insights. Do NOT invent information not present in the results.

# # # # # Sub-question: {question}

# # # # # Search Results:
# # # # # {content_text}

# # # # # Output: Summary as a paragraph or bullet points.
# # # # # """

# # # # #         response = llm.invoke([HumanMessage(content=prompt)])
# # # # #         summaries[question] = response.content

# # # # #     return summaries

# # # # # # ---------------------------
# # # # # # Example usage
# # # # # # ---------------------------
# # # # # if __name__ == "__main__":
# # # # #     # Example search results (replace with real output from your Search Agent)
# # # # #     example_results = {
# # # # #         "What is LangGraph?": [
# # # # #             {
# # # # #                 "title": "What is LangGraph? Docs, Demo and How to Deploy",
# # # # #                 "url": "https://www.shakudo.io/integrations/langgraph",
# # # # #                 "content": "LangGraph is a framework for building stateful, multi-agent applications using large language models (LLMs). It extends LangChain ..."
# # # # #             }
# # # # #         ]
# # # # #     }

# # # # #     summaries = writer_agent(example_results)
# # # # #     for question, summary in summaries.items():
# # # # #         print(f"\n=== {question} ===")
# # # # #         print(summary)




# # # # from langchain_openai import ChatOpenAI
# # # # from langchain_core.messages import HumanMessage
# # # # from typing import Dict, List

# # # # llm = ChatOpenAI(
# # # #     openai_api_key="lm-studio",
# # # #     base_url="http://127.0.0.1:1234/v1",
# # # #     model="qwen2.5-7b-instruct"
# # # # )

# # # # def writer_agent(search_results: Dict[str, List[Dict]]) -> Dict[str, str]:
# # # #     """
# # # #     Writer Agent:
# # # #     Generates structured summaries for each sub-question.
# # # #     Content truncated to 400 characters per result to speed up processing.
# # # #     """

# # # #     summaries = {}

# # # #     for question, items in search_results.items():
# # # #         content_text = ""
# # # #         for i, item in enumerate(items[:2], 1):  # top 2 results only
# # # #             title = item.get("title","No title")
# # # #             url = item.get("url","No URL")
# # # #             snippet = (item.get("content","") or "")[:400]
# # # #             content_text += f"{i}. {title}\nURL: {url}\nContent: {snippet}\n\n"

# # # #         prompt = f"""
# # # # You are a Research Writer Agent.

# # # # Write a clear, concise, and formal summary for the sub-question below
# # # # based ONLY on the provided content. Use academic/technical tone.

# # # # Sub-question:
# # # # {question}

# # # # Search Results:
# # # # {content_text}

# # # # Output: 3-4 bullet points.
# # # # """

# # # #         response = llm.invoke([HumanMessage(content=prompt)])
# # # #         summaries[question] = response.content.strip()

# # # #     return summaries



# # # # writer.py
# # # from langchain_openai import ChatOpenAI
# # # from langchain_core.messages import HumanMessage
# # # from typing import Dict, List

# # # # Initialize LM Studio Local LLM
# # # llm = ChatOpenAI(
# # #     openai_api_key="lm-studio",
# # #     base_url="http://127.0.0.1:1234/v1",
# # #     model="qwen2.5-7b-instruct"
# # # )

# # # def writer_agent(search_results: Dict[str, List[Dict]]) -> Dict[str, str]:
# # #     """
# # #     Writer Agent:
# # #     Generates structured, concise bullet-point summaries for each sub-question.
# # #     """
# # #     summaries = {}
# # #     for question, items in search_results.items():
# # #         content_text = ""
# # #         for i, item in enumerate(items[:2], 1):
# # #             title = item.get("title", "No title")
# # #             url = item.get("url", "No URL")
# # #             snippet = item.get("content", "")
# # #             content_text += f"{i}. {title}\nURL: {url}\nContent: {snippet}\n\n"

# # #         prompt = f"""
# # # You are a Research Writer Agent.
# # # Write 3 concise bullet points for the sub-question below
# # # based ONLY on the provided content. Use clear academic tone.

# # # Sub-question:
# # # {question}

# # # Search Results:
# # # {content_text}

# # # Output: 3 bullet points.
# # # """
# # #         response = llm.invoke([HumanMessage(content=prompt)])
# # #         summaries[question] = response.content.strip()
# # #     return summaries



# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage
# from typing import Dict, List

# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )

# def writer_agent(search_results: Dict[str, List[Dict]]) -> Dict[str, str]:
#     """
#     Writer Agent:
#     Generates 3-4 informative bullet points for each sub-question
#     while keeping summaries fast and concise.
#     """
#     prompt_parts = []
#     for i, (question, items) in enumerate(search_results.items(), 1):
#         snippet_text = ""
#         for item in items[:2]:  # top 2 results
#             content = (item.get("content", "") or "")[:500]  # slightly longer snippet
#             snippet_text += f"- {content}\n"
#         prompt_parts.append(f"{i}. {question}\n{snippet_text}")

#     full_prompt = f"""
# You are a Research Writer Agent.
# Write 3-4 concise bullet points for each sub-question below.
# Each bullet should be 1–2 sentences, informative, and based on the provided content.
# Do NOT write paragraphs. Include main points, examples, or insights if available.

# Sub-questions with search snippets:
# {chr(10).join(prompt_parts)}

# Output: 3-4 bullets per question only.
# """

#     response = llm.invoke([HumanMessage(content=full_prompt)])

#     # Split response into per-question summaries
#     summaries = {}
#     current_question_index = 1
#     for block in response.content.strip().split("\n\n"):
#         if current_question_index > len(search_results):
#             break
#         summaries[list(search_results.keys())[current_question_index-1]] = block.strip()
#         current_question_index += 1

#     return summaries

# # # writer.py
# # from langchain_openai import ChatOpenAI
# # from langchain_core.messages import HumanMessage
# # from typing import Dict, List

# # # Initialize LLM
# # llm = ChatOpenAI(
# #     openai_api_key="lm-studio",
# #     base_url="http://127.0.0.1:1234/v1",
# #     model="qwen2.5-7b-instruct"
# # )

# # def writer_agent(search_results: Dict[str, List[Dict]]) -> Dict[str, str]:
# #     """
# #     Writer Agent:
# #     Generates 3 concise bullet points per sub-question from search results.
# #     Uses top 1 result per question with 300-character snippets.
# #     """
# #     prompt_parts = []
# #     for i, (question, items) in enumerate(search_results.items(), 1):
# #         snippet_text = ""
# #         for item in items[:1]:  # Top 1 result only
# #             content = (item.get("content", "") or "")[:300]  # Snippet length
# #             snippet_text += f"- {content}\n"
# #         prompt_parts.append(f"{i}. {question}\n{snippet_text}")

# #     full_prompt = f"""
# # You are a Research Writer Agent.
# # Write 3 concise bullet points for each sub-question below.
# # Each bullet should be 1–2 sentences and informative.
# # Do NOT write paragraphs. Focus on main points only.

# # Sub-questions with search snippets:
# # {chr(10).join(prompt_parts)}

# # Output: 3 bullets per question only.
# # """

# #     response = llm.invoke([HumanMessage(content=full_prompt)])

# #     # Split response into per-question summaries
# #     summaries = {}
# #     current_question_index = 1
# #     for block in response.content.strip().split("\n\n"):
# #         if current_question_index > len(search_results):
# #             break
# #         summaries[list(search_results.keys())[current_question_index-1]] = block.strip()
# #         current_question_index += 1

# #     return summaries






# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage
# from typing import Dict, List

# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )

# def writer_agent(search_results: Dict[str, List[Dict]]) -> Dict[str, str]:
#     """
#     Writer Agent:
#     Generates 3 concise bullet points per sub-question.
#     Uses structured prompts like the first version but limits content length
#     and number of results for faster responses.
#     """
#     summaries = {}

#     for question, items in search_results.items():
#         # Prepare top 1–2 snippets, max 300 chars each
#         content_text = ""
#         for i, item in enumerate(items[:2], 1):
#             snippet = (item.get("content", "") or "")[:300]
#             title = item.get("title", "No title")
#             url = item.get("url", "No URL")
#             content_text += f"{i}. {title}\nURL: {url}\nContent: {snippet}\n\n"

#         # Structured prompt per question
#         prompt = f"""
# You are a Research Writer Agent.
# Write 3 concise bullet points (1–2 sentences each) for the sub-question below
# based ONLY on the provided content.

# Sub-question:
# {question}

# Search Results:
# {content_text}

# Output: 3 bullet points.
# """
#         response = llm.invoke([HumanMessage(content=prompt)])
#         summaries[question] = response.content.strip()

#     return summaries







