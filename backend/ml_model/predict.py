import pickle
import pandas as pd

# Load model
with open("ml_model/model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_difficulty(features: dict):

    input_data = pd.DataFrame([{
        "enemy_count": features["enemy_count"],
        "spawn_rate": features["spawn_rate"],
        "rewards": features["rewards"],
        "checkpoints": features["checkpoints"]
    }])

    prediction = model.predict(input_data)[0]

    return float(prediction)