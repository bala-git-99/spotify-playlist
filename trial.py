import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from parameters import *


def get_song_titles(year):
    billboard_url = "https://www.billboard.com/charts/hot-100/" + year + "/"

    response = requests.get(billboard_url)

    webpage_contents = BeautifulSoup(response.text, "html.parser")
    song_titles = webpage_contents.select("div ul li ul li h3")

    song_titles = [title.text.strip() for title in song_titles]

    return song_titles


def authentication_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username=SP_USERNAME
    ))
    return sp
    # user_id = sp.current_user()["id"]
    # print(user_id)


def search_spotify(songs_list):
    # print(songs_list)
    songs_uri = []
    for song_title in songs_list:
        results = sp.search(q=f"track:{song_title}", type="track")
        try:
            songs_uri.append(str(results["tracks"]["items"][0]["uri"]))
        except IndexError:
            print(f"{song_title} -  doesn't exist, so skipping")
    return songs_uri


def operation_playlist(songs):
    # Create a playlist
    user_id = sp.current_user()["id"]
    playlist_name = f"{year} Billboard 100"
    playlist_description = "This playlist if created by a Python program"
    playlist_id = sp.user_playlist_create(user=user_id, name=playlist_name, description=playlist_description,
                                          public=False)
    # print(playlist_id)

    # Add songs to the playlist
    final_response = sp.playlist_add_items(playlist_id["id"], items=songs, position=None)
    print(final_response)


print("Welcome to Spotify Time Machine")
year = input("Which year you want to travel to? Type the date in YYYY-MM-DD format: ")
song_titles = get_song_titles(year)
sp = authentication_spotify()
operation_playlist(search_spotify(song_titles))
