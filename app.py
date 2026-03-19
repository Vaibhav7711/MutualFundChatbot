# ==========================================
# MUTUAL FUND CHATBOT WEB APP — PROFESSIONAL UI
# ==========================================

import streamlit as st
from rag_mf import build_vector_store, ask_question

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PPFAS MF Assistant",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root & Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #F7F6F2;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0F1923;
    border-right: 1px solid #1E2D3D;
}
[data-testid="stSidebar"] * {
    color: #C8D6E5 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-family: 'DM Serif Display', serif !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #1E2D3D;
    border: 1px solid #2E4057;
    color: #FFFFFF !important;
    border-radius: 8px;
}

/* ── Main header ── */
.main-header {
    padding: 2.5rem 0 1rem 0;
    border-bottom: 2px solid #0F1923;
    margin-bottom: 2rem;
}
.main-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #0F1923;
    margin: 0;
    line-height: 1.2;
}
.main-header p {
    color: #6B7A8D;
    font-size: 0.95rem;
    margin: 0.4rem 0 0 0;
    font-weight: 300;
}

/* ── Scheme badge ── */
.scheme-badge {
    display: inline-block;
    background: #0F1923;
    color: #F7F6F2 !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
}

/* ── Welcome card ── */
.welcome-card {
    background: #FFFFFF;
    border: 1px solid #E2DDD5;
    border-left: 4px solid #0F1923;
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.5rem;
}
.welcome-card h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #0F1923;
    margin: 0 0 0.8rem 0;
}
.welcome-card p {
    color: #6B7A8D;
    font-size: 0.88rem;
    margin: 0 0 1rem 0;
    line-height: 1.6;
}

/* ── Example question pills ── */
.example-questions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.eq-pill {
    background: #F0EDE6;
    border: 1px solid #D5CFC4;
    color: #0F1923;
    font-size: 0.82rem;
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border: 1px solid #E2DDD5;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 1px 3px rgba(15,25,35,0.06);
}
[data-testid="stChatMessage"][data-testid*="user"] {
    background: #0F1923;
    border-color: #0F1923;
}
[data-testid="stChatMessage"][data-testid*="user"] p {
    color: #F7F6F2 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border: 2px solid #0F1923 !important;
    border-radius: 10px !important;
    background: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #2E7D52 !important;
    box-shadow: 0 0 0 3px rgba(46,125,82,0.12) !important;
}

/* ── Disclaimer ── */
.disclaimer-box {
    background: #FFF8E7;
    border: 1px solid #F0D080;
    border-left: 4px solid #D4A017;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-top: 1.5rem;
}
.disclaimer-box p {
    color: #5A4A1A;
    font-size: 0.82rem;
    margin: 0;
    line-height: 1.6;
}
.disclaimer-box strong {
    color: #3A2E0A;
    font-weight: 600;
}

/* ── Divider ── */
hr {
    border: none;
    border-top: 1px solid #E2DDD5;
    margin: 1.5rem 0;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #2E7D52 !important;
}

/* ── Source links in responses ── */
.stChatMessage a {
    color: #2E7D52 !important;
    font-weight: 500;
    text-decoration: underline;
}

/* ── Sidebar nav items ── */
.sidebar-section {
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1E2D3D;
}
.sidebar-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4A6080 !important;
    margin-bottom: 0.5rem;
}
.sidebar-info {
    font-size: 0.82rem;
    color: #8099B0 !important;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD VECTOR DATABASE
# ==========================================

@st.cache_resource
def load_database():
    return build_vector_store()

collection = load_database()

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("""
        <div style='padding: 1.5rem 0 0.5rem 0;'>
            <div style='font-family: DM Serif Display, serif; font-size: 1.4rem; color: #FFFFFF; line-height: 1.3;'>
                PPFAS MF<br>Assistant
            </div>
            <div style='font-size: 0.75rem; color: #4A6080; margin-top: 0.3rem; letter-spacing: 0.05em;'>
                Powered by Gemini · RAG
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-label' style='margin-top:2rem;'>Select Scheme</div>", unsafe_allow_html=True)

    scheme_map = {
        "Parag Parikh Liquid Fund": "PPLF",
        "Parag Parikh Flexi Cap Fund": "PPFCF",
        "Parag Parikh ELSS Tax Saver Fund": "PPTSF"
    }

    scheme_name = st.selectbox(
        "scheme",
        list(scheme_map.keys()),
        label_visibility="collapsed"
    )
    scheme_code = scheme_map[scheme_name]

    st.markdown("""
        <div class='sidebar-section'>
            <div class='sidebar-label'>About</div>
            <div class='sidebar-info'>
                Answers factual questions from official PPFAS factsheets and scheme documents.<br><br>
                <strong style='color:#8099B0;'>Data source:</strong> PPFAS AMC<br>
                <strong style='color:#8099B0;'>Last updated:</strong> Feb 2026<br>
                <strong style='color:#8099B0;'>Schemes:</strong> PPLF · PPFCF · PPTSF
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='sidebar-section'>
            <div class='sidebar-label'>Scope</div>
            <div class='sidebar-info'>
                ✓ Expense ratio<br>
                ✓ Exit load<br>
                ✓ AUM & NAV<br>
                ✓ Benchmark<br>
                ✓ Riskometer<br>
                ✓ Holdings & quantity<br>
                ✗ Investment advice<br>
                ✗ Return comparisons
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# MAIN AREA — HEADER
# ==========================================

st.markdown(f"""
<div class='main-header'>
    <h1>Mutual Fund<br>FAQ Assistant</h1>
    <p>Factual answers from official PPFAS scheme documents · No investment advice</p>
</div>
<div class='scheme-badge'>Currently viewing: {scheme_name}</div>
""", unsafe_allow_html=True)

# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# WELCOME CARD (shown only when no messages)
# ==========================================

if not st.session_state.messages:
    st.markdown("""
    <div class='welcome-card'>
        <h3>👋 How can I help?</h3>
        <p>
            Ask me anything factual about the selected PPFAS scheme — expense ratios,
            exit loads, holdings, benchmark, riskometer, and more.
            Every answer includes a source link.
        </p>
        <div class='sidebar-label'>Try asking</div>
        <div class='example-questions'>
            <span class='eq-pill'>What is the expense ratio?</span>
            <span class='eq-pill'>What is the exit load?</span>
            <span class='eq-pill'>What is the riskometer level?</span>
            <span class='eq-pill'>What is the benchmark index?</span>
            <span class='eq-pill'>What is the minimum SIP amount?</span>
            <span class='eq-pill'>What is the ELSS lock-in period?</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# RENDER CHAT HISTORY
# ==========================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# USER INPUT
# ==========================================

user_input = st.chat_input("Ask a factual question about the selected scheme...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching factsheet..."):
            response = ask_question(collection, user_input, scheme_code)
            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ==========================================
# DISCLAIMER
# ==========================================

st.markdown("""
<div class='disclaimer-box'>
    <p>
        <strong>⚠ Facts only. No investment advice.</strong>
        This assistant provides factual information extracted from official PPFAS Mutual Fund
        scheme documents and factsheets. It does not provide investment advice, return projections,
        or fund recommendations. For investment decisions, consult a SEBI-registered financial advisor.
        Sources are linked in every answer. Last updated from sources: <strong>February 2026</strong>.
    </p>
</div>
""", unsafe_allow_html=True)