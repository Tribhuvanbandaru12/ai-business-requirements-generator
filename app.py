from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

import database
import prompts
import mock_data
from utils import combine_export_bundle, make_title, parse_markdown_sections, validate_notes

load_dotenv()
database.init_db()

APP_NAME = "AI Business Requirements Generator"
APP_TAGLINE = "Turn messy stakeholder notes into structured BA documentation."
SAMPLE_DIR = Path(__file__).with_name("sample_inputs")

st.set_page_config(page_title=APP_NAME, page_icon="BA", layout="wide")

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* ============================================================
   BASE: Light canvas, dark text, Outfit font
   ============================================================ */
html, body, .stApp {
    font-family: 'Outfit', sans-serif !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

h1, h2, h3, h4, h5, h6, label, .stMarkdown h1,
.stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    font-family: 'Outfit', sans-serif !important;
    color: #0F172A !important;
}
p, span, li, table, td, th, div {
    font-family: 'Outfit', sans-serif !important;
    color: #1E293B !important;
}
/* Override any dark-mode colour leaks on markdown paragraphs */
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {
    color: #1E293B !important;
}

/* ============================================================
   SIDEBAR  — pure white with green accent
   ============================================================ */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 2px solid #E2E8F0 !important;
}
section[data-testid="stSidebar"] * {
    color: #1E293B !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #0F172A !important;
    font-weight: 700 !important;
}

/* Mode badges inside sidebar */
.mode-badge-demo {
    display: inline-block;
    background: #FEF3C7;
    color: #92400E;
    border: 1px solid #FDE68A;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 4px;
}
.mode-badge-gemini {
    display: inline-block;
    background: #D1FAE5;
    color: #065F46;
    border: 1px solid #A7F3D0;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 4px;
}

/* ============================================================
   HEADER BAR — transparent so canvas colour shows
   ============================================================ */
header[data-testid="stHeader"] {
    background-color: transparent !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ============================================================
   HERO TITLE
   ============================================================ */
.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0F172A 0%, #10B981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.1rem;
    letter-spacing: -0.05rem;
    line-height: 1.15;
}
.subtitle {
    font-size: 1.1rem;
    color: #475569 !important;
    margin-bottom: 1.5rem;
    font-weight: 300;
}

/* ============================================================
   FLOWCHART (concept diagram)
   ============================================================ */
.flowchart-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #FFFFFF;
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 14px;
    padding: 14px 20px;
    margin: 15px 0 25px 0;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
}
.flowchart-node {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 10px;
    text-align: center;
    cursor: help;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.flowchart-node:hover {
    transform: translateY(-3px);
    border-color: #10B981;
    box-shadow: 0 6px 18px rgba(16, 185, 129, 0.18);
    background: #DCFCE7;
}
.node-icon  { font-size: 1.4rem; margin-bottom: 4px; }
.node-label { font-size: 0.88rem; font-weight: 600; color: #0F172A !important; }
.node-desc  { font-size: 0.75rem; color: #475569 !important; margin-top: 2px; }
.flowchart-arrow {
    font-size: 1.1rem;
    color: #10B981 !important;
    margin: 0 10px;
    font-weight: bold;
    user-select: none;
    animation: pulseArrow 2s infinite ease-in-out;
}

@keyframes pulseArrow {
    0%, 100% { opacity: 0.4; transform: translateX(0); }
    50%       { opacity: 0.9; transform: translateX(4px); }
}

/* ============================================================
   STEP BADGES  (Step 1, Step 2 …)
   ============================================================ */
.step-container {
    display: flex;
    align-items: center;
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 10px;
    padding: 8px 14px;
    margin: 16px 0 12px 0;
}
.step-number {
    background: linear-gradient(135deg, #10B981, #059669);
    color: #FFFFFF !important;
    font-weight: 700;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.step-title { font-size: 1rem; font-weight: 600; color: #0F172A !important; }

/* ============================================================
   LEARNING BOX
   ============================================================ */
.learning-box {
    background: #FFFFFF;
    border-left: 3px solid #10B981;
    border-top: 1px solid #E2E8F0;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 12px 14px;
    margin: 8px 0 14px 0;
    color: #334155 !important;
}
.learning-box strong, .learning-box b { color: #0F172A !important; }

/* ============================================================
   STATUS CHIPS
   ============================================================ */
.small-muted { color: #475569 !important; font-size: 0.88rem; }
.success-chip {
    display: inline-block;
    background: rgba(16, 185, 129, 0.12);
    color: #065F46 !important;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}
.warning-chip {
    display: inline-block;
    background: rgba(245, 158, 11, 0.12);
    color: #92400E !important;
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ============================================================
   EXPORT CARDS  (light theme — was broken dark-mode remnant)
   ============================================================ */
.export-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}
.export-card h5 {
    color: #0F172A !important;
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 6px 0;
}
.export-card p {
    color: #475569 !important;
    font-size: 0.85rem;
    margin: 0;
}

/* ============================================================
   FORM INPUTS & TEXTAREA
   ============================================================ */
textarea, input[type="text"], input[type="password"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}
textarea:focus, input:focus {
    border-color: #10B981 !important;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15) !important;
}

/* Fix placeholder text colour */
textarea::placeholder, input::placeholder {
    color: #94A3B8 !important;
}

/* ============================================================
   SELECTBOX / SLIDER LABELS
   ============================================================ */
.stSelectbox label, .stSlider label, .stRadio label,
.stTextInput label, .stTextArea label {
    color: #0F172A !important;
    font-weight: 500 !important;
}

/* ============================================================
   SELECTBOX DROPDOWN — force light theme
   (Streamlit defaults to dark navy; override everything here)
   ============================================================ */
/* The visible select box container */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    color: #0F172A !important;
}
/* The displayed selected value text */
div[data-baseweb="select"] span,
div[data-baseweb="select"] [data-testid="stMarkdownContainer"] {
    color: #0F172A !important;
}
/* The dropdown popover/listbox */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.10) !important;
}
/* Each option item */
li[data-baseweb="menu-item"],
li[role="option"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
li[data-baseweb="menu-item"]:hover,
li[role="option"]:hover {
    background-color: #F0FDF4 !important;
    color: #059669 !important;
}
/* Chevron / arrow icon colour */
div[data-baseweb="select"] svg {
    fill: #64748B !important;
}
/* Focus ring */
div[data-baseweb="select"] > div:focus-within {
    border-color: #10B981 !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.15) !important;
}

/* Slider track and thumb */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #10B981 !important;
    border-color: #059669 !important;
}
.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrackFill"] {
    background-color: #10B981 !important;
}

/* ============================================================
   TABS
   ============================================================ */
button[data-baseweb="tab"] {
    color: #64748B !important;
    font-weight: 500 !important;
    background: transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #059669 !important;
    border-bottom: 3px solid #10B981 !important;
    font-weight: 700 !important;
    background: transparent !important;
}

/* ============================================================
   BUTTONS — primary: green gradient, secondary: ghost
   ============================================================ */
.stButton > button {
    background: linear-gradient(135deg, #10B981, #059669) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 9px 22px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25) !important;
    transition: all 0.22s ease !important;
    letter-spacing: 0.01em;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(16, 185, 129, 0.35) !important;
}

div.stButton button[data-testid="stBaseButton-secondary"] {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #CBD5E1 !important;
    box-shadow: none !important;
}
div.stButton button[data-testid="stBaseButton-secondary"]:hover {
    background: #F0FDF4 !important;
    border-color: #10B981 !important;
    color: #059669 !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #059669 !important;
    border: 1.5px solid #10B981 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(16,185,129,0.1) !important;
    transition: all 0.22s ease !important;
}
.stDownloadButton > button:hover {
    background: #F0FDF4 !important;
    box-shadow: 0 4px 14px rgba(16,185,129,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ============================================================
   STREAMLIT NATIVE INFO / WARNING / ERROR BOXES
   ============================================================ */
.stAlert [data-testid="stMarkdownContainer"] p {
    color: inherit !important;
}

/* ============================================================
   EXPANDERS — Modern Streamlit uses details/summary elements
   ============================================================ */
/* The old class (kept for backward compat) */
.streamlit-expanderHeader {
    color: #0F172A !important;
    font-weight: 600 !important;
    background: #F8FAFC !important;
    border-radius: 8px !important;
    border: 1px solid #E2E8F0 !important;
}
.streamlit-expanderContent {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-top: none !important;
    color: #334155 !important;
}

/* Modern Streamlit expander (details + summary) */
[data-testid="stExpander"] details {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    overflow: hidden;
}
[data-testid="stExpander"] details summary {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
    border-radius: 10px !important;
    cursor: pointer;
    list-style: none !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px;
}
[data-testid="stExpander"] details summary:hover {
    background-color: #F0FDF4 !important;
    color: #059669 !important;
}
[data-testid="stExpander"] details summary span {
    color: #0F172A !important;
}
[data-testid="stExpander"] details summary:hover span {
    color: #059669 !important;
}
/* Hide the internal Streamlit arrow/caret text artefacts */
[data-testid="stExpander"] details summary svg {
    fill: #64748B !important;
    width: 16px;
    height: 16px;
}
[data-testid="stExpander"] details[open] summary {
    border-bottom: 1px solid #E2E8F0 !important;
    border-bottom-left-radius: 0 !important;
    border-bottom-right-radius: 0 !important;
}
[data-testid="stExpander"] details .stExpanderDetails {
    background-color: #FFFFFF !important;
    padding: 14px 16px !important;
    color: #334155 !important;
}

/* ============================================================
   DEMO-MODE BANNER
   ============================================================ */
.demo-banner {
    display: flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    border: 1px solid #F59E0B;
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 16px;
    color: #78350F !important;
    font-weight: 500;
    font-size: 0.95rem;
}
.demo-banner strong { color: #78350F !important; }
.demo-banner a { color: #059669 !important; font-weight: 600; text-decoration: underline; }

/* ============================================================
   ANIMATIONS
   ============================================================ */
.fade-in {
    animation: fadeIn 0.45s ease-out forwards;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ============================================================
   MISC — remove Streamlit branding footer visual clutter
   ============================================================ */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def get_api_key() -> str:
    session_key = st.session_state.get("gemini_api_key", "")
    env_key = os.environ.get("GEMINI_API_KEY", "")
    return session_key or env_key


def call_gemini(prompt_text: str, api_key: str, system_instruction: str | None = None, temperature: float = 0.2) -> str:
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(temperature=temperature)
    if system_instruction:
        config.system_instruction = system_instruction
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_text,
        config=config,
    )
    return response.text or "No response generated."


def show_learning_box(topic: str) -> None:
    item = prompts.LEARNING_EXPLANATIONS.get(topic)
    if not item:
        return
    st.markdown(
        f"""
        <div class='learning-box'>
        <strong>Learning note</strong><br>
        <b>What:</b> {item['what']}<br>
        <b>Why:</b> {item['why']}<br>
        <b>Analyst value:</b> {item['analyst_value']}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_step_title(number: int, title: str) -> None:
    st.markdown(
        f"""
        <div class='step-container'>
            <div class='step-number'>{number}</div>
            <div class='step-title'>{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def initialize_state() -> None:
    api_key_available = bool(os.environ.get("GEMINI_API_KEY", "") or st.session_state.get("gemini_api_key", ""))
    defaults = {
        "notes_input": "",
        "generated_doc": "",
        "rtm_doc": "",
        "jira_doc": "",
        "quality_review": "",
        "executive_summary": "",
        "current_record_id": None,
        "selected_domain": "Customer Operations",
        "output_depth": "Detailed",
        "app_mode": "gemini" if api_key_available else "demo",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def load_sample_file(filename: str) -> None:
    sample_path = SAMPLE_DIR / filename
    if sample_path.exists():
        st.session_state.notes_input = sample_path.read_text(encoding="utf-8")


def reset_workspace() -> None:
    for key in ["generated_doc", "rtm_doc", "jira_doc", "quality_review", "executive_summary"]:
        st.session_state[key] = ""
    st.session_state.current_record_id = None


def render_header() -> None:
    st.markdown(f"<div class='main-title'>{APP_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{APP_TAGLINE}</div>", unsafe_allow_html=True)
    
    # Render the interactive conceptual flowchart
    st.markdown(
        """
        <div class='flowchart-container fade-in'>
          <div class='flowchart-node' title='Raw, unorganized stakeholder conversations, emails, meeting transcripts, or requirements checklists.'>
            <div class='node-icon'>💬</div>
            <div class='node-label'>1. Stakeholder Notes</div>
            <div class='node-desc'>Unstructured Input</div>
          </div>
          <div class='flowchart-arrow'>➔</div>
          <div class='flowchart-node' title='A formal Business Requirements Document outlining business case, system scope, personas, and test scenarios.'>
            <div class='node-icon'>📄</div>
            <div class='node-label'>2. BRD Specification</div>
            <div class='node-desc'>Structured System Rules</div>
          </div>
          <div class='flowchart-arrow'>➔</div>
          <div class='flowchart-node' title='A Traceability Matrix mapping BRs to functional specs and UAT tests, combined with Jira-ready user stories.'>
            <div class='node-icon'>🔄</div>
            <div class='node-label'>3. Traceability & Backlog</div>
            <div class='node-desc'>Developer & QA Ready</div>
          </div>
          <div class='flowchart-arrow'>➔</div>
          <div class='flowchart-node' title='An automated Quality Gate Review analyzing completeness, clarity, testability, and potential risk mitigation.'>
            <div class='node-icon'>🔍</div>
            <div class='node-label'>4. Quality Review</div>
            <div class='node-desc'>Analyst Validation Gate</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page",
        ["Generator", "Saved History", "Learning Guide", "Project Info"],
    )

    st.sidebar.divider()
    st.sidebar.subheader("App Mode")
    
    current_mode = st.session_state.get("app_mode", "demo")
    default_mode_index = 0 if current_mode == "demo" else 1
    
    mode = st.sidebar.radio(
        "Select Mode",
        ["Demo Mode (No API key)", "Gemini Mode (Requires API key)"],
        index=default_mode_index,
        help="Demo Mode returns simulated BA documents immediately. Gemini Mode connects to Gemini using your API key."
    )
    
    new_mode = "demo" if "Demo Mode" in mode else "gemini"
    if new_mode != current_mode:
        st.session_state["app_mode"] = new_mode
        st.rerun()

    st.sidebar.divider()
    # Only show Gemini API Setup input if we are in Gemini Mode
    if st.session_state.get("app_mode") == "gemini":
        st.sidebar.subheader("Gemini API Setup")
        key = get_api_key()
        typed_key = st.sidebar.text_input(
            "Gemini API key",
            value=key,
            type="password",
            placeholder="Paste your Gemini API key",
            help="For learning, sidebar entry is fine. For GitHub, never commit your key.",
        )
        if typed_key != st.session_state.get("gemini_api_key", ""):
            st.session_state["gemini_api_key"] = typed_key
            st.rerun()

    st.sidebar.divider()
    if st.sidebar.button("Clear workspace"):
        st.session_state.notes_input = ""
        reset_workspace()
        st.rerun()

    return page


def render_generator(api_key: str) -> None:
    render_header()
    st.divider()

    # Show info banner if Demo Mode is active
    if st.session_state.get("app_mode", "demo") == "demo":
        st.markdown(
            "<div class='demo-banner fade-in'>"
            "<span style='font-size:1.3rem;'>💡</span>"
            "<span><strong>Demo Mode active</strong> — AI generation is simulated with realistic pre-built documents. "
            "Switch to <strong>Gemini Mode</strong> in the sidebar and paste your API key to generate live, personalised results.</span>"
            "</div>",
            unsafe_allow_html=True,
        )
    
    st.markdown(
        """
        ### Welcome to the BA Workspace!
        This tool translates raw, messy notes from meetings or emails into structured analyst deliverables.
        Follow the steps below to capture notes, configure your document settings, and explore the generated analyst pack.
        """
    )

    # Quick Start helper for new users if they haven't loaded notes yet
    if not st.session_state.notes_input:
        st.markdown("#### 🚀 Quick Start: Try a Sample")
        st.write("Don't have stakeholder notes ready? Click one of the buttons below to load an example process and see how the app works:")
        col_sample1, col_sample2 = st.columns(2)
        with col_sample1:
            if st.button("Load Refund Process Sample", use_container_width=True, type="primary", help="Loads a customer service complaint process about delayed refunds."):
                load_sample_file("refund_process_notes.txt")
                reset_workspace()
                st.rerun()
        with col_sample2:
            if st.button("Load Onboarding Process Sample", use_container_width=True, type="primary", help="Loads a sales-to-operations customer onboarding process."):
                load_sample_file("customer_onboarding_notes.txt")
                reset_workspace()
                st.rerun()
        st.divider()

    # Layout: Step 1 and Step 2 on the left, Step 3 on the right if generated doc exists
    if st.session_state.generated_doc:
        left, right = st.columns([0.43, 0.57], gap="large")
    else:
        left = st.container()

    with left:
        # Step 1
        render_step_title(1, "Input Stakeholder Notes")
        show_learning_box("input")
        notes = st.text_area(
            "Paste raw meeting notes, stakeholder emails, or business problem description here",
            value=st.session_state.notes_input,
            height=280,
            placeholder="Example: The customer service team is receiving complaints because refunds are delayed...",
            help="Aim for a few sentences detailing the current problems, the departments involved, and what stakeholders want."
        )
        st.session_state.notes_input = notes

        valid, validation_message = validate_notes(notes)
        if notes:
            if valid:
                st.markdown(f"<span class='success-chip'>✓ {validation_message}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span class='warning-chip'>⚠️ {validation_message}</span>", unsafe_allow_html=True)

        # Step 2
        st.write("")
        render_step_title(2, "Configure & Generate")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.session_state.selected_domain = st.selectbox(
                "Target Business Domain",
                [
                    "Customer Operations",
                    "Sales Operations",
                    "Finance Process",
                    "HR / Onboarding",
                    "IT / Systems Change",
                    "General Business Process",
                ],
                index=[
                    "Customer Operations",
                    "Sales Operations",
                    "Finance Process",
                    "HR / Onboarding",
                    "IT / Systems Change",
                    "General Business Process",
                ].index(st.session_state.selected_domain),
                help="Aligns the prompt vocabulary to fit the industry standard terminology."
            )
        with col_c2:
            st.session_state.output_depth = st.select_slider(
                "Document Detail Level",
                options=["Concise", "Detailed", "Thesis/Portfolio Level"],
                value=st.session_state.output_depth,
                help="Concise gives a direct summary; Detailed includes full requirements; Portfolio includes advanced scenarios."
            )

        st.write("")
        generate = st.button("✨ Generate BA Documentation Pack", type="primary", use_container_width=True)

        if generate:
            if not valid:
                st.warning(validation_message)
            elif st.session_state.get("app_mode", "demo") == "gemini" and not api_key:
                st.error("Please enter your Gemini API key in the sidebar before generating output in Gemini Mode.")
            else:
                try:
                    reset_workspace()
                    with st.spinner("Generating structured BA documentation..."):
                        if st.session_state.get("app_mode", "demo") == "demo":
                            mocks = mock_data.get_mock_deliverables(
                                notes=notes,
                                domain=st.session_state.selected_domain,
                                depth=st.session_state.output_depth,
                            )
                            generated_doc = mocks["brd"]
                            st.session_state.generated_doc = generated_doc
                            record_id = database.save_generation(
                                title=make_title(notes),
                                notes=notes,
                                generated_doc=generated_doc,
                                domain=st.session_state.selected_domain,
                            )
                            st.session_state.current_record_id = record_id
                        else:
                            user_prompt = prompts.get_brd_prompt(
                                notes=notes,
                                domain=st.session_state.selected_domain,
                                depth=st.session_state.output_depth,
                            )
                            generated_doc = call_gemini(
                                prompt_text=user_prompt,
                                api_key=api_key,
                                system_instruction=prompts.SYSTEM_PROMPT,
                                temperature=0.2,
                            )
                            st.session_state.generated_doc = generated_doc
                            record_id = database.save_generation(
                                title=make_title(notes),
                                notes=notes,
                                generated_doc=generated_doc,
                                domain=st.session_state.selected_domain,
                            )
                            st.session_state.current_record_id = record_id
                    st.success("BA documentation generated and saved to history.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")

        st.write("")
        with st.expander("About the Analyst Role"):
            st.write(
                "A Business Analyst (BA) bridges the gap between business needs and technical solutions. "
                "Instead of coding, BAs analyze problem reports (like your notes) and create structured documents "
                "so software engineers know exactly what to build and how it must work."
            )

    if st.session_state.generated_doc:
        with right:
            # Step 3
            render_step_title(3, "Explore Analyst Deliverables")
            
            doc = st.session_state.generated_doc
            sections = parse_markdown_sections(doc)

            main_tabs = st.tabs(
                [
                    "📄 Core Document (BRD)",
                    "🔄 Traceability & Backlog",
                    "🔍 Quality & Review",
                    "📥 Export Centre",
                ]
            )

            # Tab 1: Core Document (BRD)
            with main_tabs[0]:
                st.markdown("### 📄 Business Requirements Document (BRD)")
                st.write(
                    "This document translates your unstructured meeting notes into an official business specification. "
                    "Developers, designers, and business owners use this as the single source of truth."
                )
                
                sub_tabs = st.tabs(
                    [
                        "1. Summary & Problem",
                        "2. Stakeholders & Personas",
                        "3. Requirements & Stories",
                        "4. Risks & Questions",
                        "5. Full Raw Document",
                    ]
                )
                
                with sub_tabs[0]:
                    st.markdown(sections.get("executive", "No executive summary found."))
                    st.divider()
                    st.markdown(sections.get("problem", "No business problem summary found."))
                    
                with sub_tabs[1]:
                    st.markdown(sections.get("stakeholders", "No stakeholder section found."))
                    
                with sub_tabs[2]:
                    st.markdown("#### System Requirements")
                    st.markdown(sections.get("business_requirements", "No business requirements found."))
                    st.markdown(sections.get("functional_requirements", "No functional requirements found."))
                    st.markdown(sections.get("non_functional_requirements", "No non-functional requirements found."))
                    st.divider()
                    st.markdown("#### User Stories & Acceptance Criteria")
                    st.markdown(sections.get("user_stories", "No user stories found."))
                    st.markdown(sections.get("acceptance_criteria", "No acceptance criteria found."))
                    st.divider()
                    st.markdown("#### UAT Test Cases")
                    st.markdown(sections.get("uat", "No UAT test cases found."))
                    
                with sub_tabs[3]:
                    if "risks_assumptions" in sections:
                        st.markdown(sections["risks_assumptions"])
                    else:
                        st.markdown(sections.get("risks", "No risks found."))
                        st.markdown(sections.get("assumptions", "No assumptions found."))
                    st.divider()
                    st.markdown(sections.get("questions", "No clarification questions found."))
                    
                with sub_tabs[4]:
                    st.markdown(doc)

            # Tab 2: Traceability & Backlog
            with main_tabs[1]:
                st.markdown("### 🔄 Traceability & Backlog")
                st.write(
                    "Traceability links business goals to system features and test cases, while user stories prepare the developer backlog."
                )
                
                trace_tabs = st.tabs(["1. Requirements Traceability Matrix (RTM)", "2. Jira Backlog Stories"])
                
                with trace_tabs[0]:
                    show_learning_box("rtm")
                    st.markdown(
                        "**What is this?** The matrix below maps business objectives (BR) to specific software behaviors (FR) and UAT test cases (TC). "
                        "This proves to stakeholders that the solution fully covers their needs without missing anything."
                    )
                    
                    if st.session_state.rtm_doc:
                        st.markdown(st.session_state.rtm_doc)
                    else:
                        if st.button("Generate Requirements Traceability Matrix", key="btn_rtm", use_container_width=True):
                            if st.session_state.get("app_mode", "demo") == "demo":
                                try:
                                    with st.spinner("Creating RTM..."):
                                        mocks = mock_data.get_mock_deliverables(
                                            notes=st.session_state.notes_input,
                                            domain=st.session_state.selected_domain,
                                            depth=st.session_state.output_depth,
                                        )
                                        rtm_doc = mocks["rtm"]
                                        st.session_state.rtm_doc = rtm_doc
                                        if st.session_state.current_record_id:
                                            database.update_generation_addons(st.session_state.current_record_id, rtm_doc=rtm_doc)
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"RTM generation failed: {exc}")
                            elif not api_key:
                                st.error("Please enter your Gemini API key first.")
                            else:
                                try:
                                    with st.spinner("Creating RTM..."):
                                        rtm_doc = call_gemini(
                                            prompts.RTM_PROMPT.format(generated_doc=doc),
                                            api_key=api_key,
                                            temperature=0.1,
                                        )
                                        st.session_state.rtm_doc = rtm_doc
                                        if st.session_state.current_record_id:
                                            database.update_generation_addons(st.session_state.current_record_id, rtm_doc=rtm_doc)
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"RTM generation failed: {exc}")
                                    
                with trace_tabs[1]:
                    st.markdown(
                        "**What is this?** These items format your stories, acceptance criteria, priorities, and tags "
                        "into backlog items that developers can build directly from project boards."
                    )
                    if st.session_state.jira_doc:
                        st.markdown(st.session_state.jira_doc)
                    else:
                        if st.button("Generate Jira Backlog Stories", key="btn_jira", use_container_width=True):
                            if st.session_state.get("app_mode", "demo") == "demo":
                                try:
                                    with st.spinner("Creating Jira-ready stories..."):
                                        mocks = mock_data.get_mock_deliverables(
                                            notes=st.session_state.notes_input,
                                            domain=st.session_state.selected_domain,
                                            depth=st.session_state.output_depth,
                                        )
                                        jira_doc = mocks["jira"]
                                        st.session_state.jira_doc = jira_doc
                                        if st.session_state.current_record_id:
                                            database.update_generation_addons(st.session_state.current_record_id, jira_doc=jira_doc)
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Jira story generation failed: {exc}")
                            elif not api_key:
                                st.error("Please enter your Gemini API key first.")
                            else:
                                try:
                                    with st.spinner("Creating Jira-ready stories..."):
                                        jira_doc = call_gemini(
                                            prompts.JIRA_PROMPT.format(generated_doc=doc),
                                            api_key=api_key,
                                            temperature=0.1,
                                        )
                                        st.session_state.jira_doc = jira_doc
                                        if st.session_state.current_record_id:
                                            database.update_generation_addons(st.session_state.current_record_id, jira_doc=jira_doc)
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Jira story generation failed: {exc}")

            # Tab 3: Quality & Review
            with main_tabs[2]:
                st.markdown("### 🔍 Quality Review & Action Plan")
                st.write(
                    "Review the quality of the generated requirements and prepare for follow-up stakeholder workshops."
                )
                
                review_tabs = st.tabs(["1. BA Quality Review", "2. Next Steps & Interview Help"])
                
                with review_tabs[0]:
                    show_learning_box("quality")
                    st.markdown(
                        "**What is this?** An automated quality gate that scores the generated BRD across completeness, "
                        "traceability, testability, and clarity, outlining strengths and recommended improvements."
                    )
                    
                    if st.session_state.quality_review:
                        st.markdown(st.session_state.quality_review)
                    else:
                        if st.button("Run BA Quality Review", key="btn_quality", use_container_width=True):
                            if st.session_state.get("app_mode", "demo") == "demo":
                                try:
                                    with st.spinner("Reviewing document quality..."):
                                        mocks = mock_data.get_mock_deliverables(
                                            notes=st.session_state.notes_input,
                                            domain=st.session_state.selected_domain,
                                            depth=st.session_state.output_depth,
                                        )
                                        quality_review = mocks["quality"]
                                        st.session_state.quality_review = quality_review
                                        if st.session_state.current_record_id:
                                            database.update_generation_addons(st.session_state.current_record_id, quality_review=quality_review)
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Quality review failed: {exc}")
                            elif not api_key:
                                st.error("Please enter your Gemini API key first.")
                            else:
                                try:
                                    with st.spinner("Reviewing document quality..."):
                                        quality_review = call_gemini(
                                            prompts.QUALITY_REVIEW_PROMPT.format(generated_doc=doc),
                                            api_key=api_key,
                                            temperature=0.1,
                                        )
                                        st.session_state.quality_review = quality_review
                                        if st.session_state.current_record_id:
                                            database.update_generation_addons(st.session_state.current_record_id, quality_review=quality_review)
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Quality review failed: {exc}")
                                    
                with review_tabs[1]:
                    st.markdown("#### Suggested Next Steps")
                    st.markdown(sections.get("next_steps", "No suggested next steps found."))
                    st.divider()
                    st.markdown("#### Analyst Workflow Note")
                    st.write(
                        sections.get(
                            "interview",
                            "This deliverable transforms unstructured stakeholder inputs into structured, audit-ready specifications. "
                            "By establishing unbroken traceability and explicit acceptance criteria, the analyst ensures technical and business alignment before development."
                        )
                    )

            # Tab 4: Export Centre
            with main_tabs[3]:
                st.markdown("### 📥 Export Centre")
                st.write("Download your structured analyst deliverables to share with stakeholders or developers.")
                
                export_bundle = combine_export_bundle(
                    generated_doc=st.session_state.generated_doc,
                    rtm_doc=st.session_state.rtm_doc,
                    jira_doc=st.session_state.jira_doc,
                    quality_review=st.session_state.quality_review,
                    executive_summary=st.session_state.executive_summary,
                )
                
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.markdown(
                        "<div class='export-card'>"
                        "<h5>📦 Full Analyst Pack (.md)</h5>"
                        "<p>Includes BRD, RTM, Jira Backlog, and Quality Review combined in one portable file.</p>"
                        "</div>",
                        unsafe_allow_html=True
                    )
                    st.download_button(
                        "⬇ Download Full Pack (.md)",
                        data=export_bundle,
                        file_name="AI_Business_Requirements_Analyst_Pack.md",
                        mime="text/markdown",
                        use_container_width=True,
                        key="dl_full"
                    )
                    
                with col_dl2:
                    st.markdown(
                        "<div class='export-card'>"
                        "<h5>📄 BRD Only (.md)</h5>"
                        "<p>Includes the core Business Requirements Document (sections 1–14) only — ideal for sharing with business stakeholders.</p>"
                        "</div>",
                        unsafe_allow_html=True
                    )
                    st.download_button(
                        "⬇ Download BRD Only (.md)",
                        data=st.session_state.generated_doc,
                        file_name="Business_Requirements_Document.md",
                        mime="text/markdown",
                        use_container_width=True,
                        key="dl_brd"
                    )



def render_history() -> None:
    st.title("Saved History")
    show_learning_box("storage")
    search_text = st.text_input("Search saved notes or titles", placeholder="refund, onboarding, dashboard...")
    history = database.get_history(search_text)

    if not history:
        st.info("No saved history found yet.")
        return

    labels = {f"ID {row[0]} | {row[1]} | {row[2]} | {row[3] or 'General'}": row[0] for row in history}
    selected_label = st.selectbox("Choose a saved generation", list(labels.keys()))
    record = database.get_record(labels[selected_label])
    if not record:
        st.error("Could not load the selected record.")
        return

    record_id, created_at, title, domain, notes, generated_doc, rtm_doc, jira_doc, quality_review, executive_summary = record
    st.caption(f"Created: {created_at} | Domain: {domain}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Load into generator", use_container_width=True):
            st.session_state.notes_input = notes
            st.session_state.generated_doc = generated_doc
            st.session_state.rtm_doc = rtm_doc
            st.session_state.jira_doc = jira_doc
            st.session_state.quality_review = quality_review
            st.session_state.executive_summary = executive_summary
            st.session_state.current_record_id = record_id
            st.success("Loaded. Go to the Generator page to continue working with it.")
    with col2:
        export_bundle = combine_export_bundle(generated_doc, rtm_doc, jira_doc, quality_review, executive_summary)
        st.download_button("Download saved pack", export_bundle, "Saved_Analyst_Pack.md", "text/markdown", use_container_width=True)
    with col3:
        if st.button("Delete record", use_container_width=True):
            database.delete_record(record_id)
            st.success("Deleted successfully.")
            st.rerun()

    preview_left, preview_right = st.columns(2)
    with preview_left:
        st.subheader("Original Notes")
        st.info(notes)
    with preview_right:
        st.subheader("Generated BRD")
        st.markdown(generated_doc)


def render_learning_guide() -> None:
    st.title("Learning Guide")
    st.write("This page explains the project in simple analyst language.")

    sections = [
        ("Why we collect stakeholder notes", "Real analyst work starts with unclear input. The skill is to convert that input into structured outputs."),
        ("Why we use a system prompt", "The system prompt tells the AI to behave like a senior BA and follow a fixed document structure."),
        ("Why we generate requirements", "Requirements explain what the business needs and what the system should do."),
        ("Why we generate acceptance criteria", "Acceptance criteria make requirements testable, so teams know when a feature is complete."),
        ("Why we generate UAT test cases", "UAT test cases help business users validate that the solution works for real scenarios."),
        ("Why we generate an RTM", "An RTM proves that business requirements are connected to functional requirements and tests."),
        ("Why we run a quality review", "Analysts should not blindly trust AI output. They must review clarity, completeness, and missing details."),
    ]

    for title, body in sections:
        with st.expander(title, expanded=False):
            st.write(body)
            st.markdown("**Interview explanation:**")
            st.write(f"This project helped me understand {title.lower()} and how AI can support analyst workflows without replacing analyst judgement.")


def render_project_info() -> None:
    st.title("Project Info")
    st.markdown(
        """
        ## What this project demonstrates
        This project shows how AI can support Business Analysts by converting unstructured stakeholder input into structured documentation.

        ## What makes this better than a basic chatbot
        - It has a clear analyst use case.
        - It uses controlled prompts and fixed document sections.
        - It stores generated outputs in SQLite.
        - It generates supporting artefacts such as RTM, Jira stories, quality review, and executive summary.
        - It includes learning explanations so the builder can understand the business reason behind each feature.

        ## How to explain it on a resume
        Built an AI-powered Business Requirements Generator using Python, Streamlit, Gemini API, and SQLite to convert unstructured stakeholder notes into structured BRDs, user stories, acceptance criteria, UAT test cases, RTMs, and executive summaries.
        """
    )


initialize_state()
api_key = get_api_key()
page = render_sidebar()

if page == "Generator":
    render_generator(api_key)
elif page == "Saved History":
    render_history()
elif page == "Learning Guide":
    render_learning_guide()
else:
    render_project_info()
