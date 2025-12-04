# streamlit_app/pages/2_📈_Curves.py

import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import fetch

st.title("📈 Forward Curves Dashboard")

market = st.selectbox("Market", ["TTF", "NBP", "JKM", "HH"])

data = fetch(f"/curves/{market.lower()}")

monthly = pd.DataFrame(data["monthly"])
daily = pd.DataFrame(data["daily"])

tab1, tab2 = st.tabs(["Monthly Curve", "Daily Curve"])

with tab1:
    st.subheader("Monthly Forward Curve")
    fig = px.line(monthly, x="month", y="price",
                  title=f"{market} Monthly Curve")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(monthly)

with tab2:
    st.subheader("Daily Interpolated Curve")
    fig = px.line(daily, x="date", y="price",
                  title=f"{market} Daily Curve (Interpolated)")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(daily)
