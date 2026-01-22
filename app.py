import streamlit as st
import os
import time
import requests
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse
import re
from dotenv import load_dotenv

# Agent Imports
from agents.planner_agent import PlannerAgent
from agents.searcher_agent import SearcherAgent
from agents.writer_agent import WriterAgent

load_dotenv()

# ---------------- CONFIG ----------------
st.set_page_config(page_title="OpenDeepResearcher | Framework", layout="wide")

# ---------------- PROFESSIONAL MINIMAL STYLING ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF; 
        color: #202124;
    }

    .stApp {
        background-color: #FFFFFF;
    }

    /* Sidebar - Grey/Professional */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #E8EAED;
    }

    /* Input Box Minimal */
    .stTextInput input {
        background-color: #F1F3F4 !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        color: #202124 !important;
    }
    
    .stTextInput input:focus {
        border-color: #DADCE0 !important;
        background-color: #FFFFFF !important;
    }

    /* Primary Action Button */
    .stButton button {
        background-color: #bdf2ed !important; /* Google Blue */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 10px 24px !important;
        transition: opacity 0.2s;
    }
    
    .stButton button:hover {
        opacity: 0.9;
    }

    /* Research Cards */
    .research-card {
        background: #FFFFFF;
        border: 1px solid #E8EAED;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Typography */
    h1, h2, h3 { color: #202124; font-weight: 500; letter-spacing: -0.5px; }
    p { color: #5F6368; line-height: 1.6; }

    /* History Sidebar items */
    .history-text {
        padding: 8px 12px;
        font-size: 14px;
        color: #3C4043;
        border-radius: 4px;
        margin-bottom: 4px;
    }
    .history-text:hover {
        background-color: #E8EAED;
    }

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR (HISTORY) ----------------
if 'history' not in st.session_state:
    st.session_state.history = ["Architecture of Agentic Systems", "Large Language Model Optimization", "Neural Network Research"]

with st.sidebar:
    st.markdown("<p style='font-weight: 600; font-size: 14px; color: #70757a; margin-bottom: 15px;'>RECENT RESEARCH</p>", unsafe_allow_html=True)
    for item in st.session_state.history:
        st.markdown(f"<div class='history-text'>{item}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.caption("Version 2.0.4 | Stable")

# ---------------- MAIN INTERFACE ----------------
st.markdown("<h2 style='text-align: center; margin-top: 60px;'>Hello, how can I help you research today?</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 40px;'>Enter a topic and our agents will synthesize a deep report for you.</p>", unsafe_allow_html=True)

# Agent Init
planner = PlannerAgent()
searcher = SearcherAgent()
writer = WriterAgent()

# Input Layout
_, mid, _ = st.columns([1, 3, 1])
with mid:
    topic = st.text_input("", placeholder="Ask me anything", label_visibility="collapsed")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        run_btn = st.button("Generate Report", use_container_width=True)

if run_btn and topic:
    if topic not in st.session_state.history:
        st.session_state.history.insert(0, topic)

    # --- STAGE 1: PLANNING ---
    st.markdown("<div class='research-card'>", unsafe_allow_html=True)
    st.markdown("<p style='font-weight: 500; color: #202124;'>Planning Phase</p>", unsafe_allow_html=True)
    with st.status("Defining research parameters...", expanded=False):
        questions = planner.run(topic)
        for q in questions: st.write(f"Query: {q}")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- STAGE 2: SEARCHING ---
    st.markdown("<div class='research-card'>", unsafe_allow_html=True)
    st.markdown("<p style='font-weight: 500; color: #202124;'>Data Acquisition</p>", unsafe_allow_html=True)
    research_log = ""
    sources = []
    p_bar = st.progress(0)
    
    status_indicator = st.empty()
    for idx, q in enumerate(questions):
        status_indicator.text(f"Processing vector {idx+1} of {len(questions)}")
        data = searcher.run([q])
        research_log += data + "\n"
        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', data)
        for u in urls: sources.append(urlparse(u).netloc.replace("www.", ""))
        p_bar.progress((idx + 1) / len(questions))
    status_indicator.text("Intelligence gathering completed.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- STAGE 3: FINAL REPORT ---
    st.markdown("### Synthesis Report")
    with st.spinner("Compiling data..."):
        final_output = writer.run(topic, research_log)
        
        st.markdown("<div class='research-card' style='background-color: #FCFDFE;'>", unsafe_allow_html=True)
        st.markdown(final_output)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.download_button("Download Document", final_output, file_name=f"Research_Report.md")

else:
    # Landing Layout
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, chip_mid, _ = st.columns([1, 4, 1])
    with chip_mid:
        st.markdown("<p style='font-size: 13px; color: #70757a; text-align: center;'>Suggested Domains</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div style='text-align:center; font-size: 14px; color: #1A73E8;'>Autonomous Systems</div>", unsafe_allow_html=True)
        c2.markdown("<div style='text-align:center; font-size: 14px; color: #1A73E8;'>Renewable Energy</div>", unsafe_allow_html=True)
        c3.markdown("<div style='text-align:center; font-size: 14px; color: #1A73E8;'>Cybersecurity Trends</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.divider()
st.markdown("<p style='text-align: center; color: #9AA0A6; font-size: 12px;'>OpenDeepResearcher | Agentic LLM Framework Submission</p>", unsafe_allow_html=True)