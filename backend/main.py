from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from datetime import datetime

from db import levels_collection

# ✅ NEW
from app.schemas import LevelJSON
from utils.json_feature_extractor import extract_features
from ml_model.predict import predict_difficulty

# =========================
# 🧠 Logging
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# 🚀 App
# =========================
app = FastAPI()

# =========================
# 🔐 CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🧪 Health
# =========================
@app.get("/")
def health():
    return {"status": "API running"}

# =========================
# 📤 Analyze JSON (MAIN ENDPOINT)
# =========================
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    if file.content_type != "application/json":
        raise HTTPException(400, "Only JSON allowed")

    content = await file.read()

    if len(content) > 1_000_000:
        raise HTTPException(400, "File too large")

    try:
        data = json.loads(content)

        # ✅ Validate structure
        LevelJSON(**data)

    except Exception as e:
        raise HTTPException(422, f"Invalid JSON: {e}")

    try:
        # =========================
        # 🧠 Feature Extraction
        # =========================
        features = extract_features(content)

        logger.info(f"Features: {features}")

        # =========================
        # 🤖 Prediction
        # =========================
        difficulty = predict_difficulty(features)

        logger.info(f"Difficulty: {difficulty}")

        # =========================
        # 💾 Save
        # =========================
        levels_collection.insert_one({
            "filename": file.filename,
            "features": features,
            "difficulty_score": difficulty,
            "created_at": datetime.utcnow(),
            "source": "json"
        })

        return {
            "difficulty_score": difficulty,
            "features": features,
            "recommendations": generate_recommendations(features)
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, "Processing error")

# =========================
# 📥 Get Levels
# =========================
@app.get("/levels")
def get_levels():
    levels = list(levels_collection.find({}, {"_id": 0}))
    return {"data": levels}

# =========================
# 💡 Recommendations
# =========================
def generate_recommendations(f):

    rec = []

    if f["enemy_density"] > 0.05:
        rec.append("Reduce enemy density")

    if f["projectile_rate"] > 2:
        rec.append("Reduce projectile fire rate")

    if f["avg_threat"] < 20:
        rec.append("Increase spacing near player spawn")

    if not rec:
        rec.append("Level looks balanced")

    return rec