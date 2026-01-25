from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(
    openai_api_key="lm-studio",
    base_url="http://127.0.0.1:1234/v1",
    model="lmstudio-community/qwen2.5-7b-instruct"
)

messages = [
    HumanMessage(content="Write a Python function for factorial"),
    HumanMessage(content="Now write a function for Fibonacci sequence")
]

response = llm.generate([messages])
print(response.generations[0][0].text)

