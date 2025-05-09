import streamlit as st
from utils.db import run_query
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
from utils.ui import apply_custom_styles

apply_custom_styles()

st.title("🔮 Energy Forecasting (30 Days)")

# Load historical data
df_forecast_ready = run_query("SELECT * FROM vw_forecast_ready_energy")
df_forecast_ready['ds'] = pd.to_datetime(df_forecast_ready['ds'])

# Sidebar filter
buildings = df_forecast_ready['building_name'].unique()
selected_building = st.sidebar.selectbox("Select Building", buildings)
df_filtered = df_forecast_ready[df_forecast_ready['building_name'] == selected_building]

# Prepare for Prophet
df_prophet = df_filtered.rename(columns={"ds": "ds", "total_kwh": "y"})[["ds", "y"]]

# Forecasting
model = Prophet()
model.fit(df_prophet)
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Plot
st.subheader(f"📈 Forecasted Energy Usage for {selected_building}")
fig = plot_plotly(model, forecast)
st.plotly_chart(fig, use_container_width=True)

# Display forecast table
st.subheader("📋 Forecast Data (Next 30 Days)")
st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))
