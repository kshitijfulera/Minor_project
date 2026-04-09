import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Sample dataset (you can improve later)
data = pd.DataFrame({
    "enemy_count": [5, 10, 15, 20, 25],
    "spawn_rate": [1, 2, 2.5, 3, 4],
    "rewards": [5, 3, 2, 1, 1],
    "checkpoints": [3, 2, 2, 1, 1],
    "difficulty": [0.2, 0.4, 0.6, 0.8, 0.95]
})

X = data[["enemy_count", "spawn_rate", "rewards", "checkpoints"]]
y = data["difficulty"]

model = RandomForestRegressor()
model.fit(X, y)

# Save model
with open("ml_model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved!")