import json
import re

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# LLM Configuration
planner_llm = ChatOpenAI(
    model="qwen2.5-7b-instruct",
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    temperature=0,
    max_tokens=1024,  # cap output length for speed
)

# Planner Agent Prompt
planner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are the Planner Agent in the OpenDeepResearcher system.

Task:
1. Understand the user's research query.
2. Break it into 4–10 clear, non-overlapping sub-questions.
3. For each sub-question, include:
   - search_query: short, web-searchable phrase
   - keywords: 3–8 important terms
   - rationale: <= 25 words
   - expected_output: <= 25 words

Rules:
- ONLY output valid JSON.
- Do NOT include markdown like ``` or ```json.
- Follow this exact JSON structure:

{{
  "main_topic": "",
  "sub_questions": [
    {{
      "id": 1,
      "question": "",
      "search_query": "",
      "keywords": [],
      "rationale": "",
      "expected_output": ""
    }}
  ]
}}
"""
    ),
    ("user", "{user_query}")
])

# Build the chain once
planner_chain = planner_prompt | planner_llm


# Clean Model Output (remove any accidental markdown)
def clean_json_output(raw_text: str) -> str:
    # Remove common code fences if the model accidentally adds them
    cleaned = re.sub(r"```json|```", "", raw_text).strip()
    cleaned = cleaned.replace("\u200b", "").strip()
    return cleaned


# Planner Agent Logic
def planner_agent(user_query: str):
    response = planner_chain.invoke({"user_query": user_query})

    raw_output = response.content.strip()
    cleaned_output = clean_json_output(raw_output)

    try:
        return json.loads(cleaned_output)
    except Exception:
        print("\nRAW OUTPUT:\n")
        print(raw_output)
        print("\nCLEANED OUTPUT:\n")
        print(cleaned_output)
        raise ValueError("Planner Agent did not return valid JSON.")


# Main Program (Take user input and print sub-questions)
if __name__ == "__main__":
    print("DEBUG: Script imported successfully")
    print(f"DEBUG: __name__ = {__name__}")

    try:
        user_query = input("Enter your main research topic: ")
        print("DEBUG: Got user input:", user_query)

        plan = planner_agent(user_query)

        print("\nGenerated Sub-Questions:\n")
        for sub in plan["sub_questions"]:
            print(f"{sub['id']}. {sub['question']}")
    except Exception as e:
        print("DEBUG: Exception occurred:", repr(e))
