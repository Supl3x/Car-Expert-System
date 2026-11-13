"""Builds docs/AurumDrive_Code_Explanation.pdf.  Run from the project root:  python build_docs_pdf.py"""
import inspect
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (PageBreak, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

import inference_engine
import knowledge_base
from demo_cases import DEMO_CASES
from inference_engine import TREE, evaluate
from knowledge_base import RULES
from questions import CATEGORIES, QUESTIONS
from report_generator import safe
from vehicle_data import DEFAULT_FORM, normalize_vehicle

GOLD, DARK, BRONZE = colors.HexColor("#D4AF37"), colors.HexColor("#0B0B0F"), colors.HexColor("#8C6B1F")
OUT = os.path.join("docs", "AurumDrive_Code_Explanation.pdf")

base = getSampleStyleSheet()["Normal"]
body = ParagraphStyle("b", parent=base, fontSize=10, leading=14)
h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=15, textColor=BRONZE, spaceBefore=12, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=11, textColor=DARK, spaceBefore=8, spaceAfter=3)
code = ParagraphStyle("c", fontName="Courier", fontSize=7, leading=8.5, backColor=colors.HexColor("#F5F1E6"))
small = ParagraphStyle("s", parent=body, fontSize=8, leading=10)


def P(t, s=body):
    return Paragraph(safe(t), s)


def C(text):
    clean = text.encode("latin-1", "replace").decode("latin-1")
    return Preformatted(clean, code)


story = []

# 1. Title page
band = Table([[Paragraph("AurumDrive", ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=30, textColor=GOLD, leading=34))],
              [Paragraph("Pakistan Used-Car Verdict System - Code Explanation", ParagraphStyle("t2", fontName="Helvetica", fontSize=13, textColor=colors.white))]],
             colWidths=[180 * mm])
band.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), DARK), ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14), ("LEFTPADDING", (0, 0), (-1, -1), 16)]))
story += [band, Spacer(1, 20),
          P("Course: Artificial Intelligence    |    Project: Rule-Based Expert System and Decision Support System"),
          P("Student name: ____________________    Roll number: ____________    Section: ______"),
          P(f"Date: {datetime.now():%d %B %Y}"),
          P("Live link: https://<your-app>.streamlit.app   (replace after deployment)"), PageBreak()]

# 2. Problem statement
story += [P("1. Problem statement and niche", h1),
          P("Buying a used car in Pakistan is risky: odometer tampering, flood-damaged imports, swapped engines, "
            "unverified registration and transfer papers, and pressure from sellers are common. Most buyers are "
            "not mechanics. AurumDrive is an expert system that captures the reasoning of an experienced inspector "
            "as explicit IF-THEN rules and explains every conclusion. It also works as a decision support system: "
            "it makes a recommendation, but the buyer makes the final decision. The niche is Pakistan-specific: "
            "registration book or smart card checks, token tax dues, ownership transfer papers, and customs "
            "clearance and auction-sheet checks for imported (mostly Japanese) vehicles.")]

# 3. Methodology
story += [P("2. Expert system methodology", h1),
          P("1) Problem identification: reduce risk when buying a used car in Pakistan."),
          P("2) Knowledge acquisition: inspection checklists, mechanic practice and local document and import "
            "procedures were converted into questions and rules."),
          P("3) Knowledge representation: production rules (IF-THEN) with severity, explanation and recommendation, "
            "plus derived facts for chaining."),
          P("4) Inference: forward chaining over working memory until a fixed point is reached."),
          P("5) Decision making: a decision tree (equivalent to the priority ladder) turns the findings into one of "
            "four verdicts."),
          P("6) Decision support: red flags, unverified checks, next steps and a PDF report help the buyer decide."),
          P("7) Explanation facility: every fired rule, the chaining trace and the decision path are displayed."),
          P("8) Validation: unit tests, five demo scenarios and UI tests.")]

# 4. Architecture
story += [P("3. System architecture", h1),
          C("USER (Streamlit UI)\n   |  vehicle form + inspection answers (Yes / No / Unknown)\n   v\n"
            "FACTS (dictionary)  <-- build_facts() adds mileage-per-year, age, hybrid flags\n   |\n   v\n"
            "INFERENCE ENGINE (forward chaining)  <-->  KNOWLEDGE BASE (86 IF-THEN rules)\n"
            "   |  pass 1: fire all matching rules, add derived facts\n"
            "   |  pass 2..n: derived facts trigger deeper (combined) rules\n"
            "   |  stop when a pass fires no new rule (fixed point)\n   v\n"
            "ACTIVATED RULES + TRACE  ->  calculate_risk_level()  (severity counts)\n   v\n"
            "DECISION TREE (walk_tree)  =  verdict ladder (generate_final_recommendation)\n   v\n"
            "VERDICT + EXPLANATION + DECISION SUPPORT + PDF REPORT (Streamlit pages)")]

# 5. Files
story += [P("4. File-by-file explanation", h1)]
files = [("app.py", "Entry point. Sets the page config, initialises state, injects the gold theme, renders the current page, then the sidebar."),
         ("theme.py", "Black and gold CSS plus helpers for cards, badges, the stepper and the verdict card."),
         ("pages_ui.py", "One function per page, the navigation callbacks (single-click buttons), state persistence, the decision tree display and the reset confirmation."),
         ("knowledge_base.py", "The 86 rules. Each rule has id, category, IF condition, THEN conclusion, severity, explanation, recommendation and an optional derived fact."),
         ("inference_engine.py", "Separate from the UI. evaluate_rule, run_inference_engine (forward chaining), collect_activated_rules, calculate_risk_level, generate_final_recommendation, and the decision tree (TREE, walk_tree, tree_to_dot)."),
         ("questions.py", "All inspection questions, their category, help text and applicability (manual, automatic, imported)."),
         ("vehicle_data.py", "Common Pakistani makes and models and cities (no prices) and form normalisation."),
         ("report_generator.py", "Builds the evaluation PDF in memory with ReportLab."),
         ("demo_cases.py", "Five scenarios used for the viva demo and the tests."),
         ("tests/", "Unit tests for rules, engine and decision tree, and UI tests with Streamlit AppTest.")]
t = Table([[P(a, small), P(b, small)] for a, b in files], colWidths=[38 * mm, 142 * mm])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, BRONZE), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
story += [t]

# 6. Rule structure
story += [P("5. Rule structure", h1),
          P("A rule is a Python dictionary. The IF part is a condition function built from three lists: facts that "
            "must be Yes, facts that must be No, and derived facts produced by earlier rules. Because a condition "
            "requires an explicit Yes or No, an Unknown answer can never satisfy it."),
          C(inspect.getsource(knowledge_base.C)),
          C('R("ENG_01", "Engine", "Engine oil burning", C(yes=("blue_smoke", "high_oil_consumption")),\n'
            '  "Possible internal engine wear", "High", "<why it fired>", "<recommendation>",\n'
            '  derive="engine_wear_suspected")')]

# 7. Rule table
story += [P(f"6. Full rule table ({len(RULES)} rules; the course minimum is 50)", h1)]
data = [[P("<b>ID</b>", small), P("<b>Category</b>", small), P("<b>Severity</b>", small), P("<b>Type</b>", small), P("<b>Conclusion</b>", small)]]
for r in RULES:
    data.append([P(r["id"], small), P(r["category"], small), P(r["severity"], small), P(r["type"], small), P(r["conclusion"], small)])
t = Table(data, colWidths=[17 * mm, 38 * mm, 20 * mm, 18 * mm, 87 * mm], repeatRows=1)
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, BRONZE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F6EFD2"))]))
story += [t, PageBreak()]

# 8. Forward chaining walkthrough (live example)
case = DEMO_CASES["4. Imported Vitz with red flags"]
vehicle, _, _ = normalize_vehicle({**DEFAULT_FORM, **case["form"]})
res = evaluate(vehicle, case["answers"])
story += [P("7. Forward-chaining engine and worked example", h1),
          C(inspect.getsource(inference_engine.run_inference_engine)),
          P("Worked example: demo case 4 (imported Vitz with red flags). Trace produced by the engine:", h2)]
for tr in res["trace"]:
    extra = f" -> derives {tr['derived']}" if tr["derived"] else ""
    story.append(P(f"Pass {tr['pass']}: {tr['rule_id']} - {tr['conclusion']}{extra}", small))
story.append(P(f"Final verdict: {res['verdict']}. {res['reason']}", body))

# 9. Decision tree
story += [P("8. Decision tree", h1),
          P("After the rules have fired, the severity counts are passed through a decision tree. Each internal node "
            "asks one question; the answer selects the branch; each leaf is one of the four verdicts. The tree is "
            "stored as data (the TREE dictionary), walked by walk_tree() and drawn in the app with Graphviz. A unit "
            "test checks that the tree and the priority ladder agree for every combination of counts."),
          P("Tree nodes (root = N1):", h2)]
for nid, (q, _, yes, no) in TREE.items():
    story.append(P(f"{nid}: {q}   YES -> {yes}   NO -> {no}", small))
story.append(P("Leaves: L_AVOID = Avoid Purchase, L_NEG = Negotiate / Proceed with Caution, "
               "L_INSP = Buy After Inspection, L_GOOD = Good Candidate.", small))
story.append(P("Path taken in the worked example:", h2))
for _, question, answer in res["tree_path"]:
    story.append(P(f"{question} -> {'Yes' if answer else 'No'}", small))
story.append(P(f"Tree result: {res['tree_verdict']}", body))
story.append(C(inspect.getsource(inference_engine.walk_tree)))

# 10. Verdict ladder
story += [P("9. Verdict ladder, Unknown handling and decision support", h1),
          C(inspect.getsource(inference_engine.generate_final_recommendation)),
          P("Unknown answers are never treated as good or bad. Eight key safety and legal checks are tracked; if 3 or "
            "more are Unknown, or fewer than 15 questions are answered, a clean result is downgraded to Buy After "
            "Inspection. Positive findings never offset Critical or High concerns, and a positive finding that is "
            "contradicted by a derived concern (for example odometer doubt) is suppressed."),
          P("Decision support: besides the verdict, the system lists the top red flags, the unverified key checks, a "
            "deduplicated list of recommended next steps ordered by severity, a price-comparison reminder and a "
            "downloadable report. The system supports the decision; the buyer decides.")]

# 11. UI
story += [P("10. User interface", h1),
          P("Streamlit only. A single st.session_state.page decides the page; all buttons use on_click callbacks, so "
            "one click always navigates. Answers are stored in session state and re-seeded into widgets, so they "
            "survive page changes. Back is always bottom-left and the primary action bottom-right. Results, Reasoning "
            "and Report are disabled until the analysis has run. Reset asks for confirmation. Theme: black and gold. "
            "The Reasoning page shows the activated rules, the chaining trace, the decision tree with the path "
            "highlighted, and the ladder."),
          P("Screenshots: insert after deployment (Home, Vehicle Info, Inspection, Results, Reasoning with tree, Report).", small)]

# 12. Tests, deployment, limitations
story += [P("11. Testing", h1),
          P("Run: python -m unittest discover -s tests -v. Tests cover rule counts and fields, every rule firing in "
            "isolation, chaining order, Unknown handling, five demo verdicts, the PDF output, tree-versus-ladder "
            "agreement and the UI flows."),
          P("12. Deployment", h1),
          P("Push the project to GitHub, create a new app on Streamlit Community Cloud pointing at app.py, copy the "
            "public URL here, and open it from a phone on mobile data to confirm it is reachable. Open the link "
            "shortly before the viva because free apps sleep after inactivity."),
          P("13. Limitations and disclaimer", h1),
          P("The system only reasons over the answers it is given, uses simple heuristic thresholds, and does not "
            "know market prices. It provides preliminary guidance and cannot replace a professional mechanic or "
            "legal verification of documents.")]

os.makedirs("docs", exist_ok=True)
SimpleDocTemplate(OUT, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=15 * mm,
                  bottomMargin=15 * mm, title="AurumDrive Code Explanation").build(story)
print("Created", OUT)