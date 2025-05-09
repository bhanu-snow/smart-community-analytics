import streamlit as st
from utils.db import run_query
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
from utils.ui import apply_custom_styles

apply_custom_styles()


st.title("🔮 Forecast: Daily Energy Usage")

# --- Load Forecast-Ready Data ---
df = run_query("SELECT * FROM vw_forecast_ready_energy")
df['ds'] = pd.to_datetime(df['ds'])

# --- Sidebar: Select Building ---
buildings = df['building_name'].unique()
selected_building = st.sidebar.selectbox("Select Building", sorted(buildings))

# --- Filter Data for Selected Building ---
df_building = df[df['building_name'] == selected_building].copy()

if len(df_building) < 10:
    st.warning("Not enough historical data to forecast. Need at least 10 days.")
else:
    # --- Prophet Forecasting ---
    m = Prophet(daily_seasonality=True)
    m.fit(df_building[['ds', 'y']])

    future = m.make_future_dataframe(periods=14)  # Forecast for next 14 days
    forecast = m.predict(future)

    # --- Plot ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_building['ds'], y=df_building['y'], mode='lines+markers', name='Actual'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dot'), opacity=0.3))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dot'), opacity=0.3))

    fig.update_layout(title=f"Energy Usage Forecast - {selected_building}",
                      xaxis_title="Date", yaxis_title="kWh Used",
                      height=500)
    st.plotly_chart(fig, use_container_width=True)

    # --- Show Forecast Table ---
    st.subheader("Forecast Data (Next 14 Days)")
    forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(14)
    forecast_display.columns = ['Date', 'Forecast (kWh)', 'Lower Bound', 'Upper Bound']
    st.dataframe(forecast_display.set_index('Date').round(2))