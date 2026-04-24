import pickle
import os

model = None

def load_model():
    global model
    if model is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "model.pkl")

        with open(model_path, "rb") as f:
            model = pickle.load(f)

    return model


def predict_difficulty(features):
    model = load_model()

    input_data = [[
        features["enemy_count"],
        features["spawn_rate"],
        features["rewards"],
        features["checkpoints"]
    ]]

    return float(model.predict(input_data)[0])