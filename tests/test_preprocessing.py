import pytest
import pandas as pd
from src.preprocessing import preprocess_data, load_data

# Test 1: Check if load_data raises error for bad path
def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data("non_existent_file.csv")

# Test 2: Check if preprocessing handles missing values (example)
def test_preprocess_missing_values():
    # Create dummy data
    data = pd.DataFrame({'age': [25, None, 30], 'bank_account': [1, 0, 1]})
    clean_data = preprocess_data(data)
    assert clean_data['age'].isnull().sum() == 0

# Test 3: Check output type
def test_preprocess_returns_dataframe():
    data = pd.DataFrame({'age': [25, 40], 'bank_account': [1, 0]})
    clean_data = preprocess_data(data)
    assert isinstance(clean_data, pd.DataFrame)

# Test 4: Check if columns are preserved (or changed as expected)
def test_preprocess_columns():
    data = pd.DataFrame({'age': [25], 'bank_account': [1]})
    clean_data = preprocess_data(data)
    assert 'age' in clean_data.columns

# Test 5: Check empty dataframe handling
def test_preprocess_empty_df():
    data = pd.DataFrame()
    clean_data = preprocess_data(data)
    assert clean_data.empty