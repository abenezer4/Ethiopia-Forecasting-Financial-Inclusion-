import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set Page Config
st.set_page_config(page_title="Ethiopia FI Dashboard", layout="wide")

# Helper to load data
@st.cache_data
def load_data():
    path = os.path.join('data', 'raw', 'ethiopia_fi_unified_data.csv')
    if not os.path.exists(path):
         path = os.path.join('..', 'data', 'raw', 'ethiopia_fi_unified_data.csv')
    return pd.read_csv(path)

st.title("🇪🇹 Ethiopia Financial Inclusion Dashboard")
st.markdown("Exploring the trajectory of digital financial transformation from 2011 to 2027.")

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar
st.sidebar.header("Scenario Control")
scenario = st.sidebar.selectbox("Select Forecast Scenario", ["Base", "Optimistic", "Pessimistic"])

# Filter Data
obs = df[df['record_type'] == 'observation'].copy()
obs['year'] = pd.to_datetime(obs['observation_date']).dt.year
access_data = obs[obs['indicator_code'] == 'ACC_OWN'].sort_values('year')

# --- SECTION 1: KEY METRICS ---
st.header("1. Key Inclusion Metrics")
latest_acc = access_data.iloc[-1]['value_numeric']
prev_acc = access_data.iloc[-2]['value_numeric']
delta = latest_acc - prev_acc

col1, col2, col3 = st.columns(3)
col1.metric("Account Ownership (2024)", f"{latest_acc}%", f"{delta:+.1f}pp vs 2021")
col2.metric("Digital Payment Adoption", "35.0%", "Est.")
col3.metric("Mobile Money Ownership", "9.45%", "2024")

# --- SECTION 2: VISUALIZATIONS ---
st.header("2. Trend Analysis")

tab1, tab2, tab3, tab4 = st.tabs(["Access Trends", "Usage & MM", "Impact Matrix", "Event Timeline"])

with tab1:
    st.subheader("Historical Account Ownership")
    st.line_chart(access_data.set_index('year')['value_numeric'])
    st.info("Insight: Growth slowed to +3pp in the 2021-2024 period.")

with tab2:
    st.subheader("Usage vs Mobile Money Ownership")
    usage_df = obs[obs['pillar'] == 'Usage'].sort_values('year')
    st.bar_chart(data=usage_df, x='indicator', y='value_numeric')
    st.info("Insight: Digital payment adoption (35%) significantly outpaces mobile money ownership (9.45%).")

with tab3:
    st.subheader("Event Impact Association Matrix")
    # Quick reconstruction of Task 3 matrix
    links = df[df['record_type'] == 'impact_link']
    st.dataframe(links[['parent_id', 'related_indicator', 'impact_direction', 'impact_magnitude']])

with tab4:
    st.subheader("Key Transformation Milestones")
    events = df[df['record_type'] == 'event'].sort_values('observation_date')
    st.table(events[['observation_date', 'category', 'parent_id']])

# --- SECTION 3: FORECASTS ---
st.header("3. Inclusion Projections (2025-2027)")

years = [2025, 2026, 2027]
slope = 2.84
last_val = latest_acc

forecast_vals = []
for i, y in enumerate(years):
    val = last_val + (slope * (y - 2024))
    if scenario == "Optimistic": val *= 1.05
    if scenario == "Pessimistic": val *= 0.95
    forecast_vals.append(round(val, 2))

forecast_df = pd.DataFrame({'Year': years, 'Projected_Ownership_%': forecast_vals})

col_f1, col_f2 = st.columns([1, 2])
with col_f1:
    st.write(f"**{scenario} Scenario Results**")
    st.table(forecast_df)

with col_f2:
    # Plot combined
    hist = access_data[['year', 'value_numeric']].rename(columns={'value_numeric': 'Value'})
    fore = forecast_df.rename(columns={'Year': 'year', 'Projected_Ownership_%': 'Value'})
    combined = pd.concat([hist, fore]).set_index('year')
    st.line_chart(combined)

st.success("Target Alignment: Under the Base scenario, Ethiopia is on track to reach ~57.7% ownership by 2026.")
