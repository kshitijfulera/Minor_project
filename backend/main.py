from FastAPI import FastAPI, UploadFile, File
from typing import List
from utils.feature_extractor import extract_features

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend running"}


@app.post("/upload-level")
async def upload_level(
    files: List[UploadFile] = File(..., description="Upload JSON or image files")
):
    results = []

    for file in files:
        content = await file.read()

        features = extract_features(content)

        results.append({
            "filename": file.filename,
            "features": features
        })

    return {
        "status": "processed",
        "data": results
    }