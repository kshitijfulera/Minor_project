import joblib
import numpy as np

model = joblib.load("ml_model/json_model.pkl")

FEATURE_ORDER = [
    "enemy_density",
    "projectile_rate",
    "avg_threat",
    "chaos",
    "cluster_score",
    "safety_factor"
]

def predict_difficulty(features: dict):

    input_data = np.array([[
        features[k] for k in FEATURE_ORDER
    ]])

    prediction = model.predict(input_data)[0]

    return float(max(0, min(1, prediction)))