import streamlit as st
from utils.db import run_query
import pandas as pd
from utils.ui import apply_custom_styles

apply_custom_styles()

st.title("🔌 Energy Usage Analytics")

# Fetch data
df_daily = run_query("SELECT * FROM vw_energy_daily")
df_monthly = run_query("SELECT * FROM vw_energy_monthly")

# Sidebar filters
buildings = df_daily['building_name'].unique()
selected_building = st.sidebar.selectbox("Select Building", buildings)
df_daily_filtered = df_daily[df_daily['building_name'] == selected_building]

# Date filter
df_daily_filtered['usage_date'] = pd.to_datetime(df_daily_filtered['usage_date'])
min_date = df_daily_filtered['usage_date'].min()
max_date = df_daily_filtered['usage_date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter by date
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
df_daily_filtered = df_daily_filtered[
    (df_daily_filtered['usage_date'] >= start_date) & (df_daily_filtered['usage_date'] <= end_date)
]

# Chart: Daily energy
st.subheader(f"📊 Daily Energy Usage for {selected_building}")
st.line_chart(df_daily_filtered.set_index('usage_date')["total_kwh"])

# Monthly summary table
st.subheader("📅 Monthly Energy Summary")
st.dataframe(df_monthly[df_monthly['building_name'] == selected_building])
