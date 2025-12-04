# streamlit_app/pages/3_🚢_Shipping.py

import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import fetch

st.title("🚢 Shipping & LNG Logistics")

origin = st.selectbox("Origin", ["USGC", "Qatar", "Australia", "Algeria"])
destination = st.selectbox("Destination", ["EU", "UK", "Asia", "Japan", "Korea"])

data = fetch(f"/shipping/eta?origin={origin}&destination={destination}")

st.subheader("Voyage ETA Model")
st.write(f"**Voyage Days:** {data['voyage_days']}")
st.write(f"**Speed (knots):** {data['speed_knots']}")

df = pd.DataFrame(data["route"])
fig = px.line_geo(df, lat="lat", lon="lon", title="Shipping Route")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df)
