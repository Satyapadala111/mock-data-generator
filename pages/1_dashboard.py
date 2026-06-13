import streamlit as st
from common import FEATURE_INFO

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">🤖 Agent Loop &nbsp;·&nbsp; LLM &nbsp;·&nbsp; External API &nbsp;·&nbsp; Team 14 &nbsp;·&nbsp; DE-15</div>
    <h1>🗄️ Mock Data Generator Agent</h1>
    <p>Schema in (DDL or YAML) → AI Agent generates realistic rows → Export CSV + SQL</p>
</div>
""", unsafe_allow_html=True)

# ── Feature Bar (clickable info cards) ──────────────────────────────────────
fcols = st.columns(len(FEATURE_INFO))
for fcol, (icon, title, desc, detail) in zip(fcols, FEATURE_INFO):
    with fcol:
        with st.popover(f"{icon}  {title}", use_container_width=True):
            st.markdown(detail)
        st.markdown(f'<div style="text-align:center;color:var(--muted);font-size:0.72rem;margin-top:-0.5rem;">{desc}</div>', unsafe_allow_html=True)

# ── Stats Row ─────────────────────────────────────────────────────────────────
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)
s1.metric("Agent Steps", "5")
s2.metric("Countries Available", "50+")
s3.metric("Export Formats", "2 (CSV/SQL)")
s4.metric("Locale", "en_IN 🇮🇳")
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── Highlight Cards (fills empty space) ─────────────────────────────────────
h1, h2 = st.columns(2)
with h1:
    st.markdown(
        '<div class="schema-card" style="text-align:center;">'
        '<div style="font-size:1.8rem;">🧬</div>'
        '<div style="color:var(--accent2);font-weight:700;font-size:0.95rem;margin-top:0.3rem;">Smart Column Detection</div>'
        '<div style="color:var(--muted);font-size:0.78rem;margin-top:0.3rem;">Automatically maps name, email, phone, gender, job title, salary, city, country and more from your schema.</div>'
        '</div>',
        unsafe_allow_html=True
    )
with h2:
    st.markdown(
        '<div class="schema-card" style="text-align:center;">'
        '<div style="font-size:1.8rem;">🚀</div>'
        '<div style="color:var(--accent2);font-weight:700;font-size:0.95rem;margin-top:0.3rem;">Zero Setup Required</div>'
        '<div style="color:var(--muted);font-size:0.78rem;margin-top:0.3rem;">No API keys, no database connections — runs fully offline with Faker, with optional Ollama LLM boost.</div>'
        '</div>',
        unsafe_allow_html=True
    )

# ── How It Works / Agent Loop Steps ─────────────────────────────────────────────
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="schema-card">', unsafe_allow_html=True)
    st.markdown("### 📖 How It Works")
    st.markdown("""
1. **Paste** your schema (DDL or YAML) on the Generate page
2. **Set** the number of rows
3. **Click** Generate Mock Data
4. **Download** CSV + SQL file
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="schema-card">', unsafe_allow_html=True)
    st.markdown("### 🔁 Agent Loop Steps")
    st.markdown("""
🔍 **PARSE** — Read schema columns & types
🌐 **API** — Fetch real countries & cities
🤖 **LLM** — Context-aware suggestions
⚙️ **GENERATE** — Realistic rows via Faker
✅ **VALIDATE** — PK unique, min/max ranges
💾 **EXPORT** — CSV + SQL INSERT statements
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

if st.button("⚡ Go to Generate Page", use_container_width=True):
    st.switch_page("pages/2_generate.py")
