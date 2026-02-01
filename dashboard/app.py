import streamlit as st
import pandas as pd
import numpy as np
import os

# Helper to load data
@st.cache_data
def load_data_dashboard():
    # Adjust path assuming app is run from root or dashboard folder
    # We'll try relative path from current working dir
    # If run with `streamlit run dashboard/app.py` from root
    path = os.path.join('data', 'raw', 'ethiopia_fi_unified_data.csv')
    if not os.path.exists(path):
         # Try going up one level if run from dashboard dir
         path = os.path.join('..', 'data', 'raw', 'ethiopia_fi_unified_data.csv')
    
    return pd.read_csv(path)

st.set_page_config(page_title="Ethiopia Financial Inclusion Forecast", layout="wide")

st.title("Ethiopia Financial Inclusion Forecasting System")

try:
    df = load_data_dashboard()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Filter Observations
obs = df[df['record_type'] == 'observation'].copy()
obs['observation_date'] = pd.to_datetime(obs['observation_date'])
obs['year'] = obs['observation_date'].dt.year

# Sidebar
st.sidebar.header("Settings")
scenario = st.sidebar.selectbox("Select Scenario", ["Base", "Optimistic", "Pessimistic"])

# Section 1: Overview
st.header("1. Historical Trends")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Account Ownership (Access)")
    access_data = obs[obs['indicator_code'] == 'ACC_OWN'].sort_values('year')
    st.line_chart(access_data.set_index('year')['value_numeric'])

with col2:
    st.subheader("Digital Payment (Usage)")
    usage_data = obs[obs['pillar'] == 'Usage'].sort_values('year')
    if not usage_data.empty:
        # Aggregate by indicator if multiple
        st.bar_chart(usage_data.set_index('indicator')['value_numeric'])
    else:
        st.write("No Usage data available.")

# Section 2: Forecasts
st.header("2. Forecasts (2025-2027)")

# Simple Forecasting Logic (Replicated from src/forecasting.py for dashboard interactivity)
years = [2025, 2026, 2027]
access_growth = 2.84 # slope from EDA
last_access = access_data.iloc[-1]['value_numeric']
last_access_year = access_data.iloc[-1]['year']

forecast_vals = []
for y in years:
    diff = y - last_access_year
    val = last_access + (access_growth * diff)
    if scenario == "Optimistic": val *= 1.05
    if scenario == "Pessimistic": val *= 0.95
    forecast_vals.append(val)

forecast_df = pd.DataFrame({'Year': years, 'Forecast': forecast_vals})

st.subheader(f"Access Forecast ({scenario} Scenario)")
st.table(forecast_df)

chart_data = pd.concat([
    access_data[['year', 'value_numeric']].rename(columns={'value_numeric': 'Value'}),
    forecast_df.rename(columns={'Year': 'year', 'Forecast': 'Value'})
]).set_index('year')

st.line_chart(chart_data)

# Section 3: Events
st.header("3. Key Events")
events = df[df['record_type'] == 'event'][['observation_date', 'category', 'parent_id']]
st.dataframe(events)