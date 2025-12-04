# streamlit_app/pages/1_📦_Storage.py

import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import fetch

st.title("📦 Storage Dashboard")

tab1, tab2, tab3 = st.tabs(["EU Gas (AGSI+)", "EU LNG (ALSI)", "US Storage (EIA)"])

# ---------------------------------------------------------
# AGSI+ Europe Gas Storage
# ---------------------------------------------------------
with tab1:
    st.subheader("AGSI+ Europe Gas Storage")

    df = pd.DataFrame(fetch("/storage/agsi?country=EU"))

    if df.empty:
        st.warning("No AGSI storage data returned.")
    else:
        fig = px.line(df, x="date", y="full_pct",
                      title="EU Gas Storage — % Full")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(
            df,
            x="date",
            y=["gas_in_storage_gwh", "injection", "withdrawal"],
            title="Gas Storage Balances (GWh)"
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(df)

# ---------------------------------------------------------
# ALSI Europe LNG Storage
# ---------------------------------------------------------
with tab2:
    st.subheader("ALSI LNG Storage")

    df = pd.DataFrame(fetch("/storage/alsi?country=EU"))

    if df.empty:
        st.warning("No ALSI LNG storage data.")
    else:
        fig = px.line(df, x="date", y="inventory_gwh",
                      title="EU LNG Storage (Inventory GWh)")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df)

# ---------------------------------------------------------
# US EIA Weekly Storage
# ---------------------------------------------------------
with tab3:
    st.subheader("EIA US Gas Storage")

    df = pd.DataFrame(fetch("/storage/us"))

    if df.empty:
        st.warning("No US EIA storage data.")
    else:
        fig = px.area(df, x="date", y="storage_bcf",
                      title="US Gas Storage (BCF)")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df)
