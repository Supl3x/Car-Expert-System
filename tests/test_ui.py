import os
import unittest

from streamlit.testing.v1 import AppTest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app.py")

import sys
sys.path.insert(0, ROOT)
from demo_cases import DEMO_CASES  # noqa: E402


def fresh():
    return AppTest.from_file(APP, default_timeout=30).run()


class TestUI(unittest.TestCase):
    def test_app_starts_without_exception(self):
        at = fresh()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state["page"], "Home")

    def test_start_button_navigates_once(self):
        at = fresh()
        at.button(key="home_start").click().run()
        self.assertEqual(at.session_state["page"], "Vehicle Info")
        self.assertEqual(len(at.exception), 0)

    def test_back_button(self):
        at = fresh()
        at.button(key="home_start").click().run()
        at.button(key="veh_back").click().run()
        self.assertEqual(at.session_state["page"], "Home")

    def test_results_gated_before_analysis(self):
        at = fresh()
        self.assertIsNone(at.session_state["result"])
        self.assertTrue(at.button(key="nav_Results").disabled)

    def test_full_demo_flow_for_every_case(self):
        for name, case in DEMO_CASES.items():
            at = fresh()
            at.selectbox(key="demo_choice").select(name).run()
            at.button(key="home_demo").click().run()
            self.assertEqual(at.session_state["page"], "Vehicle Info", name)
            at.button(key="veh_next").click().run()
            self.assertEqual(at.session_state["page"], "Inspection", name)
            at.button(key="insp_next").click().run()
            self.assertEqual(at.session_state["page"], "Results", name)
            self.assertEqual(at.session_state["result"]["verdict"], case["expected"], name)
            self.assertEqual(len(at.exception), 0, name)

    def test_reset_asks_for_confirmation(self):
        at = fresh()
        at.button(key="side_new").click().run()
        self.assertTrue(at.session_state["confirm_reset"])
        at.button(key="side_yes").click().run()
        self.assertEqual(at.session_state["page"], "Home")


if __name__ == "__main__":
    unittest.main()