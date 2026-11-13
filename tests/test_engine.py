import os
import sys
import unittest
from collections import Counter
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_cases import DEMO_CASES
from inference_engine import (build_facts, evaluate, generate_final_recommendation,
                              run_inference_engine, walk_tree)
from knowledge_base import RULES
from questions import CATEGORIES, QUESTIONS
from report_generator import build_report
from vehicle_data import DEFAULT_FORM, normalize_vehicle

MINIMUMS = {"Engine": 10, "Transmission": 7, "Exterior": 7, "Suspension & Brakes": 7, "Tires": 4,
            "Electrical": 5, "Interior": 3, "Maintenance": 5, "Documents & Ownership": 7,
            "Seller & Test Drive": 7}
VEHICLE_FACTS = {"high_mileage_for_age", "low_mileage_suspicious", "very_old_vehicle", "is_hybrid"}
FIELDS = ["id", "category", "description", "condition", "conclusion", "severity", "type",
          "explanation", "recommendation"]


class TestKnowledgeBase(unittest.TestCase):
    def test_rule_count_and_minimums(self):
        self.assertGreaterEqual(len(RULES), 62)
        counts = Counter(r["category"] for r in RULES)
        for cat, minimum in MINIMUMS.items():
            self.assertGreaterEqual(counts[cat], minimum, cat)

    def test_unique_ids_and_fields(self):
        ids = [r["id"] for r in RULES]
        self.assertEqual(len(ids), len(set(ids)))
        for r in RULES:
            for f in FIELDS:
                self.assertTrue(r[f], f"{r['id']} missing {f}")
            self.assertIn(r["severity"], ["Low", "Medium", "High", "Critical"])

    def test_rule_keys_exist(self):
        known = {q["key"] for q in QUESTIONS} | VEHICLE_FACTS
        derived = {r["derived_fact"] for r in RULES if r["derived_fact"]}
        for r in RULES:
            c = r["condition"]
            for k in c.yes + c.no:
                self.assertIn(k, known, f"{r['id']} uses unknown key {k}")
            for d in c.derived:
                self.assertIn(d, derived, f"{r['id']} needs underived fact {d}")

    def test_each_rule_fires_alone_and_not_on_empty(self):
        for r in RULES:
            c = r["condition"]
            facts = {k: "Yes" for k in c.yes}
            facts.update({k: "No" for k in c.no})
            facts.update({d: True for d in c.derived})
            self.assertTrue(c(facts), r["id"])
            self.assertFalse(c({}), f"{r['id']} fires on missing facts")
            self.assertFalse(c({k: "Unknown" for k in c.yes + c.no}), f"{r['id']} fires on Unknown")

    def test_categories_covered_by_questions(self):
        self.assertEqual(set(MINIMUMS), set(CATEGORIES))


class TestEngine(unittest.TestCase):
    def test_forward_chaining_passes(self):
        facts = {"blue_smoke": "Yes", "high_oil_consumption": "Yes", "overheating": "Yes"}
        _, fired, _, passes = run_inference_engine(facts)
        self.assertEqual(fired["ENG_01"], 1)
        self.assertEqual(fired["CMB_01"], 2)   # chained rule fires only after the derived fact exists
        self.assertGreaterEqual(passes, 2)

    def test_unknown_never_creates_findings(self):
        vehicle, _, _ = normalize_vehicle(DEFAULT_FORM)
        res = evaluate(vehicle, {})
        self.assertEqual(sum(res["counts"][s] for s in ("Critical", "High", "Medium", "Low")), 0)
        self.assertTrue(res["unverified"])

    def test_positive_suppressed_by_odometer_doubt(self):
        vehicle, _, _ = normalize_vehicle(DEFAULT_FORM)
        answers = {"service_history_complete": "Yes", "service_receipts": "Yes", "interior_wear_heavy": "Yes"}
        res = evaluate(vehicle, answers)
        self.assertNotIn("MNT_01", [r["id"] for r in res["activated"]])

    def test_demo_verdicts(self):
        for name, case in DEMO_CASES.items():
            vehicle, ok, _ = normalize_vehicle({**DEFAULT_FORM, **case["form"]})
            self.assertTrue(ok, name)
            res = evaluate(vehicle, case["answers"])
            self.assertEqual(res["verdict"], case["expected"], name)

    def test_report_is_pdf(self):
        case = DEMO_CASES["4. Imported Vitz with red flags"]
        vehicle, _, _ = normalize_vehicle({**DEFAULT_FORM, **case["form"]})
        pdf = build_report(vehicle, evaluate(vehicle, case["answers"]))
        self.assertTrue(pdf.startswith(b"%PDF"))

    def test_facts_skip_inapplicable_questions(self):
        vehicle, _, _ = normalize_vehicle(DEFAULT_FORM)   # automatic, not imported
        facts = build_facts(vehicle, {})
        self.assertNotIn("clutch_slipping", facts)
        self.assertNotIn("customs_papers", facts)


class TestDecisionTree(unittest.TestCase):
    def test_tree_matches_ladder(self):
        """The decision tree and the priority ladder must always give the same verdict."""
        for crit, high, med, insufficient in product(range(3), range(4), range(6), [False, True]):
            counts = {"Critical": crit, "High": high, "Medium": med, "Low": 0, "Positive": 0}
            answered = 5 if insufficient else 40
            ladder = generate_final_recommendation(counts, [], answered)["verdict"]
            _, tree_verdict, _ = walk_tree({"crit": crit, "high": high, "med": med,
                                            "insufficient": insufficient})
            self.assertEqual(ladder, tree_verdict, (crit, high, med, insufficient))

    def test_demo_cases_tree_equals_verdict(self):
        for name, case in DEMO_CASES.items():
            vehicle, _, _ = normalize_vehicle({**DEFAULT_FORM, **case["form"]})
            res = evaluate(vehicle, case["answers"])
            self.assertEqual(res["tree_verdict"], res["verdict"], name)
            self.assertTrue(res["tree_path"], name)
            self.assertIn("digraph", res["tree_dot"])


if __name__ == "__main__":
    unittest.main()