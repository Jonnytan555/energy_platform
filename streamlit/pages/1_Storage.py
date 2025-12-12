import streamlit as st
import pandas as pd
import plotly.express as px

from api_client import (
    fetch_agsi_latest,
    fetch_alsi_latest,
    scrape_agsi,
    scrape_alsi,
)

st.title("📦 Storage")

if not st.session_state.get("access_token"):
    st.warning("Please login first (sidebar) — endpoints require Bearer auth.")
    st.stop()

tab1, tab2 = st.tabs(["AGSI (Gas)", "ALSI (LNG)"])

# ---------------- AGSI -----------------
with tab1:
    st.subheader("AGSI — Latest only (is_latest=true) + created_date")

    colA, colB, colC = st.columns(3)
    with colA:
        zone = st.selectbox("Zone (for scrape)", ["eu", "de", "fr"], index=0)
    with colB:
        pages = st.number_input("Pages to scrape", min_value=1, value=30, step=1)
    with colC:
        limit = st.number_input("DB rows limit", min_value=1, value=365, step=10)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Fetch latest (DB)", key="agsi_fetch"):
            try:
                data = fetch_agsi_latest(limit=int(limit))
                st.session_state["agsi_rows"] = data
                st.success(f"Loaded {len(data)} rows")
            except Exception as e:
                st.error(str(e))

    with c2:
        if st.button("Scrape + refresh", key="agsi_scrape"):
            try:
                scrape_agsi(zone=zone, pages=int(pages))
                data = fetch_agsi_latest(limit=int(limit))
                st.session_state["agsi_rows"] = data
                st.success(f"Scraped + refreshed {len(data)} rows")
            except Exception as e:
                st.error(str(e))

    rows = st.session_state.get("agsi_rows", [])
    df = pd.DataFrame(rows)

    if df.empty:
        st.info("No AGSI data loaded yet. Click Fetch latest or Scrape + refresh.")
    else:
        # ensure newest first
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.sort_values("date", ascending=False)

        # KPI
        latest = df.iloc[0]
        st.metric("Latest % Full", float(latest.get("full_pct")) if pd.notna(latest.get("full_pct")) else None)
        st.caption(f"Latest date: {latest.get('date')} | Created in DB: {latest.get('created_date')}")

        # Charts
        fig = px.line(df.sort_values("date"), x="date", y="full_pct", title="AGSI % Full")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(
            df.sort_values("date"),
            x="date",
            y=["gas_in_storage_gwh", "injection", "withdrawal"],
            title="AGSI Balances (GWh)",
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Table (latest first)
        show_cols = [
            "date",
            "full_pct",
            "gas_in_storage_gwh",
            "injection",
            "withdrawal",
            "created_date",
            "version",
            "is_latest",
        ]
        st.dataframe(df[ [c for c in show_cols if c in df.columns] ], use_container_width=True)

# ---------------- ALSI -----------------
with tab2:
    st.subheader("ALSI — Latest only (is_latest=true) + created_date")

    colA, colB = st.columns(2)
    with colA:
        country = st.selectbox("Country (for scrape)", ["EU", "GB", "FR", "ES", "NL"], index=0)
    with colB:
        limit = st.number_input("DB rows limit", min_value=1, value=365, step=10, key="alsi_limit")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Fetch latest (DB)", key="alsi_fetch"):
            try:
                data = fetch_alsi_latest(limit=int(limit))
                st.session_state["alsi_rows"] = data
                st.success(f"Loaded {len(data)} rows")
            except Exception as e:
                st.error(str(e))

    with c2:
        if st.button("Scrape + refresh", key="alsi_scrape"):
            try:
                scrape_alsi(country=country)
                data = fetch_alsi_latest(limit=int(limit))
                st.session_state["alsi_rows"] = data
                st.success(f"Scraped + refreshed {len(data)} rows")
            except Exception as e:
                st.error(str(e))

    rows = st.session_state.get("alsi_rows", [])
    df = pd.DataFrame(rows)

    if df.empty:
        st.info("No ALSI data loaded yet. Click Fetch latest or Scrape + refresh.")
    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.sort_values("date", ascending=False)

        # choose correct storage column name
        storage_col = "lng_storage_gwh" if "lng_storage_gwh" in df.columns else ("inventory_gwh" if "inventory_gwh" in df.columns else None)

        latest = df.iloc[0]
        if storage_col:
            st.metric("Latest Storage (GWh)", float(latest.get(storage_col)) if pd.notna(latest.get(storage_col)) else None)
        st.caption(f"Latest date: {latest.get('date')} | Created in DB: {latest.get('created_date')}")

        if storage_col:
            fig = px.line(df.sort_values("date"), x="date", y=storage_col, title="ALSI Storage (GWh)")
            st.plotly_chart(fig, use_container_width=True)

        show_cols = [
            "date",
            storage_col,
            "sendOut",
            "dtmi_gwh",
            "dtrs",
            "created_date",
            "version",
            "is_latest",
        ]
        show_cols = [c for c in show_cols if c and c in df.columns]
        st.dataframe(df[show_cols], use_container_width=True)
