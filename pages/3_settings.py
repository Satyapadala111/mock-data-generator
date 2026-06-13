import streamlit as st

st.markdown('<div class="step-label">⬡ Settings & Configuration</div>', unsafe_allow_html=True)

# ── Hero-style header for the settings page ─────────────────────────────────
st.markdown("""
<div class="hero" style="padding:1.8rem 2rem;">
    <div class="badge">⚙️ Configuration Center</div>
    <h1 style="font-size:1.8rem;">Tune Your Agent</h1>
    <p>Control the LLM mode, review data sources, and check locale behavior — all in one place.</p>
</div>
""", unsafe_allow_html=True)

# ── LLM Configuration ─────────────────────────────────────────────────────────
st.markdown('<div class="schema-card">', unsafe_allow_html=True)
st.markdown("### 🤖 LLM Configuration")
# Fix: initialize session state BEFORE checkbox to avoid double-click bug
if "use_llm" not in st.session_state:
    st.session_state["use_llm"] = False

use_llm = st.checkbox(
    "Use Ollama LLM",
    key="use_llm",
    help="Enable if Ollama is installed locally on your machine."
)

if st.session_state["use_llm"]:
    st.markdown(
        '<div class="success-box">🟢 Ollama mode active — context-aware text generation enabled</div>',
        unsafe_allow_html=True
    )
    st.info(
        "Run these commands first to enable Ollama:\n\n"
        "```\nollama serve\nollama pull tinyllama\n```\n\n"
        "If Ollama isn't running, the app automatically falls back to Faker — generation never fails."
    )
else:
    st.markdown(
        '<div class="success-box" style="background:rgba(168,85,247,0.08);border-color:var(--accent1);color:#d8b4fe;">'
        '⚡ Faker mode active — fast, offline, zero-cost generation</div>',
        unsafe_allow_html=True
    )
    st.caption("Currently using **Faker** for all field generation (Free Tier). "
               "Enable Ollama above for context-aware AI-generated text fields.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Quick stats row (fills empty space, gives visual rhythm) ────────────────
m1, m2, m3 = st.columns(3)
m1.metric("LLM Mode", "Ollama" if st.session_state['use_llm'] else "Faker")
m2.metric("Default Locale", "en_IN 🇮🇳")
m3.metric("Data Source", "REST Countries API")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="schema-card">', unsafe_allow_html=True)
    st.markdown("### 🌐 External API")
    st.markdown(
        "**REST Countries API** is used to fetch live country and capital data.\n\n"
        "- No API key required\n"
        "- Automatically falls back to a built-in list of 50 countries if the API "
        "is unreachable\n"
        "- Used whenever your schema includes a `country`, `capital`, or `city` column"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="schema-card">', unsafe_allow_html=True)
    st.markdown("### 🇮🇳 Locale")
    st.markdown(
        "Faker is configured with the **en_IN** (Indian English) locale:\n\n"
        "- Names follow common Indian naming conventions\n"
        "- Phone numbers are 10-digit, starting with 6, 7, 8, or 9\n"
        "- Cities are matched with their correct country\n"
        "- Gender values are restricted to **Male / Female**"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

st.markdown('<div class="schema-card">', unsafe_allow_html=True)
st.markdown("### 🔁 Agent Loop Steps")
st.markdown("""
🔍 **PARSE** — Read schema columns & types
🌐 **API** — Fetch real countries & cities
🤖 **LLM** — Context-aware suggestions (if enabled above)
⚙️ **GENERATE** — Realistic rows via Faker
✅ **VALIDATE** — PK unique, min/max ranges
💾 **EXPORT** — CSV + SQL INSERT statements
""")
st.markdown('</div>', unsafe_allow_html=True)
