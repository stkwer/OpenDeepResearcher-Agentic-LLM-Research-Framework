# OpenDeepResearcher – AI Autonomous Research Assistant

> An AI-powered autonomous research platform that automatically plans, searches, analyzes, and generates comprehensive academic research papers using a local LLM, eliminating cloud AI API costs.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![React](https://img.shields.io/badge/React-18-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-purple)
![LM Studio](https://img.shields.io/badge/LLM-LM%20Studio-green)

---

# Overview

OpenDeepResearcher is a full-stack AI research assistant that mimics the workflow of a human researcher. Given any research topic, it automatically breaks the problem into sub-questions, searches the web, synthesizes information, evaluates research completeness, and produces a professional academic research paper.

The application is powered by a **local Large Language Model (LLM)** running through **LM Studio**, allowing users to perform advanced AI-powered research without paying for cloud AI APIs. The backend is built with **FastAPI** and **LangGraph**, while the frontend is developed using **React** and **Vite**, providing a fast and interactive user experience.

---

# Features

- 🤖 Autonomous Multi-Agent Research Pipeline
- 🧠 Local LLM Integration using LM Studio
- 🌐 Real-time DuckDuckGo Web Search
- 🔄 LangGraph-based Agent Workflow
- 📡 Live Progress Updates using Server-Sent Events (SSE)
- 📄 Automatic Academic Research Report Generation
- 📑 Export Reports as PDF
- 📊 Export Reports as PowerPoint (PPTX)
- 💬 Follow-up Question Answering
- 🎤 Voice Input Support
- 📚 Retrieval-Augmented Generation (RAG)
- 📝 Document Upload and Search
- 🌙 Dark & Light Theme
- 🕒 Session History
- 📱 Responsive Modern Interface

---

# Architecture

```text
                    User Topic
                        │
                        ▼
                React Frontend
                        │
                HTTP / SSE
                        │
                        ▼
                FastAPI Backend
                        │
                        ▼
             LangGraph Research Pipeline

        Planner
            │
            ▼
        Searcher
            │
            ▼
         Writer
            │
            ▼
      Reflection
     ┌────────────┐
     │ Continue?  │
     └──────┬─────┘
            │
     Yes ◄──┘
            │
            ▼
        Reporter
            │
            ▼
     Academic Research Paper
            │
            ▼
 PDF │ PPTX │ Follow-up Q&A
```

---

# Tech Stack

## Frontend
- React 18
- Vite
- React Markdown
- CSS Modules

## Backend
- Python 3.12
- FastAPI
- Uvicorn
- LangGraph
- LangChain
- LangChain OpenAI

## AI
- LM Studio
- Qwen2.5-3B-Instruct
- OpenAI Compatible API

## Search
- DuckDuckGo Search (DDGS)

## Export
- ReportLab
- python-pptx

## Other Libraries
- PyPDF2
- python-dotenv

---

# Multi-Agent Workflow

### 📝 Planner
Breaks the research topic into focused sub-questions to create a structured research plan.

### 🔍 Searcher
Retrieves real-time information using DuckDuckGo and searches uploaded RAG documents when available.

### ✍️ Writer
Summarizes search results into coherent research notes while continuously improving the report.

### 🤔 Reflection
Evaluates whether sufficient information has been collected or another research iteration is required.

### 📄 Reporter
Generates a polished academic research paper containing:
- Title
- Abstract
- Introduction
- Key Findings
- Applications
- Challenges
- Future Outlook
- Conclusion
- References

---

# Project Structure

```
OpenDeepResearcher/
│
├── agents/
│   ├── planner.py
│   ├── searcher.py
│   ├── writer.py
│   ├── reflection.py
│   └── reporter.py
│
├── frontend/
│
├── utils/
│   ├── llm_client.py
│   ├── pdf_export.py
│   ├── pptx_export.py
│   ├── rag.py
│   └── state.py
│
├── data/
│
├── graph.py
├── server.py
├── config.py
├── requirements.txt
└── .env
```

---

# API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/research` | POST | Generate complete research report |
| `/research/stream` | POST | Stream research progress |
| `/followup` | POST | Ask questions about the generated report |
| `/export/pdf` | POST | Download report as PDF |
| `/export/pptx` | POST | Download report as PowerPoint |
| `/rag/upload` | POST | Upload documents for RAG |
| `/rag/search` | POST | Search uploaded documents |
| `/health` | GET | Server health check |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/OpenDeepResearcher.git
cd OpenDeepResearcher
```

## Install Backend

```bash
pip install -r requirements.txt
```

## Install Frontend

```bash
cd frontend
npm install
```

---

# Environment Variables

Create a `.env` file:

```env
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=lm-studio
LLM_MODEL_NAME=qwen2.5-3b-instruct

MAX_SEARCH_RESULTS=5
MAX_RESEARCH_LOOPS=2

APP_HOST=0.0.0.0
APP_PORT=8000
```

---

# Running the Application

### Step 1: Start LM Studio

- Load your preferred LLM
- Start the Local Server

### Step 2: Start Backend

```bash
python server.py
```

### Step 3: Start Frontend

```bash
cd frontend
npm run dev
```

Open your browser:

```
http://localhost:5173


---

# Future Improvements

- Multiple LLM Support
- Google Scholar Integration
- Citation Quality Evaluation
- Research Mind Maps
- Docker Deployment
- Cloud Deployment
- Collaborative Research Sessions
- Advanced Semantic Search

---

# Why OpenDeepResearcher?

- Runs entirely on a local LLM
- No AI API costs
- Autonomous multi-agent workflow
- Real-time research progress
- Retrieval-Augmented Generation (RAG)
- Modern responsive UI
- Professional PDF and PPT exports
- Interactive follow-up Q&A

---

# Author

Shreeya Bhalwatkar
⭐ If you found this project useful, consider giving it a Star!
