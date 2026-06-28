from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


def create_resume_pdf(text):

    os.makedirs("static/reports", exist_ok=True)

    pdf_path = "static/reports/resume_analysis.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>CareerPilot AI</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Resume Analysis Report",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph("<br/><br/>", styles["BodyText"])
    )

    for line in text.split("\n"):

        if line.strip():

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

    doc.build(story)

    return pdf_path


# ==========================================
# Career Roadmap PDF
# ==========================================

def create_roadmap_pdf(text):

    os.makedirs("static/reports", exist_ok=True)

    pdf_path = "static/reports/career_roadmap.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>CareerPilot AI</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Career Roadmap",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph("<br/><br/>", styles["BodyText"])
    )

    for line in text.split("\n"):

        if line.strip():

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

    doc.build(story)

    return pdf_path