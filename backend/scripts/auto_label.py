import os
from ultralytics import YOLO

# =========================
# 📁 CONFIG (EDIT IF NEEDED)
# =========================
IMAGE_DIR = r"D:\minor_project\backend\dataset\images\train"
LABEL_DIR = r"D:\minor_project\backend\dataset\labels\train"

# model (use pretrained or your trained model)
MODEL_PATH = "yolov8n.pt"
# later you can switch to:
# MODEL_PATH = "runs/detect/train/weights/best.pt"

CONF_THRESHOLD = 0.25

# =========================
# 🚀 LOAD MODEL
# =========================
model = YOLO(MODEL_PATH)

# create label folder if not exists
os.makedirs(LABEL_DIR, exist_ok=True)

# =========================
# 🎯 CLASS MAPPING
# =========================
def map_class(coco_cls: int):
    # COCO class 0 = person → player
    if coco_cls == 0:
        return 0  # player
    else:
        return 1  # enemy (temporary)

# =========================
# 💾 SAVE YOLO LABEL
# =========================
def save_yolo_label(txt_path, detections, img_w, img_h):
    lines = []

    for cls, x1, y1, x2, y2 in detections:
        # normalize
        x_center = ((x1 + x2) / 2) / img_w
        y_center = ((y1 + y2) / 2) / img_h
        w = (x2 - x1) / img_w
        h = (y2 - y1) / img_h

        lines.append(f"{cls} {x_center} {y_center} {w} {h}")

    with open(txt_path, "w") as f:
        f.write("\n".join(lines))

# =========================
# 🔁 MAIN LOOP
# =========================
def auto_label():

    images = os.listdir(IMAGE_DIR)

    if not images:
        print("❌ No images found. Check dataset/images/train")
        return

    for img_name in images:

        if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        img_path = os.path.join(IMAGE_DIR, img_name)
        label_path = os.path.join(
            LABEL_DIR, img_name.rsplit(".", 1)[0] + ".txt"
        )

        results = model(img_path, conf=CONF_THRESHOLD, verbose=False)

        detections = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                coco_cls = int(box.cls[0])
                x1, y1, x2, y2 = map(float, box.xyxy[0])

                cls = map_class(coco_cls)

                # filter very small boxes
                area = (x2 - x1) * (y2 - y1)
                if area < 400:
                    continue

                detections.append((cls, x1, y1, x2, y2))

        # get image size
        h, w = results[0].orig_shape[:2]

        save_yolo_label(label_path, detections, w, h)

        print(f"✔ Labeled: {img_name}")

    print("✅ Auto-labeling completed!")


# =========================
# ▶️ RUN
# =========================
if __name__ == "__main__":
    auto_label()