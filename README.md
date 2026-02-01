# Ethiopia Financial Inclusion Forecasting

## Overview
This project aims to build a forecasting system that tracks Ethiopia's digital financial transformation using time series methods. It focuses on predicting Access (Account Ownership) and Usage (Digital Payment Adoption) for 2025-2027.

## Project Status
### Task 1: Data Exploration and Enrichment
**Objective:** Understand the unified schema and enrich the dataset with relevant indicators and events.
- **Unified Schema:** Leveraged a schema that combines observations, events, and impact links.
- **Enrichments:**
    - **New Observations:** Added 2023 Digital Payment Adoption data (30%) sourced from NBE reports.
    - **New Events:** Added the "NBE Digital Lending Directive" (June 2022) as a key policy milestone.
    - **Impact Links:** Modeled the relationship between regulatory changes and digital payment adoption.
- **Data Quality:** Assessed confidence levels across different sources (Global Findex vs. NBE reports).

### Task 2: Exploratory Data Analysis (EDA)
**Objective:** Analyze patterns and factors influencing financial inclusion.
- **Key Insights:**
    1. **Steady Growth:** Account ownership grew from 14% (2011) to 49% (2024).
    2. **Growth Deceleration:** Observed a slowdown in growth (+3pp) between 2021 and 2024, despite the launch of Telebirr and M-Pesa.
    3. **Mobile Money Gap:** Mobile money ownership (9.45%) lags significantly behind overall account ownership.
    4. **Digital Payment Adoption:** Currently stands at ~35%, showing a shift from traditional cash usage to digital ecosystem participation.
    5. **Event Impact:** Preliminary analysis suggests market entries (Telebirr 2021, Safaricom 2022, M-Pesa 2023) have yet to fully translate into broad account ownership growth, though usage volumes are rising.

## Structure
- `data/`: Contains raw and processed data.
- `notebooks/`: 
    - `Task_1_Data_Enrichment.ipynb`: Data loading and schema exploration.
    - `Task_2_EDA.ipynb`: Visualizations and trend analysis.
- `src/`: Source code for data processing and modeling.
- `dashboard/`: Streamlit dashboard application.
- `models/`: Saved models.
- `reports/figures/`: Generated plots (Trends, Timelines, etc.)
- `requirements.txt`: Project dependencies.
