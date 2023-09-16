from bs4 import BeautifulSoup
import requests
from parameters import *


def get_song_titles(year):
    billboard_url = "https://www.billboard.com/charts/hot-100/" + year + "/"

    response = requests.get(billboard_url)

    webpage_contents = BeautifulSoup(response.text, "html.parser")
    song_titles = webpage_contents.select("div ul li ul li h3")

    song_titles = [title.text.strip() for title in song_titles]

    return song_titles


def search_spotify():

    # To get the access token
    spotify_post_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    spotify_post_parameters = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    spotify_access_token = requests.post(url="https://accounts.spotify.com/api/token",
                                         headers=spotify_post_headers,
                                         params=spotify_post_parameters)
    print(spotify_access_token.json())

    spotify_get_headers = {
        "Authorization": "Bearer " + spotify_access_token.json()["access_token"],
    }

    spotify_search = requests.get(url="https://api.spotify.com/v1/search",
                                  headers=spotify_get_headers,
                                  params={
                                      "q": "track:Fast%2520Car",
                                      "type": "track",
                                  })
    print(spotify_search.json())


# print("Welcome to Spotify Time Machine")
# year = input("Which year you want to travel to? Type the date in YYYY-MM-DD format: ")
# song_titles = get_song_titles(year)
search_spotify()



