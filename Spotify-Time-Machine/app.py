import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET"
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "playlist-modify-private"

sp_oauth = SpotifyOAuth(
    scope=SCOPE,
    redirect_uri=REDIRECT_URI,
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    show_dialog=True,
    cache_path="token.txt"
)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/travel', methods=['POST'])
def travel():
   
    date = request.form.get('date') 
    year = date.split("-")[0]

    try:
        response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        song_names_spans = soup.select("li ul li h3")
        song_names = [song.get_text(strip=True) for song in song_names_spans]

        if not song_names:
            return "Error: Could not find songs for this date. Billboard structure might have changed."

    except Exception as e:
        return f"Error scraping data: {e}"

    sp = spotipy.Spotify(auth_manager=sp_oauth)
    user_id = sp.current_user()["id"]

    song_uris = []
    for song in song_names:
        try:
            result = sp.search(q=f"track:{song} year:{year}", type="track")
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            pass

    playlist_name = f"{date} Billboard 100"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

    if song_uris:
        sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)

    return render_template('success.html', playlist_url=playlist['external_urls']['spotify'], name=playlist_name)


if __name__ == "__main__":
    app.run(debug=True)

