# main.py
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from leaderboard.board import Leaderboard
from leaderboard.display import style_leaderboard
from leaderboard.redis_client import RedisClient, REDIS_KEY
from leaderboard.scraper import get_latest_game_result  

# Keys for Redis
LAST_GAME_KEY = "last_game_id"

def get_last_game_id(redis_client):
    last = redis_client.get(LAST_GAME_KEY)
    return last.decode("utf-8") if last else None

def set_last_game_id(redis_client, game_id):
    redis_client.set(LAST_GAME_KEY, game_id)

def update_leaderboard(redis_client, leaderboard_obj):
    game_data = get_latest_game_result()
    st.write("Scraped game_data:", game_data)
    last_game_id = get_last_game_id(redis_client)
    if game_data and (last_game_id is None or game_data["Game"] != last_game_id):
        leaderboard_obj.register_win(game_data["Winner"])
        set_last_game_id(redis_client, game_data["Game"])

def display_leaderboard(leaderboard_obj):
    st.title("Leaderboard")
    sorted_lb = leaderboard_obj.get_sorted()
    st.write("Loaded leaderboard:", sorted_lb)
    df = pd.DataFrame(sorted_lb)
    df.index = range(1, len(df) + 1)
    style_leaderboard(df)

def main():
    st_autorefresh(interval=10000, key="game_refresh")
    redis_client = RedisClient()
    leaderboard_obj = Leaderboard()
    update_leaderboard(redis_client, leaderboard_obj)
    display_leaderboard(leaderboard_obj)

if __name__ == "__main__":
    main()
