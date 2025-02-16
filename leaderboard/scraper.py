import os
from dotenv import load_dotenv

load_dotenv()
import requests

# Load JSON_URL from environment variables
JSON_URL = os.getenv("JSON_URL")


def get_eliminated_player():
    """
    Fetches the who got removed
    Expected JSON structure:
        {
            "Game": "1",
            "ElIMINATED": "ID"
        }
    Returns the JSON data as a dict if successful, else None.
    """
    try:
        response = requests.get(JSON_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "Game" in data and "ELIMINATED" in data:
            return data
    except Exception as e:
        print(f"Error fetching game result: {e}")
    return None
