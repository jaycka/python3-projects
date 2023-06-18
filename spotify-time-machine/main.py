import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

spotify_client_id = os.environ.get('spotify_client_id')
spotify_client_secret = os.environ.get('spotify_client_secret')
URI = 'http://example.com'
scope = "playlist-modify-private"


def url_construct() -> str:
    travel_to = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")
    return 'https://www.billboard.com/charts/hot-100/' + travel_to


def get_top_100(url: str) -> dict:
    response = requests.get(url=url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    top_100_songs = soup.select('li ul li h3')
    top_100_artists = soup.find_all(name='span', class_='u-max-width-330')
    return dict(zip([song.getText().strip() for song in top_100_songs],
                    [artist.getText().strip() for artist in top_100_artists]))


def get_spotify_client() -> spotipy:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                   client_secret=spotify_client_secret,
                                                   redirect_uri=URI,
                                                   scope=scope,
                                                   cache_path='token.txt',
                                                   show_dialog=True))
    return sp


def create_songs_uri(songs_artists: dict, sp: spotipy) -> list:
    songs_uris = []
    for (song, artist) in songs_artists.items():
        result = sp.search(q=f'track:{song} artist:{artist}', type='track')
        try:
            uri = result['tracks']['items'][0]['uri']
        except IndexError:
            print(f"{song} by {artist} not found")
            pass
        else:
            print(f"{song} by {artist} found")
            songs_uris.append(uri)
        finally:
            print(f"{len(songs_uris)} out of {len(songs_artists)} found")
    return songs_uris


def create_and_add_playlist(url: str, songs_uris: list, sp: spotipy):
    user_id = sp.current_user()["id"]
    title = f'{url.split("/")[-1]} Billboard 100'
    playlist = sp.user_playlist_create(user=user_id, name=title, public=False)
    sp.playlist_add_items(playlist['id'], songs_uris, position=None)
    print(f"New playlist '{title}' successfully created on Spotify!")


if __name__ == '__main__':
    # spotify authentication
    sp = get_spotify_client()

    # construct the url for scraping
    url = url_construct()

    # get top 100 songs and corresponding artists
    songs_and_artists = get_top_100(url)

    # search for each song in spotify and return uris
    songs_uris = create_songs_uri(songs_and_artists, sp)

    # create playlist in spotify
    create_and_add_playlist(url=url, songs_uris=songs_uris, sp=sp)
