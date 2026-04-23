from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging

# 🔧 Your services
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
# 🔐 CORS (Restrict in prod)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📤 Upload Endpoint
# =========================
@app.post("/upload-level")
async def upload_level(files: List[UploadFile] = File(...)):

    logger.info("Received upload request")

    results = []

    for file in files:

        logger.info(f"Processing file: {file.filename}")

        # =========================
        # 🔐 File Type Validation
        # =========================
        if file.content_type != "application/json":
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a JSON file"
            )

        content = await file.read()

        # =========================
        # 🔐 File Size Validation
        # =========================
        if len(content) > 1_000_000:  # ~1MB limit
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is too large"
            )

        try:
            # =========================
            # 🧠 Feature Extraction
            # =========================
            features = extract_features(content)

            if not features:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid file content"
                )

            logger.info(f"Extracted features: {features}")

            # =========================
            # 🤖 ML Prediction
            # =========================
            difficulty = predict_difficulty(features)

            logger.info(f"Predicted difficulty: {difficulty}")

            # =========================
            # 💡 Recommendation Engine
            # =========================
            recommendations = generate_recommendation(features, difficulty)

            results.append({
                "filename": file.filename,
                "features": features,
                "difficulty_score": difficulty,
                "recommendations": recommendations
            })

        except HTTPException as http_err:
            raise http_err

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")

            raise HTTPException(
                status_code=500,
                detail="Internal processing error"
            )

    logger.info("Processing complete")

    return {
        "status": "processed",
        "data": results
    }

# =========================
# 🧪 Health Check (important)
# =========================
@app.get("/")
def health_check():
    return {"status": "API is running"}