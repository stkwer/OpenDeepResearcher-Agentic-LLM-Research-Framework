import streamlit as st
from main import planner_agent, searcher_agent, writer_agent

st.set_page_config(
    page_title="Agentic RAG Research System",
    page_icon="🧠",
    layout="wide"
)

defaults = {
    "topic": "",
    "planner_questions": [],
    "writer_report": "",
    "planner_done": False,
    "writer_done": False,
    "writer_running": False,
    "current_view": "none",
    "theme": "dark"
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

if st.session_state.theme == "dark":
    BG = "#000000"
    SIDEBAR = "#050505"
    CARD = "#0b0b0b"
    TEXT = "#E5E7EB"
    BORDER = "#39FF14"
    BTN_BG = "#0b0b0b"
else:
    BG = "#efbf04"
    SIDEBAR = "#050505"
    CARD = "#ffffff"
    TEXT = "#111111"
    BORDER = "#efbf04"
    BTN_BG = "#ffffff"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap');

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

section[data-testid="stSidebar"] {{
    background-color: {SIDEBAR};
    border-right: 1px solid #d4a900;
}}

.block-container {{
    background-color: {BG};
}}

.title {{
    font-family: 'Poppins', sans-serif;
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(
        90deg,
        #39FF14,
        #FF1ACD,
        #FF69B4,
        #39FF14
    );
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleGlow 6s ease infinite;
}}

@keyframes titleGlow {{
    0% {{ background-position: 0%; }}
    50% {{ background-position: 100%; }}
    100% {{ background-position: 0%; }}
}}

.subtitle {{
    text-align: center;
    color: {"#1f2937" if st.session_state.theme == "light" else "#9ca3af"};
    margin-bottom: 30px;
}}

div[data-testid="stTextInput"] input {{
    background-color: {CARD} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 8px;
}}

div[data-testid="stTextInput"] input:focus {{
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(239,191,4,0.35);
}}

.card {{
    background-color: {CARD};
    border: 1px solid orange;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    color: {TEXT};
}}

/* ===== WRITER OUTPUT ===== */
.report-container {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 24px;
    color: {TEXT};
    line-height: 1.6;
}}

.research-title {{
    font-size: 22px;  font-weight: 600;
    margin-bottom: 20px;
    background: linear-gradient(
        90deg,
        #4facfe,   /* blue */
        #8f5cff,   /* violet */
        #ff6ec7    /* pink */
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Poppins', sans-serif;
}}


.stButton > button {{
    background-color: {BTN_BG};
    border: 1px solid {BORDER};
    color: {TEXT};
    transition: transform 0.15s ease;
    font-family: 'Poppins', sans-serif;

}}

.stButton > button:hover {{
    transform: scale(1.03);
    font-family: 'Poppins', sans-serif;

}}

</style>
""", unsafe_allow_html=True)

_, _, toggle_col = st.columns([6, 1, 1])
with toggle_col:
    if st.session_state.writer_running:
        st.markdown("⏳")   # visual lock while running
    else:
        if st.session_state.theme == "dark":
            if st.button("☀️"):
                st.session_state.theme = "light"
        else:
            if st.button("🌙"):
                st.session_state.theme = "dark"

# ================= HEADER =================
st.markdown("<div class='title'>Agentic RAG Research System</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Planner → Writer | Clean Research Workflow</div>",
    unsafe_allow_html=True
)
st.divider()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("<div class='research-title'>🔍 Research Topic</div>",unsafe_allow_html=True)

    topic = st.text_input(label="Research topic input",value=st.session_state.topic,placeholder="Enter your research topic here...",
    label_visibility="collapsed" )



    if st.button("▶ Run Planner Agent"):
        st.session_state.topic = topic
        st.session_state.planner_questions = planner_agent(topic)
        st.session_state.planner_done = True
        st.session_state.writer_done = False
        st.session_state.writer_running = False
        st.session_state.current_view = "planner"

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.session_state.writer_done:
        if st.button("👁 View Planner Agent"):
            st.session_state.current_view = "planner"
        if st.button("👁 View Writer Agent"):
            st.session_state.current_view = "writer"

# ================= MAIN CONTENT =================
with st.container():

    if st.session_state.current_view == "planner":
        st.subheader("🧩 Planner Agent – Research Questions")

        for q in st.session_state.planner_questions:
            st.markdown(f"<div class='card'>{q}</div>", unsafe_allow_html=True)

        if st.button("▶ Run Writer Agent"):
            st.session_state.writer_done = False
            st.session_state.writer_running = True

            data = searcher_agent(st.session_state.planner_questions)
            st.session_state.writer_report = writer_agent(
                st.session_state.topic,
                st.session_state.planner_questions,
                data
            )

            st.session_state.writer_running = False
            st.session_state.writer_done = True
            st.session_state.current_view = "writer"
            st.rerun()

    elif st.session_state.current_view == "writer":
        st.subheader("📄 Writer Agent – Final Report")

        st.markdown(
            f"<div class='report-container'>{st.session_state.writer_report}</div>",
            unsafe_allow_html=True
        )

        st.markdown("### 📤 Export Report")

        export_format = st.selectbox(
            "Choose format",
            ["TXT", "PDF", "WORD"],
            key="export_format"
        )

        report_text = st.session_state.writer_report

        if export_format == "TXT":
            st.download_button(
                label="⬇️ Download TXT",
                data=report_text,
                file_name="research_report.txt",
                mime="text/plain"
            )

        elif export_format == "PDF":
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            import io

            pdf_buffer = io.BytesIO()

            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )

            styles = getSampleStyleSheet()

            
            title_style = ParagraphStyle(
                "TitleStyle",
                parent=styles["Title"],
                fontSize=20,
                spaceAfter=20
            )

            heading_style = ParagraphStyle(
                "HeadingStyle",
                parent=styles["Heading2"],
                fontSize=14,
                spaceBefore=16,
                spaceAfter=8
            )

            body_style = ParagraphStyle(
                "BodyStyle",
                parent=styles["Normal"],
                fontSize=11,
                leading=16,     
                spaceAfter=8
            )

            story = []

            lines = report_text.split("\n")

            for line in lines:
                line = line.strip()

                if not line:
                    story.append(Spacer(1, 12))
                    continue

                if line.startswith("# "):
                    story.append(Paragraph(line[2:], title_style))

            
                elif line.startswith("## "):
                    story.append(Spacer(1, 12))
                    story.append(Paragraph(line[3:], heading_style))

            
                elif line.startswith("### "):
                    story.append(Spacer(1, 10))
                    story.append(Paragraph(f"<b>{line[4:]}</b>", body_style))

            
                elif line.startswith("- "):
                    story.append(Paragraph(f"• {line[2:]}", body_style))

                else:
                    story.append(Paragraph(line, body_style))

            doc.build(story)
            pdf_buffer.seek(0)

            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_buffer,
                file_name="research_report.pdf",
                mime="application/pdf"
            )

        elif export_format == "WORD":
            from docx import Document
            import io

            doc = Document()
            for line in report_text.split("\n"):
                doc.add_paragraph(line)

            doc_buffer = io.BytesIO()
            doc.save(doc_buffer)
            doc_buffer.seek(0)

            st.download_button(
                label="⬇️ Download Word",
                data=doc_buffer,
                file_name="research_report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )


    else:
        st.info("Enter a topic and run the Planner Agent to begin.")
