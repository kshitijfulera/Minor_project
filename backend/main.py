from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from datetime import datetime

# 🔧 DB
from db import levels_collection

# 🔧 ML + features
from utils.json_feature_extractor import extract_features
from ml_model.predict import predict_difficulty

# 🔧 Explainability
from services.explain import explain_prediction, feature_contributions

# =========================
# 🧠 Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
    allow_credentials=True,
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
# 📊 Analyze (MAIN)
# =========================
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        logger.info("📥 Received file for analysis")

        if file.content_type != "application/json":
            raise HTTPException(status_code=400, detail="Invalid file type")

        content = await file.read()

        # 🔍 Extract features
        features = extract_features(content)
        logger.info(f"Features: {features}")

        # 🤖 Predict
        difficulty, confidence = predict_difficulty(features)

        # 🎯 Difficulty category
        if difficulty > 0.7:
            category = "Hard"
        elif difficulty > 0.4:
            category = "Medium"
        else:
            category = "Easy"

        # 🧠 Explain
        explanation = explain_prediction(features)
        contributions = feature_contributions(features)

        # 📦 Result object
        result = {
            "filename": file.filename,
            "difficulty_score": float(difficulty),
            "confidence": float(confidence),
            "category": category,
            "features": features,
            "explanation": explanation,
            "contributions": contributions,
            "model_version": "v1.0",
            "created_at": datetime.utcnow()
        }

        # 💾 Save to DB
        inserted = levels_collection.insert_one(result)

        # 🔥 FIX ObjectId issue
        result["_id"] = str(inserted.inserted_id)

        return result

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return {"error": str(e)}

# =========================
# 📤 Upload multiple files
# =========================
@app.post("/upload-level")
async def upload_level(files: List[UploadFile] = File(...)):

    results = []

    for file in files:
        try:
            if file.content_type != "application/json":
                continue

            content = await file.read()

            features = extract_features(content)
            difficulty, confidence = predict_difficulty(features)

            if difficulty > 0.7:
                category = "Hard"
            elif difficulty > 0.4:
                category = "Medium"
            else:
                category = "Easy"

            explanation = explain_prediction(features)
            contributions = feature_contributions(features)

            result = {
                "filename": file.filename,
                "difficulty_score": float(difficulty),
                "confidence": float(confidence),
                "category": category,
                "features": features,
                "explanation": explanation,
                "contributions": contributions,
                "model_version": "v1.0",
                "created_at": datetime.utcnow()
            }

            inserted = levels_collection.insert_one(result)
            result["_id"] = str(inserted.inserted_id)

            results.append(result)

        except Exception as e:
            logger.error(f"Error processing {file.filename}: {e}")

    return {
        "status": "processed",
        "data": results
    }

# =========================
# 📥 Get all levels
# =========================
@app.get("/levels")
def get_levels():

    levels = []

    for item in levels_collection.find().sort("created_at", -1):
        item["_id"] = str(item["_id"])  # fix ObjectId
        levels.append(item)

    return {"data": levels}