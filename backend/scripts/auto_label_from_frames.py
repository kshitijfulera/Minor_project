import os
import shutil
from ultralytics import YOLO

INPUT_DIR = "dataset/temp_frames"
IMG_OUT = "dataset/images/train"
LBL_OUT = "dataset/labels/train"

os.makedirs(IMG_OUT, exist_ok=True)
os.makedirs(LBL_OUT, exist_ok=True)

model = YOLO("yolov8n.pt")  # or yolov8n.pt

CONF = 0.3

def save_label(path, boxes, w, h):
    lines = []
    for cls, x1, y1, x2, y2 in boxes:
        xc = ((x1 + x2) / 2) / w
        yc = ((y1 + y2) / 2) / h
        bw = (x2 - x1) / w
        bh = (y2 - y1) / h
        lines.append(f"{cls} {xc} {yc} {bw} {bh}")

    with open(path, "w") as f:
        f.write("\n".join(lines))


for img_name in os.listdir(INPUT_DIR):

    if not img_name.endswith(".jpg"):
        continue

    img_path = os.path.join(INPUT_DIR, img_name)

    results = model(img_path, conf=CONF, verbose=False)

    boxes = []

    for r in results:
        if r.boxes is None:
            continue

        for b in r.boxes:
            cls = int(b.cls[0])
            x1, y1, x2, y2 = map(float, b.xyxy[0])
            boxes.append((cls, x1, y1, x2, y2))

    # Skip empty detections (optional)
    if len(boxes) == 0:
        continue

    # Move image to dataset
    new_img_path = os.path.join(IMG_OUT, img_name)
    shutil.copy(img_path, new_img_path)

    # Save label
    h, w = results[0].orig_shape[:2]
    txt_path = os.path.join(LBL_OUT, img_name.replace(".jpg", ".txt"))
    save_label(txt_path, boxes, w, h)

print("✅ Auto-labeling complete")