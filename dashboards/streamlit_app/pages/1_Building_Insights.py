import streamlit as st
from utils.db import run_query
from utils.ui import apply_custom_styles

apply_custom_styles()

st.title("🏢 Building & Occupancy Insights")

df = run_query("SELECT * FROM vw_building_summary")
st.dataframe(df)

st.bar_chart(df.set_index('building_name')["occupancy_rate_pct"])
