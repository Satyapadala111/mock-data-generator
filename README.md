# 🤖 Mock Data Generator Agent
### Team 14 | UC ID: DE-15 | Data Engineering Category
### Infinite Computer Solutions Placement Drive | Round 3 | June 2026

---

## 👥 Team Members
| Name | Roll No | Branch |
|---|---|---|
| Padala Kuladeep Satya Kishore | 23U41A0541 | CSE |
| Pentakota Charishma | 23U41A0544 | CSE |
| Madisa Thanu Sri | 24u45a0419 | ECE |
| Malla Hemanjali | 23u41a4236 | CSM |

---

## 📌 Problem Statement
Realistic test data is hard to produce manually. Developers and QA engineers waste hours crafting fake datasets that still don't reflect real-world patterns or schema constraints.

## ✅ Solution
An AI-powered web application that takes a database schema (SQL DDL or YAML) and runs an **Agent Loop** to generate N rows of realistic mock data using the **Faker** library, enriched with real country/city data from the free **REST Countries API**. Outputs **CSV** + **SQL INSERT statements** — fully free and open-source, with automatic offline fallback if the API is unreachable.

---

## 🤖 AI Capabilities Demonstrated: Agent Loop + External API Integration

The application implements a **5-step Agent Loop**:

```
Step 1: PARSE    → Read schema (DDL or YAML), extract columns & types
Step 2: MAP      → Map each column type to a Faker generator
Step 3: GENERATE → Produce N realistic rows using Faker + constraints
Step 4: VALIDATE → Ensure PK uniqueness, respect min/max ranges
Step 5: EXPORT   → Write CSV + SQL INSERT statements
```

Each step is logged in real-time in the UI agent log panel.

### External API Integration
The agent calls the free **REST Countries API** (`restcountries.com`) to fetch real, up-to-date country and capital names — used whenever the schema includes a `country`, `capital`, or `city` column. No API key required. If the API is unreachable, the app automatically falls back to a built-in list of 50 countries with matched cities, so generation never fails.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit Web UI                    │
│  ┌──────────────┐         ┌───────────────────────┐  │
│  │ Schema Input │         │   Agent Log (live)    │  │
│  │ (DDL/YAML)   │         │   Results Table       │  │
│  │ Row Count    │         │   CSV Download        │  │
│  └──────┬───────┘         │   SQL Download        │  │
│         │                 └───────────────────────┘  │
└─────────┼───────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│                  Agent Loop Engine                   │
│                                                      │
│  parse_ddl() / parse_yaml_schema()                  │
│         ↓                                            │
│  generate_value(col, row_index)                     │
│    ├── Column name hints (email, phone, city...)    │
│    ├── Data type mapping (int, decimal, date...)    │
│    └── Constraint respect (min, max, values[])     │
│         ↓                                            │
│  run_agent() → validate → rows[]                    │
│         ↓                                            │
│  pd.DataFrame → CSV + SQL INSERT                    │
└─────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│              Faker (en_IN locale)                    │
│  fake.name(), fake.email(), fake.phone_number()     │
│  fake.city(), fake.address(), fake.company()...     │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack
| Tool | Purpose | Cost |
|---|---|---|
| Python 3.9+ | Core language | Free |
| Streamlit | Web UI | Free |
| Faker | Realistic fake data (Indian locale) | Free/OSS |
| Pandas | Data handling & CSV export | Free/OSS |
| PyYAML | YAML schema parsing | Free/OSS |
| pytest | Test cases | Free/OSS |
| GitHub | Source control & submission | Free |

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/Satyapadala111/mock-data-generator.git
cd mock-data-generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python -m streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## 🧪 Running Tests
```bash
pytest tests/test_agent.py -v
```

Expected output: **All tests pass ✅**

---

## 📁 Project Structure
```
mock-data-generator/
├── app.py                      # Entry point — theme + page navigation
├── common.py                   # Shared CSS theme, Agent Loop, parsers, generators
├── pages/
│   ├── 1_dashboard.py          # Dashboard — overview, feature info, stats
│   ├── 2_generate.py           # Generate — schema input, agent run, results
│   └── 3_settings.py           # Settings — Ollama LLM toggle, config info
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── samples/
│   ├── sample_schema.sql       # Example SQL DDL schemas
│   ├── sample_schema.yaml      # Example YAML schema
│   └── expected_output.csv     # Sample generated output
├── tests/
│   └── test_agent.py           # pytest test cases (20+ tests)
└── docs/
    └── AI_Usage_Note.md         # AI tools usage documentation
```

---

## 💡 How to Use

### SQL DDL Schema
```sql
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(15),
    gender VARCHAR(10),
    job_title VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    city VARCHAR(50),
    country VARCHAR(50),
    is_active BOOLEAN
);
```

### YAML Schema
```yaml
table_name: employees
columns:
  - name: id
    type: integer
    primary_key: true
  - name: gender
    type: string
    values: [Male, Female]
  - name: job_title
    type: string
  - name: department
    type: string
    values: [HR, Engineering, Finance]
  - name: salary
    type: decimal
    min: 30000
    max: 200000
  - name: city
    type: city
  - name: country
    type: string
```

---

## ⚠️ Assumptions & Limitations

- Supports column types: INT, VARCHAR, DECIMAL, BOOLEAN, DATE, DATETIME, TEXT, FLOAT
- Column name hints improve generation quality (e.g., columns named `email` auto-generate emails)
- Maximum 500 rows per generation
- Indian locale (en_IN) used for Faker — names, phone numbers, cities are India-specific
- Uses the free **REST Countries API** for live country/capital data (no API key needed); automatically falls back to a built-in list of 50 countries if unreachable — works online or offline

---

## 📹 Demo Video
🎥 Demo video will be added here after recording.

🚀 **Live App:** [Click here to open](https://mock-data-generator-team14.streamlit.app/)

---

*Submitted for Infinite Computer Solutions Placement Drive — Round 3 Case Study*
*College: DIET | Submission Deadline: June 14, 2026, 7:00 PM*
