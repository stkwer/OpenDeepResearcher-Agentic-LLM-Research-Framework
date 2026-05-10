from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import List
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192",   # or mixtral-8x7b
    temperature=0
)
def planner_agent(topic: str, num_subquestions: int = 8) -> List[str]:
    """
    Planner Agent:
    Generates exactly num_subquestions short, simple, professional sub-questions.
    Returns a Python list of sub-questions.
    """
    prompt = f"""
You are a Research Planner Agent.
Generate EXACTLY {num_subquestions} short, clear, simple sub-questions on the topic below.
Rules:
- One sentence per question
- Simple and professional tone
- No duplicates
- Cover multiple perspectives: technical, cost, security, risks, ethics, labor, future trends

Topic:
{topic}

Output: Numbered list only.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content.strip()

    sub_questions = [
        line.split(". ", 1)[1]
        for line in text.splitlines()
        if line.strip() and line[0].isdigit()
    ]

    return sub_questions














































































































# # # # from langchain_openai import ChatOpenAI
# # # # from langchain_core.messages import HumanMessage

# # # # # Initialize LM Studio Local LLM
# # # # llm = ChatOpenAI(
# # # #     openai_api_key="lm-studio",
# # # #     base_url="http://127.0.0.1:1234/v1",
# # # #     model="qwen2.5-7b-instruct"
# # # # )

# # # # def planner_agent(topic: str, num_subquestions: int = 6):
# # # #     """
# # # #     Planner Agent:
# # # #     Generates short, precise, research-focused sub-questions.
# # # #     """
# # # #     prompt = f"""
# # # # Break the topic below into EXACTLY {num_subquestions} short,
# # # # professional research sub-questions.

# # # # Rules:
# # # # - Each question must be one sentence only
# # # # - No long explanations
# # # # - No overlap between questions
# # # # - Focus on technical, economic, social, policy, risk, and future aspects

# # # # Topic:
# # # # "{topic}"

# # # # Return only a numbered list of sub-questions.
# # # # """

# # # #     response = llm.invoke([HumanMessage(content=prompt)])
# # # #     return response.content


# # # # if __name__ == "__main__":
# # # #     topic = input("Enter your topic or research question: ")
# # # #     plan = planner_agent(topic)

# # # #     print("\n--- Research Sub-Questions ---\n")
# # # #     print(plan)















































































# # from langchain_openai import ChatOpenAI
# # from langchain_core.messages import HumanMessage

# # # Initialize LM Studio Local LLM
# # llm = ChatOpenAI(
# #     openai_api_key="lm-studio",
# #     base_url="http://127.0.0.1:1234/v1",
# #     model="qwen2.5-7b-instruct"
# # )

# # def planner_agent(topic: str, num_subquestions: int = 8):
# #     """
# #     Planner Agent:
# #     Creates short and professional sub-queries strictly related to the topic.
# #     """
# #     prompt = f"""
# # You are a Research Planner Agent.

# # Generate EXACTLY {num_subquestions} high-quality sub-questions that are:
# # - Directly aligned to the topic
# # - Short (single sentence)
# # - Clear and professional
# # - Cover different perspectives (technical, cost, security, future scope, risks, etc.)
# # - Unique — no duplication

# # Main Topic: {topic}

# # Output: ONLY a numbered list of sub-questions.
# # """

# #     response = llm.invoke([HumanMessage(content=prompt)])
# #     return response.content


# # if __name__ == "__main__":
# #     topic = input("Enter your topic or research question: ")
# #     plan = planner_agent(topic)

# #     print("\n--- Research Sub-Questions ---\n")
# #     print(plan)



# # # from langchain_openai import ChatOpenAI
# # # from langchain_core.messages import HumanMessage

# # # # Initialize LM Studio Local LLM
# # # llm = ChatOpenAI(
# # #     openai_api_key="lm-studio",
# # #     base_url="http://127.0.0.1:1234/v1",
# # #     model="qwen2.5-7b-instruct"
# # # )

# # # def planner_agent(topic: str, num_subquestions: int = 8):
# # #     """
# # #     Planner Agent:
# # #     Creates short and professional sub-queries strictly related to the topic.
# # #     Returns a Python list of sub-questions.
# # #     """
# # #     prompt = f"""
# # # You are a Research Planner Agent.

# # # Generate EXACTLY {num_subquestions} high-quality sub-questions that are:
# # # - Directly aligned to the topic
# # # - Short (single sentence)
# # # - Clear and professional
# # # - Cover different perspectives (technical, cost, security, future scope, risks, etc.)
# # # - Unique — no duplication

# # # Main Topic: {topic}

# # # Output: ONLY a numbered list of sub-questions.
# # # """
# # #     response = llm.invoke([HumanMessage(content=prompt)])
# # #     text = response.content

# # #     # Convert numbered list string to Python list
# # #     sub_questions = [
# # #         line.split(". ", 1)[1]
# # #         for line in text.splitlines()
# # #         if line.strip()
# # #     ]
# # #     return sub_questions

# # # # Example usage
# # # if __name__ == "__main__":
# # #     topic = input("Enter your topic: ")
# # #     sub_questions = planner_agent(topic, num_subquestions=5)
# # #     print("\n--- Generated Sub-Questions ---")
# # #     for i, q in enumerate(sub_questions, 1):
# # #         print(f"{i}. {q}")




# # from langchain_openai import ChatOpenAI
# # from langchain_core.messages import HumanMessage
# # from typing import List

# # # Initialize LM Studio Local LLM
# # llm = ChatOpenAI(
# #     openai_api_key="lm-studio",
# #     base_url="http://127.0.0.1:1234/v1",
# #     model="qwen2.5-7b-instruct"
# # )

# # def planner_agent(topic: str, num_subquestions: int = 8) -> List[str]:
# #     """
# #     Planner Agent:
# #     Creates EXACTLY 8 formal, professional sub-questions.
# #     Returns a Python list of sub-questions.
# #     """

# #     prompt = f"""
# # You are a Research Planner Agent.

# # Generate EXACTLY {num_subquestions} formal and professional sub-questions.

# # Rules:
# # - Each question must be one clear sentence
# # - Academic and technical tone
# # - No duplication
# # - Cover multiple perspectives:
# #   definition, architecture, applications, security, risks, cost, scalability, future scope

# # Main Topic:
# # {topic}

# # Output:
# # ONLY a numbered list.
# # """

# #     response = llm.invoke([HumanMessage(content=prompt)])
# #     text = response.content.strip()

# #     # Convert numbered list to Python list
# #     sub_questions = [
# #         line.split(". ", 1)[1]
# #         for line in text.splitlines()
# #         if line.strip() and line[0].isdigit()
# #     ]

# #     return sub_questions




# # planner.py
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage
# from typing import List

# # Initialize LM Studio Local LLM
# llm = ChatOpenAI(
#     openai_api_key="lm-studio",
#     base_url="http://127.0.0.1:1234/v1",
#     model="qwen2.5-7b-instruct"
# )

# def planner_agent(topic: str, num_subquestions: int = 8) -> List[str]:
#     """
#     Planner Agent:
#     Generates exactly num_subquestions short, professional sub-questions.
#     Returns a Python list of sub-questions.
#     """
#     prompt = f"""
# You are a Research Planner Agent.
# Generate EXACTLY {num_subquestions} short, clear, professional sub-questions on the topic below.
# Rules:
# - One sentence per question
# - Academic/technical tone
# - No duplicates
# - Cover multiple perspectives: definition, architecture, applications, security, risks, cost, scalability, future scope

# Topic:
# {topic}

# Output: Numbered list only.
# """
#     response = llm.invoke([HumanMessage(content=prompt)])
#     text = response.content.strip()

#     # Convert numbered list to Python list
#     sub_questions = [
#         line.split(". ", 1)[1]
#         for line in text.splitlines()
#         if line.strip() and line[0].isdigit()
#     ]

#     return sub_questions


