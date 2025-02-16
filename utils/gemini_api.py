import os
from dotenv import load_dotenv
from google import genai

# Load env from utils/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def get_response(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents={prompt}
    )
    return response.text