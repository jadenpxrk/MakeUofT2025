import os
from dotenv import load_dotenv
from google import genai

# Load env from utils/.env
key = load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def get_response(prompt):
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents={prompt}
    )
    return response.text
