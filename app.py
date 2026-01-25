import streamlit as st
import os
Shreeya-Bhalwatkar
import json
from datetime import date

# Import your backend agents
from agents.planner import PlannerAgent
from agents.searcher import SearcherAgent
from agents.writer import WriterAgent
from agents.introducer import IntroductionAgent
from agents.concluder import ConclusionAgent
from export_pdf import export_pdf
from core.memory import SessionMemory

# =========================
# CONFIG & MEMORY
# =========================
HISTORY_FILE = "history.json"
memory = SessionMemory()

st.set_page_config(
    page_title="OpenDeep Researcher",
    layout="wide"
)

# =========================
# UTILITIES
# =========================
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def question_to_heading(question: str) -> str:
    q = question.rstrip("?")
    return q[0].upper() + q[1:]

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = load_history()

defaults = {
    "generated": False,
    "topic": "",
    "final_report": "",
    "plan": [],
    "sources": [],
    "show_history": True
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# =========================
# STYLES (ONLY UI FIXES)
# =========================
st.markdown("""
            


 <style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #1e293b, #0f172a);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}


/* FIX: Tabs visibility */
.stTabs [role="tab"] {
    color: #e5e7eb !important;
    opacity: 1 !important;
    font-weight: 500;
}

.stTabs [role="tab"][aria-selected="true"] {
    color: #ffffff !important;
    opacity: 1 !important;
    border-bottom: 2px solid #38bdf8;
}

            .stTabs [data-baseweb="tab-list"] {
    gap: 24px;
}

.stTabs [role="tab"] {
    font-size: 1rem;
    padding-bottom: 8px;
}

            
            [data-testid="stWidgetLabel"] {
    color: #e5e7eb !important;
    opacity: 1 !important;
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 6px;
}

            
[data-testid="stSidebar"] {
    background-color: #020617 !important;
    border-right: 1px solid #1e293b;
}

.res-card {
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 20px;
}

.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    color: white;
    font-weight: 600;
    border: none;
}

.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    color: #94a3b8;
    font-size: 0.9rem;





/* REMOVE TOP WHITE BAR */
[data-testid="stHeader"] {
    display: none;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1e293b;
}

/* Sidebar title - History */
[data-testid="stSidebar"] h1 {
    color: white !important;
}

/* Cards */
.card {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 16px;
}

/* Labels & headings visibility */
label,
.stTextInput label {
    color: white !important;
}

/* Tabs: Report / Plan / Sources */
.stTabs [role="tab"] {
    color: white !important;
}

/* Start Research button text BLACK */
.stButton > button {
    color: #000000 !important;
    font-weight: 600;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 60px;
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (HISTORY)
# =========================
with st.sidebar:
    st.title(" History")

    if st.button("Toggle History"):
        st.session_state.show_history = not st.session_state.show_history

    if st.session_state.show_history:
        if os.path.exists("sessions"):
            files = sorted(os.listdir("sessions"), reverse=True)
            if not files:
                st.info("No research yet")

            for file in files:
                label = file.replace(".json", "").replace("_", " ").title()
                if st.button(label, key=file):
                    with open(os.path.join("sessions", file), "r") as f:
                        data = json.load(f)
                        st.session_state.topic = data["topic"]
                        st.session_state.plan = data["plan"]
                        st.session_state.final_report = data["report"]
                        st.session_state.sources = data.get("sources", [])
                        st.session_state.generated = True
                        st.rerun()

# =========================
# MAIN UI
# =========================
st.title("🔬 OpenDeep Researcher")
st.caption("Agentic AI Research Assistant")

st.markdown('<div class="card">', unsafe_allow_html=True)
topic_input = st.text_input(
    "What would you like to research?",
    value=st.session_state.topic,
    placeholder="Enter a complex topic..."
)
generate = st.button("Start Research")
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# BACKEND AGENT LOGIC
# =========================
if generate and topic_input:
    planner = PlannerAgent()
    searcher = SearcherAgent()
    writer = WriterAgent()
    intro_agent = IntroductionAgent()
    conclusion_agent = ConclusionAgent()

    with st.status("Running research pipeline...", expanded=True) as status:
        status.update(label="Creating research plan...")
        plan = planner.plan(topic_input)
        st.session_state.plan = plan

        report = f"# {topic_input.title()}\n\n**Date:** {date.today().strftime('%B %d, %Y')}\n\n---\n\n"
        report += f"## Introduction\n\n{intro_agent.write_intro(topic_input)}\n\n---\n"

        all_contents = []
        all_sources = []

        for i, question in enumerate(plan):
            status.update(label=f"Researching & Writing section {i+1}/{len(plan)}: {question}")

            heading = question_to_heading(question)
            results = searcher.search(question)
            content = writer.write_section(question, results)

            report += f"## {heading}\n\n{content}\n\n"

            for r in results:
                if r.get("url"):
                    all_sources.append(r["url"])
            all_contents.append(content)

        status.update(label="Finalizing conclusion...")
        report += "## Conclusion\n\n"
        report += conclusion_agent.write_conclusion(topic_input, "\n".join(all_contents))

        st.session_state.final_report = report
        st.session_state.sources = list(set(all_sources))
        st.session_state.generated = True
        st.session_state.topic = topic_input

        memory.save(topic_input, {
            "topic": topic_input,
            "plan": plan,
            "report": report,
            "sources": st.session_state.sources
        })

        status.update(label="Research completed!", state="complete")
        st.rerun()

# =========================
# RESULTS DISPLAY
# =========================
if st.session_state.generated:
    col1, col2 = st.columns([4, 1])

    with col2:
        st.write("DEBUG topic:", st.session_state.topic)

        if st.button("Generate PDF"):

            # ---- Safe filenames ----
            safe_topic = (
                st.session_state.topic
                .lower()
                .replace(" ", "_")
                .replace("/", "_")
            )

            md_file = f"research_{safe_topic}.md"
            pdf_file = f"{safe_topic}.pdf"

            # ---- Write markdown fresh (CRITICAL FIX) ----
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(st.session_state.final_report)

                if st.session_state.sources:
                    f.write("\n\n## References\n")
                    for s in st.session_state.sources:
                        f.write(f"- {s}\n")

            # ---- Generate PDF ----
            export_pdf(md_file, pdf_file)

            # ---- Download ----
            with open(pdf_file, "rb") as pdf:
                st.download_button(
                    "Download PDF",
                    pdf,
                    file_name=pdf_file,
                    mime="application/pdf",
                )

    tab1, tab2, tab3 = st.tabs(["📄 Report", "📋 Plan", "🔗 Sources"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(st.session_state.final_report)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for i, p in enumerate(st.session_state.plan):
            st.markdown(f"{i+1}. {p}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for s in st.session_state.sources:
            st.markdown(f"- [{s}]({s})")
        st.markdown('</div>', unsafe_allow_html=True)
# =========================
# FOOTER
# =========================
st.markdown(
    '<div class="footer">Made with ❤️ for Researchers</div>',
    unsafe_allow_html=True
)
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Import your Agents
from planner_agent import PlannerAgent
from searcher_agent import SearcherAgent
from writer_agent import WriterAgent

# --- PAGE CONFIG ---
st.set_page_config(page_title="Agentic Research Studio", page_icon="🧠", layout="wide")

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4CAF50; color: white; }
    .report-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🧠 Agentic AI Research Studio")
st.markdown("Enter a topic and watch the **Planner**, **Searcher**, and **Writer** agents work together.")

# --- INPUT SECTION ---
with st.container():
    topic = st.text_input("🔍 Research Topic", placeholder="e.g. Future of Quantum Computing in 2026")
    run_button = st.button("🚀 Start Research Pipeline")

# --- EXECUTION PIPELINE ---
if run_button:
    if not topic:
        st.warning("Please enter a topic first!")
    else:
        # Initialize Agents
        planner = PlannerAgent()
        searcher = SearcherAgent()
        writer = WriterAgent()

        # --- STEP 1: PLANNER PROCESS ---
        with st.status("📅 **Planner Agent** is analyzing the topic...", expanded=True) as status:
            st.write("Generating research questions...")
            questions = planner.run(topic)
            st.write("### Research Questions:")
            for q in questions:
                st.write(f"- {q}")
            status.update(label="Planning Complete!", state="complete", expanded=False)

        # --- STEP 2: SEARCHER PROCESS ---
        with st.status("🔍 **Searcher Agent** is browsing the web...", expanded=True) as status:
            st.write("Searching Tavily for factual data...")
            research_data = searcher.run(questions)
            st.write("Data successfully retrieved.")
            status.update(label="Search Complete!", state="complete", expanded=False)

        # --- STEP 3: WRITER PROCESS (The Great UI Output) ---
        st.divider()
        st.subheader("✍️ Final Research Report")
        
        with st.spinner("Writer Agent is synthesizing the report..."):
            final_report = writer.run(topic, research_data)
            
            # Displaying the report in a clean card-like container
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.markdown(final_report)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add a download button for the user
            st.download_button(
                label="📥 Download Report as Markdown",
                data=final_report,
                file_name=f"{topic.replace(' ', '_')}_report.md",
                mime="text/markdown"
            )

        st.balloons()
main
