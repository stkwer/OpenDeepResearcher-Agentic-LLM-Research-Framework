import streamlit as st
from ollama_test import run_research
import time


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Open Deep Researcher",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- CSS ----------------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }
    
    /* Title styling - REMOVED WHITE LINE */
    .title-container {
        text-align: center;
        padding: 15px 0 5px 0;
        margin-bottom: 10px;
    }
    
    .main-title {
        font-size: 95px;  /* Increased from 90px */
        font-weight: 900;
        background: linear-gradient(45deg, #FF6B6B, #FFD93D, #6BCF7F);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        margin-bottom: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.2);
        letter-spacing: 1px;
    }

    .subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 18px;  /* Increased from 16px */
        margin-top: 4px;
    }
    
    /* Search container */
    .search-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px 30px;
        border-radius: 25px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        margin: 10px auto 20px auto;
        width: 80%;
        position: relative;
        z-index: 100;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    .helper-text {
        font-size: 15px;  /* Increased from 13px */
        color: #7f8c8d;
        margin-top: 6px;
    }
    
    .report-container {
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        margin: 25px 0;
        border-left: 6px solid #6BCF7F;
        animation: fadeIn 0.6s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .report-content {
        color: #ffffff !important;
        font-size: 28px;  /* Increased from 16px */
        line-height: 1.7;
        background: transparent !important;
    }
    
    .topic-tag {
        display: inline-block;
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 10px 25px;
        border-radius: 30px;
        font-weight: 700;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(106, 17, 203, 0.3);
        font-size: 28px;  /* Increased from 16px */
    }
    
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.85);
        font-size: 26px;  /* Increased from 14px */
        margin-top: 50px;
        padding: 25px;
        border-top: 1px solid rgba(255,255,255,0.15);
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px 15px 0 0;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e, #16213e) !important;
    }
    
    .sidebar .sidebar-content {
        background: transparent !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        padding: 18px 45px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 29px;  /* Increased from 17px */
        transition: all 0.3s ease;
        width: 100%;
        height: 75px;
        margin-top: 0 !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(255, 107, 107, 0.4);
        background: linear-gradient(45deg, #FF8E53, #FF6B6B);
    }
    
    /* Download button - TRANSPARENT BACKGROUND */
    .stDownloadButton > button {
        background: transparent !important;
        color: #6BCF7F !important;
        border: 2px solid #6BCF7F !important;
        padding: 10px 24px !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        font-size: 28px !important;  /* Increased from 16px */
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
        box-shadow: none !important;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(107, 207, 127, 0.1) !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(107, 207, 127, 0.3) !important;
    }
    
    /* THICKER INPUT BOX - MATCHING BUTTON HEIGHT */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 20px 30px;
        font-size: 29px;  /* Increased from 17px */
        transition: all 0.3s;
        height: 75px;  /* This matches the button height */
        min-height: 75px;
        margin-top: 0 !important;
        background: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6BCF7F;
        box-shadow: 0 0 0 4px rgba(107, 207, 127, 0.2);
        outline: none;
    }
    .stTextInput input {
        display: flex;
        align-items: center;
   }
  
    .stTextInput > div {
        height: 75px !important;
    }

    .stTextInput > div > div {
        height: 75px !important;
    }

    .stTextInput input {
        height: 75px !important;
        line-height: 75px !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        box-sizing: border-box !important;
    }

    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(25px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .history-item {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        color: #ffffff !important;
        padding: 15px 20px;
        margin: 12px 0;
        border-radius: 15px;
        border-left: 5px solid #6BCF7F;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 27px;  /* Increased from 15px */
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .history-item:hover {
        transform: translateX(8px);
        background: linear-gradient(135deg, rgba(107, 207, 127, 0.2), rgba(255, 255, 255, 0.1));
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        border-left: 5px solid #FFD93D;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6a11cb, #2575fc, #6BCF7F);
        border-radius: 10px;
    }
    
    .status-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 18px;
        border-radius: 12px;
        margin: 12px 0;
        text-align: center;
        font-weight: 600;
        color: #2c3e50;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #eaeaea;
        font-size: 18px;  /* Added font size */
    }
    
    .clear-history-btn > button {
        background: linear-gradient(45deg, #ff4757, #ff3838) !important;
        margin-top: 15px;
        box-shadow: 0 6px 20px rgba(255, 71, 87, 0.3);
    }
    
    .count-badge {
        display: inline-block;
        background: linear-gradient(45deg, #FFD93D, #FF9F1C);
        color: #2c3e50;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 17px;  /* Increased from 15px */
        font-weight: 700;
        margin-left: 12px;
        box-shadow: 0 4px 15px rgba(255, 217, 61, 0.3);
    }

    .insights-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 15px;
    }
    .insight-pill {
        background: rgba(0,0,0,0.4);
        color: #ecf0f1;
        border-radius: 999px;
        padding: 6px 14px;
        font-size: 15px;  /* Increased from 13px */
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    .welcome-message {
        background: rgba(255, 255, 255, 0.95);
        padding: 50px 40px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border: 2px dashed #6BCF7F;
        margin: 30px 0;
    }
    
    .stHorizontalBlock {
        align-items: center !important;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        padding: 25px 20px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        font-size: 18px;  /* Added font size */
    }
    
    .sidebar-header h2 {
        font-size: 24px;  /* Added font size */
    }
    
    .sidebar-header p {
        font-size: 15px;  /* Added font size */
    }
    
    .stButton button[kind="secondary"] {
        background: linear-gradient(45deg, #6BCF7F, #4CAF50) !important;
        color: white !important;
        border: none !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
        min-width: 45px !important;
        height: 38px !important;
        margin: 12px 0 0 0 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        font-size: 18px !important;  /* Increased font size */
    }
    
    .stButton button[kind="secondary"]:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 5px 15px rgba(107, 207, 127, 0.4) !important;
    }
    
    hr, .stHorizontalBlock > div > div {
        border: none !important;
    }
    
    .report-container * {
        color: #ffffff !important;
    }
    
    .stMarkdown, .element-container, .st-emotion-cache {
        color: #ffffff !important;
    }
    
    .topic-tag {
        color: #ffffff !important;
    }
    
    .clickable-history {
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .clickable-history:hover {
        background: rgba(107, 207, 127, 0.2) !important;
    }

    .planner-title {
        font-size: 18px;  /* Increased from 16px */
        font-weight: 700;
        margin-bottom: 8px;
        color: #f1c40f;
    }
    
    /* Larger placeholder text */
    input::placeholder {
        font-size: 29px;  /* Increased placeholder font size */
        color: #95a5a6 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 18px !important;  /* Increased tab font size */
        font-weight: 600 !important;
        padding: 12px 20px !important;
    }
            /* PLANNER AGENT OUTPUT FONT SIZE */
[data-testid="stExpander"] ul,
[data-testid="stExpander"] li,
[data-testid="stExpander"] p,
[data-testid="stExpander"] span {
    font-size: 20px !important;
    line-height: 1.6 !important;
}
/* WRITER AGENT (FINAL REPORT) FONT SIZE */
.report-content,
.report-content p,
.report-content li,
.report-content span {
    font-size: 30px !important;
    line-height: 1.6 !important;
}


</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "reports" not in st.session_state:
    st.session_state.reports = []

if "search_key" not in st.session_state:
    st.session_state.search_key = 0

if "jump_to_topic" not in st.session_state:
    st.session_state.jump_to_topic = None

if "show_all_reports" not in st.session_state:
    st.session_state.show_all_reports = True

if "planner_data" not in st.session_state:
    st.session_state.planner_data = {}


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2 style='color: white; margin: 0;'>📚 Search History</h2>
        <p style='color: rgba(255,255,255,0.75); font-size: 15px; margin-top: 6px;'>
            Click any topic to reopen its full research view.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.history:
        for i, topic in enumerate(reversed(st.session_state.history[-10:])):
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(
                        f"{topic[:40]}{'...' if len(topic) > 40 else ''}",
                        key=f"history_{i}_{hash(topic)}",
                        help=f"Click to view report for: {topic}",
                        use_container_width=True
                    ):
                        st.session_state.jump_to_topic = topic
                        st.session_state.show_all_reports = False
                        st.rerun()
                with col2:
                    if st.button(
                        "🔍", key=f"view_{i}_{hash(topic)}",
                        help=f"View report: {topic}", type="secondary"
                    ):
                        st.session_state.jump_to_topic = topic
                        st.session_state.show_all_reports = False
                        st.rerun()
        
        if st.button("📄 Show All Reports", use_container_width=True, type="primary"):
            st.session_state.show_all_reports = True
            st.session_state.jump_to_topic = None
            st.rerun()
        
        st.markdown('<div class="clear-history-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Clear All History", use_container_width=True, type="secondary"):
            st.session_state.history = []
            st.session_state.reports = []
            st.session_state.planner_data = {}
            st.session_state.jump_to_topic = None
            st.session_state.show_all_reports = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px; color: rgba(255,255,255,0.8);'>
            <div style='font-size: 40px; margin-bottom: 15px;'>✨</div>
            <p style='font-size: 17px;'>No searches yet</p>
        </div>
        """, unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.markdown("""
<div class="title-container">
    <div class="main-title">Deep Research AI</div>
    <div class="subtitle">Planner • Searcher • Writer — multi‑agent research pipeline</div>
</div>
""", unsafe_allow_html=True)


# ---------------- SEARCH CONTAINER ----------------
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2 = st.columns([6, 2])

with col1:
    # The input box is now thicker and matches the button height (58px)
    topic = st.text_input(
        " ",
        placeholder="🔍 Enter your research topic here...",
        label_visibility="collapsed",
        key=f"search_input_{st.session_state.search_key}"
    )
    st.markdown(
        "<div class='helper-text'>Tip: Try questions like "
        "<b>\"Impact of LLMs in education\"</b> or "
        "<b>\"Applications of LiDAR in self‑driving\"</b>.</div>",
        unsafe_allow_html=True
    )

with col2:
    # This button is 58px tall - input box now matches this height
    search_clicked = st.button("🚀 Start Research", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ---------------- PROGRESS/STATUS SECTION ----------------
progress_container = st.container()


# ---------------- SEARCH ACTION ----------------
if search_clicked and topic.strip():
    if topic not in st.session_state.history:
        st.session_state.history.append(topic)
    
    st.session_state.search_key += 1
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.markdown(
                '<div class="status-box">📝 Planning research questions...</div>',
                unsafe_allow_html=True
            )
            progress_bar.progress(20)
            time.sleep(0.3)
            
            status_text.markdown(
                '<div class="status-box">🔍 Searching for information...</div>',
                unsafe_allow_html=True
            )
            progress_bar.progress(50)

            # run_research now returns report + planner_questions
            result = run_research(topic)

            status_text.markdown(
                '<div class="status-box">✍️ Writing comprehensive report...</div>',
                unsafe_allow_html=True
            )
            progress_bar.progress(80)
            time.sleep(0.5)

            st.session_state.reports.append({
                "topic": topic,
                "content": result.get("report", "")
            })

            # store planner questions for this topic
            st.session_state.planner_data[topic] = result.get("planner_questions", [])

            progress_bar.progress(100)
            status_text.markdown(
                '<div class="status-box">✅ Research complete! Report added below.</div>',
                unsafe_allow_html=True
            )
            time.sleep(1.2)

            progress_bar.empty()
            status_text.empty()

            st.session_state.jump_to_topic = topic
            st.session_state.show_all_reports = False
        
        except Exception as e:
            st.error(f"❌ Research failed: {str(e)}")
            st.info("Please check your API keys and internet connection.")
            progress_bar.empty()
            status_text.empty()
        
        st.rerun()


# ---------------- DISPLAY REPORTS ----------------
def render_single_report_block(report_obj, total_count=None, single_view=False):
    topic = report_obj["topic"]
    content = report_obj["content"]
    planner_qs = st.session_state.planner_data.get(topic, [])

    st.markdown("<div class='report-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='topic-tag'>📌 {topic}</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Planner Questions", "📄 Final Report", "⬇️ Export"])
    
    with tab1:
        if planner_qs:
            with st.expander("View planner agent question set", expanded=True):
                st.markdown(
                    "<div class='planner-title'>Planner Agent Questions</div>",
                    unsafe_allow_html=True
                )
                for idx, q in enumerate(planner_qs, start=1):
                    st.markdown(f"- **Q{idx}**: {q}")
        else:
            st.info("No planner questions were returned for this topic. Make sure your backend run_research returns a 'planner_questions' list.")

    with tab2:
        st.markdown("<div class='report-content'>", unsafe_allow_html=True)
        st.markdown(content)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        text_to_download = f"Topic: {topic}\n\n--- Planner Questions ---\n"
        if planner_qs:
            for idx, q in enumerate(planner_qs, start=1):
                text_to_download += f"{idx}. {q}\n"
        else:
            text_to_download += "No planner questions available.\n"

        text_to_download += "\n--- Final Report ---\n"
        text_to_download += content

        st.download_button(
            label="💾 Download as TXT",
            data=text_to_download,
            file_name=f"deep_research_{topic.replace(' ', '_')}.txt",
            mime="text/plain"
        )

    st.markdown("</div>", unsafe_allow_html=True)


if st.session_state.reports:
    if st.session_state.show_all_reports:
        st.markdown(f"""
        <div style='text-align: center; margin: 20px 0 20px 0;'>
            <span style='color: white; font-size: 20px; font-weight: 600;'>
                📊 All Research Reports ({len(st.session_state.reports)})
                <span class="count-badge">Viewing All</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

        for report in reversed(st.session_state.reports):
            render_single_report_block(report)
    
    elif st.session_state.jump_to_topic:
        found_report = None
        for report in st.session_state.reports:
            if report['topic'] == st.session_state.jump_to_topic:
                found_report = report
                break
        
        if found_report:
            st.markdown(f"""
            <div style='text-align: center; margin: 20px 0 20px 0;'>
                <span style='color: white; font-size: 20px; font-weight: 600;'>
                    🎯 Viewing Specific Report
                    <span class="count-badge">1 of {len(st.session_state.reports)}</span>
                </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                "<div class='report-container' style='border: 3px solid #FFD93D; box-shadow: 0 0 20px rgba(255, 217, 61, 0.3);'>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

            render_single_report_block(found_report, total_count=len(st.session_state.reports), single_view=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📄 Back to All Reports", use_container_width=True, type="primary"):
                    st.session_state.show_all_reports = True
                    st.session_state.jump_to_topic = None
                    st.rerun()
        else:
            st.warning(f"Report for topic '{st.session_state.jump_to_topic}' not found.")
            st.session_state.show_all_reports = True
            st.session_state.jump_to_topic = None
else:
    st.markdown("""
    <div class="welcome-message">
        <div style='font-size: 60px; margin-bottom: 20px;'>🔍</div>
        <h2 style='color: #2c3e50; margin-bottom: 15px; font-size: 28px;'>Welcome to Deep Research AI</h2>
        <p style='color: #5d6d7e; font-size: 19px; line-height: 1.6;'>
            Enter a research topic above to generate comprehensive AI-powered reports.<br>
            Planner, searcher, and writer agents collaborate to give you deep insights.
        </p>
        <div style='margin-top: 25px; color: #6BCF7F; font-weight: 600; font-size: 18px;'>
            ⚡ Fast Processing • 🧠 Multi-Agent Planning • 🎯 Actionable Results
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <div style='display: flex; justify-content: center; gap: 30px; margin-bottom: 15px; flex-wrap: wrap; font-size: 18px;'>
        <div style='color: #FFD93D;'>⚡ Parallel Processing</div>
        <div style='color: #6BCF7F;'>🧠 Deep Analysis</div>
        <div style='color: #2575fc;'>📚 Persistent Storage</div>
        <div style='color: #e67e22;'>🤖 Planner Agent View</div>
    </div>
    <div style='font-size: 18px; font-weight: 600; margin-bottom: 8px; color: #FFD93D;'>
        🚀 AI-Powered Research Assistant
    </div>
    <div style='font-size: 15px; opacity: 0.8;'>
        Developed by Bhumika Shinde • All research reports are preserved
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)