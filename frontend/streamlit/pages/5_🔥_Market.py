# streamlit_app/pages/5_🔥_Market.py

import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import fetch

st.title("🔥 Market Dashboard")

tab1, tab2, tab3 = st.tabs(["ICE/CME Futures", "Yahoo Finance", "Weather Demand"])

# ===================================================================
# 1️⃣ ICE + CME Futures Tab
# API: /market/futures
# ===================================================================
with tab1:
    st.subheader("ICE / CME Futures Curve")

    try:
        df = pd.DataFrame(fetch("/market/futures"))

        if df.empty:
            st.warning("No futures data available.")
        else:
            fig = px.line(
                df,
                x="expiry",
                y="price",
                color="contract",
                title="Forward Curve — ICE/CME Futures"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading futures: {e}")

# ===================================================================
# 2️⃣ Yahoo Finance Prices
# API: /market/yahoo?symbol=NG=F
# ===================================================================
with tab2:
    st.subheader("Yahoo Finance Market Data")

    symbol = st.text_input("Symbol", value="NG=F")  # Natural Gas Futures

    try:
        df = pd.DataFrame(fetch(f"/market/yahoo?symbol={symbol}"))

        if df.empty:
            st.warning("No Yahoo Finance data available.")
        else:
            fig = px.line(
                df,
                x="date",
                y="close",
                title=f"{symbol} Price History"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading Yahoo Finance data: {e}")

# ===================================================================
# 3️⃣ Weather Demand (HDD/CDD)
# API: /market/weather
# ===================================================================
with tab3:
    st.subheader("Weather Demand (HDD / CDD)")

    try:
        df = pd.DataFrame(fetch("/market/weather"))

        if df.empty:
            st.warning("No weather data available.")
        else:
            fig = px.bar(
                df,
                x="date",
                y="hdd",
                title="Heating Degree Days (HDD)"
            )
            st.plotly_chart(fig, use_container_width=True)

            if "cdd" in df.columns:
                fig2 = px.bar(
                    df,
                    x="date",
                    y="cdd",
                    title="Cooling Degree Days (CDD)"
                )
                st.plotly_chart(fig2, use_container_width=True)

            st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading weather demand: {e}")
