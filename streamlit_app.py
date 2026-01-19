import streamlit as st
from research_graph import research_graph
from fpdf import FPDF
import uuid
import unicodedata

# =========================================================
# UNICODE SANITIZER (NO FONT DOWNLOAD)
# =========================================================
def sanitize_text(text: str) -> str:
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("latin-1", "ignore").decode("latin-1")

# =========================================================
# SESSION STATE INIT
# =========================================================
if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "last_query" not in st.session_state:
    st.session_state.last_query = None

if "show_success" not in st.session_state:
    st.session_state.show_success = False

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="OpenDeepResearcher",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# PREMIUM SAAS DARK UI
# =========================================================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
}
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
h1 {
    font-weight: 900;
    font-size: 3rem;
    background: linear-gradient(90deg, #7c7cff, #00eaff);
    -webkit-background-clip: text;
    color: transparent;
}
.stCaption, p, label {
    color: #cbd5f5 !important;
}
.card {
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 26px;
    border: 1px solid rgba(148, 163, 184, 0.15);
    box-shadow: 0 25px 40px rgba(0,0,0,0.4);
    margin-bottom: 24px;
}
textarea {
    border-radius: 16px !important;
    background-color: rgba(2, 6, 23, 0.9) !important;
    border: 1px solid #334155 !important;
    color: #e5e7eb !important;
}
button {
    border-radius: 14px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    background: linear-gradient(90deg, #6366f1, #06b6d4) !important;
    color: white !important;
    border: none !important;
}
button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 10px 25px rgba(99,102,241,0.45);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================
st.markdown("<h1>🧠 OpenDeepResearcher</h1>", unsafe_allow_html=True)
st.caption(
    "An agentic research platform that plans, reasons, and synthesizes knowledge using LLM agents."
)
st.markdown("---")

# =========================================================
# INPUT CARD
# =========================================================
# st.markdown('<div class="card">', unsafe_allow_html=True)

dynamic_placeholder = (
    f"What would you like to explore next about: {st.session_state.last_query}"
    if st.session_state.last_query
    else "e.g., Face Attendance System"
)

query = st.text_area(
    "🔍 Research Topic",
    placeholder=dynamic_placeholder,
    height=120,
    value=st.session_state.last_query or ""
)

col1, col2, spacer = st.columns([1.2, 1.2, 6])

with col1:
    if st.button("🚀 Run Research"):
        if not query.strip():
            st.warning("Please enter a research topic.")
            st.stop()

        with st.spinner("Planner → Reasoning → Synthesis in progress..."):
            result = research_graph.invoke({"user_query": query})

        st.session_state.research_result = result
        st.session_state.last_query = query
        st.session_state.show_success = True

with col2:
    if st.button("🧹 Clear Session"):
        st.session_state.clear()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FULL-WIDTH SUCCESS BAR
# =========================================================
if st.session_state.show_success:
    st.markdown("""
    <div style="
        width: 100%;
        padding: 10px 14px;
        margin: 16px 0 24px 0;
        border-left: 5px solid #22c55e;
        border-radius: 8px;
        background: rgba(34, 197, 94, 0.12);
        color: #dcfce7;
        font-size: 14px;
        font-weight: 500;
    ">
        ✔ Research completed successfully
    </div>
    """, unsafe_allow_html=True)


# Spacer between success bar and tabs
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# =========================================================
# RESULTS
# =========================================================
if st.session_state.research_result:
    result = st.session_state.research_result
    final_summary = result["final_summary"]

    tab1, tab2, tab3 = st.tabs(
        ["🧩 Research Plan", "📝 Final Summary", "📄 Export"]
    )

    with tab1:
        # st.markdown('<div class="card">', unsafe_allow_html=True)
        for sub in result["plan"]["sub_questions"]:
            st.markdown(f"• **{sub['question']}**")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        # st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(final_summary)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        # st.markdown('<div class="card">', unsafe_allow_html=True)

        def generate_full_pdf(title, final_summary):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Final Research Summary", ln=True)
            pdf.ln(6)

            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 8, sanitize_text(f"Title: {title}"))
            pdf.ln(4)

            for line in final_summary.split("\n"):
                clean = sanitize_text(line)
                if clean.strip():
                    pdf.multi_cell(0, 8, clean)
                    pdf.ln(1)

            name = "Final_Research_Summary.pdf"
            pdf.output(name)
            return name

        paragraphs = [p.strip() for p in final_summary.split("\n") if p.strip()]

        colA, colB = st.columns(2)

        with colA:
            if st.button("⬇️ Download Full Summary"):
                pdf = generate_full_pdf(query, final_summary)
                with open(pdf, "rb") as f:
                    st.download_button("📥 Download PDF", f, file_name=pdf)

        with colB:
            start = st.selectbox("Start paragraph", range(1, len(paragraphs) + 1))
            end = st.selectbox("End paragraph", range(start, len(paragraphs) + 1))

            if st.button("⬇️ Download Selected Range"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                for line in paragraphs[start - 1:end]:
                    pdf.multi_cell(0, 8, sanitize_text(line))
                    pdf.ln(1)

                name = f"Research_Excerpt_{uuid.uuid4().hex[:6]}.pdf"
                pdf.output(name)

                with open(name, "rb") as f:
                    st.download_button("📥 Download Excerpt", f, file_name=name)

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(
    "OpenDeepResearcher • Agentic AI • LangGraph • Production-grade Research Platform"
)
