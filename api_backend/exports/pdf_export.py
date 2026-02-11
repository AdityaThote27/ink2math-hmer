from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_pdf(filename, input_expr, solution, steps):
    doc = SimpleDocTemplate(filename)
    elements = []

    styles = getSampleStyleSheet()

    # Custom Title Style
    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=20
    )

    # Left aligned normal style
    normal_style = ParagraphStyle(
        name="NormalStyle",
        parent=styles["Normal"],
        alignment=TA_LEFT,
        fontSize=12,
        spaceAfter=10
    )

    # ---------- TITLE ----------
    elements.append(Paragraph("INK2MATH: SMART EQUATION SOLVER", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # ---------- QUESTION ----------
    elements.append(Paragraph("<b>Question:</b>", normal_style))
    elements.append(Paragraph(input_expr, normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # ---------- SOLUTION ----------
    elements.append(Paragraph("<b>Solution:</b>", normal_style))
    elements.append(Paragraph(f"x = {solution}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # ---------- STEPS ----------
    elements.append(Paragraph("<b>Steps to Solve:</b>", normal_style))
    elements.append(Spacer(1, 0.1 * inch))

    for step in steps:
        elements.append(
            Paragraph(f"{step['step']}. {step['description']}", normal_style)
        )
        elements.append(Spacer(1, 0.1 * inch))

    doc.build(elements)
