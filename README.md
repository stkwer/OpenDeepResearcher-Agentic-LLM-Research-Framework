# 🧠OpenDeepResearcher — Agentic LLM Research Framework
A production-ready, agentic AI research framework that decomposes complex queries, performs live web retrieval, and synthesizes structured, academic-quality research reports. The system combines a modular multi-agent backend with a polished Streamlit interface and local LLM execution via LM Studio.

## ✨ Key Capabilities
* 🎨 **Modern Research UI**
  A dark-mode, glassmorphic Streamlit interface with custom CSS, inspired by premium AI research tools.

* 🤖 **Agentic Research Pipeline**
  * **Planner Agent:** Breaks complex research topics into focused sub-questions
  * **Search Agent:** Retrieves high-signal evidence via live web search (Tavily API)
  * **Writer Agent:** Synthesizes sources into a structured academic report (450–500 words)

* 🧠 **Session Memory & History**
  Persistent local chat history with support for renaming, pinning, and revisiting research sessions.

* 📄 **Export-Ready Reports**
  One-click PDF generation for all finalized research outputs.

* 🔐 **Local LLM Execution**
  Runs entirely on your machine using **LM Studio**, ensuring privacy, low latency, and zero inference cost.

## 🏛️ System Architecture
The framework follows a clean, modular agent-based design:
1. **User Input** – A broad or complex research query
2. **Planning Phase** – `planner_agent` generates a structured research plan
3. **Evidence Collection** – `search_agent` retrieves relevant sources from the web
4. **Synthesis** – `writer_agent` uses the **Mistral-7B-Instruct** model to generate a formal 10-section research report

This separation of concerns enables clarity, extensibility, and reproducibility.

## 🚀 Getting Started
### 🔧 Prerequisites
* Python **3.10+**
* [LM Studio](https://lmstudio.ai/)
* [Tavily API Key](https://tavily.com/)

### ⚙️ Environment Setup
Create a `.env` file in the project root:
```env
# LM Studio Configuration
LMSTUDIO_URL="your_local_lmstudio_url"
LOCAL_MODEL_NAME="model_you_are_using"
# Web Search API
TAVILY_API_KEY="your_tavily_api_key_here"
```

### 📦 Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/penDeepResearcher-Agentic-LLM-Research-Framework.git
cd penDeepResearcher-Agentic-LLM-Research-Framework
# Install dependencies
pip install -r requirements.txt
```

### ▶️ Run the Application
Ensure **LM Studio** is running and the model is loaded, then launch the UI:
```bash
streamlit run ui.py
```

## 🗂️ Project Structure
```text
RESEARCHER/
├── .venv/               # Virtual environment
├── chats/               # Local research session storage
├── .env                 # Environment variables
├── chat_store.py        # The logic for saving and loading research history
├── main.py              # Sub-question extraction & evidence deduplication
├── planner_agent.py     # Agent: Research planning
├── search_agent.py      # Agent: Tavily web search
├── writer_agent.py      # Agent: Academic report synthesis
├── ui.py                # Streamlit UI with glassmorphism styling
└── requirements.txt     # Project dependencies
```

## 📚 Academic Report Generation Logic
The **Writer Agent** is strictly configured to generate research outputs using the following academic structure:
1. Title
2. Abstract
3. Keywords
4. Introduction
5. Related Work
6. Methodology
7. Experiments & Results
8. Discussion
9. Conclusion & Future Work
10. References

This structure ensures consistency, clarity, and academic credibility.

## 🎛️ UI & UX Highlights
* 🪟 **Glassmorphism Design** – Blurred, semi-transparent containers for a premium feel
* 🧩 **Interactive Planning Stage** – Review or regenerate research plans before triggering web search
* 📌 **Session Management** – Pin, rename, or delete research sessions directly from the sidebar

## 🧪 Dependencies
```text
requests
python-dotenv
tavily-python
streamlit
fpdf
```

## 👥 Author
**Arpa Kundu**

## 📜 License
This project is licensed under the **MIT License**.
See the `LICENSE` file for details.
