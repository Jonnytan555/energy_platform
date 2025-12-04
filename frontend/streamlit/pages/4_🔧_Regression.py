# streamlit_app/pages/4_🔧_Regression.py

import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import fetch

st.title("🔧 Regression Models")

model = st.selectbox("Model", ["hh_to_ttf", "ttf_to_nbp"])

data = fetch(f"/regression/{model}")

df = pd.DataFrame(data["points"])
line = pd.DataFrame(data["line"])

fig = px.scatter(df, x="x", y="y", title="Input Data")
fig.add_traces(px.line(line, x="x", y="y").data)
st.plotly_chart(fig, use_container_width=True)

st.write("**Slope:**", data["slope"])
st.write("**Intercept:**", data["intercept"])
st.dataframe(df)
