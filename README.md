# 🧠 Agentic RAG Research System

An **Agentic Retrieval-Augmented Generation (RAG) Research System** that autonomously **plans, retrieves, analyzes, and synthesizes** research content using a **multi-agent architecture**, powered by a **locally hosted Large Language Model (LLM)** via **LM Studio**.

This project is implemented as part of the **OpenDeepResearcher: Agentic LLM Research Framework** introduced during the internship.

---

## 🎯 Project Objective

The primary goal of this system is to emulate a **professional research workflow** by combining planning, retrieval, and reasoning capabilities into an automated pipeline.

The system is designed to:

- Decompose a research topic into structured questions  
- Retrieve relevant, real-time information from the web  
- Perform grounded reasoning using retrieved context  
- Generate high-quality, structured technical documentation  
- Export research outputs in multiple professional formats  

---

## 🧩 Agentic System Architecture

The application follows a **sequential multi-agent workflow**, where each agent has a clearly defined responsibility.

### 1️⃣ Planner Agent
- Analyzes the user-provided topic  
- Generates dynamic, topic-specific research questions  
- Acts as the **strategic blueprint** for the research process  

### 2️⃣ Searcher Agent
- Uses the **Tavily Search API** for real-time web retrieval  
- Collects contextual facts and reference sources  
- Supplies grounded information to the Writer Agent  

### 3️⃣ Writer Agent
- Synthesizes planner questions and retrieved context  
- Produces a professional research report with:
  - Executive Summary  
  - Technical Analysis  
  - Challenges & Ethics  
  - Strategic Conclusion  

### 🔁 Workflow Pipeline

```

User Topic
↓
Planner Agent
↓
Searcher Agent
↓
Writer Agent
↓
Final Research Report

```

---

## 🧠 LLM & Model Configuration

### LLM Runtime
- **LM Studio** (Local inference)
- OpenAI-compatible REST API

### Model Details
- **Model Name**: Qwen2.5-1.5B-Instruct  
- **Architecture**: Qwen2  
- **Parameters**: 1.5 Billion  
- **Quantization**: Q8_0 (GGUF)  
- **License**: Apache-2.0  
- **Context Length**:
  - Training: 32,768 tokens  
  - Runtime: 4,096 tokens  
- **Model File**:
```

Qwen2.5-1.5B-Instruct.Q8_0.gguf

````

### API Endpoints Used
- `GET /v1/models`
- `POST /v1/chat/completions`

The application **automatically detects the active model** from LM Studio at runtime.

---

## 🌐 Web Search Integration

- **Service**: Tavily Search API  
- **Purpose**: Real-time information retrieval  
- **Used By**: Searcher Agent  

### Environment Variable Setup (Windows)

```bash
setx TAVILY_API_KEY your_api_key_here
````

---

## 🎨 User Interface

* Built using **Streamlit**
* Clean, card-based layout
* Dark mode & light (gold) mode toggle
* Guided and intuitive research flow:

```
Research Topic → Planner Agent→ Searcher Agent → Writer Agent → Export
```

---

## 📤 Export Capabilities

The final research report can be exported in the following formats:

* 📄 TXT
* 📄 PDF
* 📄 Word (.docx)

Each format preserves structured headings and readability.

---

## 📦 Dependencies

Install all required dependencies using:

```bash
pip install streamlit requests reportlab python-docx
```

### Dependency Overview

| Library     | Purpose              |
| ----------- | -------------------- |
| streamlit   | UI and interaction   |
| requests    | API communication    |
| reportlab   | PDF generation       |
| python-docx | Word document export |

---

## ▶️ How to Run the Project

### Step 1: Start LM Studio

1. Open **LM Studio**
2. Load the **Qwen2.5-1.5B-Instruct** model
3. Start the local server at:

```
http://127.0.0.1:1234
```

---

### Step 2: Run the Application

```bash
python -m streamlit run app.py
```

### Expected Terminal Output

```text
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://<your-ip>:8501
```

---

## 📁 Project Structure

```text
.
├── app.py        # Streamlit UI and application workflow
├── main.py       # Planner, Searcher, and Writer agent logic
├── README.md     # Project documentation
```


## ✅ Internship Alignment

This project fully aligns with the internship objectives by:

* Implementing a **complete agentic research pipeline**
* Using a **locally hosted LLM via LM Studio**
* Integrating **real-time web retrieval**
* Delivering a **polished UI with professional exports**
* Demonstrating **end-to-end system design and execution**

---

## 👤 Author

**GUJJU DINESH**
B.Tech – CSE(Artificial Intelligence)


---