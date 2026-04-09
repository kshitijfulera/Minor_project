import pickle

# Load model
with open("ml_model/model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_difficulty(features: dict):

    input_data = [[
        features["enemy_count"],
        features["spawn_rate"],
        features["rewards"],
        features["checkpoints"]
    ]]

    prediction = model.predict(input_data)[0]

    return float(prediction)