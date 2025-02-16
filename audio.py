# audio handler 
# winning, eliminated player #, background music, robot/detecting sounds

import os
from utils.gemini_api import get_response

def play_winning_audio(player_id):
    # play audio of a winning player
    prompt = f"Can you say \"Player {player_id} won the game!\" for a video game. Just that part. Don't add anything else."
    
    # Get the response text (using Gemini API)
    audio_text = get_response(prompt)

    # Use macOS's 'say' command to speak the response
    os.system(f'say "{audio_text}"')
    pass


def play_eliminated_audio(player_id): # set to nothing for now
    prompt = f"Can you say \"Player {player_id} eliminated\" for a video game. Just that part. Don't add anything else."
    
    # Get the response text (using Gemini API)
    audio_text = get_response(prompt)

    # Use macOS's 'say' command to speak the response
    os.system(f'say "{audio_text}"')


def play_background_music():
    # play background music
    # use afplay to play a sound file
    os.system('afplay ./assets/background.mp3')
    pass


def play_robot_audio():
    # play robot audio
    # use afplay to play a sound file
    os.system('afplay ./assets/robots.mp3')
    pass


def play_green_light_audio():
    # play green light audio
    # use afplay to play a sound file
    os.system('afplay ./assets/green_light.mp3')
    pass


def play_red_light_audio():
    # play red light audio
    # use afplay to play a sound file
    os.system('afplay ./assets/red_light.mp3')
    pass