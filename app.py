import io
from datetime import datetime
from typing import Any, Dict, List, Optional
import streamlit as st
from planner_agent import PlannerAgent
from searcher_agent import SearcherAgent
from writer_agent import WriterAgent
def _render_css() -> None:
    st.markdown(
"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=swap');
:root {
  /* Premium white + warm brown theme */
  --bg-primary: #FFFFFF;
  --bg-secondary: #FFFAF5;
  --bg-cream: #FFF8F0;
  --bg-ivory: #FFFEF7;
  --bg-warm: #FFF5E6;
  --bg-card: #FFFFFF;
  --bg-input: #FFFAF5;
  --border-light: #F5E6D3;
  --border-soft: #E8D4BC;
  --border-medium: #D4B596;
  --text-primary: #3A2A1A;
  --text-secondary: #6B5D4D;
  --text-muted: #9A8B7B;
  --accent-brown: #8B5A3C;
  --accent-caramel: #A67C52;
  --accent-mocha: #6F4E37;
  --accent-tan: #C19A6B;
  --accent-gold: #D4AF37;
  --accent-gradient: linear-gradient(135deg, #8B5A3C 0%, #A67C52 50%, #C19A6B 100%);
  --shadow-soft: 0 4px 20px rgba(139, 90, 60, 0.08);
  --shadow-medium: 0 8px 40px rgba(139, 90, 60, 0.12);
  --shadow-elevated: 0 20px 60px rgba(139, 90, 60, 0.15);
  --shadow-glow: 0 0 30px rgba(212, 175, 55, 0.2);
}
/* Global styles */
html, body, [class*="css"] {
  color: var(--text-primary);
  font-family: 'Sora', Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
  line-height: 1.6;
}
/* App background with dramatic warm texture */
.stApp {
  background:
    radial-gradient(ellipse at 20% 30%, rgba(212, 175, 55, 0.3) 0%, transparent 40%),
    radial-gradient(ellipse at 80% 70%, rgba(166, 124, 82, 0.25) 0%, transparent 50%),
    radial-gradient(circle at 60% 20%, rgba(193, 154, 107, 0.2) 0%, transparent 40%),
    linear-gradient(135deg, #FFFFFF 0%, #FFFAF5 30%, #FFF8F0 70%, #FFF5E6 100%);
  background-attachment: fixed;
  position: relative;
  min-height: 100vh;
}
/* Rich texture overlay */
.stApp::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    repeating-linear-gradient(45deg, transparent, transparent 30px, rgba(139, 90, 60, 0.03) 30px, rgba(139, 90, 60, 0.03) 60px),
    repeating-linear-gradient(-45deg, transparent, transparent 25px, rgba(212, 175, 55, 0.02) 25px, rgba(212, 175, 55, 0.02) 50px),
    radial-gradient(circle at 25% 25%, rgba(212, 175, 55, 0.05) 0%, transparent 2%),
    radial-gradient(circle at 75% 75%, rgba(166, 124, 82, 0.04) 0%, transparent 2%);
  pointer-events: none;
  z-index: 0;
  background-size: 200px 200px, 150px 150px, 100px 100px, 120px 120px;
}
/* Container */
.block-container {
  padding: 2.5rem 2.5rem 3rem 2.5rem;
  max-width: 1200px;
  position: relative;
  z-index: 1;
}
/* Hero Section with spectacular visual impact */
.odr-hero {
  text-align: center;
  padding: 7rem 0 6rem 0;
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.odr-hero::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1000px;
  height: 1000px;
  background:
    radial-gradient(circle, rgba(212, 175, 55, 0.2) 0%, rgba(166, 124, 82, 0.15) 30%, transparent 70%),
    radial-gradient(circle at 30% 70%, rgba(193, 154, 107, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 70% 30%, rgba(139, 90, 60, 0.08) 0%, transparent 40%);
  pointer-events: none;
  z-index: 0;
  animation: float 12s ease-in-out infinite;
}
.odr-hero::after {
  content: '';
  position: absolute;
  top: 15%;
  left: 5%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.15) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
  animation: float 8s ease-in-out infinite reverse;
}
.odr-title {
  font-family: 'Sora', Inter, sans-serif;
  font-size: 6.5rem;
  font-weight: 900;
  letter-spacing: -0.05em;
  margin: 0;
  line-height: 0.8;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 60px rgba(212, 175, 55, 0.4);
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 0 30px rgba(212, 175, 55, 0.3));
}
.odr-subtitle {
  margin-top: 3rem;
  color: var(--text-secondary);
  font-size: 1.6rem;
  font-weight: 400;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.8;
  position: relative;
  z-index: 2;
}
/* Dramatic sections with rich visual effects */
.odr-section {
  border: 1px solid var(--border-light);
  border-radius: 28px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 250, 245, 0.95) 100%),
    var(--bg-card);
  padding: 3.5rem;
  box-shadow:
    var(--shadow-soft),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(139, 90, 60, 0.05);
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
.odr-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--accent-tan), var(--accent-gold), var(--accent-tan), transparent);
  opacity: 0.8;
  animation: shimmer 3s ease-in-out infinite;
}
.odr-section::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.05) 0%, transparent 70%);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.4s ease;
}
.odr-section:hover {
  border-color: var(--border-soft);
  transform: translateY(-6px) scale(1.01);
  box-shadow:
    var(--shadow-elevated),
    inset 0 1px 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 rgba(139, 90, 60, 0.1);
}
.odr-section:hover::after {
  opacity: 1;
}
/* Section headers */
.odr-section-head {
  margin-bottom: 2.5rem;
}
.odr-section-h {
  font-family: 'Sora', Inter, sans-serif;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0;
  color: var(--text-primary);
}
.odr-section-sub {
  color: var(--text-secondary);
  font-size: 1.15rem;
  margin-top: 0.75rem;
  font-weight: 400;
  line-height: 1.6;
}
/* Rich cards with depth and effects */
.odr-card {
  border: 1px solid var(--border-light);
  border-radius: 24px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 248, 240, 0.98) 100%),
    var(--bg-card);
  padding: 2.5rem;
  box-shadow:
    var(--shadow-soft),
    inset 0 1px 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 rgba(139, 90, 60, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.odr-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}
.odr-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow:
    var(--shadow-medium),
    inset 0 1px 0 rgba(255, 255, 255, 0.9),
    inset 0 -1px 0 rgba(139, 90, 60, 0.1);
  border-color: var(--border-soft);
}
.odr-card:hover::before {
  opacity: 1;
}
/* Dynamic chips with rich effects */
.odr-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-light);
  border-radius: 999px;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-secondary);
  background:
    linear-gradient(135deg, var(--bg-warm) 0%, var(--bg-cream) 100%);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow:
    0 2px 8px rgba(139, 90, 60, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}
.odr-chip::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.2), transparent);
  transition: left 0.5s ease;
}
.odr-chip:hover::before {
  left: 100%;
}
.odr-chip:hover {
  background:
    linear-gradient(135deg, var(--bg-cream) 0%, var(--bg-warm) 100%);
  border-color: var(--border-soft);
  transform: translateY(-2px) scale(1.05);
  box-shadow:
    0 4px 16px rgba(139, 90, 60, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}
.odr-chip b {
  color: var(--text-primary);
  font-weight: 600;
}
/* Spectacular buttons with rich effects */
div[data-testid="stButton"] > button {
  border-radius: 20px !important;
  border: 2px solid var(--border-medium) !important;
  background:
    var(--accent-gradient),
    linear-gradient(135deg, var(--accent-brown) 0%, var(--accent-caramel) 100%) !important;
  color: white !important;
  padding: 1rem 2rem !important;
  font-weight: 700 !important;
  font-size: 1.1rem !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative !important;
  overflow: hidden !important;
  box-shadow:
    var(--shadow-soft),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    inset 0 -1px 0 rgba(0, 0, 0, 0.2) !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}
div[data-testid="stButton"] > button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s ease;
}
div[data-testid="stButton"] > button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.4) 0%, transparent 70%);
  transition: all 0.4s ease;
  pointer-events: none;
}
div[data-testid="stButton"] > button:hover::before {
  left: 100%;
}
div[data-testid="stButton"] > button:hover::after {
  width: 300px;
  height: 300px;
}
div[data-testid="stButton"] > button:hover {
  transform: translateY(-4px) scale(1.05) !important;
  box-shadow:
    var(--shadow-elevated),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    inset 0 -1px 0 rgba(0, 0, 0, 0.3) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  transform: translateY(-4px) scale(1.08) !important;
  box-shadow:
    0 25px 80px rgba(139, 90, 60, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -1px 0 rgba(0, 0, 0, 0.3) !important;
}
div[data-testid="stButton"] > button:disabled {
  opacity: 0.5 !important;
  transform: none !important;
  cursor: not-allowed !important;
}
/* Rich text area with dramatic effects */
div[data-testid="stTextArea"] textarea {
  border-radius: 20px !important;
  background:
    linear-gradient(135deg, var(--bg-input) 0%, rgba(255, 255, 255, 0.9) 100%) !important;
  border: 2px solid var(--border-light) !important;
  color: var(--text-primary) !important;
  font-size: 1.1rem !important;
  padding: 1.5rem !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow:
    inset 0 2px 4px rgba(139, 90, 60, 0.05),
    0 2px 8px rgba(139, 90, 60, 0.08) !important;
}
div[data-testid="stTextArea"] textarea:focus {
  outline: none !important;
  border-color: var(--accent-brown) !important;
  border-width: 3px !important;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, var(--bg-card) 100%) !important;
  box-shadow:
    0 0 0 6px rgba(139, 90, 60, 0.15),
    var(--shadow-glow),
    inset 0 2px 4px rgba(139, 90, 60, 0.05),
    0 8px 32px rgba(139, 90, 60, 0.2) !important;
  transform: translateY(-3px) scale(1.01) !important;
}
div[data-testid="stTextArea"] textarea::placeholder {
  color: var(--text-muted) !important;
  font-style: italic !important;
}
/* Dataframe and tabs */
div[data-testid="stDataFrame"], details[data-testid="stExpander"] {
  border-radius: 16px !important;
  border: 1px solid var(--border-light) !important;
  overflow: hidden !important;
  background: var(--bg-card) !important;
}
/* Sidebar */
section[data-testid="stSidebar"] {
  background: var(--bg-warm) !important;
  border-right: 1px solid var(--border-light) !important;
}
/* Animations */
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-12px) rotate(2deg); }
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.85; transform: scale(1.05); }
}
@keyframes fadeInUp {
      from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
@keyframes shimmer {
  0%, 100% { opacity: 0.6; transform: translateX(-100%); }
  50% { opacity: 1; transform: translateX(100%); }
}
@keyframes glow {
  0%, 100% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
  50% { box-shadow: 0 0 40px rgba(212, 175, 55, 0.5); }
}
/* Floating elements */
.floating {
  animation: float 8s ease-in-out infinite;
}
.pulsing {
  animation: pulse 3s ease-in-out infinite;
}
.glowing {
  animation: glow 2s ease-in-out infinite;
}
</style>""",
        unsafe_allow_html=True,
    )
def _clean_report(report: str) -> str:
    """
    Clean report to remove headings and any prompt text.
    Preserves paragraph structure while ensuring natural flowing narrative.
    """
    if not report:
        return report
    
    lines = report.split('\n')
    cleaned_lines = []
    skip_next_line = False
    current_paragraph = []
    
    # Find where the actual report content ends (before research materials)
    report_content = []
    in_research_materials = False
    
    for line in lines:
        line = line.strip()
        
        # Stop processing when we hit research materials section
        if "research question:" in line.lower() or "research materials:" in line.lower():
            break
            
        # Skip empty lines (but preserve as paragraph breaks)
        if not line:
            if current_paragraph:  # End current paragraph if we have content
                cleaned_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            continue
        
        # Skip if it's a heading (contains common heading words)
        heading_indicators = [
            'introduction:', 'conclusion:', 'analysis:', 'summary:', 'findings:', 'background:', 
            'methodology:', 'results:', 'discussion:', 'how do', 'what are', 'what is', 'sources:',
            'advantages of', 'comparison with', 'different types of', 'training', 'rnns have',
            'combining', 'dropout and', 'rnns have been', 'impacts', 'challenges',
            'comparisons', 'future trends', 'how rnn', 'what are the impacts',
            'what are the challenges', 'how does', 'what are the future', 'body:', 'references:',
            'references', 'bibliography', 'appendix', 'acknowledgement', 'abstract'
        ]
        is_heading = any(line.lower().startswith(indicator) for indicator in heading_indicators)
        
        # Skip if it's prompt text (enhanced detection)
        prompt_indicators = [
            'report:', 'write a', 'please ensure', 'do not', 'weave all', 'unified narrative', 'cohesive passage',
            'requirements:', 'write exactly', 'each paragraph must', 'use complex sentence', 'ensure smooth transitions',
            'include in-text citations', 'do not include any instructions', 'only the report itself',
            'introduction: introduce topic', 'background: explain current', 'analysis: present key findings',
            'implications: discuss practical', 'conclusion: summarize and provide'
        ]
        is_prompt = any(indicator in line.lower() for indicator in prompt_indicators)
        
        # Skip reference citations like [1], [2], etc.
        if line.startswith('[') and ']' in line and len(line) < 10:
            continue
        
        if is_heading or is_prompt:
            skip_next_line = True
            continue
        
        if skip_next_line and line and len(line) < 50:  # Skip short lines after headings
            skip_next_line = False
            continue
        
        skip_next_line = False
        
        # Add line to current paragraph
        current_paragraph.append(line)
    
    # Add the last paragraph if we have content
    if current_paragraph:
        cleaned_lines.append(' '.join(current_paragraph))
    
    # Join paragraphs with proper spacing
    cleaned_report = '\n\n'.join(cleaned_lines)
    
    # Fix spacing issues
    cleaned_report = cleaned_report.replace('.  ', '. ').replace('  ', ' ')
    
    # Remove duplicate sentences while preserving paragraph structure
    paragraphs = cleaned_report.split('\n\n')
    unique_paragraphs = []
    seen_sentences = set()
    
    for paragraph in paragraphs:
        sentences = paragraph.split('. ')
        unique_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence not in seen_sentences:
                unique_sentences.append(sentence)
                seen_sentences.add(sentence)
        
        if unique_sentences:
            unique_paragraphs.append('. '.join(unique_sentences))
    
    cleaned_report = '\n\n'.join(unique_paragraphs)
    
    # Ensure it ends with a period
    if cleaned_report and not cleaned_report.endswith('.'):
        cleaned_report += '.'
    
    return cleaned_report

def _pdf_bytes(title: str, subquestions: List[Dict[str, Any]], report: str) -> bytes:
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer
    except Exception as e:
        raise RuntimeError(
            "PDF support requires 'reportlab'. Install it with: pip install reportlab"
        ) from e
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=LETTER,
        title=title,
        author="OpenDeepResearcher",
    )
    styles = getSampleStyleSheet()
    
    # Create custom styles with larger font
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=20,
        textColor='#2c3e50'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor='#34495e'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leading=16,  # Line spacing
        textColor='#2c3e50'
    )
    
    story = []
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(datetime.now().strftime("Generated on %Y-%m-%d %H:%M"), body_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Planner Output (Subquestions)", heading_style))
    sq_items: List[ListItem] = []
    for sq in subquestions:
        qid = str(sq.get("id", ""))
        qtype = str(sq.get("type", ""))
        priority = str(sq.get("priority", ""))
        text = str(sq.get("text", ""))
        line = f"{qid} (priority {priority}, {qtype}): {text}".strip()
        sq_items.append(ListItem(Paragraph(line, body_style)))
    story.append(ListFlowable(sq_items, bulletType="bullet"))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Synthesis Report", heading_style))
    
    # Split report into paragraphs and add each as separate paragraph
    paragraphs = report.split('\n\n')  # Split by paragraph breaks, not sentences
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            # Add period if it doesn't end with one
            if not paragraph.endswith('.'):
                paragraph += '.'
            story.append(Paragraph(paragraph, body_style))
            story.append(Spacer(1, 8))
    
    doc.build(story)
    return buf.getvalue()

def _init_session() -> None:
    if "planner_result" not in st.session_state:
        st.session_state.planner_result = None
    if "subquestions" not in st.session_state:
        st.session_state.subquestions = None
    if "report" not in st.session_state:
        st.session_state.report = None
    if "last_topic" not in st.session_state:
        st.session_state.last_topic = ""
def _render_header() -> None:
    st.markdown(
        """<div class="odr-hero">
<div style="position: absolute; top: 10%; left: 5%; width: 150px; height: 150px; background: radial-gradient(circle, rgba(212, 175, 55, 0.2) 0%, transparent 70%); animation: float 10s ease-in-out infinite;"></div>
<div style="position: absolute; top: 20%; right: 8%; width: 120px; height: 120px; background: radial-gradient(circle, rgba(166, 124, 82, 0.15) 0%, transparent 70%); animation: float 8s ease-in-out infinite reverse;"></div>
<div style="position: absolute; bottom: 15%; left: 10%; width: 100px; height: 100px; background: radial-gradient(circle, rgba(193, 154, 107, 0.12) 0%, transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
<div style="position: relative; z-index: 2;">
<h1 class="odr-title floating">OpenDeepResearcher</h1>
<div style="margin-top: 1rem; text-align: center;">
<div class="odr-chip glowing" style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(166, 124, 82, 0.15)); border: 2px solid var(--accent-gold); padding: 0.75rem 2rem; font-size: 1rem; color: var(--accent-brown);">
<span style="font-size: 1.2rem; margin-right: 0.5rem;">⭐</span>
<b>Premium AI Research Platform</b>
</div>
</div>
</div>
<div class="odr-subtitle" style="position: relative; z-index: 2;">
<div style="font-size: 1.8rem; margin-bottom: 1.5rem; font-weight: 600; color: var(--text-primary);">
✨ Where <span style="color: var(--accent-brown); font-weight: 700;">Curiosity</span> Meets <span style="color: var(--accent-brown); font-weight: 700;">Clarity</span>
</div>
<div style="font-size: 1.4rem; color: var(--text-secondary); font-weight: 300; line-height: 1.8; max-width: 700px; margin: 0 auto 2.5rem auto;">
Transform your research questions into comprehensive, beautifully crafted reports with <span style="color: var(--accent-brown); font-weight: 600; font-size: 1.5rem;">AI-powered precision</span> and elegant presentation.
</div>
<div style="display: flex; justify-content: center; gap: 2rem; margin: 2.5rem 0; flex-wrap: wrap;">
<div style="text-align: center;">
<div style="font-size: 2.5rem; margin-bottom: 0.5rem; filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.3));">🎯</div>
<div style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary);">Precise Analysis</div>
</div>
<div style="text-align: center;">
<div style="font-size: 2.5rem; margin-bottom: 0.5rem; filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.3));">📚</div>
<div style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary);">Comprehensive Reports</div>
</div>
<div style="text-align: center;">
<div style="font-size: 2.5rem; margin-bottom: 0.5rem; filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.3));">✨</div>
<div style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary);">Beautiful Results</div>
</div>
</div>
<div style="margin-top: 3.5rem; position: relative;">
<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 300px; height: 300px; background: radial-gradient(circle, rgba(212, 175, 55, 0.15) 0%, transparent 70%); pointer-events: none; z-index: 0;"></div>
<div class="odr-chip glowing" style="font-size: 1.2rem; padding: 1.25rem 2.5rem; background: var(--accent-gradient); border: none; color: white; box-shadow: 0 10px 40px rgba(139, 90, 60, 0.3); position: relative; z-index: 1;">
<span style="font-size: 1.6rem; margin-right: 1rem;">🚀</span>
<b style="color: white; font-size: 1.3rem;">Start Your Research Journey</b>
</div>
</div>
</div>
</div>
        """,
        unsafe_allow_html=True,
    )
def _section_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""<div class='odr-section-head'>
  <h2 class='odr-section-h'>{title}</h2>
  <p class='odr-section-sub'>{subtitle}</p>
</div>""",
        unsafe_allow_html=True,
    )
def _render_subquestions(subquestions: List[Dict[str, Any]]) -> None:
    st.markdown("<div style='height: 2.5rem'></div>", unsafe_allow_html=True)
    # Dramatic header with visual element
    st.markdown(
        f"""<div style="text-align: center; margin-bottom: 3rem;">
  <div class="odr-chip glowing" style="font-size: 1.2rem; padding: 1rem 2.5rem; background: linear-gradient(135deg, var(--accent-brown), var(--accent-caramel)); border: none; color: white; box-shadow: 0 8px 32px rgba(139, 90, 60, 0.3);">
    <span style="font-size: 1.8rem; margin-right: 1rem;">🌿</span>
    <b style="color: white; font-size: 1.3rem;">Research Plan</b>
    <span style="margin-left: 1rem; color: rgba(255, 255, 255, 0.9); font-size: 1rem;">{len(subquestions)} research questions crafted</span>
  </div>
</div>""",
        unsafe_allow_html=True,
    )
    tab_table, tab_cards = st.tabs([" Table View", "🎴 Card View"])
    with tab_table:
        try:
            import pandas as pd
            rows = [
                {
                    "#": i + 1,
                    "ID": sq.get('id', f'q{i+1}'),
                    "Priority": sq.get('priority', 'N/A'),
                    "Type": sq.get('type', 'N/A'),
                    "Subquestion": sq.get('text', ''),
                }
                for i, sq in enumerate(subquestions)
            ]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        except ImportError:
            st.info("Please install pandas to view the table format.")
    with tab_cards:
        for i, sq in enumerate(subquestions):
            # Add staggered animation delay
            delay = i * 0.1
            st.markdown(
                f"""<div class='odr-card' style='margin-bottom: 1.5rem; border-left: 4px solid var(--accent-brown); background: var(--bg-cream); animation: fadeInUp 0.5s ease-out {delay}s both;'>
  <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
    <div style='flex: 1;'>
      <div style='font-size: 1.25rem; font-weight: 600; margin-bottom: 0.75rem; color: var(--text-primary); line-height: 1.5;'>
        {i + 1}. {sq.get('text')}
      </div>
      <div style='display: flex; gap: 0.75rem; flex-wrap: wrap;'>
        <span class='odr-chip' style='background: var(--bg-warm); border-color: var(--border-soft);'>
          <span style='font-size: 0.95rem;'>🎯</span>
          Priority: <b>{sq.get('priority', 'N/A')}</b>
        </span>
        <span class='odr-chip' style='background: var(--bg-warm); border-color: var(--border-soft);'>
          <span style='font-size: 0.95rem;'>📂</span>
          Type: <b>{sq.get('type', 'N/A')}</b>
        </span>
        <span class='odr-chip' style='background: var(--bg-warm); border-color: var(--border-soft);'>
          <span style='font-size: 0.95rem;'>#️⃣</span>
          ID: <b>{sq.get('id', 'N/A')}</b>
        </span>
      </div>
    </div>
  </div>
</div></div>""",
                unsafe_allow_html=True
            )
    # Add fade in animation
    st.markdown("""<style>
@keyframes fadeInUp {
      from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>""",
        unsafe_allow_html=True,
    )
def main() -> None:
    st.set_page_config(
        page_title="OpenDeepResearcher",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_session()
    _render_css()
    _render_header()
    with st.sidebar:
        st.markdown(
"""<div style="text-align: center; margin-bottom: 2rem;">
  <div class="odr-chip" style="background: var(--bg-warm); border: 2px solid var(--border-soft); padding: 0.75rem 1.5rem;">
    <span style="font-size: 1.2rem; margin-right: 0.5rem;">⚙️</span>
    <b>Configuration</b>
  </div>
</div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
"""<div class='odr-card' style='background: var(--bg-cream); border: 2px solid var(--border-soft);'>
  <div style="font-size: 1rem; font-weight: 600; margin-bottom: 0.75rem; color: var(--text-primary);">
    ☕ Local Model Setup
  </div>
  <div style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">
    LM Studio must be running at <code style="background: var(--bg-warm); padding: 0.25rem 0.5rem; border-radius: 6px; font-size: 0.9rem;">http://127.0.0.1:1234</code> to serve the local model.
  </div>
</div>""",
            unsafe_allow_html=True,
        )
    # --- Main Content Sections with enhanced drama ---
    st.markdown("<div class='odr-section' style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 248, 240, 0.98) 100%); border: 2px solid var(--border-soft); box-shadow: 0 20px 60px rgba(139, 90, 60, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.8);'>", unsafe_allow_html=True)
    # Enhanced section header with more drama
    st.markdown("""<div class='odr-section-head' style='text-align: center; margin-bottom: 3rem;'>
  <h2 class='odr-section-h' style='font-size: 2.5rem; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1rem;'>
    🌿 Begin Your Research Journey
  </h2>
  <p class='odr-section-sub' style='font-size: 1.3rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto;'>
    Share your curiosity and we'll transform it into comprehensive insights with <span style='color: var(--accent-brown); font-weight: 600;'>elegant precision</span>.
  </p>
</div>""",
        unsafe_allow_html=True,
    )
    # Dramatic floating input area with no white box
    st.markdown(
"""<div style="text-align: center; margin: 2rem 0 4rem 0; position: relative;">
  <div style="font-size: 2rem; font-weight: 800; margin-bottom: 1.5rem; color: var(--text-primary); background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
    <span style="font-size: 2.5rem; margin-right: 1rem; filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.5));">☕</span>
    What would you like to explore today?
  </div>
  <div style="color: var(--text-secondary); font-size: 1.3rem; margin-bottom: 3rem; line-height: 1.7; font-weight: 300;">
    Share your research topic and we'll craft a comprehensive analysis with <span style="color: var(--accent-brown); font-weight: 700; font-size: 1.4rem;">AI-powered precision</span>.
  </div>
  <div style="display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 3rem; flex-wrap: wrap;">
    <div class="odr-chip glowing" style="background: linear-gradient(135deg, rgba(139, 90, 60, 0.15), rgba(166, 124, 82, 0.2)); border: 2px solid var(--accent-brown); padding: 0.875rem 1.5rem; font-size: 1rem;">
      <span style="font-size: 1.2rem; margin-right: 0.5rem;">🎯</span>
      <b>Precise</b>
    </div>
    <div class="odr-chip glowing" style="background: linear-gradient(135deg, rgba(139, 90, 60, 0.15), rgba(166, 124, 82, 0.2)); border: 2px solid var(--accent-brown); padding: 0.875rem 1.5rem; font-size: 1rem;">
      <span style="font-size: 1.2rem; margin-right: 0.5rem;">📚</span>
      <b>Comprehensive</b>
    </div>
    <div class="odr-chip glowing" style="background: linear-gradient(135deg, rgba(139, 90, 60, 0.15), rgba(166, 124, 82, 0.2)); border: 2px solid var(--accent-brown); padding: 0.875rem 1.5rem; font-size: 1rem;">
      <span style="font-size: 1.2rem; margin-right: 0.5rem;">✨</span>
      <b>Beautiful</b>
    </div>
  </div>
</div></div></div>""",
        unsafe_allow_html=True,
    )
    # Enhanced text area with dramatic styling
    st.markdown(
"""<div style="position: relative; margin-bottom: 3rem;">
  <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); z-index: 10;">
    <div class="odr-chip glowing" style="background: var(--accent-gradient); border: none; color: white; padding: 0.5rem 1.5rem; font-size: 0.9rem; box-shadow: 0 4px 20px rgba(139, 90, 60, 0.4);">
      <span style="font-size: 1rem; margin-right: 0.5rem;">📝</span>
      <b style="color: white;">Enter Your Topic</b>
    </div>
  </div>
</div></div></div>""",
        unsafe_allow_html=True,
    )
    topic = st.text_area(
        "Enter your research topic",
        value=st.session_state.last_topic,
        placeholder="🌿 The evolution of sustainable architecture in urban environments (2010-2024)\n\n✨ Share your curiosity and let AI craft comprehensive insights...",
        height=160,
        label_visibility="collapsed",
    )
    # Dramatic button area with enhanced visual effects
    st.markdown(
"""<div style="text-align: center; margin: 3rem 0; position: relative;">
  <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; height: 400px; background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%); pointer-events: none; z-index: 0; animation: float 8s ease-in-out infinite;"></div>
  <div style="position: relative; z-index: 1; display: flex; justify-content: center; align-items: center; gap: 2rem;">
    <div style="flex: 0 0 auto;">
    </div>
    <div style="flex: 0 0 320px;">
    </div>
    <div style="flex: 0 0 auto;">
    </div>
  </div>
</div></div></div>""",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
    with col2:
        plan_clicked = st.button("🚀 Plan Research", type="primary", use_container_width=True)
    with col3:
        clear_clicked = st.button("Clear All", use_container_width=True)
    # Dramatic visual flow indicator
    st.markdown(
"""<div style="display: flex; align-items: center; justify-content: center; margin: 4rem 0; gap: 1.5rem;">
  <div class="odr-chip pulsing" style="background: linear-gradient(135deg, var(--bg-warm), var(--bg-cream)); border: 2px solid var(--border-soft); padding: 1rem 1.75rem; font-size: 1.1rem;">
    <span style="font-size: 1.5rem; margin-right: 0.75rem;">☕</span>
    <b>Curiosity</b>
  </div>
  <div style="color: var(--accent-brown); font-size: 2.5rem; font-weight: 300; animation: pulse 2s ease-in-out infinite;">→</div>
  <div class="odr-chip" style="background: linear-gradient(135deg, var(--bg-warm), var(--bg-cream)); border: 2px solid var(--border-soft); padding: 1rem 1.75rem; font-size: 1.1rem;">
    <span style="font-size: 1.5rem; margin-right: 0.75rem;">🌿</span>
    <b>Research</b>
  </div>
  <div style="color: var(--accent-brown); font-size: 2.5rem; font-weight: 300; animation: pulse 2s ease-in-out infinite 0.5s;">→</div>
  <div class="odr-chip" style="background: linear-gradient(135deg, var(--bg-warm), var(--bg-cream)); border: 2px solid var(--border-soft); padding: 1rem 1.75rem; font-size: 1.1rem;">
    <span style="font-size: 1.5rem; margin-right: 0.75rem;">📖</span>
    <b>Insights</b>
  </div>
</div></div></div>""",
        unsafe_allow_html=True,
    )
    if clear_clicked:
        st.session_state.planner_result = None
        st.session_state.subquestions = None
        st.session_state.report = None
        st.session_state.last_topic = ""
        st.rerun()
    if plan_clicked:
        if not topic.strip():
            st.error("Please provide a research topic to begin.")
        else:
            st.session_state.last_topic = topic
            st.session_state.report = None
            with st.spinner("Analyzing topic and creating research plan..."):
                planner = PlannerAgent()
                st.session_state.planner_result = planner.plan(topic.strip())
                st.session_state.subquestions = st.session_state.planner_result.get("subquestions", [])
    if st.session_state.subquestions:
        _render_subquestions(st.session_state.subquestions)
    # --- Generate Report Section ---
    if st.session_state.subquestions:
        st.markdown("<div style='height: 2.5rem'></div>", unsafe_allow_html=True)
        st.markdown("<div class='odr-section'>", unsafe_allow_html=True)
        _section_header(
            "Craft Your Comprehensive Report",
            "Transform your research questions into a beautifully structured, citation-ready document with AI-powered synthesis."
        )
        # Centered generate button with warm styling
        st.markdown(
"""<div style="text-align: center; margin: 2.5rem 0;">
  <div style="display: inline-block;"></div></div>""",
            unsafe_allow_html=True,
        )
        generate_clicked = st.button(
            " Generate Full Report",
            type="primary",
            use_container_width=True
        )
        st.markdown("""""",
            unsafe_allow_html=True,
        )
        if generate_clicked:
            with st.spinner("🌿 Researching sources and crafting insights..."):
                searcher = SearcherAgent()
                search_results = searcher.search_all(st.session_state.subquestions)
                writer = WriterAgent()
                raw_report = writer.synthesize_report(
                    research_question=topic.strip(),
                    subquestions=st.session_state.subquestions,
                    search_results=search_results,
                )
                # Clean the report to remove headings and prompt text
                st.session_state.report = _clean_report(raw_report)
        if st.session_state.report:
            # Dramatic success indicator
            st.markdown(
"""<div style="text-align: center; margin: 3rem 0;">
  <div class="odr-chip glowing" style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.3)); border: 2px solid rgba(34, 197, 94, 0.4); padding: 1rem 2.5rem; font-size: 1.1rem;">
    <span style="font-size: 1.6rem; margin-right: 1rem;">🎉</span>
    <b style="color: #22C55E; font-size: 1.2rem;">Report Crafted Successfully!</b>
  </div>
</div>""",
                unsafe_allow_html=True,
            )
            # Enhanced download section only - no report display
            st.markdown("<div style='height: 2.5rem'></div>", unsafe_allow_html=True)
            st.markdown(
"""<div style="text-align: center; margin-bottom: 1.5rem;">
  <h3 style="margin: 0; font-size: 1.6rem; font-weight: 700; color: var(--text-primary);">💾 Download Your Report</h3>
</div>""",
                unsafe_allow_html=True,
            )
            pdf_data = _pdf_bytes(
                title=f"Research Report: {topic.strip()}",
                subquestions=st.session_state.subquestions,
                report=st.session_state.report
            )
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_data,
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        st.markdown("</div>", unsafe_allow_html=True)  # Close section
        st.markdown("</div>", unsafe_allow_html=True)  # Close section
        st.markdown("</div>", unsafe_allow_html=True)  # Close section
        st.markdown("</div>", unsafe_allow_html=True)  # Close section
if __name__ == "__main__":
    main()