import pandas as pd
from typing import Tuple

def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully from {filepath}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at {filepath}")

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataframe by handling missing values and encoding categories.
    
    Args:
        df (pd.DataFrame): Raw dataframe.
        
    Returns:
        pd.DataFrame: Cleaned dataframe ready for training.
    """
    # Example logic - REPLACE with your specific project logic
    df_clean = df.copy()
    
    # Handle missing values (Example)
    if 'age' in df_clean.columns:
        df_clean['age'] = df_clean['age'].fillna(df_clean['age'].median())
    
    # Example: Encoding categorical variables
    # df_clean = pd.get_dummies(df_clean, columns=['job_type'])
    
    return df_clean