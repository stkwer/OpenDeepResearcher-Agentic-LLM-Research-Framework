import streamlit as st
from src.core.langgraph_pipeline import build_graph

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📘",
    layout="centered"
)

st.title("📘 AI Research Assistant")
st.caption("Academic Research Paper Generator (Local Qwen LLM)")

# --------------------------------------------------
# Build graph once
# --------------------------------------------------
@st.cache_resource
def load_graph():
    return build_graph()

graph = load_graph()

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "paper" not in st.session_state:
    st.session_state.paper = ""

if "question" not in st.session_state:
    st.session_state.question = ""

# --------------------------------------------------
# Input
# --------------------------------------------------
question = st.chat_input("Ask a research question (academic topic)...")

if question:
    st.session_state.question = question

    with st.spinner("Generating research paper..."):
        state = {"input": question}
        result = graph.invoke(state)

        st.session_state.paper = result.get("final_answer", "")

# --------------------------------------------------
# DISPLAY QUESTION (THIS WAS MISSING)
# --------------------------------------------------
if st.session_state.question:
    st.markdown("### 🧠 Research Question")
    st.markdown(f"**{st.session_state.question}**")
    st.divider()

# --------------------------------------------------
# DISPLAY PAPER
# --------------------------------------------------
if st.session_state.paper:
    st.markdown(st.session_state.paper)

    st.divider()

    # --------------------------------------------------
    # Export buttons
    # --------------------------------------------------
    st.download_button(
        "📄 Export Markdown",
        data=st.session_state.paper,
        file_name="research_paper.md",
        mime="text/markdown"
    )



























