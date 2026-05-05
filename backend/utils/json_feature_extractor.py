import json
import numpy as np

def extract_features(content: bytes):

    data = json.loads(content)

    # =========================
    # 📦 Extract raw data safely
    # =========================
    enemies = data.get("enemies", [])
    projectiles = data.get("projectiles", [])
    checkpoints = data.get("checkpoints", [])
    spawns = data.get("spawns", [])

    map_size = data.get("map_size", {"width": 100, "height": 100})
    player_spawn = data.get("player_spawn", {"x": 0, "y": 0})

    width = map_size.get("width", 100)
    height = map_size.get("height", 100)
    area = width * height if width * height > 0 else 1

    px = player_spawn.get("x", 0)
    py = player_spawn.get("y", 0)

    # =========================
    # 🎯 1. Enemy pressure
    # =========================
    enemy_count = len(enemies)
    enemy_density = enemy_count / area

    # =========================
    # 🔁 2. Spawn pressure
    # =========================
    spawn_rate = len(spawns)

    # =========================
    # 🔫 3. Projectile intensity
    # =========================
    projectile_rate = sum(
        p.get("fire_rate", 1) for p in projectiles
    ) / (len(projectiles) + 1)

    # =========================
    # ⚠️ 4. Threat (distance to player)
    # =========================
    threat_distances = []

    for e in enemies:
        ex = e.get("x", 0)
        ey = e.get("y", 0)

        dist = ((ex - px)**2 + (ey - py)**2)**0.5
        threat_distances.append(dist)

    avg_threat = min(threat_distances) if threat_distances else 999

    # =========================
    # ⚡ 5. Danger score
    # =========================
    danger_score = 1 / avg_threat if avg_threat > 0 else 0

    # =========================
    # 🧠 6. Chaos (spatial variance)
    # =========================
    positions = [(e.get("x", 0), e.get("y", 0)) for e in enemies]

    if positions:
        xs = [p[0] for p in positions]
        ys = [p[1] for p in positions]
        chaos = np.var(xs) + np.var(ys)
    else:
        chaos = 0

    # =========================
    # 🔥 7. Cluster pressure
    # =========================
    cluster_score = 0

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            x1, y1 = positions[i]
            x2, y2 = positions[j]

            dist = ((x1 - x2)**2 + (y1 - y2)**2)**0.5

            if dist < 20:
                cluster_score += 1

    # =========================
    # 🛟 8. Checkpoint relief
    # =========================
    checkpoint_factor = len(checkpoints) / (enemy_count + 1)

    # =========================
    # 🎯 9. Difficulty pressure (CORE FEATURE)
    # =========================
    difficulty_pressure = (
        enemy_density * 0.3 +
        projectile_rate * 0.3 +
        danger_score * 0.2 +
        cluster_score * 0.2
    )

    # =========================
    # 📦 FINAL FEATURE VECTOR
    # =========================
    return {
        "enemy_density": float(enemy_density),
        "projectile_rate": float(projectile_rate),
        "danger_score": float(danger_score),
        "cluster_score": float(cluster_score),
        "difficulty_pressure": float(difficulty_pressure)
    }