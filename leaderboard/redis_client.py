import json
import redis
from .config import get_redis_config

REDIS_KEY = "leaderboard_data"

class RedisClient:
    def __init__(self):
        config = get_redis_config()
        self.client = redis.Redis(**config)

    def get_json(self, key):
        data = self.client.get(key)
        return json.loads(data) if data else None

    def set_json(self, key, data):
        self.client.set(key, json.dumps(data, indent=4))

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value):
        self.client.set(key, value)
