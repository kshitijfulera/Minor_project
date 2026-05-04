from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from datetime import datetime

from db import levels_collection
from utils.feature_extractor import extract_features
from ml_model.predict import predict_difficulty
from services.recommendation_engine import generate_recommendation
from tasks import process_file_task
from utils.video_feature_extractor import extract_video_features

# =========================
# 🧠 Logging Setup
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# =========================
# 🚀 FastAPI App
# =========================
app = FastAPI()

# =========================
# 🔐 CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🔄 Background Processor
# =========================
def process_file(content, filename):
    try:
        logger.info(f"[BG] Processing {filename}")

        features = extract_features(content)

        if not features:
            logger.error("Invalid features")
            return

        difficulty = predict_difficulty(features)
        recommendations = generate_recommendation(features, difficulty)

        levels_collection.insert_one({
            "filename": filename,
            "features": features,
            "difficulty_score": difficulty,
            "recommendations": recommendations,
            "created_at": datetime.utcnow()
        })

        logger.info(f"[BG] Done {filename}")

    except Exception as e:
        logger.error(f"[BG] Error: {e}")

# =========================
# 📤 Upload (INSTANT)
# =========================
@app.post("/upload-level")
async def upload_level(files: List[UploadFile] = File(...)):

    for file in files:
        content = await file.read()

        # 🚀 send to queue
        process_file_task.delay(content, file.filename)

    return {
        "status": "queued",
        "message": "Processing in background"
    }

# =========================
# 📥 Get Levels
# =========================
@app.get("/levels")
def get_levels():
    levels = list(levels_collection.find({}, {"_id": 0}))
    return {"data": levels}

# =========================
# 🧪 Health Check
# =========================
@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):

    if not file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 allowed")

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    features = extract_video_features(temp_path)

    difficulty = predict_difficulty(features)

    return {
        "features": features,
        "difficulty": difficulty
    }