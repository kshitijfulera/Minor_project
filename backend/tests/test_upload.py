from fastapi.testclient import TestClient
from app.main import app  # adjust if your main file path is different

client = TestClient(app)


def test_upload():

    # sample test JSON file
    test_file = {
        "files": (
            "test.json",
            b'{"enemies": ["e1"], "spawn_rate": 1, "rewards": ["coin"], "checkpoints": ["cp1"]}',
            "application/json",
        )
    }

    response = client.post("/upload-level", files=test_file)

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "difficulty_score" in data["data"][0]