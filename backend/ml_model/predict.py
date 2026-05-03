import pickle

model = None

def load_model():
    global model
    if model is None:
        with open("ml_model/model.pkl", "rb") as f:
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