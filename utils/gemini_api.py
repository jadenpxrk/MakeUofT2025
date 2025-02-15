from google import genai


def get_response(prompt):
    import os

    # load from env
    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents={prompt}
    )

    return response.text
