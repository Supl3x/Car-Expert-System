"""In-memory PDF evaluation report (ReportLab). Nothing is written to disk."""
import io
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from inference_engine import DISCLAIMER, VERDICTS

GOLD = colors.HexColor("#D4AF37")
DARK = colors.HexColor("#0B0B0F")
BRONZE = colors.HexColor("#8C6B1F")
SEV = {"Critical": "#E5484D", "High": "#F2873A", "Medium": "#B8860B", "Low": "#3B7DBE"}
VCOL = {"Good Candidate": "#2E9E6B", "Buy After Inspection": "#B8860B",
        "Negotiate / Proceed with Caution": "#D9731F", "Avoid Purchase": "#C73A3F"}


def safe(text):
    """Standard PDF fonts only support Latin-1, so replace unsupported characters."""
    text = (str(text).replace("→", "->").replace("–", "-").replace("—", "-")
            .replace("“", '"').replace("”", '"').replace("’", "'"))
    return escape(text.encode("latin-1", "replace").decode("latin-1"))


def build_report(vehicle, result):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=15 * mm, bottomMargin=15 * mm, title="RecycleDrive Report")
    base = getSampleStyleSheet()["Normal"]
    body = ParagraphStyle("body", parent=base, fontSize=9, leading=12)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10)
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=13,
                        textColor=BRONZE, spaceBefore=10, spaceAfter=4)
    title = ParagraphStyle("title", parent=body, fontName="Helvetica-Bold", fontSize=22,
                           textColor=GOLD, leading=26)
    tagline = ParagraphStyle("tag", parent=body, textColor=colors.HexColor("#F3E2A9"), fontSize=10)

    def P(t, s=body):
        return Paragraph(safe(t), s)

    story = []
    band = Table([[P("RecycleDrive - Vehicle Evaluation Report", title)],
                  [P("Know the car before you pay for it.  |  " + datetime.now().strftime("%d %b %Y, %H:%M"), tagline)]],
                 colWidths=[180 * mm])
    band.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), DARK), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                              ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story += [band, Spacer(1, 8)]

    story.append(P("Vehicle details", h2))
    rows = [["Vehicle", f"{vehicle['year']} {vehicle['make']} {vehicle['model']}"],
            ["Mileage", f"{vehicle['mileage']:,} km"], ["Transmission / Fuel", f"{vehicle['transmission']} / {vehicle['fuel']}"],
            ["City", vehicle["city"]], ["Imported", vehicle["imported"]],
            ["Asking price", f"PKR {vehicle['price']:,}" if vehicle["price"] else "Not entered"]]
    t = Table([[P(a, small), P(b)] for a, b in rows], colWidths=[45 * mm, 135 * mm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, BRONZE), ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F6EFD2"))]))
    story.append(t)

    v = result["verdict"]
    story.append(P("Verdict", h2))
    vstyle = ParagraphStyle("v", parent=body, fontName="Helvetica-Bold", fontSize=16, textColor=colors.HexColor(VCOL[v]))
    story += [P(v, vstyle), P(VERDICTS[v]), P(result["reason"], small)]

    c = result["counts"]
    story.append(P(f"Concern summary (counts, not a probability): Critical {c['Critical']}, High {c['High']}, "
                   f"Medium {c['Medium']}, Low {c['Low']}.  Positive findings: {c['Positive']} "
                   "(positive findings never offset Critical or High concerns).", small))

    if result["unverified"]:
        story.append(P("Unverified key checks", h2))
        for item in result["unverified"]:
            story.append(P("- " + item, small))

    story.append(P("Activated concern rules", h2))
    if result["negatives"]:
        data = [[P("<b>ID</b>", small), P("<b>Category</b>", small), P("<b>Severity</b>", small),
                 P("<b>Conclusion</b>", small), P("<b>Why it fired</b>", small)]]
        for r in result["negatives"]:
            data.append([P(r["id"], small), P(r["category"], small),
                         Paragraph(f'<font color="{SEV[r["severity"]]}"><b>{r["severity"]}</b></font>', small),
                         P(r["conclusion"], small), P(r["explanation"], small)])
        t = Table(data, colWidths=[16 * mm, 28 * mm, 17 * mm, 53 * mm, 66 * mm], repeatRows=1)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, BRONZE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F6EFD2"))]))
        story.append(t)
    else:
        story.append(P("No concern rules were activated by the information provided."))

    story.append(P("Positive findings", h2))
    story.append(P("; ".join(r["conclusion"] for r in result["positives"]) or "None recorded.", small))

    story.append(P("Forward-chaining trace", h2))
    for tr in result["trace"]:
        extra = f"  [derives: {tr['derived']}]" if tr["derived"] else ""
        story.append(P(f"Pass {tr['pass']}: {tr['rule_id']} - {tr['conclusion']} (IF {tr['when']}){extra}", small))

    story.append(P("Recommended next steps", h2))
    for i, step in enumerate(result["next_steps"], 1):
        story.append(P(f"{i}. {step}", small))

    story += [Spacer(1, 10), P("Disclaimer", h2), P(DISCLAIMER, small)]
    doc.build(story)
    return buf.getvalue()