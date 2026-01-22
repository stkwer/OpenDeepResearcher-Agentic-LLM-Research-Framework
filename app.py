import streamlit as st
import uuid
from OpenResearcher import (
    planner_agent,
    searcher_agent,
    writer_agent,
    synthesize_final_report,
    stream_synthesize_final_report
)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import textwrap
import tempfile
import os

def generate_pdf(report_text, filename="research_report.pdf"):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=A4)

    width, height = A4
    x_margin = 1 * inch
    y_margin = 1 * inch
    max_width = width - 2 * x_margin

    y = height - y_margin

    c.setFont("Times-Roman", 11)

    for paragraph in report_text.split("\n"):
        wrapped_lines = textwrap.wrap(paragraph, 90)

        if not wrapped_lines:
            y -= 14
            continue

        for line in wrapped_lines:
            if y < y_margin:
                c.showPage()
                c.setFont("Times-Roman", 11)
                y = height - y_margin

            c.drawString(x_margin, y, line)
            y -= 14

        y -= 6  # space between paragraphs

    c.save()
    return temp_file.name

# =========================
# SESSION STATE (GLOBAL)
# =========================
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

if "active_query" not in st.session_state:
    st.session_state.active_query = None

if "force_regenerate" not in st.session_state:
    st.session_state.force_regenerate = False

if "planner_done" not in st.session_state:
    st.session_state.planner_done = False

if "show_main_warning" not in st.session_state:
    st.session_state.show_main_warning = True

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="OpenDeepResearcher",
    page_icon="🔬",
    layout="wide"
)

# =========================
# HEADER
# =========================
st.title("🔬 OpenDeepResearcher")
st.markdown(
    "An **AI-powered research assistant** that plans, searches, and synthesizes information into structured reports."
)


# =========================
# MAIN SCREEN WELCOME
# =========================
if st.session_state.show_main_warning and not st.session_state.planner_done:
    st.markdown(
        """
        <div style="
            padding: 1.5rem;
            border-radius: 14px;
            background: linear-gradient(135deg, #1f2933, #111827);
            border: 1px solid #2d3748;
            margin-top: 1.5rem;
            max-width: 900px;
        ">
            <h3>👋 Welcome to OpenDeepResearcher</h3>
            <p>For your <b>first research</b>, we recommend using <b>Deep mode</b>.</p>
            <ul>
                <li>🧠 Planner breaks the topic</li>
                <li>🔎 Searcher gathers evidence</li>
                <li>✍️ Writer produces a structured report</li>
            </ul>
            <p style="opacity:0.7;">⌨️ Start by typing a research question below.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("⚙️ Settings")
    # ---- NEW RESEARCH ----
    if st.button("➕ New Research", use_container_width=True):
        st.session_state.current_session_id = None
        st.session_state.active_query = None
        st.session_state.planner_done = False
        st.session_state.show_main_warning = True
        st.rerun()

    mode = st.radio(
        "Research mode",
        ["Deep", "Fast"],
        help="Deep = full research, Fast = quicker summary"
    )

    if mode == "Deep":
        st.success(
            "🔍 Deep mode\n\n"
            "- First-time exploration\n"
            "- Academic / detailed reports\n"
            "- Maximum sources"
        )
    else:
        st.info(
            "⚡ Fast mode\n\n"
            "- Overviews\n"
            "- Follow-ups\n"
            "- Faster answers"
        )

    # ---------- HISTORY ----------
    st.divider()
    st.subheader("🕘 History")

    for sid, session in reversed(st.session_state.sessions.items()):
        if st.button(
            session["title"],
            key=f"session_{sid}",
            use_container_width=True
        ):
            st.session_state.current_session_id = sid

            current = st.session_state.sessions[sid]
            st.session_state.planner_questions = current["planner_questions"]
            st.session_state.result = current["result"]
            st.session_state.sources = current["sources"]
            st.session_state.planner_done = bool(current["planner_questions"])

            st.rerun()

# =========================
# DISPLAY CHAT (ACTIVE SESSION)
# =========================
if st.session_state.current_session_id:
    current = st.session_state.sessions[st.session_state.current_session_id]

    for msg in current["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# =========================
# USER INPUT
# =========================
user_input = st.chat_input("Ask a research question...")

if user_input:
    # Create session if none
    if st.session_state.current_session_id is None:
        sid = str(uuid.uuid4())
        st.session_state.sessions[sid] = {
            "title": user_input[:40],
            "chat_history": [],
            "planner_questions": None,
            "result": None,
            "sources": []
        }
        st.session_state.current_session_id = sid

    current = st.session_state.sessions[st.session_state.current_session_id]
    st.session_state.active_query = user_input

    # Reset state for new query
    current["planner_questions"] = None
    current["result"] = None
    current["sources"] = []
    st.session_state.planner_done = False

    current["chat_history"].append(
        {"role": "user", "content": user_input}
    )

# =========================
# PLANNER
# =========================
if st.session_state.active_query and not st.session_state.planner_done:
    with st.spinner("🧠 Generating research questions..."):
        plan = planner_agent(st.session_state.active_query)
        questions = plan.get("sub_questions", [])

        current = st.session_state.sessions[st.session_state.current_session_id]
        current["planner_questions"] = questions

        st.session_state.planner_done = True
        st.session_state.show_main_warning = False

    st.success("✅ Research questions generated")

# =========================
# REVIEW & EDIT PLAN
# =========================
edited_questions = []

if st.session_state.current_session_id:
    current = st.session_state.sessions[st.session_state.current_session_id]

    if current["planner_questions"]:
        st.markdown("### 🧠 Review & Edit Research Plan")

        for i, q in enumerate(current["planner_questions"]):
            edited_questions.append(
                st.text_input(f"Question {i+1}", q, key=f"planner_edit_{i}")
            )

# =========================
# ACTION BUTTONS
# =========================
if st.session_state.planner_done:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Regenerate Questions"):
            current["planner_questions"] = None
            current["result"] = None
            current["sources"] = []
            st.session_state.planner_done = False
            st.rerun()

    with col2:
        generate_report = st.button(
            "▶️ Generate Report",
            disabled=not edited_questions
        )
else:
    generate_report = False

# =========================
# GENERATE REPORT
# =========================
if generate_report:
    with st.spinner("🔎 Running research..."):
        if mode == "Fast":
            search_questions = edited_questions[:2]
        else:
            search_questions = edited_questions[:4]  # 👈 use only top 4 for report


        search_data = searcher_agent(search_questions)

        sources = sorted({
            item["url"]
            for items in search_data.values()
            for item in items
            if item.get("url")
        })

        sections = writer_agent(search_data)
        stream_container = st.empty()
        streamed_text = ""
        
        def on_stream_update(text):
            stream_container.markdown("### 📘 Research Report\n" + text)

        report = stream_synthesize_final_report(
            sections,
            stream_callback=on_stream_update
            )
        current["result"] = report
        current["chat_history"].append(
            {"role": "assistant", "content": "### 📘 Research Report\n" + report}
            )



        current["sources"] = sources
        current["result"] = report

        current["chat_history"].append(
            {"role": "assistant", "content": "### 📘 Research Report\n" + report}
        )

# =========================
# DISPLAY REPORT
# =========================
if st.session_state.current_session_id:
    current = st.session_state.sessions[st.session_state.current_session_id]

    if current["result"]:
        with st.chat_message("assistant"):
            st.markdown("### 📘 Research Report")
            st.markdown(current["result"])

            if current["sources"]:
                with st.expander(f"🔗 Sources ({len(current['sources'])})"):
                    for link in current["sources"]:
                        st.markdown(f"- [{link}]({link})")

            col_txt, col_pdf = st.columns(2)
            with col_txt:
                st.download_button(
                    "📄 Download TXT",
                    current["result"],
                    file_name="research_report.txt",
                    mime="text/plain"
                )
            with col_pdf:
                pdf_path = generate_pdf(current["result"])
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📕 Download PDF",
                        f,
                        file_name="research_report.pdf",
                        mime="application/pdf"
                        )
                   
                    
