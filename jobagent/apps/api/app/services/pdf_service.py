"""
PDF Service — generates a resume PDF from Markdown content using ReportLab.
"""
import os
from pathlib import Path
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from loguru import logger


PDFS_DIR = Path("static/resumes")
PDFS_DIR.mkdir(parents=True, exist_ok=True)


def _md_to_paragraphs(md_text: str, styles) -> list:
    """Basic Markdown→ReportLab conversion."""
    flowables = []
    for line in md_text.splitlines():
        line = line.strip()
        if not line:
            flowables.append(Spacer(1, 0.2 * cm))
        elif line.startswith("# "):
            flowables.append(Paragraph(line[2:], styles["h1_style"]))
            flowables.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#6366f1")))
        elif line.startswith("## "):
            flowables.append(Paragraph(line[3:], styles["h2_style"]))
        elif line.startswith("- "):
            flowables.append(Paragraph(f"• {line[2:]}", styles["body_style"]))
        elif line.startswith("**") and line.endswith("**"):
            flowables.append(Paragraph(f"<b>{line[2:-2]}</b>", styles["body_style"]))
        else:
            flowables.append(Paragraph(line, styles["body_style"]))
    return flowables


async def generate_pdf(resume_md: str, user_id: int, resume_id: int) -> str:
    """
    Generate a PDF from Markdown resume content.
    Returns the file path relative to the static directory.
    """
    filename = f"resume_{user_id}_{resume_id}.pdf"
    filepath = PDFS_DIR / filename

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    base_styles = getSampleStyleSheet()
    custom_styles = {
        "h1_style": ParagraphStyle(
            "H1", parent=base_styles["Heading1"],
            fontSize=18, textColor=colors.HexColor("#1e293b"), spaceAfter=4
        ),
        "h2_style": ParagraphStyle(
            "H2", parent=base_styles["Heading2"],
            fontSize=13, textColor=colors.HexColor("#6366f1"), spaceAfter=4
        ),
        "body_style": ParagraphStyle(
            "Body", parent=base_styles["Normal"],
            fontSize=10, leading=14, textColor=colors.HexColor("#374151")
        ),
    }

    flowables = _md_to_paragraphs(resume_md, custom_styles)
    doc.build(flowables)

    logger.info(f"[PDFService] Generated PDF: {filepath}")
    return f"static/resumes/{filename}"
