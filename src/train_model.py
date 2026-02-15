import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """
    Trains a Random Forest model.
    
    Args:
        X (pd.DataFrame): Features.
        y (pd.Series): Target variable.
        
    Returns:
        RandomForestClassifier: Trained model.
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Accuracy: {acc:.4f}")
    
    return model

def save_model(model, filename: str = "model.pkl"):
    joblib.dump(model, filename)