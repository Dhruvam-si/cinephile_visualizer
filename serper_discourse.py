import requests
# paste your serper.dev API key here
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("SERPER_API_KEY")


def get_discourse(movie_name):
    """
    Fetches online discourse/opinions about a movie.
    Returns a single string of combined snippets, ready to feed into Groq.
    """
    url = "https://google.serper.dev/search"
    payload = {
        "q": f"{movie_name} movie reviews controversial opinions reddit"
    }
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        # if the call fails, return empty string so Groq just gets no discourse
        # instead of crashing the whole app
        return ""

    data = response.json()
    results = data.get("organic", [])[:5]

    snippets = [r.get("snippet", "") for r in results]
    return " ".join(snippets)


if __name__ == "__main__":
    movie = input("Enter a movie name to test: ")
    discourse = get_discourse(movie)
    print("\nCOMBINED DISCOURSE STRING:\n")
    print(discourse)