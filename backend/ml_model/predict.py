import joblib
import numpy as np
import pandas as pd

model = joblib.load("ml_model/json_model.pkl")

FEATURE_ORDER = [
    "enemy_density",
    "projectile_rate",
    "danger_score",
    "cluster_score",
    "difficulty_pressure"
]


def predict_difficulty(features: dict):

    # convert to DataFrame (fix warning + keep names)
    input_df = pd.DataFrame([features])[FEATURE_ORDER]

    # 🌲 Get predictions from all trees
    all_preds = np.array([
        tree.predict(input_df)[0]
        for tree in model.estimators_
    ])

    # 🎯 final prediction
    prediction = float(np.mean(all_preds))

    # 📊 confidence = inverse of variance
    variance = np.var(all_preds)

    confidence = float(1 / (1 + variance))

    # clamp values
    confidence = max(0.2, min(0.95, confidence))

    return prediction, confidence