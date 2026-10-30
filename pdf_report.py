from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from xml.sax.saxutils import escape

DISCLAIMER = (
    "This tool analyzes linguistic and content-based warning signals. "
    "It does not independently verify whether a news item is true or false."
)

def create_pdf_report(title, article, result):
    """Build a small PDF report in memory so users can download it."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph("AI-Based News Sentiment and Credibility Assistance Dashboard", styles["Title"]),
        Spacer(1, 12),
        Paragraph("<b>Headline:</b> " + escape(title or "Untitled analysis"), styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("<b>Sentiment:</b> " + escape(result["sentiment"]), styles["BodyText"]),
        Paragraph("<b>Polarity score:</b> " + f'{result["sentiment_score"]:.3f}', styles["BodyText"]),
        Paragraph("<b>Clickbait status:</b> " + escape(result["clickbait_status"]), styles["BodyText"]),
        Paragraph("<b>Credibility-assistance score:</b> " + f'{result["credibility_score"]}/100', styles["BodyText"]),
        Paragraph("<b>Risk category:</b> " + escape(result["risk_category"]), styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("<b>Summary</b>", styles["Heading2"]),
        Paragraph(escape(result["summary"]), styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("<b>Warning signals</b>", styles["Heading2"]),
    ]
    warnings = result.get("warning_signals") or ["No configured warning patterns detected."]
    for warning in warnings:
        story.append(Paragraph("• " + escape(warning), styles["BodyText"]))
    story += [
        Spacer(1, 10),
        Paragraph("<b>Submitted text</b>", styles["Heading2"]),
        Paragraph(escape((article or "")[:8000]).replace("\n", "<br/>"), styles["BodyText"]),
        Spacer(1, 10),
        Paragraph("<b>Disclaimer:</b> " + escape(DISCLAIMER), styles["Italic"]),
    ]
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
