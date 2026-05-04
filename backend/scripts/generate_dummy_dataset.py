import os
import random
import cv2
import numpy as np

# =========================
# 📁 Paths
# =========================
BASE_DIR = "dataset"
IMG_TRAIN = os.path.join(BASE_DIR, "images/train")
IMG_VAL = os.path.join(BASE_DIR, "images/val")
LBL_TRAIN = os.path.join(BASE_DIR, "labels/train")
LBL_VAL = os.path.join(BASE_DIR, "labels/val")

# Create folders
for path in [IMG_TRAIN, IMG_VAL, LBL_TRAIN, LBL_VAL]:
    os.makedirs(path, exist_ok=True)

# =========================
# 🎨 Class colors
# =========================
CLASSES = {
    0: (255, 0, 0),   # player
    1: (0, 0, 255),   # enemy
    2: (0, 255, 0),   # projectile
    3: (0, 255, 255)  # hazard
}

# =========================
# 🧠 Generate one image
# =========================
def generate_image(width=640, height=480, num_objects=5):
    img = np.zeros((height, width, 3), dtype=np.uint8)

    labels = []

    for _ in range(num_objects):
        cls = random.randint(0, 3)

        w = random.randint(30, 100)
        h = random.randint(30, 100)

        x = random.randint(0, width - w)
        y = random.randint(0, height - h)

        # Draw rectangle
        color = CLASSES[cls]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)

        # YOLO format (normalized)
        x_center = (x + w / 2) / width
        y_center = (y + h / 2) / height
        w_norm = w / width
        h_norm = h / height

        labels.append(f"{cls} {x_center} {y_center} {w_norm} {h_norm}")

    return img, labels

# =========================
# 🚀 Generate dataset
# =========================
def generate_dataset(num_train=100, num_val=20):

    print("Generating training data...")
    for i in range(num_train):
        img, labels = generate_image()

        img_path = os.path.join(IMG_TRAIN, f"img_{i}.jpg")
        lbl_path = os.path.join(LBL_TRAIN, f"img_{i}.txt")

        cv2.imwrite(img_path, img)

        with open(lbl_path, "w") as f:
            f.write("\n".join(labels))

    print("Generating validation data...")
    for i in range(num_val):
        img, labels = generate_image()

        img_path = os.path.join(IMG_VAL, f"img_{i}.jpg")
        lbl_path = os.path.join(LBL_VAL, f"img_{i}.txt")

        cv2.imwrite(img_path, img)

        with open(lbl_path, "w") as f:
            f.write("\n".join(labels))

    print("✅ Dummy dataset created!")

# =========================
# ▶️ Run
# =========================
if __name__ == "__main__":
    generate_dataset()