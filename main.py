import time
import random
from audio import (
    play_background_music,
    play_robot_audio,
    play_eliminated_audio,
    play_winning_audio,
    play_green_light_audio,
    play_red_light_audio,
)
from leaderboard.redis_client import RedisClient  # import the class
from app import get_last_game_id, set_last_game_id
from leaderboard.scraper import get_eliminated_player


# --- Audio & Game Round Functions ---
def green_light_phase():
    print("GREEN LIGHT! Players can move.")
    play_green_light_audio()
    time.sleep(1)


def background_phase():
    play_background_music()
    time.sleep(1)


def red_light_phase():
    print("RED LIGHT! Stop moving!")
    play_red_light_audio()
    play_robot_audio()


# --- Game State Functions ---
def check_for_button_press(redis_client):
    # Check for a winner (set by app.py) in Redis.
    winner = get_last_game_id(redis_client)
    if winner:
        redis_client.delete("last_game_id")
        return winner
    return None


def eliminate_player(players):
    eliminated = get_eliminated_player()["ELIMINATED"]
    print(f"No button press detected. Player {eliminated} eliminated for moving.")
    play_eliminated_audio(eliminated)
    # players.remove(eliminated)


def run_game(redis_client):
    players = [13, 390, 191, 473]
    max_rounds = 5
    round_count = 1
    winner = None

    while round_count <= max_rounds:
        print(f"\n--- Round {round_count} ---")

        # Green Light Phase
        green_light_phase()
        winner = check_for_button_press(redis_client)
        if winner is not None:
            break

        # Background Phase
        background_phase()
        winner = check_for_button_press(redis_client)
        if winner is not None:
            break

        # Red Light Phase
        red_light_phase()
        winner = check_for_button_press(redis_client)
        if winner is not None:
            break

        eliminate_player(players)
        if not players:
            print("No players left. Game over.")
            return

        round_count += 1
        time.sleep(2)

    if winner is not None:
        print(
            f"Player {winner} pressed their button first and reached the finish line!"
        )
        play_winning_audio(winner)
    else:
        print("Game Over. No finish line reached this session.")


def main():
    redis_client = RedisClient()  # create your redis client instance
    run_game(redis_client)


if __name__ == "__main__":
    main()
