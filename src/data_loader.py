import pandas as pd
import os

def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'raw', 'ethiopia_fi_unified_data.csv')
    
    try:
        df = pd.read_csv(data_path)
        print("Data loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"File not found at {data_path}")
        return None

def explore_data(df):
    if df is None:
        return

    print("\n--- Data Structure ---")
    print(df.info())

    print("\n--- Record Type Counts ---")
    print(df['record_type'].value_counts())

    print("\n--- Pillar Counts ---")
    print(df['pillar'].value_counts(dropna=False))

    observations = df[df['record_type'] == 'observation']
    if not observations.empty:
        print("\n--- Observation Date Range ---")
        print(f"Start: {observations['observation_date'].min()}")
        print(f"End: {observations['observation_date'].max()}")
        
        print("\n--- Unique Indicators ---")
        print(observations['indicator'].unique())

    events = df[df['record_type'] == 'event']
    if not events.empty:
        print("\n--- Events ---")
        print(events[['observation_date', 'category', 'parent_id']].to_string(index=False))

    impacts = df[df['record_type'] == 'impact_link']
    if not impacts.empty:
        print("\n--- Impact Links ---")
        print(impacts[['parent_id', 'related_indicator', 'impact_direction', 'impact_magnitude']].to_string(index=False))

if __name__ == "__main__":
    df = load_data()
    explore_data(df)
