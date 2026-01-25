# config.py - Configuration settings for OpenDeepResearcher

# LLM Configuration
LLM_CONFIG = {
    "api_key": "lm-studio",
    "base_url": "http://127.0.0.1:1234/v1",
    "model": "qwen2.5-7b-instruct",
    "temperature": 0.7,
    "max_tokens": 2000
}

# Research Configuration
RESEARCH_CONFIG = {
    "num_subquestions": 8,
    "max_results_per_query": 1,  # Reduced from 2 to 1 for speed
    "search_timeout": 3,  # Reduced from 5 to 3 seconds
    "content_snippet_length": 200,  # Reduced from 350 to 200 chars
    "search_depth": "basic"
}

# UI Configuration
UI_CONFIG = {
    "page_title": "OpenDeepResearcher",
    "page_icon": "🔍",
    "layout": "wide",
    "sidebar_state": "expanded"
}

# File Configuration
FILE_CONFIG = {
    "report_format": "txt",
    "max_history_items": 50
}