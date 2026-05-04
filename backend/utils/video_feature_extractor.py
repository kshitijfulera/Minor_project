import cv2
import numpy as np
from ultralytics import YOLO

# =========================
# 🔥 Load YOLO model
# =========================
yolo_model = YOLO("runs/detect/train/weights/best.pt")  # use your trained model

# =========================
# 🎯 Feature Extractor
# =========================
def extract_video_features(video_path: str):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Cannot open video")

    # =========================
    # 📊 Counters
    # =========================
    frame_count = 0
    enemy_count = 0
    projectile_count = 0
    player_count = 0
    motion_sum = 0
    chaos_sum = 0

    # =========================
    # 🧍 Player tracking
    # =========================
    player_positions = []
    death_count = 0
    frame_since_seen = 0

    # =========================
    # ⚠️ Threat tracking
    # =========================
    threat_distances = []

    prev_gray = None
    FRAME_SKIP = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        frame = cv2.resize(frame, (320, 240))

        # =========================
        # 🎯 Motion + Chaos
        # =========================
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)

            motion = np.sum(diff) / (320 * 240)
            chaos = np.var(diff)

            motion_sum += motion
            chaos_sum += chaos

        prev_gray = gray

        # =========================
        # 🤖 YOLO Detection
        # =========================
        player_found = False
        enemies = []
        player_pos = None

        if frame_count % FRAME_SKIP == 0:

            results = yolo_model(frame, verbose=False)

            for r in results:
                if r.boxes is None:
                    continue

                for box in r.boxes:
                    cls = int(box.cls[0])
                    x1, y1, x2, y2 = map(float, box.xyxy[0])

                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2

                    # 🎮 Player
                    if cls == 0:
                        player_positions.append((cx, cy))
                        player_pos = (cx, cy)
                        player_count += 1
                        player_found = True
                        frame_since_seen = 0

                    # 👾 Enemy
                    elif cls == 1:
                        enemy_count += 1
                        enemies.append((cx, cy))

                    # 🔫 Projectile
                    elif cls == 2:
                        projectile_count += 1

        # =========================
        # 💀 Death Detection
        # =========================
        if not player_found:
            frame_since_seen += 1

            if frame_since_seen > 10:
                death_count += 1
                frame_since_seen = 0

        # =========================
        # ⚠️ Threat Distance
        # =========================
        if player_pos and enemies:
            for ex, ey in enemies:
                dist = ((ex - player_pos[0])**2 + (ey - player_pos[1])**2)**0.5
                threat_distances.append(dist)

    cap.release()

    # =========================
    # 🧠 Post Processing
    # =========================
    if frame_count == 0:
        raise Exception("Empty video")

    avg_motion = motion_sum / frame_count
    chaos = chaos_sum / frame_count

    enemy_density = enemy_count / frame_count
    projectile_rate = projectile_count / frame_count
    player_presence = player_count / frame_count

    # =========================
    # 🧍 Player Speed
    # =========================
    speeds = []

    for i in range(1, len(player_positions)):
        x1, y1 = player_positions[i - 1]
        x2, y2 = player_positions[i]

        dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        speeds.append(dist)

    avg_speed = sum(speeds) / len(speeds) if speeds else 0

    # =========================
    # 🧱 Stuck Ratio
    # =========================
    stuck_frames = sum(1 for s in speeds if s < 2)
    stuck_ratio = stuck_frames / len(speeds) if speeds else 0

    # =========================
    # ⚠️ Threat Score
    # =========================
    avg_threat = min(threat_distances) if threat_distances else 999

    # =========================
    # ⏱ Survival Time
    # =========================
    time_alive = frame_count / (death_count + 1)

    # =========================
    # 🎯 Difficulty Pressure
    # =========================
    difficulty_pressure = (
        enemy_density * 0.3 +
        projectile_rate * 0.3 +
        (1 / avg_threat if avg_threat > 0 else 0) * 0.2 +
        death_count * 0.2
    )

    # =========================
    # 📦 Final Features
    # =========================
    return {
        "avg_motion": float(avg_motion),
        "chaos": float(chaos),
        "enemy_density": float(enemy_density),
        "projectile_rate": float(projectile_rate),
        "player_presence": float(player_presence),

        "player_speed": float(avg_speed),
        "death_count": int(death_count),
        "stuck_ratio": float(stuck_ratio),

        "avg_threat": float(avg_threat),
        "time_alive": float(time_alive),
        "difficulty_pressure": float(difficulty_pressure),

        "frame_count": frame_count
    }