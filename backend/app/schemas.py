from pydantic import BaseModel
from typing import List

class Vec2(BaseModel):
    x: float
    y: float

class Enemy(BaseModel):
    x: float
    y: float
    type: str
    speed: float = 1.0

class Projectile(BaseModel):
    source: str
    fire_rate: float = 1.0

class Checkpoint(BaseModel):
    x: float
    y: float

class MapSize(BaseModel):
    width: float
    height: float

class LevelJSON(BaseModel):
    map_size: MapSize
    player_spawn: Vec2
    enemies: List[Enemy] = []
    projectiles: List[Projectile] = []
    checkpoints: List[Checkpoint] = []