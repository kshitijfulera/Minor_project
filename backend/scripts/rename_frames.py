import os

FOLDER = "dataset/temp_frames"

files = [f for f in os.listdir(FOLDER) if f.endswith(".jpg")]
files.sort()  # important for order

for i, file in enumerate(files):
    new_name = f"frame_{i:06d}.jpg"

    old_path = os.path.join(FOLDER, file)
    new_path = os.path.join(FOLDER, new_name)

    os.rename(old_path, new_path)

print("✅ Renaming complete")