"""AurumDrive entry point. Run with:  streamlit run app.py"""
import streamlit as st

st.set_page_config(page_title="AurumDrive", page_icon="🚗", layout="wide")  # must be first

import pages_ui as ui  # noqa: E402
from theme import inject_css  # noqa: E402

ui.init_state()
inject_css()
ui.render_current_page()   # page first, so the sidebar below sees this run's latest state
ui.render_sidebar()