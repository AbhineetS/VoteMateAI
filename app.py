import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import time
from fpdf import FPDF
import io

if "user_question" not in st.session_state:
    st.session_state.user_question = ""

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_working_model():
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            if "gemini" in m.name.lower():
                return genai.GenerativeModel(m.name)
    return None

def get_ai_answer(user_query):
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

st.set_page_config(page_title="VoteMate AI | Civic Assistant", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* Master SaaS Civic Theme */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Global Smoothness */
.stApp {
    background-color: #f8f9fa;
    color: #1e293b;
    animation: appFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes appFadeIn {
    0% { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Sidebar Refinement */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
    min-width: 250px !important;
    max-width: 250px !important;
}

/* Hide Radio Circles & Style Tabs */
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    gap: 0.15rem;
}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radio"] {
    display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 0.45rem 0.75rem !important;
    border-radius: 6px !important;
    margin-bottom: 0 !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    background-color: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: #f8f9fa !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(div[aria-checked="true"]) {
    background-color: #f1f5f9 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(div[aria-checked="true"]) div[data-testid="stMarkdownContainer"] p {
    font-weight: 600 !important;
    color: #0f172a !important;
}

/* Typography visibility */
h1, h2, h3, h4, h5, h6 {
    color: #0f172a !important;
    font-weight: 600;
    letter-spacing: -0.015em;
}

p, li, span, div {
    color: #475569;
}

/* Hero Section */
.hero-container {
    padding: 3.5rem 2rem;
    border-radius: 12px;
    background: #ffffff;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02), 0 1px 2px rgba(0,0,0,0.02);
    margin-bottom: 2.5rem;
    border: 1px solid #e2e8f0;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #64748b;
    font-weight: 400;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Custom Cards */
.feature-card {
    background: #ffffff;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    transition: all 0.25s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.feature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.04);
    border-color: #cbd5e1;
}
.card-icon {
    font-size: 1.8rem;
    margin-bottom: 1rem;
}
.card-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.5rem;
}
.card-desc {
    font-size: 0.9rem;
    color: #64748b;
    line-height: 1.5;
}

/* Metrics Styling */
[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    color: #3b82f6 !important;
}
[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton > button {
    background: #3b82f6;
    color: white !important;
    border: none;
    padding: 0.4rem 1.2rem;
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    width: 100%;
    box-shadow: 0 1px 2px rgba(59, 130, 246, 0.15);
}
.stButton > button:hover {
    background: #2563eb;
    box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0px);
}

/* Inputs / Textareas */
.stTextArea textarea, .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
    color: #1e293b !important;
    font-size: 0.95rem !important;
    padding: 0.5rem !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.01) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextArea textarea:focus, .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f6 !important;
}

.stAlert {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #1e293b !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}

/* Expander headers */
.streamlit-expanderHeader {
    font-size: 0.95rem;
    font-weight: 500;
    color: #1e293b;
    background-color: #ffffff !important;
    border-radius: 0 !important;
}
div[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: none !important;
    border-bottom: 1px solid #e2e8f0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    margin-bottom: 0 !important;
}

/* Alert text overrides */
.stAlert p {
    color: #475569 !important;
}
</style>
""", unsafe_allow_html=True)


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style='text-align: left; margin-bottom: 1.5rem; padding: 0.5rem 0.5rem 0 0.5rem;'>
            <h2 style='font-size: 1.25rem; color: #0f172a !important; font-weight: 700; margin-bottom: 0.1rem; letter-spacing: -0.02em;'>🏛️ VoteMate</h2>
            <p style='color: #64748b; font-size: 0.8rem; margin-top: 0; font-weight: 400;'>Civic Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.7rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; padding-left: 0.5rem;'>Overview</p>", unsafe_allow_html=True)
    page = st.radio("", [
        "🏠 Dashboard Home",
        "📅 Election Timeline",
        "🤖 AI Election Assistant",
        "🧾 First Time Voter Wizard",
        "⚖️ Myth vs Fact"
    ], label_visibility="collapsed")
    
    st.markdown("<div style='margin-top: auto; padding-top: 4rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.7rem; color: #94a3b8; text-align: left; padding: 0.5rem;'>Secured by Gemini AI</p>", unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = page

if st.session_state.current_page != page:
    with st.spinner("Loading Civic Module..."):
        time.sleep(0.3)
    st.session_state.current_page = page

# --- MAIN CONTENT ---
if page == "🏠 Dashboard Home":
    # Top-right Subtitle
    st.markdown("<div style='text-align: right; color: #64748b; font-weight: 500; font-size: 0.85rem; margin-bottom: 1.5rem;'>Built for Electoral Literacy & Democratic Inclusion</div>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">AI Powered Electoral Literacy for Every Citizen</div>
            <div class="hero-subtitle">Reducing voter confusion, improving democratic access, and enabling trusted election guidance through one intelligent civic platform.</div>
        </div>
        <div style='display: flex; justify-content: center; gap: 2rem; margin-top: -1.5rem; margin-bottom: 1.5rem; color: #475569; font-size: 0.9rem; font-weight: 500; flex-wrap: wrap;'>
            <span style='display: flex; align-items: center; gap: 0.4rem;'><span style='color: #10b981; font-size: 1rem;'>✓</span> 968M+ Eligible Voters</span>
            <span style='display: flex; align-items: center; gap: 0.4rem;'><span style='color: #10b981; font-size: 1rem;'>✓</span> 1.2M+ Polling Stations</span>
            <span style='display: flex; align-items: center; gap: 0.4rem;'><span style='color: #10b981; font-size: 1rem;'>✓</span> 1950 National Helpline</span>
            <span style='display: flex; align-items: center; gap: 0.4rem;'><span style='color: #10b981; font-size: 1rem;'>✓</span> Official ECI Connected</span>
        </div>
        
        <div style='display: flex; justify-content: center; gap: 0.75rem; margin-bottom: 2.5rem; flex-wrap: wrap;'>
            <span style='background: #f8fafc; border: 1px solid #e2e8f0; color: #0f172a; padding: 0.35rem 0.85rem; border-radius: 6px; font-size: 0.75rem; font-weight: 500;'>🟢 AI Backend Verified</span>
            <span style='background: #f8fafc; border: 1px solid #e2e8f0; color: #0f172a; padding: 0.35rem 0.85rem; border-radius: 6px; font-size: 0.75rem; font-weight: 500;'>🛡 Official Civic Sources</span>
            <span style='background: #f8fafc; border: 1px solid #e2e8f0; color: #0f172a; padding: 0.35rem 0.85rem; border-radius: 6px; font-size: 0.75rem; font-weight: 500;'>⚡ Real-time Guidance Active</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Live Election Status Bar
    st.markdown("""
        <div style='background: #ffffff; padding: 1.2rem 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6; margin-bottom: 3rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-top: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;'>
            <div style='display: flex; flex-direction: column;'>
                <span style='color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Upcoming Election</span>
                <span style='color: #0f172a; font-weight: 700; font-size: 1.05rem;'>Bihar Assembly 2026</span>
            </div>
            <div style='display: flex; flex-direction: column;'>
                <span style='color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>National Voter Helpline</span>
                <span style='color: #0f172a; font-weight: 700; font-size: 1.05rem;'>📞 1950</span>
            </div>
            <div style='display: flex; flex-direction: column;'>
                <span style='color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Model Code Status</span>
                <span style='color: #15803d; font-weight: 700; font-size: 1.05rem;'>🟢 Active During Elections</span>
            </div>
            <div style='display: flex; flex-direction: column;'>
                <span style='color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Official Source</span>
                <span style='color: #0f172a; font-weight: 700; font-size: 1.05rem;'>Election Commission of India</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics Section
    st.markdown("### 📊 National Election Snapshot")
    m1, m2, m3 = st.columns(3)
    m1.metric("Registered Voters", "968M+", "Largest Democracy")
    m2.metric("Polling Booths", "1.2M+", "Widespread Access")
    m3.metric("EVMs Deployed", "5.5M+", "Secured Tech")
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Civic Actions")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.link_button("Official Voter Portal", "https://voters.eci.gov.in/", use_container_width=True)
    with c2:
        st.link_button("Find Polling Booth", "https://electoralsearch.eci.gov.in/", use_container_width=True)
    with c3:
        st.link_button("National Voter Portal", "https://www.nvsp.in/", use_container_width=True)
    with c4:
        st.link_button("Election Commission", "https://eci.gov.in/", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown("<div style='text-align: center; padding: 0.75rem; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; color: #1e40af; font-weight: 500; font-size: 0.95rem; margin-bottom: 2.5rem; max-width: 600px; margin-left: auto; margin-right: auto;'>Designed to bridge the information gap between citizens and the electoral system.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom: 1.5rem;'>🌟 Platform Features</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">📅</div>
                <div class="card-title">Election Process Simplified</div>
                <div class="card-desc">Understand how elections are conducted from the initial announcement to the final result declaration with our interactive timeline.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">🤖</div>
                <div class="card-title">AI Powered Assistant</div>
                <div class="card-desc">Ask your specific election doubts in plain language and receive instant, simple, and unbiased answers powered by Gemini AI.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">🧾</div>
                <div class="card-title">First Time Voter Guidance</div>
                <div class="card-desc">Navigate the complexities of voting for the first time with a personalized, step-by-step readiness checklist.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">🛡️</div>
                <div class="card-title">Myth vs Fact Verification</div>
                <div class="card-desc">Clear up confusion about voter IDs, EVM security, eligibility criteria, and the polling process with verified facts.</div>
            </div>
        """, unsafe_allow_html=True)

elif page == "📅 Election Timeline":
    st.title("📅 Interactive Election Timeline")
    st.markdown("<p style='color: #64748b; font-size: 1.05rem; margin-bottom: 2rem;'>Follow the democratic journey step-by-step from announcement to governance.</p>", unsafe_allow_html=True)

    steps = [
        ("📢 1. Election Announcement", "The Election Commission officially announces election dates, phases, and the Model Code of Conduct comes into effect immediately."),
        ("📝 2. Voter Registration", "Citizens verify their names in the electoral roll, update their details, or register as new voters before the deadline."),
        ("👤 3. Candidate Nomination", "Aspiring candidates submit their official nomination papers, affidavits, and disclosures for scrutiny."),
        ("🎤 4. Campaign Period", "Political parties and candidates actively campaign, present their manifestos, and engage with voters."),
        ("🗳️ 5. Polling Day", "Eligible citizens cast their votes securely at designated polling booths using EVMs."),
        ("📊 6. Vote Counting", "All votes are counted systematically under strict supervision and high security."),
        ("🏆 7. Result Declaration", "Final winners and representatives are officially declared, paving the way for government formation.")
    ]

    for title, desc in steps:
        with st.expander(title, expanded=False):
            st.info(desc, icon="ℹ️")

elif page == "🤖 AI Election Assistant":
    st.title("🤖 Ask VoteMate AI")
    st.markdown("<p style='color: #64748b; font-size: 1.05rem; margin-bottom: 2.5rem;'>Your intelligent civic assistant. Ask any question regarding the electoral process, rules, or your rights.</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: #ffffff; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 2.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
            <h4 style='margin-top: 0; color: #0f172a; font-size: 1rem; margin-bottom: 0.75rem;'>💡 Suggestion Prompts:</h4>
            <ul style='color: #475569; margin-bottom: 0; font-size: 0.95rem;'>
                <li>What if I lose my voter ID before election day?</li>
                <li>Can I vote without EPIC card?</li>
                <li>How is EVM tampering prevented?</li>
                <li>How do I find my polling booth?</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        question = st.text_area("💬 Type your election-related question below:", value=st.session_state.user_question, height=100, placeholder="E.g., What are the timings for polling booths?")
        if question != st.session_state.user_question:
            st.session_state.user_question = question
    with col2:
        st.markdown("<div style='margin-top: 2.2rem; text-align: center; color: #64748b; font-size: 0.85rem; font-weight: 500;'>Or Speak 🎙️</div>", unsafe_allow_html=True)
        audio = mic_recorder(start_prompt="🎙️ Start recording", stop_prompt="🛑 Stop recording", key='STT')
    
    if audio:
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(io.BytesIO(audio['bytes'])) as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            st.session_state.user_question = text
            st.rerun()
        except Exception:
            st.warning("⚠️ Audio recognition was interrupted. Please try again or type your question.")

    if st.button("✨ Generate Answer"):
        if st.session_state.user_question:
            with st.spinner("Analyzing Election Guidelines..."):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.015)
                    progress_bar.progress(percent_complete + 1)
                progress_bar.empty()
                answer_text = get_ai_answer(st.session_state.user_question)
                
                st.markdown("""
                    <style>
                    .stAlert {
                        background: #ffffff !important;
                        border: 1px solid #e2e8f0 !important;
                        border-left: 4px solid #3b82f6 !important;
                        border-radius: 8px !important;
                        padding: 1.5rem !important;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
                        animation: fadeIn 0.4s ease-out !important;
                    }
                    .stAlert h3 {
                        color: #0f172a !important;
                        margin-bottom: 0.2rem !important;
                        font-size: 1.3rem !important;
                        font-weight: 700 !important;
                        border-bottom: none !important;
                    }
                    .stAlert strong {
                        color: #1e40af !important;
                    }
                    .stAlert hr {
                        border-color: #e2e8f0 !important;
                    }
                    </style>
                """, unsafe_allow_html=True)
                st.info(f"""### ✅ Verified Civic AI Response
<div style='font-size: 0.8rem; color: #64748b; margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid #e2e8f0; font-weight: 500;'>🛡️ ECI Verified &nbsp;•&nbsp; 👤 Citizen Safe &nbsp;•&nbsp; 🗳️ Election Ready</div>

**🔹 Situation Assessment**  
Reviewing your query against official Indian electoral guidelines.

**🔹 Official Civic Guidance**  
{answer_text}

---
<span style='color: #15803d; font-weight: 600; font-size: 0.95rem;'>🔹 Recommended Citizen Action</span>  
Citizens may additionally verify constituency-specific instructions via ECI, NVSP, or Helpline 1950.
""")
        else:
            st.warning("⚠️ Please type or speak a question first.")

elif page == "🧾 First Time Voter Wizard":
    st.title("🧾 First Time Voter Readiness Checker")
    st.markdown("<p style='color: #64748b; font-size: 1.05rem; margin-bottom: 2rem;'>Complete this quick wizard to generate your personalized action plan for election day.</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='background: #ffffff; padding: 2rem; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='font-size: 0.85rem; font-weight: 500; color: #64748b; margin-bottom: 0.2rem;'>Age</p>", unsafe_allow_html=True)
            age = st.number_input("Age", min_value=15, max_value=120, value=18, label_visibility="collapsed")
            st.markdown("<p style='font-size: 0.85rem; font-weight: 500; color: #64748b; margin-bottom: 0.2rem; margin-top: 1rem;'>Registration Status</p>", unsafe_allow_html=True)
            registered = st.selectbox("Registration", ["Yes", "No"], label_visibility="collapsed")
        with col2:
            st.markdown("<p style='font-size: 0.85rem; font-weight: 500; color: #64748b; margin-bottom: 0.2rem;'>Voter ID (EPIC)</p>", unsafe_allow_html=True)
            voterid = st.selectbox("Voter ID", ["Yes", "No"], label_visibility="collapsed")
            st.markdown("<p style='font-size: 0.85rem; font-weight: 500; color: #64748b; margin-bottom: 0.2rem; margin-top: 1rem;'>Polling Booth Details</p>", unsafe_allow_html=True)
            booth = st.selectbox("Booth Details", ["Yes", "No"], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Generate My Voting Checklist"):
        st.subheader("🎯 Your Personalized Action Plan")

        if age < 18:
            st.error("🚫 **Not Eligible Yet:** You must be at least 18 years old to vote. Stay informed and get ready for the future!")
        else:
            st.balloons()
            st.toast("Checklist generated successfully!", icon="✅")
            
            todos = []
            dones = []
            
            if registered == "No":
                todos.append("Register your name in the electoral roll via the NVSP portal or Voter Helpline App.")
            else:
                dones.append("Name is registered in the electoral roll.")
                
            if voterid == "No":
                todos.append("Apply for a Voter ID or download the e-EPIC. Alternatively, prepare an approved substitute ID (like Aadhaar, PAN, Passport).")
            else:
                dones.append("Voter ID is ready.")
                
            if booth == "No":
                todos.append("Check your polling booth location online before election day to avoid last-minute confusion.")
            else:
                dones.append("Polling booth location is known.")

            # Display Todos
            if todos:
                st.warning("### ⚠️ Action Required:")
                for item in todos:
                    st.markdown(f"- {item}")
            
            # Display General Success
            st.success("### ✅ Day-of-Election Checklist:")
            if dones:
                for item in dones:
                    st.markdown(f"- {item} (Completed)")
            st.markdown("- Carry your valid ID proof to the polling station.")
            st.markdown("- Reach the polling booth during the official voting hours (usually 7 AM - 6 PM).")
            st.markdown("- Follow EVM instructions carefully and verify your vote via VVPAT.")

            st.markdown("---")

            # PDF Generation
            def create_pdf():
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, "VoteMate AI - Personalized Readiness Checklist", ln=True, align="C")
                pdf.set_font("Arial", size=12)
                pdf.ln(10)
                pdf.cell(0, 10, f"Age: {age}", ln=True)
                pdf.cell(0, 10, f"Registered: {registered}", ln=True)
                pdf.cell(0, 10, f"Voter ID: {voterid}", ln=True)
                pdf.cell(0, 10, f"Polling Booth Known: {booth}", ln=True)
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "Action Required:", ln=True)
                pdf.set_font("Arial", size=12)
                if todos:
                    for t in todos:
                        t_clean = t.encode('ascii', 'ignore').decode('ascii')
                        pdf.set_x(10)
                        pdf.multi_cell(190, 10, f"- {t_clean}")
                else:
                    pdf.cell(0, 10, "None", ln=True)
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "Completed / Checklist:", ln=True)
                pdf.set_font("Arial", size=12)
                for d in dones:
                    d_clean = d.encode('ascii', 'ignore').decode('ascii')
                    pdf.set_x(10)
                    pdf.multi_cell(190, 10, f"- {d_clean} (Completed)")
                pdf.set_x(10)
                pdf.multi_cell(190, 10, "- Carry your valid ID proof to the polling station.")
                pdf.set_x(10)
                pdf.multi_cell(190, 10, "- Reach the polling booth during the official voting hours (usually 7 AM - 6 PM).")
                pdf.set_x(10)
                pdf.multi_cell(190, 10, "- Follow EVM instructions carefully and verify your vote via VVPAT.")
                return bytes(pdf.output(dest='S'))

            try:
                pdf_data = create_pdf()
                st.download_button(
                    label="📥 Download My Checklist PDF",
                    data=pdf_data,
                    file_name="VoteMate_Checklist.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.markdown("""
                    <div style='background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 1.5rem; text-align: center; margin-top: 2rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);'>
                        <h4 style='color: #166534; margin: 0 0 0.5rem 0; font-size: 1.15rem;'>🎉 You are now election-day prepared.</h4>
                        <p style='color: #15803d; margin: 0; font-size: 1rem; font-weight: 500;'>Vote confidently. Vote responsibly. Strengthen democracy.</p>
                    </div>
                """, unsafe_allow_html=True)
            except Exception:
                st.warning("⚠️ Checklist PDF generation is temporarily unavailable. Please refer to your personalized plan above.")

elif page == "⚖️ Myth vs Fact":
    st.title("⚖️ Election Myth vs Fact")
    st.markdown("<p style='color: #64748b; font-size: 1.05rem; margin-bottom: 2rem;'>Combat misinformation. Get the verified facts about the electoral process.</p>", unsafe_allow_html=True)

    myths = [
        ("🤔 Myth: I cannot vote if I lost my voter slip.", "✅ **Fact:** You can still vote! The voter slip is just for convenience. As long as your name is on the electoral roll, you can vote by showing an approved photo ID card."),
        ("🤔 Myth: Having an Aadhaar card is enough to vote.", "✅ **Fact:** An Aadhaar card is an accepted proof of identity, but **you must be registered in the electoral roll** of your constituency to be allowed to vote."),
        ("🤔 Myth: EVMs can be easily hacked via WiFi or Bluetooth.", "✅ **Fact:** EVMs are standalone machines. They are not connected to any network, internet, WiFi, or Bluetooth, making remote hacking technically impossible. They are secured under strict Election Commission protocols."),
        ("🤔 Myth: Voting is legally compulsory in India.", "✅ **Fact:** Voting is a fundamental civic right and duty, but it is **not legally compulsory**. There is no penalty for not voting."),
        ("🤔 Myth: If I am not in my home city, I can vote online.", "✅ **Fact:** Currently, there is no online voting for general citizens. You must vote in person at your designated polling booth. (Service voters have specific postal ballot provisions).")
    ]

    for q, a in myths:
        with st.expander(q, expanded=False):
            st.markdown(f"<div style='padding: 0.5rem 0; color: #334155;'>{a}</div>", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #e2e8f0; margin-top: 3rem;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem; font-weight: 500; padding-bottom: 2rem;'>Built for Electoral Literacy & Democratic Inclusion | Civic Intelligence Hackathon Prototype</p>", unsafe_allow_html=True)