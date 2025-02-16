from .redis_client import RedisClient, REDIS_KEY

class Leaderboard:
    def __init__(self):
        self.redis = RedisClient()

    def load(self):
        data = self.redis.get_json(REDIS_KEY)
        return data if data is not None else []

    def save(self, leaderboard):
        self.redis.set_json(REDIS_KEY, leaderboard)

    def register_win(self, player_id):
        leaderboard = self.load()
        for entry in leaderboard:
            if entry["Player"] == player_id:
                entry["Wins"] += 1
                break
        else:
            leaderboard.append({"Player": player_id, "Wins": 1})
        self.save(leaderboard)

    def get_sorted(self):
        leaderboard = self.load()
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x["Wins"], reverse=True)
        for rank, player in enumerate(sorted_leaderboard):
            if rank == 0:
                player["Medal"] = "Gold"
            elif rank == 1:
                player["Medal"] = "Silver"
            elif rank == 2:
                player["Medal"] = "Bronze"
            else:
                player["Medal"] = "-"
        return sorted_leaderboard
