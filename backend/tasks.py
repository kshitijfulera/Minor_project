from celery_worker import celery
from db import levels_collection
from utils.feature_extractor import extract_features
from ml_model.predict import predict_difficulty
from services.recommendation_engine import generate_recommendation
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@celery.task
def process_file_task(content, filename):
    try:
        logger.info(f"[CELERY] Processing {filename}")

        features = extract_features(content)
        difficulty = predict_difficulty(features)
        recommendations = generate_recommendation(features, difficulty)

        levels_collection.insert_one({
            "filename": filename,
            "features": features,
            "difficulty_score": difficulty,
            "recommendations": recommendations,
            "created_at": datetime.utcnow()
        })

        logger.info(f"[CELERY] Done {filename}")

    except Exception as e:
        logger.error(f"[CELERY] Error: {e}")