import cv2
import os
import numpy as np

# =========================
# 📁 Paths
# =========================
VIDEO_DIR = "dataset/videos"
OUTPUT_DIR = "dataset/temp_frames"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# ⚙️ Settings
# =========================
FRAME_SKIP = 5        # save every Nth frame
BRIGHTNESS_THRESH = 10
CONTRAST_THRESH = 5
DIFF_THRESH = 2      # similarity threshold

# =========================
# 🚀 Extract Frames
# =========================
def extract_frames():

    saved = 0

    for video_name in os.listdir(VIDEO_DIR):

        if not video_name.lower().endswith((".mp4", ".avi", ".mov")):
            continue

        video_path = os.path.join(VIDEO_DIR, video_name)
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"❌ Cannot open {video_name}")
            continue

        print(f"🎥 Processing: {video_name}")

        frame_idx = 0
        prev_gray = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1

            # =========================
            # ⏩ Frame skipping
            # =========================
            if frame_idx % FRAME_SKIP != 0:
                continue

            # Resize (optional, faster processing)
            frame = cv2.resize(frame, (320, 240))

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # =========================
            # 🌑 Skip dark / low-contrast frames
            # =========================
            brightness = np.mean(gray)
            contrast = np.std(gray)

            if brightness < BRIGHTNESS_THRESH or contrast < CONTRAST_THRESH:
                continue

            # =========================
            # 🔁 Skip similar frames
            # =========================
            if prev_gray is not None:
                diff = cv2.absdiff(prev_gray, gray)

                if np.mean(diff) < DIFF_THRESH:
                    continue

            prev_gray = gray

            # =========================
            # 💾 Save frame
            # =========================
            filename = f"{video_name.replace('.', '_')}_{saved}.jpg"
            save_path = os.path.join(OUTPUT_DIR, filename)

            cv2.imwrite(save_path, frame)
            saved += 1

        cap.release()

    print(f"\n✅ Total frames saved: {saved}")


# =========================
# ▶️ Run
# =========================
if __name__ == "__main__":
    extract_frames()