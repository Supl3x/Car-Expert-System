# RECYCLEDRIVE - COMPREHENSIVE PROJECT DOCUMENTATION

## 🚗 Project Overview

**RecycleDrive: The Golden Standard in Used-Car Verdicts**  
*Tagline: "Know the car before you pay for it."*

RecycleDrive is a rule-based expert system designed to help buyers evaluate second-hand cars in the Pakistani market before making a purchase decision. It provides transparent, explainable verdicts based on explicit IF-THEN rules covering engine condition, transmission, exterior, interior, documentation, and seller behavior. https://recycle-drive.streamlit.app/

---

## 📋 Table of Contents

1. [Academic Requirements Fulfillment](#academic-requirements-fulfillment)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Knowledge Base Design](#knowledge-base-design)
6. [Inference Engine](#inference-engine)
7. [Forward Chaining Mechanism](#forward-chaining-mechanism)
8. [Verdict System](#verdict-system)
9. [User Interface Design](#user-interface-design)
10. [Data Flow](#data-flow)
11. [Installation & Setup](#installation--setup)
12. [Running the Application](#running-the-application)
13. [Testing](#testing)
14. [Deployment](#deployment)
15. [Demo Cases](#demo-cases)
16. [File-by-File Explanation](#file-by-file-explanation)
17. [Rule Categories & Distribution](#rule-categories--distribution)
18. [Example Rules](#example-rules)
19. [Forward Chaining Example](#forward-chaining-example)
20. [Limitations & Disclaimer](#limitations--disclaimer)
21. [Future Enhancements](#future-enhancements)
22. [Viva Preparation](#viva-preparation)

---

## 1. Academic Requirements Fulfillment

### ✅ Requirement Checklist

| Requirement | Status | Evidence |
|-------------|--------|----------|
| **50+ Conditions** | ✅ Met | 86 explicit IF-THEN rules in `knowledge_base.py` |
| **Unique Niche** | ✅ Met | Pakistan-specific used-car evaluation (token tax, ownership transfer, customs papers for imports) |
| **Streamlit UI** | ✅ Met | 100% Streamlit-based interface (`app.py`, `pages_ui.py`, `theme.py`) |
| **Live WAN Deployment** | ✅ Ready | GitHub repo ready, Streamlit Cloud deployment instructions provided |
| **Viva Week 14 Ready** | ✅ Ready | Demo cases, VIVA_PREP.md, architecture diagrams |
| **Submission Package** | ✅ Complete | Code ZIP, PDF documentation, live link placeholder |

**Rule Count Breakdown:**
- Engine: 11 rules
- Transmission: 8 rules
- Exterior: 8 rules
- Suspension & Brakes: 8 rules
- Tires: 5 rules
- Electrical: 6 rules
- Interior: 4 rules
- Maintenance: 5 rules
- Documents & Ownership: 10 rules
- Seller & Test Drive: 8 rules
- Vehicle Context: 4 rules
- Combined Findings (Chained): 9 rules
- **Total: 86 rules**

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RECYCLEDRIVE SYSTEM                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────┐
        │      USER INPUT (Streamlit UI)        │
        │  - Vehicle Information (Make/Model)   │
        │  - Inspection Questionnaire (60+ Qs)  │
        └───────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────┐
        │         FACTS COLLECTION              │
        │  - User Answers (Yes/No/Unknown)      │
        │  - Vehicle Context (Age/Mileage)      │
        │  - Derived Facts (Initially Empty)    │
        └───────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────┐
        │      INFERENCE ENGINE (Forward        │
        │           Chaining Loop)              │
        │                                       │
        │  Pass 1: Evaluate all rules against  │
        │          current facts                │
        │          → Fire matching rules        │
        │          → Add derived facts          │
        │                                       │
        │  Pass 2: Re-evaluate with new facts  │
        │          → Fire chained rules         │
        │          → Add more derived facts     │
        │                                       │
        │  Pass N: Repeat until no new rules   │
        │          fire (Fixed Point Reached)   │
        └───────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────┐
        │    ACTIVATED RULES COLLECTION         │
        │  - Separate by Type (Negative/        │
        │    Positive)                          │
        │  - Count by Severity (Critical/High/  │
        │    Medium/Low)                        │
        │  - Handle Suppressions                │
        └───────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────┐
        │      VERDICT DECISION LADDER          │
        │  1. Critical ≥ 1 → Avoid Purchase     │
        │  2. High ≥ 2 → Negotiate              │
        │  3. High = 1 → Buy After Inspection   │
        │  4. Medium ≥ 4 → Negotiate            │
        │  5. Medium 1-3 → Buy After Inspection │
        │  6. Only Low/None → Good Candidate*   │
        │     (*unless insufficient info)       │
        └───────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────┐
        │         OUTPUT TO USER                │
        │  - Verdict Card (Colored)             │
        │  - Severity Summary                   │
        │  - Top Red Flags                      │
        │  - Unverified Items                   │
        │  - Recommended Next Steps             │
        │  - Forward Chaining Trace             │
        │  - Downloadable PDF Report            │
        └───────────────────────────────────────┘
```

---

## 3. Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | Python | 3.10+ | Core logic and rules |
| **UI Framework** | Streamlit | ≥1.28.0 | Complete web interface |
| **PDF Generation** | ReportLab | ≥4.0.0 | In-memory PDF reports |
| **Testing** | unittest + pytest | Built-in | Unit and UI tests |
| **Version Control** | Git + GitHub | - | Source control and deployment |

### Why These Technologies?

**Python**: 
- Clean, readable syntax ideal for rule-based systems
- Easy to explain in a viva
- Rich standard library

**Streamlit**:
- Rapid UI development (no HTML/CSS/JS required)
- Built-in state management
- Perfect for data apps and dashboards
- Free hosting on Streamlit Community Cloud

**ReportLab**:
- Pure Python PDF generation
- No external dependencies
- In-memory generation (works on ephemeral filesystems)

**No Machine Learning**:
- Requirements specified rule-based expert system
- Transparent, explainable decisions
- Deterministic outcomes
- No training data needed

---

## 4. Project Structure

```
Recycledrive/
│
├── src/                          # Source code directory
│   ├── app.py                    # Entry point, page routing
│   ├── theme.py                  # CSS styling and UI helpers
│   ├── pages_ui.py               # Page rendering functions
│   ├── knowledge_base.py         # 86 IF-THEN rules
│   ├── inference_engine.py       # Forward chaining logic
│   ├── questions.py              # Questionnaire definitions
│   ├── vehicle_data.py           # Pakistani vehicle data
│   ├── report_generator.py       # PDF generation
│   ├── demo_cases.py             # 5 preset test scenarios
│   └── build_docs_pdf.py         # Documentation PDF builder
│
├── tests/                        # Test suite
│   ├── test_engine.py            # Inference engine tests
│   └── test_ui.py                # Streamlit UI tests
│
├── .streamlit/                   # Streamlit configuration
│   └── config.toml               # Theme settings
│
├── docs/                         # Documentation
│   └── (Generated PDFs go here)
│
├── requirements.txt              # Python dependencies
├── .python-version               # Python version pin
├── .gitignore                    # Git exclusions
├── README.md                     # This file
└── VIVA_PREP.md                  # Viva Q&A preparation
```

---

## 5. Knowledge Base Design

### Rule Structure

Every rule is a Python dictionary with the following fields:

```python
{
    "id": "ENG_01",                    # Unique identifier
    "category": "Engine",              # Diagnostic category
    "description": "Engine oil burning", # Short description
    "condition": lambda f: f.get("blue_smoke") == "Yes" and 
                          f.get("high_oil_consumption") == "Yes",
    "conclusion": "Possible internal engine wear",
    "severity": "High",                # Critical/High/Medium/Low
    "type": "negative",                # negative or positive
    "explanation": "Blue smoke together with frequent oil top-ups...",
    "recommendation": "Arrange a professional engine inspection.",
    "derived_fact": "engine_wear_suspected",  # For chaining (optional)
    "suppress_if": None                # Suppression condition (optional)
}
```

### Condition Function Design

```python
# Helper function to build conditions
def C(yes=(), no=(), derived=()):
    """
    Creates a condition function that checks:
    - yes: facts that must be "Yes"
    - no: facts that must be "No"
    - derived: facts that must exist (derived by previous rules)
    """
    yes, no, derived = _t(yes), _t(no), _t(derived)
    
    def cond(f):
        return (all(f.get(k) == "Yes" for k in yes) and
                all(f.get(k) == "No" for k in no) and
                all(f.get(k) is True for k in derived))
    
    cond.text = " AND ".join([...])  # Human-readable description
    return cond
```

### Rule Categories

```
┌────────────────────────────────────────────────────────┐
│ 1. ENGINE (11 rules)                                   │
│    - Smoke conditions, overheating, leaks, knocking   │
│    - Oil consumption, starting issues                  │
├────────────────────────────────────────────────────────┤
│ 2. TRANSMISSION (8 rules)                             │
│    - Slipping, delayed engagement, hard shifting      │
│    - Clutch condition, vibrations, fluid leaks        │
├────────────────────────────────────────────────────────┤
│ 3. EXTERIOR (8 rules)                                 │
│    - Paint inconsistencies, rust, flood indicators    │
│    - Structural repair signs, panel gaps              │
├────────────────────────────────────────────────────────┤
│ 4. SUSPENSION & BRAKES (8 rules)                      │
│    - Brake pulling, soft pedal, warning lights        │
│    - Suspension noise, steering vibration             │
├────────────────────────────────────────────────────────┤
│ 5. TIRES (5 rules)                                    │
│    - Uneven wear, sidewall damage, tread depth        │
│    - Mismatched sizes                                 │
├────────────────────────────────────────────────────────┤
│ 6. ELECTRICAL (6 rules)                               │
│    - Battery warnings, light faults, repeated issues  │
│    - Power windows, indicator problems                │
├────────────────────────────────────────────────────────┤
│ 7. INTERIOR (4 rules)                                 │
│    - Wear vs mileage, damp carpets, airbag light     │
│    - AC condition                                     │
├────────────────────────────────────────────────────────┤
│ 8. MAINTENANCE (5 rules)                              │
│    - Service history, odometer consistency            │
│    - Overdue maintenance, accident history            │
├────────────────────────────────────────────────────────┤
│ 9. DOCUMENTS & OWNERSHIP (10 rules)                   │
│    - Registration papers, number matching             │
│    - Token tax, transfer papers, customs (imported)   │
│    - Auction sheet verification                       │
├────────────────────────────────────────────────────────┤
│ 10. SELLER & TEST DRIVE (8 rules)                     │
│     - Inspection refusal, test drive issues           │
│     - Seller transparency, pressure tactics           │
├────────────────────────────────────────────────────────┤
│ 11. VEHICLE CONTEXT (4 rules)                         │
│     - Age-based concerns, mileage analysis            │
│     - Hybrid battery considerations                   │
├────────────────────────────────────────────────────────┤
│ 12. COMBINED FINDINGS (9 rules - CHAINED)             │
│     - Multi-symptom critical issues                   │
│     - Example: Engine wear + Overheating              │
│     - Example: Flood signs + Electrical faults        │
│     - Example: Unverified docs + Seller avoidance     │
└────────────────────────────────────────────────────────┘
```

---

## 6. Inference Engine

### Core Functions

```python
# 1. Build initial facts
def build_facts(vehicle, answers):
    """
    Combines:
    - User questionnaire answers
    - Vehicle context facts (age, mileage rate)
    Returns: dict of facts
    """

# 2. Evaluate single rule
def evaluate_rule(rule, facts):
    """
    Returns: True if rule's condition is satisfied
    """

# 3. Forward chaining loop
def run_inference_engine(facts):
    """
    Multi-pass inference:
    - Pass 1: Fire all matching rules
    - Pass 2: Fire rules that depend on derived facts
    - Pass N: Continue until fixed point
    Returns: (final_facts, fired_rules, trace, num_passes)
    """

# 4. Collect activated rules
def collect_activated_rules(fired, memory):
    """
    Split into active and suppressed rules
    Returns: (active, suppressed)
    """

# 5. Calculate risk level
def calculate_risk_level(active):
    """
    Count concerns per severity
    Returns: (counts_dict, highest_severity)
    """

# 6. Generate verdict
def generate_final_recommendation(counts, unknown_critical, answered):
    """
    Apply deterministic verdict ladder
    Returns: verdict_dict with reason and ladder
    """

# 7. Main evaluation pipeline
def evaluate(vehicle, answers):
    """
    Complete pipeline orchestration
    Returns: comprehensive result dict
    """
```

---

## 7. Forward Chaining Mechanism

### Algorithm Pseudocode

```
FUNCTION run_inference_engine(initial_facts):
    working_memory ← initial_facts
    fired_rules ← empty set
    trace ← empty list
    pass_number ← 0
    
    LOOP:
        pass_number ← pass_number + 1
        newly_fired ← empty list
        
        FOR EACH rule IN knowledge_base:
            IF rule NOT IN fired_rules:
                IF evaluate_rule(rule, working_memory):
                    newly_fired.append(rule)
                    fired_rules.add(rule)
                    trace.append({
                        pass: pass_number,
                        rule_id: rule.id,
                        conclusion: rule.conclusion
                    })
                    
                    IF rule.derived_fact IS NOT NULL:
                        working_memory[rule.derived_fact] ← True
        
        IF newly_fired IS EMPTY:
            BREAK  # Fixed point reached
        
        IF pass_number > MAX_PASSES:
            BREAK  # Safety limit
    
    RETURN (working_memory, fired_rules, trace, pass_number)
```

### Multi-Pass Example

```
INITIAL FACTS:
├─ blue_smoke: Yes
├─ high_oil_consumption: Yes
└─ overheating: Yes

PASS 1: Direct Rule Matching
├─ ENG_01 fires: blue_smoke=Yes AND high_oil_consumption=Yes
│   → Conclusion: "Possible internal engine wear"
│   → Derives: engine_wear_suspected = True
│
└─ ENG_03 fires: overheating=Yes
    → Conclusion: "Cooling system problem"
    → Derives: (none)

PASS 2: Chained Rule Matching
└─ CMB_01 fires: engine_wear_suspected=True AND overheating=Yes
    → Conclusion: "Probable major engine problem"
    → Severity: CRITICAL
    → Derives: (none)

PASS 3: No new rules match
└─ FIXED POINT REACHED

FINAL VERDICT: Avoid Purchase (Critical finding)
```

### Why Forward Chaining?

**Advantages for this system:**
1. **Exhaustive**: Evaluates ALL facts, discovers all problems
2. **Natural fit**: Data-driven (we have many facts from inspection)
3. **Chaining**: Allows complex multi-symptom diagnosis
4. **Explainable**: Clear trace of what fired and why
5. **Efficient**: Usually reaches fixed point in 2-3 passes

**Comparison with Backward Chaining:**
- Backward: Goal-driven, works backward from hypothesis
- Forward: Data-driven, works forward from facts
- Our case: We don't start with a hypothesis, we gather facts and discover problems → Forward chaining is appropriate

---

## 8. Verdict System

### Deterministic Priority Ladder

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Check for Critical findings                    │
│ IF Critical ≥ 1                                         │
│ THEN Verdict = "Avoid Purchase"                        │
│ ELSE continue ↓                                         │
├─────────────────────────────────────────────────────────┤
│ STEP 2: Check for multiple High findings               │
│ IF High ≥ 2 OR (High = 1 AND Medium ≥ 4)              │
│ THEN Verdict = "Negotiate / Proceed with Caution"     │
│ ELSE continue ↓                                         │
├─────────────────────────────────────────────────────────┤
│ STEP 3: Check for single High finding                  │
│ IF High = 1                                             │
│ THEN Verdict = "Buy After Inspection"                  │
│ ELSE continue ↓                                         │
├─────────────────────────────────────────────────────────┤
│ STEP 4: Check for many Medium findings                 │
│ IF Medium ≥ 4                                           │
│ THEN Verdict = "Negotiate / Proceed with Caution"     │
│ ELSE continue ↓                                         │
├─────────────────────────────────────────────────────────┤
│ STEP 5: Check for some Medium findings                 │
│ IF Medium = 1-3                                         │
│ THEN Verdict = "Buy After Inspection"                  │
│ ELSE continue ↓                                         │
├─────────────────────────────────────────────────────────┤
│ STEP 6: Check information sufficiency                   │
│ IF (Critical checks unknown ≥ 3) OR (Answered < 15)   │
│ THEN Verdict = "Buy After Inspection"                  │
│      Reason = "Insufficient information"               │
│ ELSE Verdict = "Good Candidate"                        │
└─────────────────────────────────────────────────────────┘
```

### Verdict Meanings

| Verdict | Icon | Meaning |
|---------|------|---------|
| **Good Candidate** | ✅ | No major concerns identified from the provided information |
| **Buy After Inspection** | 🔍 | Some concerns exist and need professional verification |
| **Negotiate / Proceed with Caution** | ⚠️ | Multiple concerns may justify negotiation or reconsideration |
| **Avoid Purchase** | ⛔ | Serious safety, documentation or mechanical red flags identified |

### Unknown Handling

```
PRINCIPLE: Unknown is NEVER assumed bad, NEVER assumed good

IF question_answer = "Unknown":
    ├─ Does NOT fire negative rules (not counted as a concern)
    ├─ Does NOT fire positive rules (not counted as reassurance)
    └─ Tracked separately as "Unverified"

IF critical_unverified_count ≥ 3:
    └─ Prevents "Good Candidate" verdict
    └─ Downgrades to "Buy After Inspection" with reason

CRITICAL CHECKS (must be verified):
- Original registration documents
- Engine number match
- Chassis number match
- Registered owner identity
- Transfer papers ready
- Soft brake pedal (safety)
- Flood indicators
- Coolant in oil (head gasket)
```

---

## 9. User Interface Design

### Page Flow

```
┌──────────────────────────────────────────────────────────┐
│                        HOME                              │
│  • Welcome hero                                          │
│  • System metrics (# rules, categories, questions)       │
│  • How it works explanation                              │
│  • Demo case selector                                    │
│  • [Start Evaluation] [Load Demo] [Browse Rules]        │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                   VEHICLE INFO                           │
│  • Make / Model selectors (Pakistani vehicles)           │
│  • Year, Mileage, Transmission, Fuel                     │
│  • City, Price (optional), Imported status               │
│  • Validation & inline errors                            │
│  • [← Back] ────────────────────── [Next: Inspection →] │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                   INSPECTION                             │
│  • Progress: 37/62 answered                              │
│  • Tabs: Engine | Transmission | Exterior | ...         │
│  • Each Q: Radio (Yes / No / Unknown) + tooltip          │
│  • Questions filter by vehicle (manual/auto, imported)   │
│  • [← Back] [Reset Section] ────── [Run Analysis ⚡]     │
└──────────────────────────────────────────────────────────┘
                        ↓
              (INFERENCE ENGINE RUNS)
                        ↓
┌──────────────────────────────────────────────────────────┐
│                    RESULTS                               │
│  • Large colored verdict card                            │
│  • Severity summary (counts)                             │
│  • Top red flags (Critical/High)                         │
│  • Unverified items list                                 │
│  • Recommended next steps                                │
│  • [← Back to Inspection] ──── [View Reasoning →]       │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                   REASONING                              │
│  • Filterable activated rules table                      │
│  • Forward chaining trace (pass-by-pass)                 │
│  • Verdict ladder explanation                            │
│  • [← Back to Results] ────────── [Generate Report →]   │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                    REPORT                                │
│  • PDF preview description                               │
│  • [Download PDF Report] button                          │
│  • [← Back] [Start New Evaluation]                      │
└──────────────────────────────────────────────────────────┘

                   (PARALLEL ACCESS)
                        ↓
┌──────────────────────────────────────────────────────────┐
│                  ABOUT / RULES                           │
│  • Project explanation                                   │
│  • Limitations & disclaimer                              │
│  • Searchable rule browser (all 86 rules)                │
│  • [← Back to Home]                                      │
└──────────────────────────────────────────────────────────┘
```

---

## 10. Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (for cloning)

### Step 1: Clone Repository

```bash
git clone https://github.com/Supl3x/Car-Expert-System.git
cd Car-Expert-System
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Execution Policy Error (Windows)?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import streamlit; print(f'Streamlit {streamlit.__version__}')"
python -c "import reportlab; print('ReportLab OK')"
```

Expected output:
```
Streamlit 1.28.0  (or higher)
ReportLab OK
```

---

## 11. Running the Application

### Local Development

```bash
# From project root (where app.py is located)
streamlit run src/app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open browser to `http://localhost:8501`

---

## 12. Deployment

### Streamlit Community Cloud (Recommended)

#### Prerequisites
- GitHub account
- Project pushed to GitHub repository

#### Step-by-Step Deployment

**1. Prepare Repository**

Ensure these files are in your repo root:
```
✓ src/app.py
✓ requirements.txt
✓ .streamlit/config.toml
```

**2. Go to Streamlit Cloud**

Visit: https://share.streamlit.io

**3. Sign In**

Click "Sign in with GitHub"

**4. Deploy New App**

- Click "New app"
- Select your repository: `Supl3x/Car-Expert-System`
- Branch: `main`
- Main file path: `src/app.py`
- App URL: `recycledrive-car-expert` (or your choice)

**5. Click "Deploy"**

Wait 2-5 minutes for build.

**6. Get Your Live URL**

```
https://recycledrive-car-expert.streamlit.app
```

---

## 13. Demo Cases

### Available Cases

#### 1. Clean Toyota Corolla
```python
Vehicle: 2019 Toyota Corolla, 55k km, Automatic, Petrol, Karachi
Answers: All concerns = No, All positive checks = Yes
Expected: "Good Candidate"
```

#### 2. Suzuki Wagon R with Minor Issues
```python
Vehicle: 2017 Suzuki Wagon R, 90k km, Manual, Petrol, Lahore
Issues: Oil leak, Sidewall damage, AC not cooling
Expected: "Buy After Inspection"
```

#### 3. Honda Civic with Several Concerns
```python
Vehicle: 2015 Honda Civic, 130k km, Automatic, Petrol, Islamabad
Issues: Brake pulling, Transmission slipping, Service history incomplete,
        Major service overdue, Headlight fault
Expected: "Negotiate / Proceed with Caution"
```

#### 4. Imported Vitz with Red Flags
```python
Vehicle: 2014 Toyota Vitz, 40k km, Automatic, Petrol, Karachi, IMPORTED
Issues: Engine number mismatch, Flood indicators, Damp carpets,
        Docs not original, Seller refuses inspection, No customs papers
Expected: "Avoid Purchase"
```

#### 5. Mostly Unknown Answers
```python
Vehicle: 2018 Toyota Corolla, 60k km, Automatic, Petrol, Karachi
Answers: Almost all "Unknown"
Expected: "Buy After Inspection" (insufficient information)
```

---

## 14. Viva Preparation

### Key Questions & Answers

**Q1: What is an expert system?**
**A:** An expert system is an AI program that emulates the decision-making ability of a human expert in a specific domain. It uses a knowledge base (rules) and an inference engine (reasoning logic) to solve problems.

**Q2: Why forward chaining?**
**A:** Forward chaining is data-driven reasoning. We gather many facts upfront (questionnaire) and want to discover ALL problems, not test one hypothesis. It allows multi-symptom diagnosis through chained rules.

**Q3: How many rules?**
**A:** 86 explicit IF-THEN rules across 12 categories, exceeding the 50-condition requirement.

**Q4: How does the verdict work?**
**A:** Deterministic priority ladder: Critical findings → Avoid Purchase. Multiple High findings → Negotiate. Limited Medium findings → Buy After Inspection. Clean → Good Candidate (unless insufficient information).

**Q5: What makes this Pakistan-specific?**
**A:** Token tax verification, registration book/smart card, ownership transfer papers, customs clearance for imported vehicles, auction sheet verification, common Pakistani makes/models.

---

## 15. Live Deployment Link

**GitHub Repository:**  
https://github.com/Supl3x/Car-Expert-System

**Live Streamlit App:**  
https://recycle-drive.streamlit.app/

---

## 16. Limitations & Disclaimer

### What RecycleDrive Does NOT Do

❌ **Estimate market value or fair price**
- Prices vary by trim, condition, location, market demand
- Recommendation: Compare asking price with current listings yourself

❌ **Replace a professional mechanic**
- Always get physical inspection before finalizing purchase

❌ **Guarantee future reliability**
- Cannot predict future breakdowns

### Official Disclaimer

> RecycleDrive gives preliminary guidance only based on the answers you provide. It cannot replace a professional mechanic's inspection or legal and registration verification of the vehicle's documents.

---

## License

This project is created for academic purposes as part of an Artificial Intelligence course.

---

## Contact

For questions or feedback, please open an issue on the GitHub repository.
