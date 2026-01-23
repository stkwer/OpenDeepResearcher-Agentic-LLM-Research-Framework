# OpenDeepResearcher

**OpenDeepResearcher** is an autonomous AI research system that transforms any complex topic into a comprehensive, structured report. It utilizes a multi-agent architecture to plan research strategies, gather real-time data from the web, and synthesize findings into professional-grade documents.

## Key Features

* **Autonomous Planning**: Decomposes broad research topics into specific, logical sub-questions.
* **Real-time Web Search**: Integrates with the **Tavily API** to perform deep, multi-query web searches for every research sub-question.
* **Intelligent Synthesis**: A dedicated Writer Agent analyzes search results to create executive summaries, detailed topical sections, and synthesized conclusions.
* **Streamlit Interface**: A modern, interactive web dashboard to monitor agent progress in real-time.
* **Local LLM Support**: Designed to work with local models via **LM Studio** for privacy and cost-efficiency.

## Multi-Agent Architecture

The system operates through three specialized agents:

1. **Planner Agent**: Breaks down the main topic into a structured roadmap of {N} sub-questions.
2. **Searcher Agent**: Executes high-precision web searches for each sub-question and gathers raw information.
3. **Writer Agent**: Synthesizes the gathered information, tracks unique references, and compiles the final report.

## Quick Start

### 1. Prerequisites

* Python 3.9+
* [LM Studio](https://lmstudio.ai/) (running a local model)
* [Tavily API Key](https://tavily.com/)

### 2. Installation

```bash
git clone https://github.com/yourusername/OpenDeepResearcher.git
cd OpenDeepResearcher
pip install -r requirements.txt

```

### 3. Configuration

Update `config.py` with your Tavily API key and local LLM endpoint details:

```python
SEARCHER_CONFIG = {
    "api_key": "your-tavily-api-key-here",
    "max_results_per_query": 5,
}

```

### 4. Running the App

```bash
streamlit run app.py

```

## Project Structure

* `app.py` / `main.py`: Streamlit web interface and session management.
* `pipeline.py`: Orchestrates the flow between planning and searching phases.
* `agents/`: Contains the logic for `PlannerAgent`, `SearcherAgent`, and `WriterAgent`.
* `config.py`: Centralized configuration for LLM providers and agent parameters.
* `llm_config.py`: Initialization for LangChain-based LLM connections.

## Technology Stack

* **Framework**: LangChain
* **UI**: Streamlit
* **Search Engine**: Tavily API
* **LLM Connectivity**: OpenAI-compatible API (LM Studio)

---
