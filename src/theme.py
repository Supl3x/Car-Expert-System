"""Black & gold theme: CSS injection and small HTML helpers."""
import streamlit as st

SEV_COLORS = {"Critical": "#E5484D", "High": "#F2873A", "Medium": "#E8C547",
              "Low": "#6CA6E0", "Positive": "#3DBA7E"}
SEV_ICONS = {"Critical": "⛔", "High": "🔶", "Medium": "🟡", "Low": "🔹", "Positive": "✅"}
VERDICT_STYLE = {"Good Candidate": ("✅", "#3DBA7E"),
                 "Buy After Inspection": ("🔍", "#E8C547"),
                 "Negotiate / Proceed with Caution": ("⚠️", "#F2873A"),
                 "Avoid Purchase": ("⛔", "#E5484D")}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap');
html, body, .stApp { font-family: 'Inter', system-ui, sans-serif; }
.stApp { background: #E8E8E8; }
h1, h2, h3, h4 { font-family: 'Playfair Display', Georgia, serif !important; color: #8C6B1F !important; letter-spacing: .3px; }
[data-testid="stSidebar"] { background: #D4D4D4; border-right: 1px solid #8C6B1F; }
label, .stMarkdown, p, span { color: #1a1a1a !important; }
.block-container { padding-top: 2rem; max-width: 1150px; }

/* Buttons */
.stButton > button, .stDownloadButton > button {
  border-radius: 10px; font-weight: 600; border: 1px solid #8C6B1F; transition: all .15s ease; }
.stButton > button[kind="secondary"], .stButton > button[data-testid="stBaseButton-secondary"] {
  background: white; color: #8C6B1F; }
.stButton > button[kind="secondary"] p, .stButton > button[data-testid="stBaseButton-secondary"] p { color: #8C6B1F; }
.stButton > button[kind="secondary"]:hover, .stButton > button[data-testid="stBaseButton-secondary"]:hover {
  background: #F5F5F5; box-shadow: 0 0 14px rgba(140,107,31,.35); }
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"], .stDownloadButton > button {
  background: linear-gradient(135deg, #D4AF37, #F3E2A9); color: #0B0B0F; border: none; }
.stButton > button[kind="primary"] p, .stButton > button[data-testid="stBaseButton-primary"] p,
.stDownloadButton > button p { color: #0B0B0F !important; }
.stButton > button[kind="primary"]:hover, .stButton > button[data-testid="stBaseButton-primary"]:hover,
.stDownloadButton > button:hover { box-shadow: 0 0 18px rgba(212,175,55,.55); transform: translateY(-1px); }
.stButton > button:disabled { opacity: .4; }

/* Tabs */
.stTabs [data-baseweb="tab"] { color: #4a4a4a; }
.stTabs [aria-selected="true"] { color: #8C6B1F !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #8C6B1F; }

/* Cards and badges */
.aw-card { background: white; border: 1px solid #C0C0C0; border-radius: 14px; padding: 18px 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,.1); height: 100%; }
.aw-card h4 { margin: 0 0 6px 0; color: #2a2a2a !important; }
.aw-card p { color: #4a4a4a; margin: 0; font-size: .93rem; }
.aw-badge { display: inline-block; border: 1px solid; border-radius: 999px; padding: 2px 10px;
  font-size: .78rem; font-weight: 600; margin-right: 6px; }
.aw-hero { background: linear-gradient(135deg, #F5F5F5 0%, #FFFFFF 100%); border: 1px solid #C0C0C0;
  border-radius: 18px; padding: 34px 36px; margin-bottom: 18px; }
.aw-hero h1 { margin: 0; font-size: 2.6rem; color: #8C6B1F !important; }
.aw-hero .tag { color: #8C6B1F; font-style: italic; margin: 4px 0 12px 0; }
.aw-hero p { color: #2a2a2a; max-width: 760px; }
.aw-logo { font-family: 'Playfair Display', Georgia, serif; font-size: 1.7rem; font-weight: 700; letter-spacing: 2px; }
.aw-logo b { color: #D4AF37; } .aw-logo span { color: #2a2a2a; }
.aw-sub { color: #5a5a5a; font-size: .8rem; margin-bottom: 10px; }

/* Stepper */
.aw-stepper { display: flex; gap: 10px; margin: 6px 0 18px 0; flex-wrap: wrap; }
.aw-step { flex: 1; min-width: 110px; text-align: center; padding: 8px 6px; border-radius: 10px;
  border: 1px solid #C0C0C0; color: #5a5a5a; font-size: .85rem; background: white; }
.aw-step .aw-dot { display: inline-block; width: 22px; height: 22px; line-height: 22px; border-radius: 50%;
  background: #E0E0E0; margin-right: 6px; font-size: .75rem; color: #5a5a5a; }
.aw-step.active { border-color: #8C6B1F; color: #8C6B1F; background: #FFFEF8; }
.aw-step.active .aw-dot { background: #8C6B1F; color: white; }
.aw-step.done { color: #2a2a2a; border-color: #A0A0A0; }
.aw-step.done .aw-dot { background: #A0A0A0; color: white; }

/* Verdict */
.aw-verdict { display: flex; gap: 20px; align-items: center; background: white; border: 2px solid;
  border-radius: 18px; padding: 24px 28px; margin: 8px 0 18px 0; }
.aw-verdict-icon { font-size: 3.2rem; }
.aw-verdict-label { color: #5a5a5a; font-size: .75rem; letter-spacing: 3px; }
.aw-verdict-name { font-family: 'Playfair Display', Georgia, serif; font-size: 2rem; font-weight: 700; }
.aw-verdict-text { color: #2a2a2a; }
.aw-verdict-reason { color: #5a5a5a; font-size: .9rem; margin-top: 4px; }
@media (max-width: 640px) { .aw-hero { padding: 22px; } .aw-hero h1 { font-size: 1.9rem; }
  .aw-verdict { flex-direction: column; text-align: center; } }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def logo_html():
    return ('<div class="aw-logo"><b>Recycle</b><span>DRIVE</span> 🚗</div>'
            '<div class="aw-sub">Know the car before you pay for it.</div>')


def badge(text, color):
    return f'<span class="aw-badge" style="border-color:{color};color:{color}">{text}</span>'


def card(title, body):
    st.markdown(f'<div class="aw-card"><h4>{title}</h4><p>{body}</p></div>', unsafe_allow_html=True)


def stepper(active):
    steps = ["Vehicle", "Inspection", "Verdict", "Report"]
    html = '<div class="aw-stepper">'
    for i, name in enumerate(steps):
        cls = "done" if i < active else ("active" if i == active else "")
        mark = "✓" if i < active else str(i + 1)
        html += f'<div class="aw-step {cls}"><span class="aw-dot">{mark}</span>{name}</div>'
    st.markdown(html + "</div>", unsafe_allow_html=True)


def verdict_card(verdict, reason, meaning):
    icon, color = VERDICT_STYLE[verdict]
    st.markdown(
        f'<div class="aw-verdict" style="border-color:{color};box-shadow:0 0 28px {color}33">'
        f'<div class="aw-verdict-icon">{icon}</div><div>'
        f'<div class="aw-verdict-label">VERDICT</div>'
        f'<div class="aw-verdict-name" style="color:{color}">{verdict}</div>'
        f'<div class="aw-verdict-text">{meaning}</div>'
        f'<div class="aw-verdict-reason">{reason}</div></div></div>',
        unsafe_allow_html=True)