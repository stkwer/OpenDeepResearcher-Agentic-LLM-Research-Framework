import time
import json
from datetime import datetime

import streamlit as st

from agents import planner_agent, searcher_agent, writer_agent


# ============== Page Config & Styles ==============

st.set_page_config(
    page_title="OpenDeepResearcher",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
        text-align: center;
        margin-bottom: 1.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .chat-wrapper {
        max-width: 900px;
        margin: 0 auto;
    }
    .chat-bubble {
        padding: 0.9rem 1rem;
        border-radius: 12px;
        margin: 0.35rem 0;
        font-size: 0.95rem;
    }
    .chat-user {
        background: #ecfeff;
        border-left: 4px solid #06b6d4;
    }
    .chat-agent {
        background: #eef2ff;
        border-left: 4px solid #4f46e5;
    }
    .chat-meta {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 0.1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-header">🔬 OpenDeepResearcher</h1>', unsafe_allow_html=True)
st.markdown(
    """
<div style='text-align: center; color: #64748b; font-size: 1.05rem; margin-bottom: 1.5rem;'>
Transform any research topic into a comprehensive report in seconds.<br>
<small>Powered by AI Agents: Planner → Searcher → Writer</small>
</div>
""",
    unsafe_allow_html=True,
)


# ============== Helpers ==============

def add_history(role: str, stage: str, text: str):
    """Append a message to the visible interaction history."""
    st.session_state.history.append(
        {
            "role": role,      # "user" or "agent"
            "stage": stage,    # "Topic", "Planner", "Searcher", "Writer"
            "text": text,
            "ts": datetime.now().isoformat(),
        }
    )


# ============== Session State ==============

if "history" not in st.session_state:
    st.session_state.history = []
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "status" not in st.session_state:
    st.session_state.status = "Ready"
if "last_report" not in st.session_state:
    st.session_state.last_report = None


# ============== Sidebar ==============

with st.sidebar:
    st.markdown("## 🤖 Agents")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Planner", "Ready", "v1.0")
    with col2:
        st.metric("Searcher", "Ready", "Tavily")
    with col3:
        st.metric("Writer", "Ready", "v1.0")

    st.markdown("---")
    st.caption(f"Status: {st.session_state.status}")

    if st.button("🔄 Reset conversation", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ============== Main Chat Area ==============

st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

for msg in st.session_state.history:
    is_user = msg["role"] == "user"
    bubble_class = "chat-user" if is_user else "chat-agent"
    who = "You" if is_user else "Researcher"
    stage = msg["stage"]
    text_html = msg["text"].replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="chat-bubble {bubble_class}">
          <div class="chat-meta"><strong>{who}</strong> · {stage}</div>
          <div>{text_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Show final report (if exists) as the last agent message
if st.session_state.last_report:
    report = st.session_state.last_report
    exec_summary = report.get("executive_summary", "")
    conclusion = report.get("conclusion", "")
    sections = report.get("sections", {})
    refs = report.get("references", [])

    parts = []

    if exec_summary:
        parts.append("### Executive Summary\n\n" + exec_summary)

    if sections:
        parts.append("### Sections")
        for i, (sec_key, sec) in enumerate(sections.items(), start=1):
            sub_q = sec.get("sub_question", "")
            content = sec.get("content", "")
            parts.append(f"**{i}. {sub_q}**\n\n{content}")

    if conclusion:
        parts.append("### Conclusion\n\n" + conclusion)

    if refs:
        parts.append("### References")
        for ref in refs:
            num = ref.get("number", "")
            url = ref.get("url", "")
            title = ref.get("title") or url
            parts.append(f"{num}. [{title}]({url})")

    report_text = "\n\n".join(parts)
    report_text_html = report_text.replace("\n", "<br>")

    st.markdown(
        """
        <div class="chat-bubble chat-agent">
          <div class="chat-meta"><strong>Researcher</strong> · Final Report</div>
          <div>""" + report_text_html + """</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)


# ============== Input Bar ==============

st.markdown("---")
with st.form(key="topic_form", clear_on_submit=False):
    topic = st.text_input(
        "Enter a research topic:",
        placeholder="e.g., AI in healthcare",
    )
    submitted = st.form_submit_button("Generate Plan & Report")

# ============== Pipeline: Planner → Searcher → Writer ==============

if submitted and not st.session_state.is_running:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        st.session_state.is_running = True
        st.session_state.status = "Running pipeline..."
        add_history("user", "Topic", topic.strip())
        st.rerun()

if st.session_state.is_running:
    # get latest topic
    user_msgs = [m for m in st.session_state.history if m["role"] == "user"]
    current_topic = user_msgs[-1]["text"] if user_msgs else None

    if not current_topic:
        st.session_state.is_running = False
        st.session_state.status = "Ready"
    else:
        # 1) Planner
        with st.spinner("Planner Agent: creating sub-questions..."):
            plan = planner_agent.run(current_topic)
        if not plan:
            add_history("agent", "Planner", "Failed to generate sub-questions. Try a clearer topic.")
            st.session_state.status = "Planner failed"
            st.session_state.is_running = False
            st.rerun()

        sub_qs = plan["sub_questions"]
        lines = []
        for i, q in enumerate(sub_qs, start=1):
            lines.append(f"Q{i}. {q}")
        planner_text = "Generated sub-questions:\n" + "\n".join(lines)
        add_history("agent", "Planner", planner_text)
        st.session_state.status = "Searching..."
        st.rerun()

        # 2) Searcher
        with st.spinner("Searcher Agent: gathering sources for each sub-question..."):
            search_results = searcher_agent.search_multiple(sub_qs)

        if not search_results:
            add_history("agent", "Searcher", "Search failed. Check API key or network.")
            st.session_state.status = "Search failed"
            st.session_state.is_running = False
            st.rerun()

        success_count = search_results["search_session"]["successful_searches"]
        add_history(
            "agent",
            "Searcher",
            f"Found information for {success_count} sub-questions.",
        )
        st.session_state.status = "Writing final report..."
        st.rerun()

        # 3) Writer
        with st.spinner("Writer Agent: synthesizing final report..."):
            report = writer_agent.synthesize_multiple(plan, search_results)

        if not report:
            add_history("agent", "Writer", "Failed to generate final report.")
            st.session_state.status = "Writer failed"
            st.session_state.is_running = False
            st.rerun()

        st.session_state.last_report = report
        add_history("agent", "Writer", "Generated the full research report (see below).")
        st.session_state.status = "Done"
        st.session_state.is_running = False
        st.rerun()


# ============== Footer ==============

st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>
Built with ❤️ for AI Research · OpenDeepResearcher v1.0
</div>
""",
    unsafe_allow_html=True,
)
