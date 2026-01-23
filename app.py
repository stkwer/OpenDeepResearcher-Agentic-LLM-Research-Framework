import time
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
            "stage": stage,    # e.g., "Topic", "Planner", "Decision", "Searcher", "Writer"
            "text": text,
            "ts": datetime.now().isoformat(),
        }
    )


# ============== Session State ==============

if "history" not in st.session_state:
    st.session_state.history = []
if "status" not in st.session_state:
    st.session_state.status = "Ready"
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "current_search_results" not in st.session_state:
    st.session_state.current_search_results = None
if "awaiting_decision" not in st.session_state:
    st.session_state.awaiting_decision = False
if "stage" not in st.session_state:
    # "idle", "planning", "searching", "writing"
    st.session_state.stage = "idle"


# ============== Sidebar ==============

with st.sidebar:
    st.markdown("## 🤖 Agents")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Planner", "Ready", "v1.0")
    with c2:
        st.metric("Searcher", "Ready", "Tavily")
    with c3:
        st.metric("Writer", "Ready", "v1.0")

    st.markdown("---")
    st.caption(f"Status: {st.session_state.status}")

    if st.button("🔄 Reset conversation", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ============== Chat History Display ==============

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

st.markdown("</div>", unsafe_allow_html=True)


# ============== Decision Buttons (after sub-questions) ==============

st.markdown("---")

if st.session_state.awaiting_decision and st.session_state.current_plan is not None:
    st.info("Generate a full research report based on these sub-questions?")
    c_yes, c_no = st.columns(2)
    with c_yes:
        yes_generate = st.button("✅ Yes, generate report", key="btn_yes_generate")
    with c_no:
        no_regen = st.button("🔁 No, regenerate sub-questions", key="btn_no_regen")

    if yes_generate:
        add_history("user", "Decision", "Yes, generate report based on these sub-questions.")
        st.session_state.awaiting_decision = False
        st.session_state.stage = "searching"
        st.session_state.status = "Searching and writing report..."
        st.rerun()

    if no_regen:
        topic = st.session_state.current_topic
        add_history("user", "Decision", "No, regenerate sub-questions.")
        st.session_state.awaiting_decision = False
        st.session_state.current_plan = None
        st.session_state.status = "Regenerating sub-questions..."

        with st.spinner("Planner Agent: regenerating sub-questions..."):
            new_plan = planner_agent.run(topic)

        if not new_plan:
            add_history(
                "agent",
                "Planner",
                "Failed to regenerate sub-questions. Try a different or clearer topic.",
            )
            st.session_state.status = "Planner failed"
        else:
            st.session_state.current_plan = new_plan
            sub_qs = new_plan["sub_questions"]
            lines = [f"Q{i}. {q}" for i, q in enumerate(sub_qs, start=1)]
            planner_text = "Regenerated sub-questions:\n" + "\n".join(lines)
            add_history("agent", "Planner", planner_text)
            st.session_state.awaiting_decision = True

        st.rerun()


# ============== Topic Input (when idle / no decision pending) ==============

if not st.session_state.awaiting_decision and st.session_state.stage == "idle":
    with st.form(key="topic_form", clear_on_submit=True):
        topic = st.text_input(
            "Enter a research topic to start a new analysis:",
            placeholder="e.g., AI in healthcare",
        )
        submitted = st.form_submit_button("Generate sub-questions")

    if submitted:
        if not topic.strip():
            st.warning("Please enter a research topic.")
        else:
            topic = topic.strip()
            st.session_state.current_topic = topic
            st.session_state.current_plan = None
            st.session_state.current_search_results = None
            st.session_state.awaiting_decision = False
            st.session_state.stage = "planning"
            add_history("user", "Topic", topic)
            st.session_state.status = "Planning..."
            st.rerun()


# ============== Orchestration Logic ==============

# 1) Planner stage
if (
    st.session_state.stage == "planning"
    and st.session_state.current_topic is not None
    and st.session_state.current_plan is None
):
    with st.spinner("Planner Agent: creating research roadmap..."):
        plan = planner_agent.run(st.session_state.current_topic)

    if not plan:
        add_history(
            "agent",
            "Planner",
            "Failed to generate sub-questions. Try a different or clearer topic.",
        )
        st.session_state.status = "Planner failed"
        st.session_state.stage = "idle"
    else:
        st.session_state.current_plan = plan
        sub_qs = plan["sub_questions"]
        lines = [f"Q{i}. {q}" for i, q in enumerate(sub_qs, start=1)]
        planner_text = "Generated sub-questions:\n" + "\n".join(lines)
        add_history("agent", "Planner", planner_text)
        st.session_state.awaiting_decision = True
        st.session_state.status = "Waiting for your decision."
        st.session_state.stage = "idle"

    st.rerun()

# 2a) Searcher stage
if st.session_state.stage == "searching" and st.session_state.current_plan is not None:
    plan = st.session_state.current_plan
    sub_qs = plan["sub_questions"]

    with st.spinner("Searcher Agent: gathering information for all sub-questions..."):
        search_results = searcher_agent.search_multiple(sub_qs)

    if not search_results:
        add_history(
            "agent",
            "Searcher",
            "Search failed. Check Tavily API key or network.",
        )
        st.session_state.status = "Search failed"
        st.session_state.stage = "idle"
        st.rerun()

    st.session_state.current_search_results = search_results
    success_count = search_results["search_session"]["successful_searches"]
    add_history("agent", "Searcher", f"Found information for {success_count} sub-questions.")

    st.session_state.status = "Writing final report..."
    st.session_state.stage = "writing"
    st.rerun()

# 2b) Writer stage
if (
    st.session_state.stage == "writing"
    and st.session_state.current_plan is not None
    and st.session_state.current_search_results is not None
):
    plan = st.session_state.current_plan
    search_results = st.session_state.current_search_results

    with st.spinner("Writer Agent: synthesizing final report..."):
        report = writer_agent.synthesize_multiple(plan, search_results)

    if not report:
        add_history("agent", "Writer", "Failed to generate final report.")
        st.session_state.status = "Writer failed"
        st.session_state.stage = "idle"
        st.rerun()

    exec_summary = report.get("executive_summary", "")
    conclusion = report.get("conclusion", "")
    references = report.get("references", [])

    parts = []
    if exec_summary:
        parts.append("### Executive Summary\n\n" + exec_summary)
    if conclusion:
        parts.append("### Conclusion\n\n" + conclusion)
    if references:
        ref_lines = []
        for ref in references:
            num = ref.get("number", "")
            url = ref.get("url", "")
            ref_lines.append(f"{num}. {url}")
        parts.append("### References\n\n" + "\n".join(ref_lines))

    report_text = "\n\n".join(parts)
    add_history("agent", "Writer", report_text)

    st.session_state.status = "Done. You can start a new topic below."
    st.session_state.stage = "idle"
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
