from groq import Groq
from serper_discourse import get_discourse
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# paste your groq API key here (same one from your Jarvis project)
client = Groq(api_key=GROQ_API_KEY)


def generate_unhinged_insight(movie_name, user_review, discourse , user_name):
    
    """
    Takes the movie name, the user's own review, and scraped online discourse,
    and asks Groq to generate a witty/unhinged insight around 40-70 words.
    """
    prompt = f"""
You are writing a short, witty, Spotify-Wrapped-style "insight" about a review written by {user_name}.

Movie: {movie_name}

User's review: "{user_review}"

Online discourse about this movie (random opinions from the internet): {discourse} 

Write a short (under 80 words), funny, slightly roasting insight about the user's
take on this movie. Reference the online discourse if it's relevant or contrasts
with the user's opinion. Keep it punchy and conversational, like a recap card.Also try to reference user name
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    movie = input("Movie name: ")
    review = input("Your review of it: ")
    discourse=get_discourse(movie)
 
    # using the discourse string you already got working from Serper
    if discourse:
        insight = generate_unhinged_insight(movie, review, discourse)
        print("\n--- UNHINGED INSIGHT ---\n")
        print(insight)
    else:
        print("Couldn't fetch discourse for this movie — skipping insight generation.")