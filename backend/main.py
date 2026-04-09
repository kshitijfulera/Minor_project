from fastapi import FastAPI, UploadFile, File
from typing import List
from utils.feature_extractor import extract_features
from ml_model.predict import predict_difficulty

app = FastAPI()

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

        results.append({
            "filename": file.filename,
            "features": features,
            "difficulty_score": difficulty
        })

    return {
        "status": "processed",
        "data": results
    }