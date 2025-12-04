import streamlit as st
from config import settings

st.set_page_config(
    page_title="Energy Analytics Platform",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Energy Analytics Platform")
st.markdown(f"Connected to API: `{settings.API_URL}`")

st.markdown("""
Welcome to your **full-stack energy analytics platform**.

Use the sidebar to explore:
- 📦 Storage dashboards (AGSI, ALSI, EIA)
- 📈 Forward curves + interpolated curves
- 🚢 Shipping analytics (AIS, ETA, floating storage)
- 🔧 Regression models
- 🔥 Market analytics (ICE, CME, Yahoo, Weather)
""")

st.sidebar.title("Navigation")
st.sidebar.page_link("pages/1_📦_Storage.py", label="📦 Storage")
st.sidebar.page_link("pages/2_📈_Curves.py", label="📈 Curves")
st.sidebar.page_link("pages/3_🚢_Shipping.py", label="🚢 Shipping")
st.sidebar.page_link("pages/4_🔧_Regression.py", label="🔧 Regression")
st.sidebar.page_link("pages/5_🔥_Market.py", label="🔥 Market")
