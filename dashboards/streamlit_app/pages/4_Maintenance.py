import streamlit as st
from utils.db import run_query
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
from utils.ui import apply_custom_styles

apply_custom_styles()


# --- Streamlit Layout ---
st.title("Maintenance Summary")

# Fetch the maintenance data
df_maintenance =  run_query("SELECT * FROM vw_maintenance_summary")

# Display the data as a table
st.subheader("Maintenance Tickets Summary")
st.write(df_maintenance)

# Clean up the filters and ensure they match the available data
status_options = df_maintenance['status'].dropna().unique().tolist()
priority_options = df_maintenance['priority'].dropna().unique().tolist()

status_filter = st.selectbox("Filter by Status", ["All"] + status_options)
priority_filter = st.selectbox("Filter by Priority", ["All"] + priority_options)

# Apply filters if not "All"
if status_filter != "All":
    df_maintenance = df_maintenance[df_maintenance['status'].str.lower() == status_filter.lower()]

if priority_filter != "All":
    df_maintenance = df_maintenance[df_maintenance['priority'] == int(priority_filter)]

# Show filtered data
st.write(df_maintenance)

# Charts
ticket_counts_by_priority = df_maintenance.groupby('priority')['ticket_count'].sum().reset_index()
st.subheader("Ticket Counts by Priority")
st.bar_chart(ticket_counts_by_priority.set_index('priority')['ticket_count'])

ticket_counts_by_building = df_maintenance.groupby('building_name')['ticket_count'].sum().reset_index()
st.subheader("Ticket Counts by Building")
st.bar_chart(ticket_counts_by_building.set_index('building_name')['ticket_count'])