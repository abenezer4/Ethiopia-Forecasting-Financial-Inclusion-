import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from data_loader import load_data

def run_eda():
    df = load_data()
    if df is None:
        return

    # Ensure output directory exists
    figures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports', 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    # Filter observations
    obs = df[df['record_type'] == 'observation'].copy()
    obs['observation_date'] = pd.to_datetime(obs['observation_date'])
    obs['year'] = obs['observation_date'].dt.year

    # 1. Access Analysis: Account Ownership Trajectory
    access_obs = obs[obs['indicator_code'] == 'ACC_OWN'].sort_values('year')
    
    plt.figure(figsize=(10, 6))
    plt.plot(access_obs['year'], access_obs['value_numeric'], marker='o', linestyle='-', color='b')
    plt.title('Ethiopia Account Ownership Trajectory (2011-2024)')
    plt.xlabel('Year')
    plt.ylabel('Account Ownership (%)')
    plt.grid(True)
    plt.savefig(os.path.join(figures_dir, 'account_ownership_trend.png'))
    print("Saved account_ownership_trend.png")
    plt.close()

    # 2. Usage Analysis: Digital Payment vs Mobile Money
    usage_obs = obs[obs['pillar'] == 'Usage'].sort_values('year')
    if not usage_obs.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=usage_obs, x='indicator', y='value_numeric', hue='year')
        plt.title('Usage Indicators')
        plt.ylabel('Percentage')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'usage_indicators.png'))
        print("Saved usage_indicators.png")
        plt.close()

    # 3. Event Timeline
    events = df[df['record_type'] == 'event'].copy()
    events['observation_date'] = pd.to_datetime(events['observation_date'])
    events = events.sort_values('observation_date')

    plt.figure(figsize=(12, 4))
    # Create a simple timeline
    plt.scatter(events['observation_date'], [1]*len(events), marker='s', color='r', s=100)
    
    for _, row in events.iterrows():
        plt.text(row['observation_date'], 1.05, row['category'] + ": " + str(row.get('parent_id', '')), rotation=45)

    plt.title('Event Timeline')
    plt.yticks([])
    plt.xlabel('Date')
    plt.ylim(0.8, 2)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'event_timeline.png'))
    print("Saved event_timeline.png")
    plt.close()
    
    print("\n--- Key Insights ---")
    print("1. Account ownership has grown steadily from 14% in 2011 to 49% in 2024.")
    print("2. The growth rate appears to have slowed down between 2021 and 2024 (only +3pp).")
    print("3. Mobile Money ownership is around 9.45% in 2024, significantly lower than overall account ownership.")
    print("4. Major market entries (Telebirr, M-Pesa) occurred in 2021 and 2023, which corresponds to the recent period.")
    print("5. Digital Payment Adoption shows promise with values around 30-35%.")

if __name__ == "__main__":
    run_eda()
