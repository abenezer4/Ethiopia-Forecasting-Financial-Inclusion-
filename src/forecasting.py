import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from data_loader import load_data

def run_forecasting():
    df = load_data()
    if df is None: return

    obs = df[df['record_type'] == 'observation'].copy()
    obs['observation_date'] = pd.to_datetime(obs['observation_date'])
    obs['year'] = obs['observation_date'].dt.year

    # Forecast Years
    future_years = np.array([2025, 2026, 2027]).reshape(-1, 1)

    print("\n--- FORECASTS (2025-2027) ---")

    # Access Forecast (Account Ownership)
    access_data = obs[obs['indicator_code'] == 'ACC_OWN'].sort_values('year')
    if len(access_data) > 1:
        X = access_data[['year']].values
        y = access_data['value_numeric'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        preds = model.predict(future_years)
        
        print("\nIndicator: Account Ownership (Access)")
        print(f"Historical Trend Slope: {model.coef_[0]:.2f} pp/year")
        
        results = pd.DataFrame({
            'Year': future_years.flatten(),
            'Base_Forecast': preds,
            'Optimistic': preds * 1.05,
            'Pessimistic': preds * 0.95
        })
        print(results.to_string(index=False))
    else:
        print("\nNot enough data for Access forecast.")

    # Usage Forecast (Digital Payment)
    # Using limited points, maybe just assume growth from last point
    usage_data = obs[obs['indicator_code'] == 'USG_DIG_PAY'].sort_values('year')
    if not usage_data.empty:
        last_val = usage_data.iloc[-1]['value_numeric']
        print("\nIndicator: Digital Payment Adoption (Usage)")
        print(f"Last Observed: {last_val}% in {usage_data.iloc[-1]['year']}")
        
        # Simple heuristic growth
        growth_rate = 1.1 # 10% growth per year
        
        forecasts = []
        for i, year in enumerate([2025, 2026, 2027]):
            # Calculate distance from last observed
            years_diff = year - usage_data.iloc[-1]['year']
            val = last_val * (growth_rate ** years_diff)
            forecasts.append(val)
            
        results_usage = pd.DataFrame({
            'Year': [2025, 2026, 2027],
            'Base_Forecast': forecasts,
            'Optimistic': [f * 1.1 for f in forecasts],
            'Pessimistic': [f * 0.9 for f in forecasts]
        })
        print(results_usage.to_string(index=False))

if __name__ == "__main__":
    run_forecasting()
