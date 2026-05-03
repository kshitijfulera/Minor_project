from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from datetime import datetime

from db import levels_collection
from utils.feature_extractor import extract_features
from ml_model.predict import predict_difficulty
from services.recommendation_engine import generate_recommendation

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
async def upload_level(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    logger.info("Received upload request")

    for file in files:

        if file.content_type != "application/json":
            raise HTTPException(status_code=400, detail="Invalid file")

        content = await file.read()

        # 🚀 Run in background
        background_tasks.add_task(process_file, content, file.filename)

    return {
        "status": "accepted",
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