import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# =========================
# 📥 Load dataset
# =========================
df = pd.read_csv("dataset/json_features.csv")

print("Dataset preview:")
print(df.head())

# =========================
# 🎯 Split features/target
# =========================
X = df.drop("difficulty", axis=1)
y = df["difficulty"]

# =========================
# 🤖 Train model
# =========================
model = RandomForestRegressor(n_estimators=200)
model.fit(X, y)

# =========================
# 💾 Save model
# =========================
joblib.dump(model, "ml_model/json_model.pkl")
print("✅ Model trained and saved")

# =========================
# 📊 Feature importance
# =========================
feature_names = X.columns
importances = model.feature_importances_

# sort
indices = importances.argsort()[::-1]

sorted_features = [feature_names[i] for i in indices]
sorted_importances = importances[indices]

print("\nFeature Importance Ranking:")
for i in range(len(sorted_features)):
    print(f"{i+1}. {sorted_features[i]}: {sorted_importances[i]:.4f}")

# =========================
# 📈 Plot
# =========================
plt.figure(figsize=(10, 6))
plt.barh(sorted_features[::-1], sorted_importances[::-1])
plt.xlabel("Importance")
plt.title("Feature Importance")
plt.tight_layout()
plt.show()