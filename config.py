"""
Configuration file for OpenDeepResearcher
"""

# LLM Configuration
LLM_CONFIG = {
    "provider": "lm_studio",
    "base_url": "http://localhost:1234/v1",
    "api_key": "lm-studio",
    "model": "local-model",
    "temperature": 0.3,  # Lower for consistent planning
}

# Planner Agent Configuration
PLANNER_CONFIG = {
    "num_sub_questions": 5,
    "output_format": "json",  # Always JSON for structured data
    "include_research_strategy": True,
}

# Searcher Agent Configuration (Week 3-4)
SEARCHER_CONFIG = {
    "api_provider": "tavily",
    "api_key": "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",  # Replace with your actual key
    "max_results_per_query": 5,
    "include_source_urls": True,
    "include_answer_snippet": True,
}

# Writer Agent Configuration (Week 3-4)
WRITER_CONFIG = {
    "output_format": "markdown",
    "include_citations": True,
    "include_timestamps": True,
}

# Report Generation Configuration
REPORT_CONFIG = {
    "sections": ["Overview", "Detailed Findings", "Synthesis", "Conclusion"],
    "include_references": True,
    "include_metadata": True,
}

# Memory Configuration (Week 5-6)
MEMORY_CONFIG = {
    "save_threads": True,
    "storage_type": "local",  # local, database, etc.
}
