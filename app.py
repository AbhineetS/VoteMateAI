import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import time
from fpdf import FPDF
import io
from datetime import datetime

if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "rc_age" not in st.session_state:
    st.session_state.rc_age = 18
if "rc_reg" not in st.session_state:
    st.session_state.rc_reg = "Registered"
if "rc_vid" not in st.session_state:
    st.session_state.rc_vid = "Possessed"
if "rc_booth" not in st.session_state:
    st.session_state.rc_booth = "Known"

if "current_page" not in st.session_state:
    st.session_state.current_page = "⌂ Home"

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_working_model():
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            if "gemini" in m.name.lower():
                return genai.GenerativeModel(m.name)
    return None

def get_ai_answer(user_query):
    query_lower = user_query.lower()
    
    if any(kw in query_lower for kw in ["epic", "voter card", "lost card"]):
        return "Verified Civic Guidance:\nCitizen can still vote if name exists on electoral roll and any approved alternate photo ID is carried."
    if any(kw in query_lower for kw in ["id proof", "aadhaar", "passport", "id"]):
        return "Verified Civic Guidance:\nAccepted alternate IDs: Aadhaar, Passport, Driving License, PAN, Government Service ID, Bank Passbook, Pension Card etc."
    if any(kw in query_lower for kw in ["evm", "hack", "security"]):
        return "Verified Civic Guidance:\nIndian EVMs are standalone non-networked air-gapped units with no WiFi/Bluetooth/internet hardware and are protected by multi-layer sealing and candidate verification."
    if any(kw in query_lower for kw in ["booth", "location", "where vote"]):
        return "Verified Civic Guidance:\nVoter can locate booth via NVSP portal, voter helpline 1950, or booth slip lookup."

    fallback_msg = (
        "Verified Civic Guidance:\n\n"
        "For this election-related concern, citizens are advised to consult the Election Commission "
        "official voter services portal or use the National Voter Helpline 1950 for constituency-specific "
        "assistance. VoteMate AI remains committed to directing you toward official and verified democratic resources."
    )
    try:
        model = get_working_model()
        if model is None:
            return fallback_msg
            
        response = model.generate_content(
            f'''
            You are VoteMate AI, an intelligent Indian election assistant.
            Give clear, concise and trustworthy civic guidance.

            User Question: {user_query}
            '''
        )
        
        if response and hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts') and candidate.content.parts:
                return response.text
                
        return fallback_msg
    except Exception:
        return fallback_msg

st.set_page_config(page_title="VoteMate | Civic Intelligence", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# JS Auto-opener removed. Pure CSS strict-layout applied.

today_date = datetime.now().strftime("%B %d, %Y").upper()

st.markdown(f"""
<div class="custom-top-bar">

<div style="display: flex; align-items: center; gap: 10px; min-width: 180px; padding: 4px 12px; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); border-radius: 6px; color: #059669; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px;">
<div style="width: 6px; height: 6px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px #10b981; animation: pulse-green 2s infinite;"></div>
ENCRYPTED SECURE LINK
</div>

<div class="marquee-container" style="flex-grow: 1; margin: 0 2rem;">
<div class="marquee">
<div class="scrolling-text-content" style="color: #334155; font-family: 'Georgia', serif; font-style: italic; font-size: 1.05rem; letter-spacing: 0.5px;">
"The ballot is stronger than the bullet." — Abraham Lincoln &nbsp;&nbsp;&nbsp;&nbsp;✦&nbsp;&nbsp;&nbsp;&nbsp; "Voting is not only our right, it is our power." — Loung Ung &nbsp;&nbsp;&nbsp;&nbsp;✦&nbsp;&nbsp;&nbsp;&nbsp; "There's no such thing as a vote that doesn't matter." — Barack Obama &nbsp;&nbsp;&nbsp;&nbsp;✦&nbsp;&nbsp;&nbsp;&nbsp; "Nobody will ever deprive the American people of the right to vote except the American people themselves." — Franklin D. Roosevelt
</div>
</div>
</div>

<div style="display: flex; align-items: center; gap: 12px; min-width: 150px; font-family: 'Plus Jakarta Sans', monospace; font-size: 0.8rem; font-weight: 800; letter-spacing: 1px; color: #475569; justify-content: flex-end;">
<div>{today_date}</div>
<div style="display: flex; gap: 4px; align-items: flex-end; height: 14px; margin-left: 4px;">
<div class="telemetry-bar" style="animation-delay: 0.1s"></div>
<div class="telemetry-bar" style="animation-delay: 0.2s"></div>
<div class="telemetry-bar" style="animation-delay: 0.3s"></div>
</div>
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

#MainMenu, footer, [data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
    z-index: 9999998 !important;
}

[data-testid="stSidebarHeader"], 
[data-testid="stSidebar"] button[kind="header"],
[data-testid="collapsedControl"], 
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 4px; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    scroll-behavior: smooth;
}

.stApp {
    background-color: #f8fafc !important;
    color: #0f172a;
}

.custom-top-bar {
    position: fixed; top: 0; left: 15rem; right: 0; height: 64px;
    background: #ffffff;
    color: #1e293b; display: flex; justify-content: space-between;
    align-items: center; padding: 0 2rem;
    z-index: 99999; border-bottom: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.top-badge {
    background: #eff6ff; border: 1px solid #bfdbfe; color: #2563eb;
    padding: 4px 12px; border-radius: 6px; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px;
}

.marquee-container {
    overflow: hidden; white-space: nowrap; width: 100%; position: relative;
    mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
    -webkit-mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
}
.marquee {
    display: inline-block; animation: scroll 40s linear infinite;
    font-size: 0.85rem; font-weight: 600; opacity: 0.85;
}
@keyframes scroll {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

.telemetry-bar {
    width: 4px; height: 12px; background: #3b82f6; border-radius: 2px;
    animation: pulse-blue 1.5s infinite alternate;
}
@keyframes equalize {
    0% { height: 4px; }
    100% { height: 14px; }
}

/* Use bulletproof selectors for the main block container */
[data-testid="stAppViewBlockContainer"], 
[data-testid="stMainBlockContainer"], 
.block-container {
    max-width: 1600px !important; 
    margin-left: 0 !important; 
    margin-right: 0 !important;
    padding-top: 6rem !important;
    padding-left: calc(15rem + 3rem) !important; /* 15rem sidebar + 3rem safety margin */
    padding-right: 3rem !important;
    padding-bottom: 4rem !important;
    animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(15px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-blue {
    0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
    70% { box-shadow: 0 0 0 8px rgba(59, 130, 246, 0); }
    100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}
@keyframes pulse-green {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
.pulse-dot-blue {
    width: 10px; height: 10px; background: #3b82f6; border-radius: 50%;
    animation: pulse-blue 2s infinite;
}

/* =========================================
   TIMELINE SEQUENCE STYLES
   ========================================= */
.timeline-container {
    position: relative;
    max-width: 1000px;
    margin: 2rem 0;
}
.timeline-line {
    position: absolute;
    left: 17px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, #3b82f6 0%, rgba(59,130,246,0.1) 100%);
    z-index: 0;
}
.timeline-item {
    position: relative;
    margin-bottom: 2rem;
    padding-left: 3rem;
    animation: fadeIn 0.6s ease-out forwards;
    opacity: 0;
}
.timeline-dot {
    position: absolute;
    left: -25px;
    top: 24px;
    width: 14px;
    height: 14px;
    background: #ffffff;
    border: 3px solid #3b82f6;
    border-radius: 50%;
    z-index: 2;
    box-shadow: 0 0 10px rgba(59,130,246,0.3);
    transition: all 0.3s ease;
}
.timeline-item:hover .timeline-dot {
    transform: scale(1.3);
    background: #3b82f6;
    box-shadow: 0 0 15px rgba(59,130,246,0.5);
}

.custom-expander {
    background: #ffffff;
    border-radius: 20px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
}
.custom-expander:hover {
    transform: translateX(10px);
    box-shadow: 0 10px 30px rgba(59,130,246,0.08);
    border-color: rgba(59,130,246,0.2);
}
.custom-expander summary {
    padding: 1.5rem 2rem;
    list-style: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    outline: none;
    cursor: pointer;
}
.custom-expander summary::-webkit-details-marker {
    display: none;
}
.summary-content {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}
.step-num {
    font-size: 0.75rem;
    font-weight: 800;
    color: #3b82f6;
    background: rgba(59,130,246,0.1);
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 1px;
}
.step-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1e293b;
}
.expand-icon {
    font-size: 1.2rem;
    color: #94a3b8;
    transition: transform 0.3s ease;
}
.custom-expander[open] .expand-icon {
    transform: rotate(180deg);
}
.custom-expander[open] {
    background: #fdfdfd;
}
.details-content {
    padding: 0 2rem 2rem 5.5rem;
    color: #475569;
    font-size: 1.1rem;
    line-height: 1.8;
    animation: slideDown 0.4s ease-out;
}
@keyframes slideDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* =========================================
   PERMANENT INDESTRUCTIBLE SIDEBAR
   ========================================= */
[data-testid="stSidebar"] {
    transform: translateX(0px) !important;
    visibility: visible !important;
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    height: 100vh !important;
    width: 15rem !important;
    min-width: 15rem !important;
    max-width: 15rem !important;
    display: block !important;
    z-index: 999999 !important;
    background-color: transparent !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

@keyframes sidebar-glow {
    0% { box-shadow: 0 8px 30px rgba(0,0,0,0.2), 0 0 0px rgba(59,130,246,0); border-color: rgba(255,255,255,0.05); }
    100% { box-shadow: 0 12px 40px rgba(0,0,0,0.3), 0 0 20px rgba(59,130,246,0.15); border-color: rgba(59,130,246,0.3); }
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%) !important; 
    margin: 1rem !important;
    border-radius: 24px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    height: calc(100vh - 2rem) !important;
    width: calc(100% - 2rem) !important;
    animation: sidebar-glow 4s ease-in-out infinite alternate !important;
}

/* Apply background to the main section using reliable attributes */
[data-testid="stMain"], [data-testid="stAppViewMain"], section[tabindex="0"] {
    background-color: #f8fafc !important;
}

[data-testid="stSidebarUserContent"] {
    padding-top: 1.5rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child { display: none !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] { gap: 0.2rem; }

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 1rem 1.25rem !important;
    margin: 0.25rem 0.5rem !important;
    border-radius: 14px !important;
    background-color: transparent !important;
    border: 1px solid transparent !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    cursor: pointer !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: rgba(255,255,255,0.08) !important;
    transform: translateX(4px);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(div[aria-checked="true"]),
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important; 
    box-shadow: 0 8px 24px rgba(37,99,235,0.5) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    transform: translateY(-2px);
}
[data-testid="stSidebar"] [data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
    font-size: 1.05rem !important; /* Larger text */
    font-weight: 700 !important;
    color: #cbd5e1 !important; /* Brighter non-active text */
    margin: 0 !important;
    display: flex; align-items: center; gap: 12px;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(div[aria-checked="true"]) div[data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
    font-weight: 800 !important;
}

.home-hero-container {
    position: relative;
    padding: 0 0 1rem 0;
    z-index: 1;
}
.hero-grid {
    position: absolute; inset: -50% 0 0 0;
    background-image: linear-gradient(rgba(59, 130, 246, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(59, 130, 246, 0.05) 1px, transparent 1px);
    background-size: 40px 40px; z-index: -2;
    mask-image: linear-gradient(to bottom, rgba(0,0,0,1), rgba(0,0,0,0));
    -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1), rgba(0,0,0,0));
    pointer-events: none;
}
.hero-bg-blob-1 {
    position: absolute; top: -30%; left: -10%; width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, rgba(255,255,255,0) 70%);
    filter: blur(60px); z-index: -1; pointer-events: none;
}
.hero-bg-blob-2 {
    position: absolute; top: 10%; right: -10%; width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(217,70,239,0.1) 0%, rgba(255,255,255,0) 70%);
    filter: blur(60px); z-index: -1; pointer-events: none;
}

.gradient-text {
    background: linear-gradient(135deg, #2563eb 0%, #d946ef 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-size: 200% auto;
    animation: shine 4s linear infinite;
}
@keyframes shine {
    to { background-position: 200% center; }
}

.hero-title {
    font-size: 6rem;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.05em;
    color: #0f172a;
    margin-top: -1.5rem;
    margin-bottom: 1.75rem;
    text-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
.hero-sub {
    font-size: 1.35rem;
    color: #475569;
    line-height: 1.6;
    max-width: 800px;
    margin-bottom: 2.5rem;
}

.stButton > button {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    padding: 1rem 2rem !important;
    border-radius: 14px !important; 
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    width: 100%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
}
.stButton > button:hover {
    background: #f8fafc !important;
    border-color: rgba(0,0,0,0.2) !important;
    box-shadow: 0 12px 32px rgba(0,0,0,0.08) !important;
    transform: translateY(-4px);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 25px rgba(37, 99, 235, 0.2) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    box-shadow: 0 15px 35px rgba(37, 99, 235, 0.35) !important;
    transform: translateY(-2px);
}

.pill-button .stButton > button {
    border-radius: 30px !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 0.9rem !important;
}

.metric-card, .capability-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 12px 32px rgba(0,0,0,0.03), 0 4px 12px rgba(0,0,0,0.02);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
    height: 100%;
}
.shimmer {
    position: absolute; top: 0; left: -150%; width: 50%; height: 100%;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.8), transparent);
    transform: skewX(-20deg); animation: shimmer 4s infinite; opacity: 0.5; pointer-events: none;
}
@keyframes shimmer {
    100% { left: 200%; }
}
.metric-card::after, .capability-card::after {
    content: ''; position: absolute; inset: 0; border-radius: 20px; padding: 2px;
    background: linear-gradient(135deg, rgba(59,130,246,0.6), rgba(217,70,239,0.3));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor; mask-composite: exclude;
    opacity: 0; transition: opacity 0.3s ease; pointer-events: none;
}
.metric-card:hover, .capability-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 24px 48px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.05);
}
.metric-card:hover::after, .capability-card:hover::after { opacity: 1; }

.cap-number {
    font-size: 0.9rem; font-weight: 800; color: #64748b;
    background: #f1f5f9; padding: 6px 14px; border-radius: 8px;
    display: inline-block; letter-spacing: 0.05em; align-self: flex-start;
}
.cap-title {
    font-size: 1.4rem; font-weight: 800; color: #0f172a;
    margin-bottom: 0.75rem; letter-spacing: -0.02em; margin-top: 1.25rem;
}
.cap-desc {
    font-size: 1.1rem; color: #475569; line-height: 1.6;
}

.stTextArea textarea, .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 16px !important; 
    color: #1e293b !important;
    font-size: 1.1rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: none !important;
    outline: none !important;
    height: 52px !important; /* Slightly taller for premium feel */
}

/* Fix for Selectbox value visibility */
.stSelectbox div[data-baseweb="select"] * {
    color: #1e293b !important;
    font-weight: 500 !important;
}

/* Fix for Number Input buttons and containers */
.stNumberInput div[data-testid="stNumberInputStepDown"], 
.stNumberInput div[data-testid="stNumberInputStepUp"] {
    background-color: #f8fafc !important;
    border: none !important;
    color: #1e293b !important;
    border-radius: 8px !important;
    margin: 4px !important;
    transition: all 0.2s ease !important;
}
.stNumberInput div[data-testid="stNumberInputStepDown"]:hover, 
.stNumberInput div[data-testid="stNumberInputStepUp"]:hover {
    background-color: #e2e8f0 !important;
}

/* Aggressive reset for the input containers */
[data-testid="stTextInput"] > div, 
[data-testid="stTextInput"] > div > div,
[data-testid="stTextInput"],
[data-testid="stSelectbox"] > div,
[data-testid="stNumberInput"] > div,
[data-testid="stNumberInput"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.stTextArea textarea:focus, .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08) !important;
    background-color: #ffffff !important;
}

.stButton > button {
    border-radius: 16px !important;
    padding: 0.6rem 2.2rem !important;
    font-weight: 700 !important;
    height: 48px !important;
    transition: all 0.2s ease !important;
}

.editorial-panel {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 24px;
    padding: 2.5rem; 
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.04); 
    transition: all 0.3s ease;
}
.editorial-panel:focus-within {
    border-color: rgba(59,130,246,0.3);
    box-shadow: 0 20px 60px rgba(59,130,246,0.08);
}

.chat-response {
    background: linear-gradient(145deg, #f8fafc 0%, #ffffff 100%);
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    padding: 2.5rem;
    margin-top: 2rem;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.01);
    animation: fadeIn 0.6s ease-out;
}
.verified-badge {
    background: #e0e7ff;
    color: #4338ca;
    padding: 8px 16px;
    border-radius: 10px;
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1.5rem;
}

[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.05) !important;
    border-radius: 16px !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.02) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(0,0,0,0.1) !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.06) !important;
    transform: translateY(-2px);
}
[data-testid="stExpander"] summary { padding: 1.5rem 1.75rem !important; }
[data-testid="stExpander"] summary p { font-size: 1.15rem !important; font-weight: 800 !important; color: #0f172a !important; }
[data-testid="stExpanderDetails"] > div { padding-top: 0.5rem !important; }

.split-container {
    display: flex; flex-direction: column;
    border: 1px solid rgba(0,0,0,0.05);
    margin-bottom: 1.5rem; background: #ffffff;
    border-radius: 20px; box-shadow: 0 12px 32px rgba(0,0,0,0.03);
}
.split-top, .split-bottom { padding: 1.75rem; }
.split-top { border-bottom: 1px solid rgba(0,0,0,0.04); }
.split-bottom { background-color: #f8fafc; border-radius: 0 0 20px 20px; }

.score-circle {
    width: 80px; height: 80px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.75rem; font-weight: 800;
    border: 5px solid rgba(0,0,0,0.05); margin: 0 auto 1rem auto;
}
.score-circle.success { color: #10b981; border-color: #10b981; }
.score-circle.warning { color: #f59e0b; border-color: #f59e0b; }
.score-circle.danger { color: #ef4444; border-color: #ef4444; }

.compliance-bar {
    height: 8px; background: #f1f5f9; border-radius: 4px;
    overflow: hidden; margin-top: 1rem;
}
.compliance-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
<div style='padding: 0.5rem 0.5rem 1.5rem 0.5rem;'>
<div style='display: flex; align-items: center; gap: 14px;'>
<div style='width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.3rem; box-shadow: 0 8px 24px rgba(37,99,235,0.5);'>V</div>
<h2 style='font-size: 1.6rem; color: #ffffff !important; font-weight: 800; margin: 0; letter-spacing: -0.04em;'>VoteMate</h2>
</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.75rem; font-weight: 800; color: #475569; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.75rem; padding-left: 0.5rem;'>Dashboard</p>", unsafe_allow_html=True)
    
    pages = ["⌂ Home", "≡ Timeline", "✦ AI Assistant", "✓ Readiness Check", "◫ Myth vs Fact"]
    
    selected = st.radio(
        "",
        pages,
        key="nav_selector",
        index=pages.index(st.session_state.current_page),
        label_visibility="collapsed"
    )
    st.session_state.current_page = selected

actual_page = st.session_state.current_page.split(" ", 1)[1]

if actual_page == "Home":
    st.markdown("""
<div class='home-hero-container'>
<div class='hero-grid'></div>
<div class='hero-bg-blob-1'></div>
<div class='hero-bg-blob-2'></div>
<h1 class="hero-title">Algorithmic clarity for<br><span class="gradient-text">democratic infrastructure.</span></h1>
<p class="hero-sub">VoteMate AI brings cryptographic transparency to the electoral process. Instantly access verified guidance, sequence protocols, and personalized readiness compliance in real-time.</p>
</div>
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 1.5, 2.0])
    
    def navigate_to(page):
        st.session_state.current_page = page
        st.session_state.nav_selector = page

    with col1:
        st.button("Consult Engine", type="primary", on_click=navigate_to, args=("✦ AI Assistant",))
    with col2:
        st.button("View Protocol", on_click=navigate_to, args=("≡ Timeline",))

    st.markdown("<div style='height: 5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size: 1.4rem; font-weight: 800; color: #0f172a; margin-bottom: 2rem; letter-spacing: -0.03em;'>System Telemetry</h3>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
<div class='metric-card' style='background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);'>
<div class='shimmer'></div>
<div style='position: absolute; right: -5px; bottom: -15px; font-size: 6rem; opacity: 0.03;'>👥</div>
<div style='color: #3b82f6; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem;'>Registered Base</div>
<div style='font-size: 3.2rem; font-weight: 800; color: #0f172a; letter-spacing: -0.04em;'>968M+</div>
<div style='font-size: 0.9rem; color: #10b981; font-weight: 800; margin-top: 10px; display: flex; align-items: center; gap: 8px;'><div style='width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px rgba(16,185,129,0.5);'></div> Verified Secure</div>
</div>
""", unsafe_allow_html=True)
    with m2:
        st.markdown("""
<div class='metric-card' style='background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);'>
<div class='shimmer'></div>
<div style='position: absolute; right: -5px; bottom: -15px; font-size: 6rem; opacity: 0.03;'>🏛️</div>
<div style='color: #8b5cf6; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem;'>Active Booths</div>
<div style='font-size: 3.2rem; font-weight: 800; color: #0f172a; letter-spacing: -0.04em;'>1.2M</div>
<div style='font-size: 0.9rem; color: #10b981; font-weight: 800; margin-top: 10px; display: flex; align-items: center; gap: 8px;'><div style='width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px rgba(16,185,129,0.5);'></div> Operational</div>
</div>
""", unsafe_allow_html=True)
    with m3:
        st.markdown("""
<div class='metric-card' style='background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);'>
<div class='shimmer'></div>
<div style='position: absolute; right: -5px; bottom: -15px; font-size: 6rem; opacity: 0.03;'>🔒</div>
<div style='color: #f59e0b; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem;'>Secured EVMs</div>
<div style='font-size: 3.2rem; font-weight: 800; color: #0f172a; letter-spacing: -0.04em;'>5.5M</div>
<div style='font-size: 0.9rem; color: #10b981; font-weight: 800; margin-top: 10px; display: flex; align-items: center; gap: 8px;'><div style='width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px rgba(16,185,129,0.5);'></div> Air-Gapped</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 1.4rem; font-weight: 800; color: #0f172a; margin-bottom: 2rem; letter-spacing: -0.03em;'>Core Architecture</h3>", unsafe_allow_html=True)
    
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""
<div class="capability-card">
<div style='display: flex; justify-content: space-between; align-items: flex-start;'>
<div class="cap-number">01</div>
<div style='font-size: 1.8rem; opacity: 0.9; background: #f8fafc; padding: 12px; border-radius: 14px; box-shadow: 0 8px 16px rgba(0,0,0,0.04);'>⏱️</div>
</div>
<div class="cap-title">Sequence Timeline</div>
<div class="cap-desc">A structured, real-time overview of the democratic journey from initial constitutional announcement to the final algorithmic declaration of results.</div>
</div>
<div class="capability-card">
<div style='display: flex; justify-content: space-between; align-items: flex-start;'>
<div class="cap-number">02</div>
<div style='font-size: 1.8rem; opacity: 0.9; background: #f8fafc; padding: 12px; border-radius: 14px; box-shadow: 0 8px 16px rgba(0,0,0,0.04);'>🧠</div>
</div>
<div class="cap-title">AI Consultation Engine</div>
<div class="cap-desc">Direct complex inquiries regarding specific election protocols answered instantly with context-aware, verified civic intelligence.</div>
</div>
""", unsafe_allow_html=True)
        
    with f2:
        st.markdown("""
<div class="capability-card">
<div style='display: flex; justify-content: space-between; align-items: flex-start;'>
<div class="cap-number">03</div>
<div style='font-size: 1.8rem; opacity: 0.9; background: #f8fafc; padding: 12px; border-radius: 14px; box-shadow: 0 8px 16px rgba(0,0,0,0.04);'>✓</div>
</div>
<div class="cap-title">Compliance Analyzer</div>
<div class="cap-desc">A bespoke algorithmic assessment generating a personalized, exportable action plan to ensure full legal compliance and preparedness.</div>
</div>
<div class="capability-card">
<div style='display: flex; justify-content: space-between; align-items: flex-start;'>
<div class="cap-number">04</div>
<div style='font-size: 1.8rem; opacity: 0.9; background: #f8fafc; padding: 12px; border-radius: 14px; box-shadow: 0 8px 16px rgba(0,0,0,0.04);'>🛡️</div>
</div>
<div class="cap-title">Integrity Verification</div>
<div class="cap-desc">Deconstruction of prevalent systemic vulnerabilities and myths through authoritative, protocol-backed factual cryptographic corrections.</div>
</div>
""", unsafe_allow_html=True)

elif actual_page == "Timeline":
    st.markdown("""
<div style='margin-bottom: 2.5rem;'>
<h1 style='font-size: 3rem; font-weight: 800; letter-spacing: -0.04em; color: #0f172a; margin-bottom: 0.75rem;'>Protocol Sequence</h1>
<p style='font-size: 1.25rem; color: #475569; max-width: 800px;'>A chronological breakdown of the democratic infrastructure protocol.</p>
</div>
""", unsafe_allow_html=True)

    steps = [
        ("01", "Official Announcement", "The Election Commission officially announces election dates, phases, and the Model Code of Conduct comes into effect immediately. All administrative machinery shifts under ECI purview."),
        ("02", "Voter Registration", "Citizens verify their names in the electoral roll, update their biometric/demographic details, or register as new voters before the strict constitutional deadline."),
        ("03", "Candidate Nomination", "Aspiring candidates submit their official nomination papers, financial affidavits, and criminal disclosures for deep legal scrutiny."),
        ("04", "Campaign Phase", "Political parties and candidates actively campaign, present their manifestos, and engage with voters while adhering strictly to expenditure caps."),
        ("05", "Polling Day", "Eligible citizens cast their votes securely at designated polling booths using air-gapped Electronic Voting Machines (EVMs) with VVPAT verification."),
        ("06", "Secure Counting", "All EVMs are transported under multi-tier security to strong rooms. Votes are counted systematically under strict CCTV surveillance and micro-observer supervision."),
        ("07", "Results Declaration", "Final winners and representatives are officially declared by the Returning Officer, formally paving the way for government formation and swearing-in.")
    ]

    timeline_html = "<div class='timeline-container'><div class='timeline-line'></div>"
    for i, (num, title, desc) in enumerate(steps):
        delay = i * 0.1
        timeline_html += f"""
<div class='timeline-item' style='animation-delay: {delay}s;'>
<div class='timeline-dot'></div>
<details class='custom-expander'>
<summary>
<div class='summary-content'>
<span class='step-num'>{num}</span>
<span class='step-title'>{title}</span>
</div>
<div class='expand-icon'>▼</div>
</summary>
<div class='details-content'>
{desc}
</div>
</details>
</div>
"""
    timeline_html += "</div>"
    st.markdown(timeline_html, unsafe_allow_html=True)

elif actual_page == "AI Assistant":
    st.markdown("""
<div style='margin-bottom: 2.5rem;'>
<h1 style='font-size: 3rem; font-weight: 800; letter-spacing: -0.04em; color: #0f172a; margin-bottom: 0.75rem;'>Civic Engine</h1>
<p style='font-size: 1.25rem; color: #475569; max-width: 800px;'>Consult the intelligence matrix regarding protocols, security, or booth infrastructure.</p>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.85rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.25rem;'>Quick Inquiries</p>", unsafe_allow_html=True)
    
    p1, p2, p3, p4 = st.columns(4)
    def set_prompt(text): st.session_state.user_question = text
    
    with p1: 
        st.markdown("<div class='pill-button'>", unsafe_allow_html=True)
        st.button("Lost EPIC Card", on_click=set_prompt, args=("I lost my EPIC card. How can I vote?",), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with p2: 
        st.markdown("<div class='pill-button'>", unsafe_allow_html=True)
        st.button("ID Proofs", on_click=set_prompt, args=("What alternative ID proofs are accepted at the booth?",), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with p3: 
        st.markdown("<div class='pill-button'>", unsafe_allow_html=True)
        st.button("EVM Security", on_click=set_prompt, args=("Explain how EVMs are secured against hacking.",), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with p4: 
        st.markdown("<div class='pill-button'>", unsafe_allow_html=True)
        st.button("Booth Location", on_click=set_prompt, args=("How do I find the exact location of my polling booth?",), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.5rem;'>Input Terminal</p>", unsafe_allow_html=True)
    
    question = st.text_input("Query Input", value=st.session_state.user_question, placeholder="Ask anything about the electoral process...", label_visibility="collapsed")
    if question != st.session_state.user_question:
        st.session_state.user_question = question
        
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 1.5, 1])
    with col_b2:
        generate_clicked = st.button("Submit Query", type="primary", use_container_width=True)
    
    if generate_clicked:
        if st.session_state.user_question:
            with st.spinner("Processing intelligence query..."):
                answer_text = get_ai_answer(st.session_state.user_question)
                st.markdown(f"""
<div class='chat-response'>
<div class='verified-badge'>
<div style='width: 6px; height: 6px; background: #4338ca; border-radius: 50%;'></div>
Verified Response
</div>
<div style='font-size: 1.15rem; line-height: 1.8; color: #0f172a; font-weight: 500;'>
{answer_text.replace('\n', '<br>')}
</div>
</div>
""", unsafe_allow_html=True)
        else:
            st.error("Please provide a query.")

elif actual_page == "Readiness Check":
    st.markdown("""
<div style='margin-bottom: 2.5rem;'>
<h1 style='font-size: 3rem; font-weight: 800; letter-spacing: -0.04em; color: #0f172a; margin-bottom: 0.75rem;'>Compliance Analyzer</h1>
<p style='font-size: 1.25rem; color: #475569; max-width: 800px;'>Evaluate personal electoral readiness to generate an operational checklist.</p>
</div>
""", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("<p style='font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.25rem; color: #64748b;'>Age Qualification</p>", unsafe_allow_html=True)
            age = st.number_input("Age", min_value=15, max_value=120, key='rc_age', label_visibility="collapsed")
            st.markdown("<div style='height: 2.5rem;'></div><p style='font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.25rem; color: #64748b;'>Roll Registration Status</p>", unsafe_allow_html=True)
            registered = st.selectbox("Registration", ["Registered", "Not Registered"], key='rc_reg', label_visibility="collapsed")
        with col2:
            st.markdown("<p style='font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.25rem; color: #64748b;'>EPIC Credential</p>", unsafe_allow_html=True)
            voterid = st.selectbox("Voter ID", ["Possessed", "Not Possessed"], key='rc_vid', label_visibility="collapsed")
            st.markdown("<div style='height: 2.5rem;'></div><p style='font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.25rem; color: #64748b;'>Booth Designation</p>", unsafe_allow_html=True)
            booth = st.selectbox("Booth Details", ["Known", "Unknown"], key='rc_booth', label_visibility="collapsed")
        
        st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
        col_b1, col_b2, col_b3 = st.columns([1, 1.5, 1])
        with col_b2:
            generate_checklist = st.button("Execute Analysis", type="primary", use_container_width=True)

    if generate_checklist:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        if age < 18:
            st.markdown("""
<div class='editorial-panel' style='border: 1px solid rgba(239,68,68,0.3); background: #fef2f2; padding: 2.5rem;'>
<h3 style='color: #ef4444; font-size: 1.4rem; font-weight: 800; margin-bottom: 0.75rem;'>Status: Ineligible</h3>
<p style='font-size: 1.1rem; color: #0f172a; margin: 0;'>Minimum constitutional age requirement (18) is not met.</p>
</div>
""", unsafe_allow_html=True)
        else:
            todos = []
            dones = []
            score = 25
            
            if registered == "Registered":
                dones.append("Electoral roll registration confirmed in database.")
                score += 25
            else:
                todos.append("Complete electoral roll registration before polling.")
                
            if voterid == "Possessed":
                dones.append("EPIC credential / Valid ID secured.")
                score += 25
            else:
                todos.append("Carry alternate approved ID.")
                
            if booth == "Known":
                dones.append("Polling infrastructure location verified.")
                score += 25
            else:
                todos.append("Verify polling booth through NVSP/1950.")

            score_color = "success" if score == 100 else ("warning" if score >= 50 else "danger")

            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"""
<div class='editorial-panel' style='text-align: center; padding: 3.5rem 2rem;'>
<p style='font-size: 0.95rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 2rem;'>Readiness Index</p>
<div class='score-circle {score_color}' style='width: 120px; height: 120px; font-size: 2.5rem; border-width: 6px;'>{score}%</div>
<div class='compliance-bar' style='margin-top: 2rem;'>
<div class='compliance-fill' style='width: {score}%; background: {"#10b981" if score == 100 else ("#f59e0b" if score >= 50 else "#ef4444")};'></div>
</div>
</div>
""", unsafe_allow_html=True)
            
            with c2:
                st.markdown("<div class='editorial-panel' style='padding: 2.5rem;'>", unsafe_allow_html=True)
                if score == 100:
                    st.markdown("""
<div style='background: #ecfdf5; border: 1px solid rgba(16,185,129,0.2); padding: 2rem; border-radius: 16px; margin-bottom: 0.5rem;'>
<p style='font-size: 1.25rem; font-weight: 800; color: #059669; margin: 0;'>✓ Verified Readiness Achieved</p>
<p style='font-size: 1.1rem; color: #475569; margin: 0; margin-top: 8px;'>All compliance protocols met successfully.</p>
</div>
""", unsafe_allow_html=True)
                else:
                    if todos:
                        st.markdown("<p style='font-size: 0.9rem; font-weight: 800; color: #ef4444; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.25rem;'>Pending Actions</p>", unsafe_allow_html=True)
                        for item in todos:
                            st.markdown(f"""
<div style='display: flex; gap: 12px; margin-bottom: 1.25rem; align-items: flex-start;'>
<div style='color: #ef4444; font-weight: 800; font-size: 1.2rem;'>!</div>
<div style='color: #0f172a; font-size: 1.15rem; font-weight: 600;'>{item}</div>
</div>
""", unsafe_allow_html=True)
                        st.markdown("<div style='height: 1px; background: rgba(0,0,0,0.05); margin: 2rem 0;'></div>", unsafe_allow_html=True)
                    
                    if dones:
                        st.markdown("<p style='font-size: 0.9rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.25rem;'>Verified Systems</p>", unsafe_allow_html=True)
                        for item in dones:
                            st.markdown(f"""
<div style='display: flex; gap: 12px; margin-bottom: 1.25rem; align-items: flex-start;'>
<div style='color: #10b981; font-weight: 800; font-size: 1.2rem;'>✓</div>
<div style='color: #475569; font-size: 1.15rem; font-weight: 500;'>{item}</div>
</div>
""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            try:
                pdf_data = create_pdf()
                col_d1, col_d2, col_d3 = st.columns([1, 1.5, 1])
                with col_d2:
                    st.download_button("Export Formal PDF Report", data=pdf_data, file_name="VoteMate_Compliance_Report.pdf", mime="application/pdf", use_container_width=True)
            except Exception: pass

elif actual_page == "Myth vs Fact":
    st.markdown("""
<div style='margin-bottom: 2.5rem;'>
<h1 style='font-size: 3rem; font-weight: 800; letter-spacing: -0.04em; color: #0f172a; margin-bottom: 0.75rem;'>Information Integrity</h1>
<p style='font-size: 1.25rem; color: #475569; max-width: 800px;'>Cryptographic clarification of systemic vulnerabilities and misconceptions.</p>
</div>
""", unsafe_allow_html=True)

    myths = [
        ("I cannot vote if I lost my voter slip.", "System accepts vote. The voter slip is solely for operational convenience. As long as your record exists in the electoral roll, any approved photo ID card suffices for verification."),
        ("Having an Aadhaar card guarantees my right to vote.", "Aadhaar is accepted for identity verification, but localized electoral roll registration for your specific constituency is the absolute fundamental prerequisite."),
        ("EVMs can be intercepted via WiFi or Bluetooth.", "EVMs are strictly air-gapped standalone units. They lack any network hardware components, rendering remote interception technically impossible."),
        ("Voting is legally compulsory in India.", "Voting is a fundamental civic duty, but it remains strictly voluntary under constitutional law. There are zero penal consequences for abstention."),
        ("If I am out of station, I can vote digitally.", "Digital voting is not implemented for the general populace. In-person verification at designated booths is mandatory.")
    ]

    for myth, fact in myths:
        st.markdown(f"""
<div class='split-container'>
<div class='split-top'>
<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;'>
<div style='width: 28px; height: 28px; border-radius: 8px; background: #fef2f2; border: 1px solid rgba(239,68,68,0.2); color: #ef4444; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.95rem;'>✗</div>
<div style='color: #ef4444; margin: 0; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.05em;'>Myth</div>
</div>
<p style='font-size: 1.2rem; color: #0f172a; margin: 0; font-weight: 700;'>"{myth}"</p>
</div>
<div class='split-bottom'>
<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;'>
<div style='width: 28px; height: 28px; border-radius: 8px; background: #ecfdf5; border: 1px solid rgba(16,185,129,0.2); color: #10b981; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.95rem;'>✓</div>
<div style='color: #10b981; margin: 0; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.05em;'>Fact</div>
</div>
<p style='font-size: 1.15rem; color: #475569; margin: 0; line-height: 1.8;'>{fact}</p>
</div>
</div>
""", unsafe_allow_html=True)
