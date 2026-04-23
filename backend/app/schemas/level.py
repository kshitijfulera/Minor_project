from pydantic import BaseModel

class LevelFeatures(BaseModel):
    enemy_count: int
    spawn_rate: float
    rewards: int
    checkpoints: int