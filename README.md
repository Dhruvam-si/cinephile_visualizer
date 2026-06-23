# cinephile_visualizer
# Film Review Site

A Flask web app for writing and viewing your brain mindmap visualize according to movies watched and reviews wrote.

## Features
- User login with sessions
- Write and submit film reviews (stored in SQLite via SQLAlchemy)
- Flash messages for logout
- Review display page
- **AI-powered "unhinged insight"** — generates a witty, personalized take on your review by combining:
  - your written review
  - live online discourse about the film (fetched via Serper.dev)
  - your username, for a personalized roast-style insight
- UI styling assisted by GPT

## Tech Stack
- Flask + Flask-SQLAlchemy (backend + database)
- SQLite (local storage)
- Serper.dev API (fetches real-time online discourse/opinions about a film)
- Groq API running LLaMA 3.3 70B (generates the unhinged insight, chosen for free/low-cost access)

## Setup

1. Clone the repo and navigate into the project folder.

2. Create a virtual environment and activate it:
   ```
   python -m venv env
   env\Scripts\Activate.ps1   # Windows PowerShell
   ```

3. Install dependencies:
   ```
   pip install flask flask-sqlalchemy groq requests python-dotenv
   ```

4. Create a `.env` file in the project root (same folder as `app.py`) and add your own keys:
   ```
   FLASK_SECRET_KEY=your_secret_key_here
   GROQ_API_KEY=your_groq_key_here
   SERPER_API_KEY=your_serper_key_here
   ```
   Get a free Groq key at console.groq.com and a free Serper key at serper.dev.
   
   **Never commit your `.env` file** — it's already listed in `.gitignore`.

5. Run the app:
   ```
   python app.pys
   ```

## Roadmap
- [ ] Generate insight per individual review (currently uses first matching review)
- [ ] Generate one combined insight across multiple reviews/films at once
- [ ] Let user choose which film to generate insight on, instead of defaulting to the first one found
