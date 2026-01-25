import os
import re
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


def export_pdf(input_md, output_pdf):
    if not os.path.exists(input_md):
        raise FileNotFoundError(input_md)

    # Force delete old PDF
    if os.path.exists(output_pdf):
        os.remove(output_pdf)

    with open(input_md, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    story = []

    for line in lines:
        raw = line.strip()
        if not raw:
            story.append(Spacer(1, 12))
            continue

        if raw.startswith("# "):
            story.append(Paragraph(raw[2:], styles["Title"]))
        elif raw.startswith("## "):
            story.append(Paragraph(raw[3:], styles["Heading2"]))
        else:
            story.append(Paragraph(raw, styles["BodyText"]))

    doc.build(story)

    return output_pdf