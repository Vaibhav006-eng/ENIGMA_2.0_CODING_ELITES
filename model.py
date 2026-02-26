import xgboost as xgb
import numpy as np
import pickle
import os

MODEL_PATH = "model.pkl"

def train_mock_model():
    """
    Train a dummy XGBoost model for testing the pipeline if no model exists.
    """
    X_mock = np.random.rand(100, 320)
    y_mock = np.random.randint(0, 2, 100)
    model = xgb.XGBClassifier(eval_metric='logloss')
    model.fit(X_mock, y_mock)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    return model

def load_or_train_model():
    if not os.path.exists(MODEL_PATH):
        return train_mock_model()
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def predict_risk(feature_vector):
    """
    Returns probability and risk score category
    """
    model = load_or_train_model()
    # XGBoost classifier predict_proba expects a 2d array
    prob = float(model.predict_proba(feature_vector.reshape(1, -1))[0][1])
    
    # Calculate Risk Score (0-100)
    risk_score = round(prob * 100, 2)
    
    if risk_score < 30:
        category = "Low Risk"
    elif risk_score < 60:
        category = "Moderate Risk"
    elif risk_score < 80:
        category = "High Risk"
    else:
        category = "Very High Risk"
        
    return {
        "probability": prob,
        "risk_score": float(risk_score),
        "category": category,
        "confidence": float(round(np.random.uniform(0.85, 0.98), 2))  # Mock confidence interval
    }
