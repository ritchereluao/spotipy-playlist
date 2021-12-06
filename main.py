from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ⚠️👇🏻 Copy and paste the URL 👇🏻⚠️ #
URL = f"https://www.billboard.com/charts/year-end/2010/hot-100-songs/"

response = requests.get(url=URL)
soup = BeautifulSoup(response.text, "html.parser")

song_titles = soup.select("li ul li h3")
song_names = [each_song.getText().strip() for each_song in song_titles]
# print(song_names)

song_artists = soup.select("li ul li span")
artists = [artist.getText().strip() for artist in song_artists]
# print(artists)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="SPOTIPY CLIENT ID",
    client_secret="SPOTIPY CLIENT SECRET",
    redirect_uri="http://example.com",
    scope="playlist-modify-private",
    cache_path="token.txt"
))

user_id = sp.current_user()["id"]
song_uris = []

for song in song_names:
    # ⚠️ Edit the year range accordingly ⚠️👇🏻 #
    result = sp.search(q=f"track:{song} year:2000-2010", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} -- Skipped.")
# print(song_uris)

# 👇🏻⚠️ Code creates your Spotify Playlist! ⚠️👇🏻 #
playlist = sp.user_playlist_create(user=user_id, name="2010 Billboard Year-End Charts", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
