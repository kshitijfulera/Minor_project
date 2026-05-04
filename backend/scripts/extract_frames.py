import cv2
import os

def extract_frames(video_path, output_dir, skip=10):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % skip == 0:
            filename = os.path.join(output_dir, f"frame_{saved}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1

        count += 1

    cap.release()
    print(f"Saved {saved} frames")

# Example
extract_frames("contra.mp4", "dataset/images")