
🎵 The Spotify Time Machine 🕰️
Ever wondered what the world was listening to on the exact day you were born? Or maybe you want to relive the summer hits of 1999?

This is a Python web application that lets you travel back in time musically. You simply pick a date in history, and the app scrapes the Billboard Hot 100 chart for that week, finds those exact songs on Spotify, and instantly creates a private playlist in your account.

It’s nostalgia, automated.

🎥 See it in Action
Watch a quick demo of how it works here:

https://youtu.be/cE-hXqZPWKI?si=ADWTQ3YnBCN5rN0X

⚙️ How It Works Under the Hood
It looks simple on the front end, but there's some cool Python logic happening backstage:

The Interface: A clean Flask web app (styled with Bootstrap) asks for a date.

The Scraping: It takes that date and sends Python’s requests and BeautifulSoup to crawl the historical Billboard Hot 100 page to grab song titles and artists.

The Matching: It uses Spotipy (the Spotify Web API wrapper) to search for those specific tracks within that specific year.

The Creation: It authenticates into your Spotify account and builds a new, private playlist with the songs it found.

Error Handling: Sometimes a song from 1974 isn't on Spotify. The success page intelligently lists any tracks that had to be skipped so you know exactly what's missing.

🛠️ Getting Started (Run it yourself!)
Want to run this locally? Here is the step-by-step guide.

Prerequisites
Python 3.x installed.

A Spotify account 

Step 1: Clone the Repo

cd Spotify-Time-Machine

Step 2: Install Dependencies
It's recommended to use a virtual environment. Install the required libraries:
pip install -r requirements.txt

Step 3: The Crucial Part - Spotify Credentials 🔑
To create playlists on your behalf, the app needs permission from Spotify.

Go to the Spotify Developer Dashboard and log in.

Create an App. Give it any name (e.g., "Time Machine Project").

Once created, go to the app settings and find your Client ID and Client Secret.

Important: In the app settings on the Spotify dashboard, find "Redirect URIs" and add exactly: http://example.com (or whatever URI you set in your code, but http://example.com works fine for local testing).

Back in your project folder on your computer, rename the file .env.example to just .env 

Open the .env file and paste your credentials:

Ini, TOML

# .env file
SPOTIPY_CLIENT_ID=your_pasted_client_id_here
SPOTIPY_CLIENT_SECRET=your_pasted_client_secret_here
SPOTIPY_REDIRECT_URI=http://example.com
Note: This .env file is ignored by Git, so your secrets stay safe on your machine.

Step 4: Run it!
python app.py
Open your browser to the localhost link provided in the terminal (usually http://127.0.0.1:5000/).

📚 Built With

Python
Flask (Web Framework)
BeautifulSoup4 (Web Scraping)
Spotipy (Spotify Web API)
Bootstrap 5 (Frontend Styling)

Enjoy your musical time travel! 🚀
