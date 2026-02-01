import pandas as pd
from data_loader import load_data

def quantify_impact(magnitude):
    if magnitude == 'High': return 0.05
    if magnitude == 'Medium': return 0.02
    if magnitude == 'Low': return 0.01
    return 0.0

def run_impact_modeling():
    df = load_data()
    if df is None: return

    events = df[df['record_type'] == 'event'].set_index('parent_id')
    links = df[df['record_type'] == 'impact_link']

    # Unique indicators in impact links
    indicators = links['related_indicator'].unique()
    event_ids = events.index.unique()

    # Initialize matrix
    matrix = pd.DataFrame(0.0, index=event_ids, columns=indicators)

    print("\n--- Impact Association Matrix (Estimated Effect) ---")
    
    for _, link in links.iterrows():
        evt = link['parent_id']
        ind = link['related_indicator']
        mag = link['impact_magnitude']
        
        val = quantify_impact(mag)
        if link['impact_direction'] == 'Decrease':
            val = -val
            
        if evt in matrix.index:
            matrix.loc[evt, ind] = val

    # Join with Event Names for clarity
    matrix = matrix.join(events['category'])
    print(matrix)

    return matrix

if __name__ == "__main__":
    run_impact_modeling()

