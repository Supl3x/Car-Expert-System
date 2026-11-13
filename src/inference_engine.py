"""Inference engine: forward chaining + decision tree + deterministic verdict ladder.

Independent of the UI. Flow:
 facts -> run_inference_engine (repeat passes until no new rule fires)
       -> collect_activated_rules -> calculate_risk_level
       -> generate_final_recommendation (ladder) and walk_tree (decision tree, same logic)
"""
from datetime import datetime

from knowledge_base import RULES
from questions import QUESTIONS, CRITICAL_KEYS, applicable

VERDICT_GOOD = "Good Candidate"
VERDICT_INSPECT = "Buy After Inspection"
VERDICT_NEGOTIATE = "Negotiate / Proceed with Caution"
VERDICT_AVOID = "Avoid Purchase"

VERDICTS = {
    VERDICT_GOOD: "No major concerns identified from the provided information.",
    VERDICT_INSPECT: "Some concerns exist and need professional verification.",
    VERDICT_NEGOTIATE: "Multiple concerns may justify negotiation or reconsideration.",
    VERDICT_AVOID: "Serious safety, documentation or mechanical red flags were identified.",
}
DISCLAIMER = ("AurumDrive gives preliminary guidance only based on the answers you provide. "
              "It cannot replace a professional mechanic's inspection or legal and "
              "registration verification of the vehicle's documents.")

SEVERITIES = ["Critical", "High", "Medium", "Low"]
SEVERITY_RANK = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
MIN_ANSWERED = 15
MAX_PASSES = 10


def build_facts(vehicle, answers):
    """Collect facts: questionnaire answers (applicable ones) plus facts derived from the vehicle form."""
    facts = {q["key"]: answers.get(q["key"], "Unknown") for q in QUESTIONS if applicable(q, vehicle)}
    age = max(0, datetime.now().year - int(vehicle["year"]))
    per_year = vehicle["mileage"] / age if age > 0 else vehicle["mileage"]

    def yn(flag):
        return "Yes" if flag else "No"

    facts["high_mileage_for_age"] = yn(age >= 1 and per_year > 25000)      # simple heuristic
    facts["low_mileage_suspicious"] = yn(age >= 5 and per_year < 4000)     # simple heuristic
    facts["very_old_vehicle"] = yn(age >= 15)
    facts["is_hybrid"] = yn(vehicle["fuel"] == "Hybrid")
    return facts


def evaluate_rule(rule, facts):
    """True if the rule's IF part is satisfied by the current facts."""
    return bool(rule["condition"](facts))


def run_inference_engine(facts):
    """Forward chaining. Each pass fires all newly matching rules, then adds their derived
    facts to working memory. Stops when a pass fires nothing (fixed point)."""
    memory = dict(facts)
    fired, trace, passes = {}, [], 0
    while passes < MAX_PASSES:
        newly = [r for r in RULES if r["id"] not in fired and evaluate_rule(r, memory)]
        if not newly:
            break
        passes += 1
        for r in newly:
            fired[r["id"]] = passes
            trace.append({"pass": passes, "rule_id": r["id"], "conclusion": r["conclusion"],
                          "when": r["condition"].text, "derived": r["derived_fact"]})
        for r in newly:
            if r["derived_fact"]:
                memory[r["derived_fact"]] = True
    return memory, fired, trace, passes


def collect_activated_rules(fired, memory):
    """Split fired rules into active and suppressed (a positive finding contradicted by a derived concern)."""
    active, suppressed = [], []
    for r in RULES:
        if r["id"] not in fired:
            continue
        rec = {k: v for k, v in r.items() if k != "condition"}
        rec["when"] = r["condition"].text
        rec["pass"] = fired[r["id"]]
        if r["suppress_if"] and memory.get(r["suppress_if"]) is True:
            suppressed.append(rec)
        else:
            active.append(rec)
    active.sort(key=lambda r: (-SEVERITY_RANK[r["severity"]], r["id"]))
    return active, suppressed


def calculate_risk_level(active):
    """Count concerns per severity. Positive findings are counted separately and never offset concerns."""
    counts = {s: 0 for s in SEVERITIES}
    counts["Positive"] = 0
    for r in active:
        if r["type"] == "positive":
            counts["Positive"] += 1
        else:
            counts[r["severity"]] += 1
    highest = next((s for s in SEVERITIES if counts[s]), "None")
    return counts, highest


def generate_final_recommendation(counts, unknown_critical, answered):
    """Deterministic priority ladder. The first matching step decides the verdict."""
    crit, high, med = counts["Critical"], counts["High"], counts["Medium"]
    insufficient = len(unknown_critical) >= 3 or answered < MIN_ANSWERED
    steps = [
        ("Any Critical finding -> Avoid Purchase", crit >= 1, VERDICT_AVOID),
        ("2+ High findings, or 1 High with 4+ Medium -> Negotiate / Proceed with Caution",
         high >= 2 or (high == 1 and med >= 4), VERDICT_NEGOTIATE),
        ("Exactly 1 High finding -> Buy After Inspection", high == 1, VERDICT_INSPECT),
        ("4+ Medium findings -> Negotiate / Proceed with Caution", med >= 4, VERDICT_NEGOTIATE),
        ("1-3 Medium findings -> Buy After Inspection", 1 <= med <= 3, VERDICT_INSPECT),
        ("Only Low or no findings -> Good Candidate (Buy After Inspection if information is insufficient)",
         True, VERDICT_INSPECT if insufficient else VERDICT_GOOD),
    ]
    decided = next(i for i, s in enumerate(steps) if s[1])
    verdict = steps[decided][2]
    if decided == 5 and insufficient:
        reason = ("No concerns were found, but too little was checked "
                  f"({answered} answers; {len(unknown_critical)} key safety/legal checks unverified).")
    elif decided == 5:
        reason = "Only minor or no concerns were found in the information provided."
    else:
        reason = f"Findings: {crit} Critical, {high} High, {med} Medium."
    ladder = [{"text": s[0], "matched": s[1], "decisive": i == decided} for i, s in enumerate(steps)]
    return {"verdict": verdict, "reason": reason, "ladder": ladder, "decided_step": decided,
            "insufficient": insufficient}


# ---------------------------------------------------------------- DECISION TREE
# Same decision logic as the ladder, stored as a tree: node -> (question, test, yes-branch, no-branch)
TREE = {
    "N1": ("Any Critical finding?", lambda c: c["crit"] >= 1, "L_AVOID", "N2"),
    "N2": ("2 or more High findings?", lambda c: c["high"] >= 2, "L_NEG", "N3"),
    "N3": ("Exactly 1 High finding?", lambda c: c["high"] == 1, "N3A", "N4"),
    "N3A": ("4 or more Medium findings?", lambda c: c["med"] >= 4, "L_NEG", "L_INSP"),
    "N4": ("4 or more Medium findings?", lambda c: c["med"] >= 4, "L_NEG", "N5"),
    "N5": ("1 to 3 Medium findings?", lambda c: c["med"] >= 1, "L_INSP", "N6"),
    "N6": ("Information insufficient?", lambda c: c["insufficient"], "L_INSP", "L_GOOD"),
}
LEAVES = {"L_AVOID": VERDICT_AVOID, "L_NEG": VERDICT_NEGOTIATE,
          "L_INSP": VERDICT_INSPECT, "L_GOOD": VERDICT_GOOD}
LEAF_COLORS = {"L_AVOID": "#E5484D", "L_NEG": "#F2873A", "L_INSP": "#E8C547", "L_GOOD": "#3DBA7E"}


def walk_tree(ctx):
    """Walk the decision tree from the root. Returns (path, verdict, leaf_id)."""
    node, path = "N1", []
    while node in TREE:
        question, test, yes, no = TREE[node]
        answer = bool(test(ctx))
        path.append((node, question, answer))
        node = yes if answer else no
    return path, LEAVES[node], node


def tree_to_dot(path, leaf_id):
    """Graphviz DOT text for st.graphviz_chart. The path taken is highlighted in gold."""
    taken = {nid: ans for nid, _, ans in path}
    out = ["digraph G {", "rankdir=TB;", 'bgcolor="transparent";',
           'node [fontname="Helvetica", fontsize=11, shape=box, style="filled,rounded", '
           'color="#8C6B1F", fillcolor="#16161C", fontcolor="#F7F3E8"];',
           'edge [color="#8C6B1F", fontcolor="#A9A491", fontname="Helvetica", fontsize=10];']
    for nid, (q, _, yes, no) in TREE.items():
        hit = nid in taken
        fill, font = ("#D4AF37", "#0B0B0F") if hit else ("#16161C", "#F7F3E8")
        out.append(f'{nid} [label="{q}", fillcolor="{fill}", fontcolor="{font}"];')
        for label, target in (("Yes", yes), ("No", no)):
            on_path = hit and ((label == "Yes") == taken[nid])
            style = 'color="#F3E2A9", penwidth=3' if on_path else ""
            out.append(f'{nid} -> {target} [label="{label}" {(", " + style) if style else ""}];')
    for lid, verdict in LEAVES.items():
        color = LEAF_COLORS[lid]
        width = 4 if lid == leaf_id else 1
        out.append(f'{lid} [label="{verdict}", shape=box, fillcolor="{color}", '
                   f'fontcolor="#0B0B0F", penwidth={width}];')
    out.append("}")
    return "\n".join(out)


def evaluate(vehicle, answers):
    """Full pipeline used by the UI, the tests and the PDF builder."""
    facts = build_facts(vehicle, answers)
    memory, fired, trace, passes = run_inference_engine(facts)
    active, suppressed = collect_activated_rules(fired, memory)
    counts, highest = calculate_risk_level(active)

    labels = {q["key"]: q["label"] for q in QUESTIONS}
    unknown_critical = [k for k in CRITICAL_KEYS if facts.get(k) == "Unknown"]
    applicable_keys = [q["key"] for q in QUESTIONS if q["key"] in facts]
    answered = sum(1 for k in applicable_keys if facts[k] != "Unknown")

    rec = generate_final_recommendation(counts, unknown_critical, answered)

    # Decision tree: same inputs as the ladder, stored and displayed as a tree
    ctx = {"crit": counts["Critical"], "high": counts["High"], "med": counts["Medium"],
           "insufficient": rec["insufficient"]}
    tree_path, tree_verdict, tree_leaf = walk_tree(ctx)

    negatives = [r for r in active if r["type"] == "negative"]
    positives = [r for r in active if r["type"] == "positive"]

    steps, seen = [], set()
    for r in negatives:
        if r["recommendation"] not in seen:
            seen.add(r["recommendation"])
            steps.append(r["recommendation"])
    steps += [f"Verify: {labels[k]}" for k in unknown_critical]
    if rec["verdict"] == VERDICT_GOOD:
        steps.append("Even for a good candidate, arrange a final professional inspection "
                     "and verify the documents before paying.")

    return {"facts": facts, "memory": memory, "activated": active, "negatives": negatives,
            "positives": positives, "suppressed": suppressed, "trace": trace, "passes": passes,
            "counts": counts, "highest": highest, "verdict": rec["verdict"], "reason": rec["reason"],
            "ladder": rec["ladder"], "decided_step": rec["decided_step"],
            "insufficient": rec["insufficient"], "unverified": [labels[k] for k in unknown_critical],
            "answered": answered, "total": len(applicable_keys), "next_steps": steps,
            "tree_path": tree_path, "tree_verdict": tree_verdict,
            "tree_dot": tree_to_dot(tree_path, tree_leaf)}