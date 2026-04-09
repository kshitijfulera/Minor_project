import json

def extract_features(file_content: bytes):

    try:
        data = json.loads(file_content)

        features = {
            "enemy_count": len(data.get("enemies", [])),
            "spawn_rate": data.get("spawn_rate", 0),
            "rewards": len(data.get("rewards", [])),
            "checkpoints": len(data.get("checkpoints", []))
        }

        return features

    except Exception as e:
        return {"error": str(e)}