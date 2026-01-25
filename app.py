import streamlit as st
from graph.research_graph import run_research
from utils import sanitize_filename

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="OpenDeepResearcher",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Session State ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("🔍 Search History")

    if not st.session_state.history:
        st.info("No research yet")
    else:
        for idx, item in enumerate(st.session_state.history):
            topic = item["topic"][:40] + "..." if len(item["topic"]) > 40 else item["topic"]
            if st.button(topic, key=f"h_{idx}", use_container_width=True):
                st.session_state.selected_index = idx
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ✅ Clear All ONLY when history exists
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.history.clear()
            st.session_state.selected_index = None
            st.rerun()

# ---------------- CSS (UNCHANGED) ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #e8f4fd;
}
[data-testid="stHeader"] {
    background: transparent;
}
.main {
    background: transparent;
}
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(44, 90, 160, 0.2);
    box-shadow: 0 8px 32px rgba(44, 90, 160, 0.1);
}
[data-testid="stSidebar"] h1 {
    color: #2c5aa0 !important;
    font-weight: 800;
    text-align: center;
    padding: 1.5rem 0;
    text-shadow: 0 2px 4px rgba(44, 90, 160, 0.2);
}
.main-header {
    text-align: center;
    padding: 3rem 4rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(25px);
    border: 2px solid rgba(44, 90, 160, 0.2);
    border-radius: 30px;
    margin-bottom: 4rem;
    box-shadow: 0 20px 60px rgba(44, 90, 160, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.8);
    position: relative;
    overflow: hidden;
    transform: translateY(0);
    transition: all 0.3s ease;
}
.main-header:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 80px rgba(44, 90, 160, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.9);
}
.main-header h1 {
    color: #2c5aa0;
    font-size: 3.5rem;
    font-weight: 900;
    text-shadow: 0 4px 12px rgba(44, 90, 160, 0.3);
    position: relative;
    z-index: 1;
    background: linear-gradient(135deg, #2c5aa0, #1e3a8a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.main-header p {
    color: #2c5aa0 !important;
    font-size: 1.3rem;
    font-weight: 500;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 4px rgba(44, 90, 160, 0.2);
}
.stSpinner > div > div {
    color: #2c5aa0 !important;
}
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #2c5aa0 0%, #1e3a8a 100%) !important;
    color: white !important;
    border-radius: 20px !important;
    border: none !important;
    box-shadow: 0 8px 25px rgba(44, 90, 160, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    font-weight: 700;
    font-size: 1.1rem;
    padding: 0.8rem 2rem !important;
}
.stButton button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 40px rgba(44, 90, 160, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3);
    background: linear-gradient(135deg, #1e3a8a 0%, #2c5aa0 100%) !important;
}
.stTextArea textarea {
    background: white !important;
    border: 2px solid rgba(44, 90, 160, 0.2) !important;
    border-radius: 15px !important;
    color: #2c5aa0 !important;
    font-size: 1.1rem !important;
}
.stTextArea textarea:focus {
    outline: none !important;
    border: 2px solid rgba(44, 90, 160, 0.4) !important;
    box-shadow: 0 0 0 0px transparent !important;
}
.stTextArea > div {
    border: none !important;
}
.stTextArea > div > div {
    border: none !important;
}
.stTextArea {
    border: none !important;
}
.stTextArea div[data-baseweb="base-input"] {
    border: none !important;
    outline: none !important;
}
.stTextArea div[data-baseweb="base-input"]:focus-within {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}
.stTabs [data-baseweb="tab"] {
    flex: 1;
    background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(232, 244, 253, 0.6) 100%);
    border-radius: 15px 15px 0 0;
    padding: 20px 0;
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c5aa0;
    border: 1px solid rgba(44, 90, 160, 0.2);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}
.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(232, 244, 253, 0.8) 100%);
    transform: translateY(-2px);
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #2c5aa0 0%, #1e3a8a 100%);
    color: white;
    font-weight: 700;
    box-shadow: 0 5px 15px rgba(44, 90, 160, 0.3);
}
.question-box {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(232, 244, 253, 0.8) 100%);
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 15px;
    border-left: 5px solid #2c5aa0;
    box-shadow: 0 5px 20px rgba(44, 90, 160, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(44, 90, 160, 0.1);
    transition: all 0.3s ease;
}
.question-box:hover {
    transform: translateX(10px);
    box-shadow: 0 8px 30px rgba(44, 90, 160, 0.2);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(232, 244, 253, 0.9) 100%);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("""
<div class="main-header">
    <h1>🧠 OpenDeepResearcher</h1>
    <p>AI-Powered Multi-Agent Research Assistant</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Input ----------------
col1, col2, col3 = st.columns([0.5, 4, 0.5])
with col2:
    query = st.text_area(
        "",
        placeholder="Enter your research topic...",
        height=70,
        label_visibility="collapsed"
    )

col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    run_button = st.button("🚀 Research", use_container_width=True, type="primary")

# ---------------- Run Research ----------------
if run_button and query.strip():
    with st.spinner("🔄 Generating comprehensive research analysis..."):
        result = run_research(query)
        st.session_state.history.insert(0, result)
        st.session_state.selected_index = 0
        st.rerun()

# ---------------- Results ----------------
if st.session_state.selected_index is not None:
    item = st.session_state.history[st.session_state.selected_index]

    # Topic with enhanced styling
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(232, 244, 253, 0.8) 100%);
            padding: 1.5rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(44, 90, 160, 0.15);
            border: 1px solid rgba(44, 90, 160, 0.2);
            backdrop-filter: blur(15px);
        ">
            <h2 style="color:#2c5aa0; font-weight:800; margin:0; font-size:1.8rem; text-shadow: 0 2px 4px rgba(44, 90, 160, 0.2);">
                📌 Topic: {item['topic']}
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    tab1, tab2 = st.tabs(["📝 Research Report", "🧠 Research Questions"])

    with tab1:
        st.markdown(
            f"""
            <div style="
                color:#2c5aa0; 
                line-height:1.8; 
                font-size:16px;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(232, 244, 253, 0.6) 100%);
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(44, 90, 160, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(44, 90, 160, 0.1);
            ">
                {item["final_report"].replace("\\n", "<br>")}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            "💾 Download Report",
            data=item["final_report"],
            file_name=f"{sanitize_filename(item['topic'])}_report.txt",
            use_container_width=True
        )

    with tab2:
        st.markdown("#### 🎯 Generated Research Questions")
        for i, q in enumerate(item.get("sub_questions", []), 1):
            st.markdown(
                f"""
                <div class="question-box">
                    <strong>🔹 Question {i}:</strong> {q}
                </div>
                """,
                unsafe_allow_html=True
            )