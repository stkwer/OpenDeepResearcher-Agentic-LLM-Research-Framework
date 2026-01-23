"""
LLM configuration and initialization
Handles connection to local LM Studio
"""

from langchain_openai import ChatOpenAI
from config import LLM_CONFIG

def initialize_llm():
    """
    Initialize and return the LLM instance
    
    Returns:
        ChatOpenAI: Configured LLM instance
    """
    llm = ChatOpenAI(
        base_url=LLM_CONFIG["base_url"],
        api_key=LLM_CONFIG["api_key"],
        model=LLM_CONFIG["model"],
        temperature=LLM_CONFIG["temperature"],
    )
    return llm

# Create global LLM instance
llm = initialize_llm()
