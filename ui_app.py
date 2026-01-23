import streamlit as st
import uuid
import random
from fpdf import FPDF
from planner_agent import plan
from search_agent import get_evidence
from writer_agent import write_final_summary
from main import extract_sub_questions, deduplicate_evidence


# --------------------------------------------------
# PDF GENERATION LOGIC
# --------------------------------------------------
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Deep Researcher",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = []
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "plan_ready" not in st.session_state:
    st.session_state.plan_ready = False
if "researching" not in st.session_state:
    st.session_state.researching = False


# --------------------------------------------------
# CSS (PRESERVING STYLE + CURSOR FIX)
# --------------------------------------------------
st.markdown("""
<style>
[data-testid="stHeader"] { background-color: #020617 !important; }
#MainMenu, footer {visibility: hidden;}
.stApp { background: linear-gradient(135deg, #020617, #020617); color: white; }
[data-testid="stSidebar"] { background: #0f172a; padding: 12px; }


textarea {
    background: #ffffff !important;
    color: #000000 !important;    
    border-radius: 14px !important;
    caret-color: black !important;
}


div[data-testid="stSidebar"] .stButton > button {
    text-align: left;
    background: linear-gradient(90deg, #38bdf8, #a855f7) !important;
    border: none !important;
    color: white !important;
    border-radius: 10px !important;
    margin-bottom: 5px;
}


div[data-testid="stSidebar"] [data-testid="stPopover"] > button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #64748b !important;
    opacity: 0;
    transition: opacity 0.2s ease-in-out;
    padding: 0px !important;
    margin-top: 8px !important;
}


div[data-testid="stSidebar"] [data-testid="element-container"]:hover [data-testid="stPopover"] > button {
    opacity: 1;
}


.top-title {
    font-size: 34px; font-weight: 700; margin: -10px 0 20px 0;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center;
}


.main-box {
    max-width: 1000px; margin: 0 auto; padding: 20px 30px;
    background: rgba(255,255,255,0.06); border-radius: 20px; backdrop-filter: blur(14px);
}


.agent-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
    padding: 20px; border-radius: 15px; margin-bottom: 25px;
}


.agent-header {
    font-size: 1.2rem; font-weight: 600; margin-bottom: 15px; color: #38bdf8;
}


div.stButton > button:not([key*="sidebar"]):not([key*="menu"]),
div.stDownloadButton > button {
    background: linear-gradient(90deg, #38bdf8, #a855f7) !important;
    border-radius: 12px !important; border: none !important; color: white !important;
}


div.stButton > button:hover,
div.stDownloadButton > button:hover {
    color: white !important; opacity: 0.9 !important;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR LOGIC
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🧠 Research History")
    if st.button("＋ New Chat", key="new_chat_top", use_container_width=True):
        st.session_state.active_chat_id = None
        st.session_state.current_plan = None
        st.session_state.plan_ready = False
        st.session_state.researching = False
        if "new_research_input" in st.session_state:
            del st.session_state["new_research_input"]
        st.rerun()
    st.markdown("---")
   
    for idx, chat in enumerate(st.session_state.chats):
        with st.container():
            col1, col2 = st.columns([0.85, 0.15])
            display_title = f"📌 {chat['title']}" if chat.get("pinned") else chat['title']
            with col1:
                if st.button(display_title, key=f"sidebar_btn_{chat['id']}", use_container_width=True):
                    st.session_state.active_chat_id = chat['id']
                    st.rerun()
            with col2:
                with st.popover("⋮"):
                    new_title = st.text_input("Rename", value=chat['title'], key=f"ren_{chat['id']}")
                    if new_title != chat['title']:
                        st.session_state.chats[idx]['title'] = new_title
                        st.rerun()
                    if st.button("📍 Pin/Unpin", key=f"pin_{chat['id']}", use_container_width=True):
                        st.session_state.chats[idx]['pinned'] = not chat.get("pinned", False)
                        st.session_state.chats.sort(key=lambda x: x.get("pinned", False), reverse=True)
                        st.rerun()
                    st.divider()
                    if st.button("🗑️ Delete", key=f"del_{chat['id']}", use_container_width=True):
                        st.session_state.chats = [c for c in st.session_state.chats if c['id'] != chat['id']]
                        st.rerun()


# --------------------------------------------------
# MAIN UI
# --------------------------------------------------
active_chat = next((c for c in st.session_state.chats if c['id'] == st.session_state.active_chat_id), None)


if active_chat:
    st.markdown(f'<div class="top-title">{active_chat["title"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
   
    hcol1, hcol2 = st.columns([0.7, 0.3])
    with hcol1:
        if st.button("← New Research"):
            st.session_state.active_chat_id = None
            st.rerun()
    with hcol2:
        pdf_output = create_pdf(active_chat["answer"])
        st.download_button(label="📥 Export Report (PDF)", data=pdf_output,
                           file_name=f"{active_chat['title'].replace(' ', '_')}.pdf",
                           mime="application/pdf", use_container_width=True)


    st.markdown(f'<div class="agent-card" style="border: 1px solid #38bdf8;"><div class="agent-header">✍️ Writer Agent - Research Report</div>{active_chat["answer"]}</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown(f'<div class="agent-card"><div class="agent-header">🧠 Planner Agent</div></div>', unsafe_allow_html=True)
    for i, sq in enumerate(active_chat["sub_questions"], 1):
        st.markdown(f"**{i}.** {sq}")
    st.divider()


    with st.expander("🔍 Show Search Evidence & Sources"):
        for ev in active_chat["evidence"]:
            st.markdown(f'''
                <div style="background: rgba(255,255,255,0.02); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 3px solid #a855f7;">
                    <p style="margin-bottom: 10px;">{ev["content"]}</p>
                    <a href="{ev["url"]}" target="_blank" style="color: #38bdf8; text-decoration: none; font-size: 0.9rem;">🔗 Source: {ev["url"]}</a>
                </div>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


else:
    st.markdown('<div class="top-title">Multi-Agent Deep Researcher</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
   
    user_query = st.text_area("Query", label_visibility="collapsed", placeholder="Ask a deep research question...", height=120, key="new_research_input")
   
    btn_col1, btn_col2 = st.columns([0.7, 0.3])
    with btn_col1:
        run_research = st.button("🚀 Run Research", use_container_width=True)
    with btn_col2:
        if st.session_state.chats:
            latest_pdf = create_pdf(st.session_state.chats[0]["answer"])
            st.download_button("📥 Export Latest", data=latest_pdf, file_name="Latest_Report.pdf", use_container_width=True)
        else:
            st.button("📥 Export", disabled=True, use_container_width=True)


    if run_research and user_query.strip():
        with st.status("🧠 Planner Agent Drafting Research Plan..."):
            plan_raw = plan(user_query.strip())
            st.session_state.current_plan = extract_sub_questions(plan_raw)
            st.session_state.plan_ready = True
            st.session_state.researching = False


    if st.session_state.plan_ready and st.session_state.current_plan:
        st.markdown('<div class="agent-card"><div class="agent-header">🧠 Proposed Research Plan</div>', unsafe_allow_html=True)
        for i, sq in enumerate(st.session_state.current_plan, 1):
            st.markdown(f"**{i}.** {sq}")
        st.markdown('</div>', unsafe_allow_html=True)


        # FIXED ACTION AREA TO PREVENT DUPLICATION
        action_placeholder = st.empty()
       
        if not st.session_state.researching:
            with action_placeholder.container():
                icol1, icol2 = st.columns(2)
                with icol1:
                    if st.button("✅ Proceed to Report", use_container_width=True):
                        st.session_state.researching = True
                        st.rerun()
                with icol2:
                    if st.button("🔄 Regenerate Plan", use_container_width=True):
                        # Use the placeholder to show status immediately, replacing the buttons
                        with action_placeholder.container():
                            with st.status("♻️ Generating a NEW set of questions..."):
                                diverse_query = f"Regenerate a different research plan for: {user_query.strip()}. Ensure the sub-questions are unique and cover different aspects than these: {st.session_state.current_plan[:3]}"
                                plan_raw = plan(diverse_query)
                                st.session_state.current_plan = extract_sub_questions(plan_raw)
                        st.rerun()


        if st.session_state.researching:
            with action_placeholder.container():
                with st.status("🔬 Deep Research & Writing in progress..."):
                    found_evidence = []
                    for sq in st.session_state.current_plan:
                        res = get_evidence(sq)
                        if res.get("url"): found_evidence.append(res)
                    final_evidence = deduplicate_evidence(found_evidence)
                   
                    report_prompt = (
                        f"Generate a formal research report (strictly 450-500 words) for: {user_query}. "
                        "The report MUST include exactly these sections: Title, Abstract, Keywords, "
                        "Introduction, Related Work, Methodology, Experiments & Results, Discussion, "
                        "Conclusion & Future Work, and References."
                    )
                    summary = write_final_summary(report_prompt, final_evidence)


                new_id = str(uuid.uuid4())
                new_chat = {
                    "id": new_id,
                    "title": user_query.strip()[:45] + "..." if len(user_query.strip()) > 45 else user_query.strip(),
                    "pinned": False,
                    "sub_questions": st.session_state.current_plan,
                    "evidence": final_evidence,
                    "answer": summary
                }
                st.session_state.chats.insert(0, new_chat)
                st.session_state.active_chat_id = new_id
                st.session_state.current_plan = None
                st.session_state.plan_ready = False
                st.session_state.researching = False
                st.rerun()


    st.markdown('</div>', unsafe_allow_html=True)

