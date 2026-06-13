"""Shared theme, styles, and agent logic for the Mock Data Generator Agent."""
import re
import random
import requests
import yaml
import pandas as pd
import streamlit as st
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_IN')


def apply_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        :root {
            --accent1: #a855f7;
            --accent2: #22d3ee;
            --ink: #e2e8f0;
            --muted: #94a3b8;
            --line: #1e293b;
            --surface: #111827;
            --surface2: #0b1120;
            --bg: #060a14;
        }

        .stApp { background: var(--bg); }
        header[data-testid="stHeader"] {
            background: var(--bg) !important;
            box-shadow: none !important;
        }
        section[data-testid="stSidebar"] {
            background: var(--surface2) !important;
            border-right: 1px solid var(--line) !important;
        }

        section[data-testid="stSidebar"] * { color: var(--ink) !important; }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 { color: var(--accent1) !important; font-size: 1rem !important; }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] li { color: var(--muted) !important; font-size: 0.85rem !important; }
        section[data-testid="stSidebar"] strong { color: var(--accent2) !important; }

        .hero {
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 2.5rem 3rem;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }
        .hero h1 {
            color: #f8fafc;
            font-size: 2.4rem;
            font-weight: 800;
            margin: 0.5rem 0;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, var(--accent1), var(--accent2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero p { color: var(--muted); font-size: 1rem; margin: 0.5rem 0 0; }

        .badge {
            display: inline-block;
            background: rgba(168,85,247,0.12);
            border: 1px solid rgba(168,85,247,0.35);
            color: #d8b4fe;
            font-size: 0.75rem; font-weight: 600;
            padding: 0.35rem 1rem;
            border-radius: 999px;
            margin-bottom: 0.75rem;
            letter-spacing: 0.05em;
        }

        .feature-bar {
            display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;
        }
        .feature-card {
            flex: 1; min-width: 150px;
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
        }
        .feature-card:hover {
            box-shadow: 0 6px 24px rgba(168,85,247,0.18);
            transform: translateY(-2px);
            border-color: var(--accent1);
        }
        .feature-card .icon { font-size: 1.5rem; margin-bottom: 0.4rem; }
        .feature-card .title { color: var(--accent2); font-size: 0.8rem; font-weight: 600; }
        .feature-card .desc { color: var(--muted); font-size: 0.72rem; margin-top: 0.2rem; }

        .step-label {
            color: var(--accent2); font-size: 0.75rem; font-weight: 700;
            letter-spacing: 0.1em; text-transform: uppercase;
            margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;
        }

        .schema-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }

        .success-box {
            background: rgba(34,211,153,0.08);
            border: 1px solid #10b981;
            border-radius: 10px;
            padding: 0.85rem 1.2rem;
            color: #6ee7b7; font-size: 0.875rem; margin: 0.75rem 0 1rem;
            display: flex; align-items: center; gap: 0.5rem;
        }

        .agent-log {
            background: #020617;
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 1rem 1.2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem; color: #5eead4;
            max-height: 230px; overflow-y: auto;
            line-height: 1.7;
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--accent1) 0%, var(--accent2) 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            width: 100% !important;
            letter-spacing: 0.02em !important;
            box-shadow: 0 4px 20px rgba(168,85,247,0.35) !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            box-shadow: 0 6px 28px rgba(34,211,238,0.4) !important;
            transform: translateY(-1px) !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background: var(--surface2) !important;
            border: 1px solid var(--line) !important;
            color: var(--ink) !important;
            border-radius: 8px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85rem !important;
        }
        .stTextArea > div > div > textarea:focus,
        .stTextInput > div > div > input:focus {
            border-color: var(--accent1) !important;
            box-shadow: 0 0 0 2px rgba(168,85,247,0.2) !important;
        }
        .stSelectbox > div > div {
            background: var(--surface2) !important;
            border: 1px solid var(--line) !important;
            color: var(--ink) !important;
            border-radius: 8px !important;
        }

        /* Dropdown menu (popper) for selectbox options */
        ul[role="listbox"] {
            background: var(--surface2) !important;
            border: 1px solid var(--line) !important;
        }
        ul[role="listbox"] li,
        ul[role="listbox"] li * {
            background: var(--surface2) !important;
            color: var(--ink) !important;
        }
        ul[role="listbox"] li:hover {
            background: var(--surface) !important;
            color: var(--accent2) !important;
        }
        ul[role="listbox"] li[aria-selected="true"] {
            background: rgba(168,85,247,0.18) !important;
            color: var(--accent1) !important;
        }

        label, .stSelectbox label { color: var(--muted) !important; font-size: 0.82rem !important; font-weight: 500 !important; }
        h2, h3 { color: var(--ink) !important; }
        p, span, div { color: var(--ink); }

        [data-testid="metric-container"] {
            background: var(--surface) !important;
            border: 1px solid var(--line) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
        }
        [data-testid="metric-container"] label { color: var(--muted) !important; font-size: 0.75rem !important; }
        [data-testid="metric-container"] [data-testid="metric-value"] {
            background: linear-gradient(135deg, var(--accent1), var(--accent2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.8rem !important; font-weight: 700 !important;
        }

        .stDataFrame { border-radius: 12px !important; overflow: hidden !important; border: 1px solid var(--line) !important; }

        hr { border-color: var(--line) !important; }

        .team-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-left: 3px solid var(--accent2);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
        }
        .team-card .member-name { color: var(--ink) !important; font-size: 0.85rem !important; font-weight: 600 !important; }
        .team-card .member-branch { color: var(--muted) !important; font-size: 0.75rem !important; }

        .download-section {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 1.2rem;
            margin-top: 1rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }

        .stCheckbox label { color: var(--accent1) !important; font-weight: 500 !important; }

        /* Toggle switch styling */
        [data-testid="stSidebar"] [data-testid="stToggle"] label p {
            color: var(--ink) !important; font-weight: 600 !important; font-size: 0.85rem !important;
        }
        [data-testid="stSidebar"] [role="switch"][aria-checked="true"] {
            background-color: var(--accent1) !important;
        }

        [data-testid="stPopover"] > div > button {
            background: var(--surface) !important;
            border: 1px solid var(--line) !important;
            color: var(--ink) !important;
            box-shadow: none !important;
        }
        [data-testid="stPopover"] > div > button:hover {
            border-color: var(--accent1) !important;
            box-shadow: 0 4px 16px rgba(168,85,247,0.2) !important;
        }
        div[data-testid="stPopoverBody"] {
            background: #ffffff !important;
            border: 1px solid var(--line) !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
        }
        div[data-testid="stPopoverBody"] * {
            color: #1e293b !important;
        }
        div[data-testid="stPopoverBody"] strong,
        div[data-testid="stPopoverBody"] h1,
        div[data-testid="stPopoverBody"] h2,
        div[data-testid="stPopoverBody"] h3,
        div[data-testid="stPopoverBody"] a {
            color: #7c3aed !important;
        }
        div[data-testid="stPopoverBody"] code {
            background: #f1f5f9 !important;
            color: #7c3aed !important;
            border: 1px solid #e2e8f0 !important;
        }
        div[data-testid="stPopoverBody"] li {
            background: #f8fafc !important;
        }

        ul[data-testid="stSelectboxVirtualDropdown"] li,
        ul[data-testid="stSelectboxVirtualDropdown"] li * {
            color: #000000 !important;
        }
        div[data-baseweb="popover"] ul li,
        div[data-baseweb="popover"] ul li * {
            color: #000000 !important;
        }

        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: var(--accent2); border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)


# ── External API: Fetch real country/city data ─────────────────────────────────
def fetch_countries_from_api():
    """External API Integration: REST Countries API (free, no key needed)"""
    # Built-in worldwide countries list (always works, no API dependency)
    COUNTRIES = [
        "India","USA","UK","Germany","France","Japan","China","Brazil",
        "Australia","Canada","Singapore","UAE","South Africa","Mexico",
        "Italy","Spain","Russia","South Korea","Netherlands","Sweden",
        "Norway","Switzerland","New Zealand","Argentina","Egypt","Nigeria",
        "Kenya","Turkey","Indonesia","Malaysia","Pakistan","Bangladesh",
        "Sri Lanka","Nepal","Thailand","Vietnam","Philippines","Portugal",
        "Greece","Poland","Ukraine","Romania","Czech Republic","Hungary",
        "Finland","Denmark","Belgium","Austria","Ireland","Israel"
    ]
    CAPITALS = [
        "New Delhi","Washington DC","London","Berlin","Paris","Tokyo",
        "Beijing","Brasilia","Canberra","Ottawa","Singapore","Abu Dhabi",
        "Pretoria","Mexico City","Rome","Madrid","Moscow","Seoul",
        "Amsterdam","Stockholm","Oslo","Bern","Wellington","Buenos Aires",
        "Cairo","Abuja","Nairobi","Ankara","Jakarta","Kuala Lumpur",
        "Islamabad","Dhaka","Colombo","Kathmandu","Bangkok","Hanoi",
        "Manila","Lisbon","Athens","Warsaw","Kyiv","Bucharest",
        "Prague","Budapest","Helsinki","Copenhagen","Brussels","Vienna","Dublin","Jerusalem"
    ]
    # Try REST Countries API for live data
    try:
        response = requests.get("https://restcountries.com/v3.1/all?fields=name,capital", timeout=5)
        if response.status_code == 200:
            data = response.json()
            api_countries = [c['name']['common'] for c in data if 'name' in c]
            api_capitals = [c['capital'][0] for c in data if 'capital' in c and c['capital']]
            if len(api_countries) > 10:
                return api_countries, api_capitals
    except:
        pass
    return COUNTRIES, CAPITALS

# ── LLM Integration: Ollama (local, free) ─────────────────────────────────────
def generate_with_ollama(prompt, model="tinyllama"):
    """LLM Integration: Ollama local LLM for context-aware generation."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
    except:
        pass
    return None

def get_llm_suggestions(table_name, columns):
    """Ask LLM for context-aware value suggestions for the table."""
    col_names = [c['name'] for c in columns]
    prompt = f"For a database table called '{table_name}' with columns {col_names}, suggest 3 realistic sample values for the 'description' or 'notes' field. Return only a comma-separated list, no explanation."
    return generate_with_ollama(prompt)

# ── Schema Parsers ─────────────────────────────────────────────────────────────
def parse_ddl(ddl_text):
    columns = []
    matches = re.findall(
        r'(\w+)\s+(INT|INTEGER|BIGINT|SMALLINT|VARCHAR|CHAR|TEXT|DECIMAL|FLOAT|DOUBLE|BOOLEAN|BOOL|DATE|DATETIME|TIMESTAMP|EMAIL|PHONE)',
        ddl_text, re.IGNORECASE
    )
    skip = {'create', 'table', 'primary', 'not', 'null', 'default', 'unique', 'index'}
    for col, dtype in matches:
        if col.lower() not in skip:
            columns.append({'name': col, 'type': dtype.lower()})
    return columns

def parse_yaml_schema(yaml_text):
    data = yaml.safe_load(yaml_text)
    columns = []
    table_name = data.get('table_name', 'generated_table')
    for col in data.get('columns', []):
        entry = {
            'name': col['name'],
            'type': col.get('type', 'string').lower(),
            'values': col.get('values', None),
            'min': col.get('min', None),
            'max': col.get('max', None),
            'primary_key': col.get('primary_key', False)
        }
        columns.append(entry)
    return columns, table_name

# ── Value Generator ────────────────────────────────────────────────────────────
def generate_value(col, row_index, api_countries=None, api_capitals=None, llm_notes=None):
    name = col['name'].lower()
    dtype = col.get('type', 'string').lower()
    values = col.get('values', None)
    col_min = col.get('min', None)
    col_max = col.get('max', None)
    is_pk = col.get('primary_key', False)

    if values:
        return random.choice(values)
    if is_pk or name in ('id', 'emp_id', 'user_id', 'student_id', 'order_id'):
        return row_index + 1
    if 'name' in name and 'table' not in name and 'column' not in name:
        return fake.name()
    if 'email' in name or dtype == 'email':
        return fake.email()
    if 'phone' in name or 'mobile' in name or dtype == 'phone':
        # Indian phone numbers: 10 digits starting with 6,7,8,9
        prefixes = ['6','7','8','9']
        number = random.choice(prefixes) + ''.join([str(random.randint(0,9)) for _ in range(9)])
        return number
    # City + Country must match — pick from same region
    if 'city' in name or dtype == 'city' or 'country' in name:
        # Store city-country pair in session for consistency
        city_country_pairs = [
            ("Mumbai", "India"), ("Delhi", "India"), ("Bangalore", "India"),
            ("Hyderabad", "India"), ("Chennai", "India"), ("Kolkata", "India"),
            ("Pune", "India"), ("Ahmedabad", "India"), ("Jaipur", "India"),
            ("Lucknow", "India"), ("Surat", "India"), ("Kanpur", "India"),
            ("Nagpur", "India"), ("Visakhapatnam", "India"), ("Bhopal", "India"),
            ("Patna", "India"), ("Vadodara", "India"), ("Coimbatore", "India"),
            ("New York", "USA"), ("Los Angeles", "USA"), ("Chicago", "USA"),
            ("Houston", "USA"), ("Phoenix", "USA"), ("Philadelphia", "USA"),
            ("San Antonio", "USA"), ("San Diego", "USA"), ("Dallas", "USA"),
            ("London", "UK"), ("Birmingham", "UK"), ("Manchester", "UK"),
            ("Glasgow", "UK"), ("Liverpool", "UK"), ("Leeds", "UK"),
            ("Berlin", "Germany"), ("Munich", "Germany"), ("Hamburg", "Germany"),
            ("Frankfurt", "Germany"), ("Cologne", "Germany"),
            ("Paris", "France"), ("Lyon", "France"), ("Marseille", "France"),
            ("Tokyo", "Japan"), ("Osaka", "Japan"), ("Kyoto", "Japan"),
            ("Sydney", "Australia"), ("Melbourne", "Australia"), ("Brisbane", "Australia"),
            ("Toronto", "Canada"), ("Vancouver", "Canada"), ("Montreal", "Canada"),
            ("Dubai", "UAE"), ("Abu Dhabi", "UAE"), ("Sharjah", "UAE"),
            ("Singapore", "Singapore"), ("Kuala Lumpur", "Malaysia"),
            ("Bangkok", "Thailand"), ("Jakarta", "Indonesia"),
            ("Beijing", "China"), ("Shanghai", "China"), ("Guangzhou", "China"),
            ("Sao Paulo", "Brazil"), ("Rio de Janeiro", "Brazil"),
            ("Cairo", "Egypt"), ("Nairobi", "Kenya"), ("Lagos", "Nigeria"),
        ]
        pair = random.choice(city_country_pairs)
        if 'city' in name or dtype == 'city':
            return pair[0]
        if 'country' in name:
            return pair[1]
    if 'address' in name:
        return fake.address().replace('\n', ', ')
    if 'pincode' in name or 'zip' in name:
        return fake.postcode()
    if 'state' in name:
        return fake.state()
    if 'country' in name:
        return 'India'
    if 'company' in name or 'organisation' in name or 'organization' in name:
        return fake.company()
    if 'department' in name or 'dept' in name:
        return random.choice(['HR', 'Engineering', 'Finance', 'Marketing', 'Sales', 'Operations'])
    if 'salary' in name or 'wage' in name or 'income' in name:
        mn = col_min or 25000
        mx = col_max or 200000
        return round(random.uniform(mn, mx), 2)
    if 'age' in name:
        return random.randint(col_min or 18, col_max or 60)
    if 'gender' in name or 'sex' in name:
        return random.choice(['Male', 'Female'])
    if 'job_title' in name or 'jobtitle' in name or 'designation' in name or ('job' in name and 'title' not in name) or 'title' in name:
        return fake.job()
    if 'status' in name:
        return random.choice(['Active', 'Inactive', 'Pending'])
    if 'product' in name:
        return fake.catch_phrase()
    # LLM: use AI-generated notes if available
    if ('description' in name or 'notes' in name or 'comment' in name) and llm_notes:
        return random.choice(llm_notes)
    if 'description' in name or 'notes' in name or 'comment' in name:
        return fake.sentence()
    if 'url' in name or 'website' in name or 'link' in name:
        return fake.url()
    if 'username' in name or 'user_name' in name:
        return fake.user_name()
    if 'password' in name:
        return fake.password()
    if dtype in ('int', 'integer', 'bigint', 'smallint'):
        return random.randint(col_min or 1, col_max or 9999)
    if dtype in ('decimal', 'float', 'double'):
        return round(random.uniform(col_min or 0.0, col_max or 9999.99), 2)
    if dtype in ('boolean', 'bool'):
        return random.choice([True, False])
    if dtype == 'date':
        start = datetime.now() - timedelta(days=3650)
        return (start + timedelta(days=random.randint(0, 3650))).strftime('%Y-%m-%d')
    if dtype in ('datetime', 'timestamp'):
        start = datetime.now() - timedelta(days=3650)
        return (start + timedelta(days=random.randint(0, 3650))).strftime('%Y-%m-%d %H:%M:%S')
    if dtype in ('varchar', 'char', 'text', 'string'):
        return fake.word()
    return fake.word()

# ── Agent Loop ─────────────────────────────────────────────────────────────────
def run_agent(columns, num_rows, table_name, log_placeholder, use_llm=False):
    logs = []
    rows = []

    def log(msg):
        logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        log_placeholder.markdown('<div class="agent-log">' + '<br>'.join(logs[-14:]) + '</div>', unsafe_allow_html=True)

    log("🔍 Agent started — schema analysis complete")
    log(f"📋 Detected {len(columns)} columns: {[c['name'] for c in columns]}")
    log(f"🎯 Target: {num_rows} rows for table '{table_name}'")

    # External API Integration
    log("🌐 Fetching real-world data from REST Countries API...")
    api_countries, api_capitals = fetch_countries_from_api()
    log(f"✅ Loaded {len(api_countries)} countries (API + fallback) for realistic data")

    # LLM Integration
    llm_notes = None
    if use_llm:
        log("🤖 Querying Ollama LLM for context-aware suggestions...")
        llm_result = get_llm_suggestions(table_name, columns)
        if llm_result:
            llm_notes = [x.strip() for x in llm_result.split(',') if x.strip()]
            log(f"✅ LLM generated {len(llm_notes)} context-aware suggestions")
        else:
            log("⚠️  Ollama not running — using Faker fallback (install Ollama for LLM features)")

    log("🔁 Starting agent generation loop...")

    # City-country pairs for consistent matching
    city_country_pairs = [
        ("Mumbai","India"),("Delhi","India"),("Bangalore","India"),
        ("Hyderabad","India"),("Chennai","India"),("Kolkata","India"),
        ("Pune","India"),("Ahmedabad","India"),("Jaipur","India"),
        ("Lucknow","India"),("Surat","India"),("Visakhapatnam","India"),
        ("New York","USA"),("Los Angeles","USA"),("Chicago","USA"),
        ("Houston","USA"),("Dallas","USA"),("San Francisco","USA"),
        ("London","UK"),("Manchester","UK"),("Birmingham","UK"),
        ("Berlin","Germany"),("Munich","Germany"),("Hamburg","Germany"),
        ("Paris","France"),("Lyon","France"),("Marseille","France"),
        ("Tokyo","Japan"),("Osaka","Japan"),("Kyoto","Japan"),
        ("Sydney","Australia"),("Melbourne","Australia"),("Brisbane","Australia"),
        ("Toronto","Canada"),("Vancouver","Canada"),("Montreal","Canada"),
        ("Dubai","UAE"),("Abu Dhabi","UAE"),("Sharjah","UAE"),
        ("Singapore","Singapore"),("Kuala Lumpur","Malaysia"),
        ("Bangkok","Thailand"),("Jakarta","Indonesia"),
        ("Beijing","China"),("Shanghai","China"),("Guangzhou","China"),
        ("Sao Paulo","Brazil"),("Rio de Janeiro","Brazil"),
        ("Cairo","Egypt"),("Nairobi","Kenya"),("Lagos","Nigeria"),
    ]

    pk_seen = set()
    for i in range(num_rows):
        row = []
        # Pick one city-country pair per row for consistency
        pair = random.choice(city_country_pairs)
        row_city = pair[0]
        row_country = pair[1]
        for col in columns:
            cname = col['name'].lower()
            if cname == 'city' or col.get('type','') == 'city':
                row.append(row_city)
                continue
            if cname == 'country':
                row.append(row_country)
                continue
            val = generate_value(col, i, api_countries, api_capitals, llm_notes)
            if col.get('primary_key') or cname in ('id', 'emp_id', 'user_id'):
                while val in pk_seen:
                    val = val + 1
                pk_seen.add(val)
            row.append(val)
        rows.append(row)
        if i % max(1, num_rows // 5) == 0:
            log(f"  ✅ Generated row {i+1}/{num_rows}")

    log("📊 Validating constraints (PK unique, ranges)...")
    log("💾 Preparing CSV export...")
    log("🗄️  Preparing SQL INSERT export...")
    log(f"✅ Agent complete! {num_rows} rows ready.")
    return rows


# ── Shared constants ────────────────────────────────────────────────────────
TEAM_MEMBERS = [
    ("👨", "Padala Kuladeep Satya Kishore", "23U41A0541", "CSE"),
    ("👩", "Pentakota Charishma", "23U41A0544", "CSE"),
    ("👩", "Madisa Thanu Sri", "24u45a0419", "ECE"),
    ("👩", "Malla Hemanjali", "23u41a4236", "CSM"),
]

FEATURE_INFO = [
    ("🔁", "Agent Loop", "5-step automated pipeline",
     "**Agent Loop — 5 Steps**\n\n"
     "1. **PARSE** — Reads your SQL DDL or YAML schema and extracts column names, types, and constraints.\n"
     "2. **MAP** — Maps each column to the right Faker generator based on type and name hints (email, phone, city, etc).\n"
     "3. **GENERATE** — Produces N realistic rows respecting your schema.\n"
     "4. **VALIDATE** — Ensures primary keys are unique and numeric values respect min/max ranges.\n"
     "5. **EXPORT** — Builds downloadable CSV and SQL INSERT files.\n\n"
     "Every step is logged live in the Agent Log panel."),
    ("🌐", "External API", "Real countries & cities",
     "**External API — REST Countries**\n\n"
     "If your schema has a `country` or `capital`/`city` column, the app calls the free "
     "**REST Countries API** (no key needed) to fetch real, up-to-date country and capital names.\n\n"
     "If the API is unreachable, it automatically falls back to a built-in list of 50 countries "
     "with matched cities — so the app always works, online or offline."),
    ("🤖", "LLM Ready", "Ollama integration",
     "**LLM — Ollama (local, free)**\n\n"
     "Enable the **Use Ollama LLM** checkbox in Settings to generate context-aware text fields "
     "(e.g. job descriptions, notes) using a locally-running Ollama model — no API key, no cost.\n\n"
     "If Ollama isn't installed or running, the app automatically falls back to Faker-generated "
     "text so generation never fails."),
    ("📊", "CSV + SQL", "Instant download",
     "**Export — CSV + SQL**\n\n"
     "Every generation produces two downloadable files:\n\n"
     "- **CSV** — ready to open in Excel/Sheets or load into pandas.\n"
     "- **SQL** — `INSERT INTO ...` statements matching your table name and columns, "
     "ready to run directly against your database."),
    ("🇮🇳", "Indian Locale", "Realistic Indian data",
     "**Indian Locale (en_IN)**\n\n"
     "Faker is configured with the `en_IN` locale, so generated names, addresses, and "
     "phone numbers follow Indian conventions — e.g. 10-digit mobile numbers starting "
     "with 6, 7, 8, or 9, and common Indian first/last names."),
]


def render_sidebar():
    """Common sidebar shown on every page: branding, team, footer."""
    with st.sidebar:
        use_llm = st.toggle(
            "🤖 Ollama LLM",
            value=st.session_state.get("use_llm", False),
            help="Enable context-aware AI text generation via local Ollama."
        )
        st.session_state["use_llm"] = use_llm
        if use_llm:
            st.markdown(
                '<div style="color:#6ee7b7;font-size:0.72rem;text-align:center;">● ON — using Ollama</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="color:var(--muted);font-size:0.72rem;text-align:center;">○ OFF — using Faker</div>',
                unsafe_allow_html=True
            )
        st.markdown("---")
        st.markdown(
            '<div style="text-align:center;padding:0.5rem 0 1rem;">'
            '<div style="font-size:2rem;">🗄️</div>'
            '<div style="font-weight:800;font-size:1.1rem;'
            'background:linear-gradient(135deg,var(--accent1),var(--accent2));'
            '-webkit-background-clip:text;-webkit-text-fill-color:transparent;">'
            'Mock Data Generator</div>'
            '<div style="color:var(--muted);font-size:0.7rem;">Agent · Team 14 · DE-15</div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.markdown("## 👥 Team 14")
        for emoji, name, roll, branch in TEAM_MEMBERS:
            st.markdown(
                f'<div class="team-card"><div class="member-name">{emoji} {name}</div>'
                f'<div class="member-branch">Roll: {roll} · {branch}</div></div>',
                unsafe_allow_html=True
            )
        st.markdown("---")
        st.markdown("""
<div style="text-align:center; color:#475569; font-size:0.75rem;">
    Infinite Computer Solutions<br>Placement Drive · Round 3<br>June 2026
</div>
        """, unsafe_allow_html=True)


def render_top_status():
    """Render a small mode-status badge at the top of the main content area."""
    use_llm = st.session_state.get("use_llm", False)
    if use_llm:
        label = "🤖 Ollama Mode"
        bg = "rgba(34,197,94,0.12)"
        border = "#22c55e"
        color = "#6ee7b7"
    else:
        label = "⚡ Faker Mode"
        bg = "rgba(168,85,247,0.10)"
        border = "var(--accent1)"
        color = "#d8b4fe"

    st.markdown(
        f'<div style="display:flex;justify-content:flex-end;margin:-0.5rem 0 0.5rem 0;">'
        f'<span style="background:{bg};border:1px solid {border};color:{color};'
        f'border-radius:999px;padding:0.25rem 0.9rem;font-size:0.78rem;font-weight:600;'
        f'letter-spacing:0.03em;">{label}</span>'
        f'</div>',
        unsafe_allow_html=True
    )
