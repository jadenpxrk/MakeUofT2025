import os
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import pandas as pd
import json
import redis
import scraper
from streamlit_autorefresh import (
    st_autorefresh,
)

REDIS_KEY = "leaderboard_data"

# Load Redis configuration from environment variables
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD")
redis_ssl = os.getenv("REDIS_SSL", "True").lower() in ["true", "1", "yes"]
redis_ssl_cert_reqs = os.getenv("REDIS_SSL_CERT_REQS")
if redis_ssl_cert_reqs == "None":
    redis_ssl_cert_reqs = None

r = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    ssl=redis_ssl,
    ssl_cert_reqs=redis_ssl_cert_reqs,
)


def load_leaderboard():
    data = r.get(REDIS_KEY)
    if data:
        return json.loads(data)
    # fallback
    return []


def get_last_game_id():
    last = r.get("last_game_id")
    if last:
        return last.decode("utf-8")
    return None


def set_last_game_id(game_id):
    r.set("last_game_id", game_id)


def save_leaderboard(data):
    r.set(REDIS_KEY, json.dumps(data, indent=4))


def register_win(player_id):
    leaderboard = load_leaderboard()
    found = False
    for entry in leaderboard:
        if entry["Player"] == player_id:
            entry["Wins"] += 1
            found = True
            break
    if not found:
        # Add new player with one win if not found
        leaderboard.append({"Player": player_id, "Wins": 1})
    save_leaderboard(leaderboard)


if "last_game_id" not in st.session_state:
    st.session_state.last_game_id = None


if "last_game_id" not in st.session_state:
    st.session_state.last_game_id = None


def main():
    st_autorefresh(interval=10000, key="game_refresh")

    # Scrape the latest game result
    game_data = scraper.get_latest_game_result()
    st.write("Scraped game_data:", game_data)

    last_game_id = get_last_game_id()

    # Only register win if this game hasn't been processed yet
    if game_data:
        if last_game_id is None or game_data["Game"] != last_game_id:
            register_win(game_data["Winner"])
            set_last_game_id(game_data["Game"])

    st.title("Leaderboard")
    leaderboard = load_leaderboard()
    st.write("Loaded leaderboard:", leaderboard)

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

    df = pd.DataFrame(sorted_leaderboard)
    df.index = range(1, len(df) + 1)

    def color_row(row):
        if row["Medal"] == "Gold":
            return ["background-color: gold"] * len(row)
        elif row["Medal"] == "Silver":
            return ["background-color: silver"] * len(row)
        elif row["Medal"] == "Bronze":
            return ["background-color: #cd7f32"] * len(row)
        else:
            return ["" for _ in row]

    styled_df = df.style.apply(color_row, axis=1)
    styled_df = styled_df.set_table_styles(
        [{"selector": "table", "props": [("width", "100%")]}]
    )
    st.write(styled_df)


if __name__ == "__main__":
    main()
