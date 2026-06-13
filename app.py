import streamlit as st
from common import apply_theme, render_sidebar, render_top_status

st.set_page_config(page_title="Mock Data Generator Agent", page_icon="🗄️", layout="wide")
apply_theme()

dashboard = st.Page("pages/1_dashboard.py", title="Dashboard", icon="📊", default=True)
generate = st.Page("pages/2_generate.py", title="Generate", icon="⚡")
settings = st.Page("pages/3_settings.py", title="Settings", icon="⚙️")

pg = st.navigation([dashboard, generate, settings])
render_sidebar()
render_top_status()
pg.run()
