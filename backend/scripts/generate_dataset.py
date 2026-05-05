import pandas as pd
import random

rows = []

for _ in range(100):

    enemy_density = random.uniform(0.01, 0.1)
    projectile_rate = random.uniform(0.1, 1.0)
    avg_threat = random.uniform(10, 100)

    danger_score = 1 / avg_threat
    cluster_score = random.randint(0, 10)

    difficulty_pressure = (
        enemy_density * 0.3 +
        projectile_rate * 0.3 +
        danger_score * 0.2 +
        cluster_score * 0.2
    )

    difficulty = difficulty_pressure + random.uniform(-0.05, 0.05)

    rows.append({
        "enemy_density": enemy_density,
        "projectile_rate": projectile_rate,
        "danger_score": danger_score,
        "cluster_score": cluster_score,
        "difficulty_pressure": difficulty_pressure,
        "difficulty": difficulty
    })

df = pd.DataFrame(rows)

df.to_csv("dataset/json_features.csv", index=False)

print("✅ Clean dataset generated")