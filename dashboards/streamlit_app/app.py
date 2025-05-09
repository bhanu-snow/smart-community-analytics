# dashboard/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from utils.ui import apply_custom_styles

apply_custom_styles()

# DB Connection
engine = create_engine("postgresql://postgres:123@localhost:5432/smart_community")

st.title("🏙️ Smart Community Analytics - Lite")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🏢 Building Summary", "📊 Occupancy Analysis", "⚡ Energy Usage"])

# --- Building Summary ---
with tab1:
    df = pd.read_sql("SELECT * FROM vw_building_summary", engine)
    st.subheader("Building Overview")
    st.dataframe(df)

    fig = px.bar(df, x="building_name", y="occupancy_rate_pct", color="occupancy_rate_pct",
                 title="Occupancy Rate by Building", labels={"occupancy_rate_pct": "% Occupied"})
    st.plotly_chart(fig, use_container_width=True)

# --- Occupancy by Type ---
with tab2:
    df = pd.read_sql("SELECT * FROM vw_unit_occupancy", engine)
    st.subheader("Unit Occupancy by Type")

    fig = px.bar(df, x="building_name", y="occupancy_pct", color="unit_type",
                 barmode="group", title="Occupancy Rate by Unit Type")
    st.plotly_chart(fig, use_container_width=True)

# --- Energy Usage ---
with tab3:
    daily = pd.read_sql("SELECT * FROM vw_energy_daily", engine)
    monthly = pd.read_sql("SELECT * FROM vw_energy_monthly", engine)

    st.subheader("Energy Usage Overview")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(daily, x="usage_date", y="total_kwh", color="building_name",
               title="Daily Energy Usage")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(monthly, x="month", y="total_kwh", color="building_name",
              title="Monthly Energy Usage")
        st.plotly_chart(fig2, use_container_width=True)
