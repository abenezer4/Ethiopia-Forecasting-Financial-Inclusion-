import pandas as pd
import joblib
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from preprocessing import load_data, preprocess_data # Assuming these exist from Sunday

# 1. Load and Process Data
# REPLACE 'data/Financial_inclusion_dataset.csv' with your actual path
df = load_data('../data/raw/ethiopia_fi_unified_data.csv') 
df_clean = preprocess_data(df)
print("Current Columns:", df_clean.columns.tolist())

# Define features and target (Adjust column names to match your dataset)
target_col = 'bank_account'
X = df_clean.drop(columns=[target_col])
y = df_clean[target_col]

# 2. Train Model
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X, y)

# 3. Create SHAP Explainer
# We use a TreeExplainer for Random Forest
explainer = shap.TreeExplainer(model)

# 4. Save Artifacts
joblib.dump(model, 'model.pkl')
joblib.dump(explainer, 'shap_explainer.pkl')
joblib.dump(X.columns.tolist(), 'features.pkl') # Save column names to keep order

print("Artifacts saved: model.pkl, shap_explainer.pkl, features.pkl")