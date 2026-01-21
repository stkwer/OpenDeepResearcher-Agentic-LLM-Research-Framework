import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def export_markdown(text: str) -> str:
    """
    Export research paper as Markdown
    """
    return text


def export_pdf(text: str) -> bytes:
    """
    Export research paper as PDF using ReportLab
    """
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    for line in text.split("\n"):
        if line.strip() == "":
            story.append(Spacer(1, 12))
        else:
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()




