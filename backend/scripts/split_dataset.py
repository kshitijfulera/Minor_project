import os
import shutil
import random

IMG_DIR = "dataset/images/train"
LBL_DIR = "dataset/labels/train"

VAL_IMG = "dataset/images/val"
VAL_LBL = "dataset/labels/val"

os.makedirs(VAL_IMG, exist_ok=True)
os.makedirs(VAL_LBL, exist_ok=True)

files = os.listdir(IMG_DIR)
random.shuffle(files)

split = int(len(files) * 0.2)

val_files = files[:split]

for f in val_files:
    shutil.move(os.path.join(IMG_DIR, f), os.path.join(VAL_IMG, f))

    label = f.replace(".jpg", ".txt")
    shutil.move(os.path.join(LBL_DIR, label), os.path.join(VAL_LBL, label))

print("✅ Dataset split complete")