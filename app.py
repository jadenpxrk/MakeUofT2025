import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from leaderboard.board import Leaderboard
from leaderboard.display import style_leaderboard
from leaderboard.redis_client import RedisClient, REDIS_KEY

# Keys for Redis
LAST_GAME_KEY = "last_game_id"


def get_last_game_id(redis_client):
    last = redis_client.get(LAST_GAME_KEY)
    return last.decode("utf-8") if last else None


def set_last_game_id(redis_client, game_id):
    redis_client.set(LAST_GAME_KEY, game_id)


# def update_leaderboard(redis_client, leaderboard_obj):
# game_data = get_latest_game_result()
# # st.write("Scraped game_data:", game_data)
# last_game_id = get_last_game_id(redis_client)
# if game_data and (last_game_id is None or game_data["Game"] != last_game_id):
#     leaderboard_obj.register_win(game_data["Winner"])
#     set_last_game_id(redis_client, game_data["Game"])
# do it based off what button was pressed


def display_leaderboard(redis_client, leaderboard_obj):
    st.title("Leaderboard")

    # Initialize last_winner in session state if not already set
    if "last_winner" not in st.session_state:
        st.session_state.last_winner = None

    # Create three columns for the win buttons
    col1, col2, col3 = st.columns(3)

    # Register win based on button press and store the winner in session state
    if col1.button("Red"):
        st.session_state.last_winner = "191"
        leaderboard_obj.register_win("191")
        set_last_game_id(redis_client, "191")
    if col2.button("Green"):
        st.session_state.last_winner = "473"
        leaderboard_obj.register_win("473")
        set_last_game_id(redis_client, "473")
    if col3.button("Blue"):
        st.session_state.last_winner = "013"
        leaderboard_obj.register_win("013")
        set_last_game_id(redis_client, "013")

    # Display the last winner if one exists
    if st.session_state.last_winner:
        st.success(f"Player {st.session_state.last_winner} wins! Win registered.")

    sorted_lb = leaderboard_obj.get_sorted()
    df = pd.DataFrame(sorted_lb)
    df.index = range(1, len(df) + 1)
    style_leaderboard(df)


def main():
    st_autorefresh(interval=10000, key="game_refresh")
    redis_client = RedisClient()
    leaderboard_obj = Leaderboard()
    # update_leaderboard(redis_client, leaderboard_obj)
    display_leaderboard(redis_client, leaderboard_obj)


if __name__ == "__main__":
    main()
