from fastapi import FastAPI, UploadFile, File
from typing import List
from utils.feature_extractor import extract_features
from ml_model.predict import predict_difficulty
from services.recommendation_engine import generate_recommendation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend running"}


@app.post("/upload-level")
async def upload_level(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        content = await file.read()

        features = extract_features(content)

        difficulty = predict_difficulty(features)

        recommendations = generate_recommendation(features, difficulty)

        results.append({
            "filename": file.filename,
            "features": features,
            "difficulty_score": difficulty,
            "recommendations": recommendations
        })

    return {
        "status": "processed",
        "data": results
    }