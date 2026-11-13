"""All Streamlit pages. One render function per page, plus navigation and state helpers."""
import streamlit as st

import theme
from demo_cases import DEMO_CASES
from inference_engine import DISCLAIMER, MIN_ANSWERED, SEVERITIES, VERDICTS, evaluate
from knowledge_base import RULES
from questions import CATEGORIES, OPTIONS, QUESTIONS, applicable
from report_generator import build_report
from vehicle_data import (CITIES, DEFAULT_FORM, FUELS, IMPORTED, MAKES, OTHER,
                          THIS_YEAR, TRANSMISSIONS, normalize_vehicle)

PAGE_ORDER = ["Home", "Vehicle Info", "Inspection", "Results", "Reasoning", "Report", "About / Rules"]
GATED = ("Results", "Reasoning", "Report")


# ------------------------------------------------------------------ state & callbacks
def init_state():
    ss = st.session_state
    ss.setdefault("page", "Home")
    ss.setdefault("form", dict(DEFAULT_FORM))
    ss.setdefault("answers", {})
    ss.setdefault("result", None)
    ss.setdefault("confirm_reset", False)
    ss.vehicle, ss.vehicle_ok, ss.vehicle_errors = normalize_vehicle(ss.form)


def seed(key, value):
    """Widgets that are not rendered lose their state, so re-seed from our own stored data."""
    if key not in st.session_state:
        st.session_state[key] = value


def go(page):
    st.session_state.page = page


def save_answer(key):
    st.session_state.answers[key] = st.session_state[f"q_{key}"]


def reset_section(cat):
    for q in QUESTIONS:
        if q["category"] == cat:
            st.session_state.answers[q["key"]] = "Unknown"
            st.session_state[f"q_{q['key']}"] = "Unknown"


def reset_answers():
    for q in QUESTIONS:
        st.session_state.answers[q["key"]] = "Unknown"
        st.session_state[f"q_{q['key']}"] = "Unknown"
    st.session_state.result = None


def run_analysis():
    ss = st.session_state
    ss.result = evaluate(ss.vehicle, ss.answers)
    ss.page = "Results"


def load_demo():
    ss = st.session_state
    case = DEMO_CASES[ss.demo_choice]
    for k in list(ss.keys()):
        if k.startswith(("q_", "v_")):
            del ss[k]
    ss.form = {**DEFAULT_FORM, **case["form"]}
    ss.answers = dict(case["answers"])
    ss.result = None
    ss.demo_loaded = ss.demo_choice
    ss.page = "Vehicle Info"


def request_reset():
    st.session_state.confirm_reset = True


def cancel_reset():
    st.session_state.confirm_reset = False


def reset_all():
    for k in list(st.session_state.keys()):
        del st.session_state[k]


def page_enabled(page):
    ss = st.session_state
    if page in GATED:
        return ss.result is not None
    if page == "Inspection":
        return ss.vehicle_ok
    return True


# ------------------------------------------------------------------ shared UI pieces
def nav_bar(key, back_to=None, back_label="← Back", next_label=None, next_cb=None,
            next_args=(), next_disabled=False, mid=None):
    """Back on the left, optional middle action, primary action on the right."""
    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if back_to:
            st.button(back_label, key=f"{key}_back", on_click=go, args=(back_to,), use_container_width=True)
    with c2:
        if mid:
            st.button(mid[0], key=f"{key}_mid", on_click=mid[1], use_container_width=True)
    with c3:
        if next_label:
            st.button(next_label, key=f"{key}_next", type="primary", on_click=next_cb or go,
                      args=next_args, disabled=next_disabled, use_container_width=True)


def reset_control(key):
    if st.session_state.get("confirm_reset"):
        st.warning("This clears the vehicle and all answers. Continue?")
        c1, c2 = st.columns(2)
        c1.button("Yes, reset", key=f"{key}_yes", type="primary", on_click=reset_all, use_container_width=True)
        c2.button("Cancel", key=f"{key}_no", on_click=cancel_reset, use_container_width=True)
    else:
        st.button("Start New Evaluation", key=f"{key}_new", on_click=request_reset, use_container_width=True)


def need_result():
    st.warning("Complete the inspection and run the analysis first.")
    target = "Inspection" if st.session_state.vehicle_ok else "Vehicle Info"
    st.button(f"Go to {target}", key="guard_go", type="primary", on_click=go, args=(target,))


# ------------------------------------------------------------------ pages
def page_home():
    st.markdown(
        '<div class="aw-hero"><h1>RecycleDrive</h1>'
        '<div class="tag">The Golden Standard in Used-Car Verdicts</div>'
        '<p>A rule-based expert system for the Pakistani used-car market. Answer a guided '
        'inspection questionnaire and RecycleDrive applies a knowledge base of explicit IF-THEN rules '
        'to give a transparent, explainable verdict before you pay.</p></div>', unsafe_allow_html=True)

    c = st.columns(4)
    c[0].metric("Knowledge-base rules", len(RULES))
    c[1].metric("Diagnostic categories", len(CATEGORIES))
    c[2].metric("Inspection questions", len(QUESTIONS))
    c[3].metric("Verdict levels", len(VERDICTS))

    st.subheader("How RecycleDrive Thinks")
    cols = st.columns(4)
    cards = [("1. Facts", "Your answers are stored as facts. Unknown stays unknown, never good or bad."),
             ("2. Rules", "Every rule is an explicit IF-THEN with a severity and an explanation."),
             ("3. Forward chaining", "Rules fire, add new facts, and trigger deeper rules until nothing new fires."),
             ("4. Decision tree", "The findings walk a decision tree that ends in one of four verdicts.")]
    for col, (t, b) in zip(cols, cards):
        with col:
            theme.card(t, b)

    st.subheader("The four verdicts")
    cols = st.columns(4)
    for col, (name, meaning) in zip(cols, VERDICTS.items()):
        icon, color = theme.VERDICT_STYLE[name]
        with col:
            st.markdown(f'<div class="aw-card" style="border-color:{color}"><h4 style="color:{color}!important">'
                        f'{icon} {name}</h4><p>{meaning}</p></div>', unsafe_allow_html=True)

    st.info(DISCLAIMER)
    st.write("")
    c1, c2, c3 = st.columns([1.2, 2, 1.2])
    with c1:
        st.button("Start Evaluation →", key="home_start", type="primary", on_click=go,
                  args=("Vehicle Info",), use_container_width=True)
        st.button("Browse Knowledge Base", key="home_kb", on_click=go, args=("About / Rules",),
                  use_container_width=True)
    with c2:
        st.selectbox("Viva demo cases", list(DEMO_CASES), key="demo_choice")
        st.caption(f"Expected verdict: {DEMO_CASES[st.session_state.demo_choice]['expected']}")
        st.button("Load Demo Case", key="home_demo", on_click=load_demo, use_container_width=True)


def page_vehicle():
    theme.stepper(0)
    st.title("Vehicle Information")
    ss = st.session_state
    form = ss.form
    if ss.get("demo_loaded"):
        st.info(f"Demo case loaded: {ss.demo_loaded}. Check the details, then continue to the inspection.")

    c1, c2 = st.columns(2)
    with c1:
        makes = list(MAKES) + [OTHER]
        seed("v_make_sel", form["make_sel"] if form["make_sel"] in makes else makes[0])
        form["make_sel"] = st.selectbox("Manufacturer", makes, key="v_make_sel")
        if form["make_sel"] == OTHER:
            seed("v_make_cus", form["make_cus"])
            form["make_cus"] = st.text_input("Type the manufacturer", key="v_make_cus")

        models = MAKES.get(form["make_sel"], []) + [OTHER]
        current = st.session_state.get("v_model_sel", form["model_sel"])
        st.session_state["v_model_sel"] = current if current in models else models[0]
        form["model_sel"] = st.selectbox("Model", models, key="v_model_sel")
        if form["model_sel"] == OTHER:
            seed("v_model_cus", form["model_cus"])
            form["model_cus"] = st.text_input("Type the model", key="v_model_cus")

        seed("v_year", int(form["year"]))
        form["year"] = st.number_input("Manufacturing year", min_value=1980, max_value=THIS_YEAR + 1,
                                       step=1, key="v_year")
        seed("v_mileage", int(form["mileage"]))
        form["mileage"] = st.number_input("Mileage (km)", min_value=0, step=1000, key="v_mileage")
    with c2:
        seed("v_transmission", form["transmission"])
        form["transmission"] = st.selectbox("Transmission", TRANSMISSIONS, key="v_transmission")
        seed("v_fuel", form["fuel"])
        form["fuel"] = st.selectbox("Fuel type", FUELS, key="v_fuel")

        cities = CITIES + [OTHER]
        seed("v_city_sel", form["city_sel"] if form["city_sel"] in cities else cities[0])
        form["city_sel"] = st.selectbox("City of purchase", cities, key="v_city_sel")
        if form["city_sel"] == OTHER:
            seed("v_city_cus", form["city_cus"])
            form["city_cus"] = st.text_input("Type the city", key="v_city_cus")

        seed("v_price", int(form["price"]))
        form["price"] = st.number_input("Asking price (PKR)", min_value=0, step=50000, key="v_price",
                                        help="Only used for a reminder. RecycleDrive never estimates market value.")
        seed("v_imported", form["imported"])
        form["imported"] = st.radio("Is the car imported?", IMPORTED, key="v_imported", horizontal=True,
                                    help="Unlocks the customs and auction-sheet questions.")

    vehicle, ok, errors = normalize_vehicle(form)
    ss.vehicle, ss.vehicle_ok, ss.vehicle_errors = vehicle, ok, errors
    for e in errors:
        st.error(e)
    nav_bar("veh", back_to="Home", next_label="Next: Inspection →", next_args=("Inspection",),
            next_disabled=not ok)


def page_inspection():
    theme.stepper(1)
    st.title("Inspection Questionnaire")
    ss = st.session_state
    v, answers = ss.vehicle, ss.answers
    qs_all = [q for q in QUESTIONS if applicable(q, v)]
    answered = sum(1 for q in qs_all if answers.get(q["key"], "Unknown") != "Unknown")
    st.progress(answered / len(qs_all), text=f"{answered} of {len(qs_all)} questions answered")
    st.caption("Choose Unknown for anything you have not checked. Unknown is never counted as good or bad.")

    tabs = st.tabs(CATEGORIES)
    for cat, tab in zip(CATEGORIES, tabs):
        with tab:
            qs = [q for q in qs_all if q["category"] == cat]
            done = sum(1 for q in qs if answers.get(q["key"], "Unknown") != "Unknown")
            st.caption(f"{cat}: {done}/{len(qs)} answered")
            for q in qs:
                key = f"q_{q['key']}"
                seed(key, answers.get(q["key"], "Unknown"))
                st.radio(q["label"], OPTIONS, key=key, horizontal=True, help=q["help"] or None,
                         on_change=save_answer, args=(q["key"],))
            st.button("Reset this section", key=f"reset_{cat}", on_click=reset_section, args=(cat,))

    if answered < MIN_ANSWERED:
        st.warning(f"Only {answered} questions answered. You can still run the analysis, but the "
                   "verdict will say that information is insufficient.")
    nav_bar("insp", back_to="Vehicle Info", next_label="Run Analysis ⚡", next_cb=run_analysis,
            mid=("Reset all answers", reset_answers))


def page_results():
    theme.stepper(2)
    st.title("Your Verdict")
    ss = st.session_state
    res, v = ss.result, ss.vehicle
    st.caption(f"{v['year']} {v['make']} {v['model']} · {v['mileage']:,} km · {v['transmission']} · "
               f"{v['fuel']} · {v['city']}")
    theme.verdict_card(res["verdict"], res["reason"], VERDICTS[res["verdict"]])

    cols = st.columns(5)
    for col, sev in zip(cols, SEVERITIES + ["Positive"]):
        col.metric(f"{theme.SEV_ICONS[sev]} {sev}", res["counts"][sev])
    st.caption("These are counts of rules that fired, not a probability of the car being defective. "
               "Positive findings never offset Critical or High concerns.")

    st.subheader("Top red flags")
    flags = [r for r in res["negatives"] if r["severity"] in ("Critical", "High")]
    if flags:
        for r in flags:
            color = theme.SEV_COLORS[r["severity"]]
            st.markdown(f'{theme.badge(r["severity"], color)} **{r["conclusion"]}**  \n{r["explanation"]}',
                        unsafe_allow_html=True)
    else:
        st.success("No Critical or High concerns were found in the information provided.")

    if res["unverified"]:
        st.subheader("Unverified key checks")
        st.warning("These were marked Unknown. They are unverified, not assumed bad:\n\n"
                   + "\n".join(f"- {u}" for u in res["unverified"]))

    st.subheader("Recommended next steps")
    for step in res["next_steps"]:
        st.markdown(f"☐ {step}")

    st.info("Price reminder: compare the asking price"
            + (f" (PKR {v['price']:,})" if v["price"] else "")
            + " with several current listings of similar cars. RecycleDrive does not estimate market value.")
    st.caption(DISCLAIMER)
    nav_bar("res", back_to="Inspection", back_label="← Back to Inspection",
            next_label="View Reasoning →", next_args=("Reasoning",))


def page_reasoning():
    theme.stepper(2)
    st.title("Reasoning Explanation")
    res = st.session_state.result

    st.subheader("Activated rules")
    f1, f2 = st.columns(2)
    sev_sel = f1.multiselect("Severity", SEVERITIES, default=SEVERITIES, key="rs_sev")
    cats = sorted({r["category"] for r in res["activated"]})
    cat_sel = f2.multiselect("Category", cats, default=cats, key="rs_cat")
    rows = [{"Rule": r["id"], "Category": r["category"], "Severity": r["severity"], "Type": r["type"],
             "Conclusion": r["conclusion"], "Why it fired": r["explanation"],
             "Recommendation": r["recommendation"], "Pass": r["pass"]}
            for r in res["activated"] if r["severity"] in sev_sel and r["category"] in cat_sel]
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No activated rules match these filters.")
    if res["suppressed"]:
        st.info("Suppressed positive finding(s): " + ", ".join(
            f"{r['id']} ({r['conclusion']})" for r in res["suppressed"])
            + ". A derived concern contradicts them, so they are not counted as reassurance.")

    st.subheader("Forward-chaining trace")
    if not res["trace"]:
        st.write("No rules fired, so there was nothing to chain.")
    for p in range(1, res["passes"] + 1):
        items = [t for t in res["trace"] if t["pass"] == p]
        with st.expander(f"Pass {p}: {len(items)} rule(s) fired", expanded=(p == 1)):
            for t in items:
                derived = f"  → derives **{t['derived']}**" if t["derived"] else ""
                st.markdown(f"`{t['rule_id']}` {t['conclusion']}  \nIF {t['when']}{derived}")
    if res["passes"]:
        st.caption(f"Pass {res['passes'] + 1}: no new rules fired, so the fixed point was reached.")

    st.subheader("Decision tree")
    st.caption("The verdict is reached by walking this tree from the top. "
               "The gold path is the route taken for this car.")
    try:
        st.graphviz_chart(res["tree_dot"], use_container_width=True)
    except Exception:
        st.info("The tree diagram could not be drawn here; the path is listed below.")
    for _, question, answer in res["tree_path"]:
        st.markdown(f"- {question} → **{'Yes' if answer else 'No'}**")
    st.success(f"Decision tree result: {res['tree_verdict']}")

    st.subheader("Why this verdict?")
    for i, step in enumerate(res["ladder"]):
        if step["decisive"]:
            st.success(f"➡ Step {i + 1} decided: {step['text']}")
        elif step["matched"]:
            st.markdown(f"▫ Step {i + 1} also matched but was outranked: {step['text']}")
        else:
            st.markdown(f"▫ Step {i + 1} did not match: {step['text']}")
    nav_bar("rsn", back_to="Results", back_label="← Back to Results",
            next_label="Generate Report →", next_args=("Report",))


def page_report():
    theme.stepper(3)
    st.title("Report")
    ss = st.session_state
    res, v = ss.result, ss.vehicle
    st.markdown("The PDF report contains the vehicle details, verdict, severity summary, all activated rules "
                "with explanations, the forward-chaining trace, next steps and the disclaimer.")
    try:
        pdf = build_report(v, res)
        name = f"RecycleDrive_Report_{v['make']}_{v['model']}".replace(" ", "_")
        st.download_button("Download PDF Report", data=pdf, file_name=f"{name}.pdf",
                           mime="application/pdf", key="rep_download")
    except Exception as exc:  # never show a raw traceback to the user
        st.error(f"The report could not be generated: {exc}")
    st.write("")
    reset_control("rep")
    nav_bar("rep", back_to="Reasoning", back_label="← Back to Reasoning")


def page_about():
    st.title("About RecycleDrive")
    st.markdown(
        "RecycleDrive is a university AI project: a **rule-based expert system** with a knowledge base, an "
        "inference engine using **forward chaining**, a **decision tree** for the final verdict, and an "
        "explanation facility. It uses no machine learning and no external AI services.\n\n"
        "**Limitations:** it only reasons over what you tell it, it does not know market prices, and "
        "its thresholds (for example mileage per year) are simple heuristics.\n\n"
        "**Unknown answers** are never counted as good or bad. Key safety and legal checks left Unknown "
        "are listed as unverified, and too many of them stops a Good Candidate verdict.")
    st.warning(DISCLAIMER)

    st.subheader("Expert system methodology")
    st.markdown(
        "1. **Problem identification:** reduce risk when buying a used car in Pakistan.\n"
        "2. **Knowledge acquisition:** inspection checklists, mechanic practice and local document/import "
        "procedures were turned into questions and rules.\n"
        "3. **Knowledge representation:** production rules (IF-THEN) with severity, explanation and "
        "recommendation, plus derived facts for chaining.\n"
        "4. **Inference:** forward chaining over working memory until a fixed point is reached.\n"
        "5. **Decision making:** a decision tree (and equivalent priority ladder) turns findings into one verdict.\n"
        "6. **Decision support:** red flags, unverified checks, next steps and a PDF report help the buyer decide.\n"
        "7. **Explanation facility:** every fired rule, the chaining trace and the decision path are shown.\n"
        "8. **Validation:** unit tests, five demo scenarios and UI tests.")

    st.subheader("Knowledge base browser")
    c1, c2, c3 = st.columns(3)
    cats = sorted({r["category"] for r in RULES})
    cat = c1.selectbox("Category", ["All"] + cats, key="kb_cat")
    sev = c2.multiselect("Severity", SEVERITIES, default=SEVERITIES, key="kb_sev")
    text = c3.text_input("Search", key="kb_text").lower().strip()
    rows = []
    for r in RULES:
        if cat != "All" and r["category"] != cat:
            continue
        if r["severity"] not in sev:
            continue
        blob = f"{r['id']} {r['description']} {r['conclusion']} {r['condition'].text}".lower()
        if text and text not in blob:
            continue
        rows.append({"ID": r["id"], "Category": r["category"], "Severity": r["severity"], "Type": r["type"],
                     "IF": r["condition"].text, "THEN": r["conclusion"]})
    st.caption(f"Showing {len(rows)} of {len(RULES)} rules")
    st.dataframe(rows, use_container_width=True, hide_index=True)
    nav_bar("abt", back_to="Home", back_label="← Back to Home")


PAGES = {"Home": page_home, "Vehicle Info": page_vehicle, "Inspection": page_inspection,
         "Results": page_results, "Reasoning": page_reasoning, "Report": page_report,
         "About / Rules": page_about}


def render_current_page():
    page = st.session_state.page
    if page not in PAGES or not page_enabled(page):
        if page in GATED:
            need_result()
        else:
            go("Home")
            st.rerun()
        return
    PAGES[page]()


def render_sidebar():
    ss = st.session_state
    with st.sidebar:
        st.markdown(theme.logo_html(), unsafe_allow_html=True)
        for p in PAGE_ORDER:
            enabled = page_enabled(p)
            st.button(("▶ " if p == ss.page else "") + p, key=f"nav_{p}", on_click=go, args=(p,),
                      disabled=not enabled, use_container_width=True,
                      type="primary" if p == ss.page else "secondary",
                      help=None if enabled else "Complete the earlier steps first")
        done = [ss.vehicle_ok, any(v != "Unknown" for v in ss.answers.values()),
                ss.result is not None, ss.page == "Report"]
        st.progress(sum(done) / 4, text="Evaluation progress")
        st.divider()
        reset_control("side")