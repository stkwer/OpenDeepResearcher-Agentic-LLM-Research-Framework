# 🤖 OpenDeepResearcher — Agentic LLM Research Framework

An agent-based research assistant that decomposes complex queries, retrieves relevant information, and produces clear, human-like explanations using a modular multi-agent architecture. The system combines a Streamlit interface with local LLM execution via LM Studio for private and low-latency inference.

---

## 🌿 Branch Information
All work in this branch is implemented under:

**Pranathi-Brahmasa**

This branch contains my complete implementation for evaluation and review.

---

## ✨ Key Capabilities

- **Modern Research Interface**  
  A dark-mode Streamlit UI with a conversational layout, session memory, and export options for generated research outputs.

- **Agentic Reasoning Pipeline**  
  A structured multi-agent workflow that mirrors human research reasoning:
  - **Planner Agent** – Breaks the user query into focused sub-questions  
  - **Searcher Agent** – Gathers relevant information for each sub-question  
  - **Writer Agent** – Synthesizes collected data into a coherent final response  

- **Transparent Reasoning Display**  
  Planner questions and search sources are displayed alongside the final answer for better interpretability.

- **Session Memory**  
  Maintains recent conversational context to improve continuity across interactions.

- **Export Support**  
  Allows generated responses to be exported as PDF or DOCX files.

- **Local LLM Execution**  
  Uses LM Studio’s OpenAI-compatible local API for privacy-preserving inference with zero external API cost.

---

## 🧠 System Architecture

User input flows through the system as follows:

1. The Planner Agent analyzes the query and generates sub-questions  
2. The Searcher Agent retrieves relevant information for each sub-question  
3. The Writer Agent produces a natural, structured explanation using the collected context  
4. The Streamlit interface presents the answer along with planner reasoning and sources  

This modular design makes the system extensible and easy to maintain.

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- LM Studio (local LLM server)  
- Git & GitHub  

---

## ▶️ How to Run

1. Start **LM Studio** and load a compatible instruction-tuned model  
2. Enable the local API server (default: `http://127.0.0.1:1234`)  
3. Install required dependencies:
   ```
   pip install streamlit fpdf python-docx requests
   ```
4. Run the application:
   ```
   streamlit run agents/app.py
   ```

---

## 📌 Notes

- This branch is intended for **individual evaluation**
- The `main` branch is maintained by the repository owner
- All implementation and documentation in this branch reflect my contribution

---

## 📜 License

This project is released under the MIT License.
