import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

token = SpotifyOAuth(client_id=os.environ.get("SPOTIPY_SWITCHER_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_SWITCHER_CLIENT_SECRET"), redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"), scope="playlist-modify-public", username=os.environ.get("SPOTIFY_USERNAME"))
sp = spotipy.Spotify(auth_manager=token)

def main():
    user_id = sp.me()['id']
    popey_playlists = sp.user_playlists('sirpopey')

    while popey_playlists:
        for playlist in popey_playlists['items']:
            line_split = playlist['name'].split()
            line_joined = " ".join(line_split[1:])
            line_edited = "RPG: " + line_joined
            print(line_edited)
            new_playlist = sp.user_playlist_create(user_id, line_edited)
            song_dict = sp.playlist_items(playlist['id'], fields='items')
            songs = [element['track']['id'] for element in song_dict['items'] if element['track']['id'] is not None]
            sp.playlist_add_items(new_playlist['id'], songs)
        if popey_playlists['next']:
            popey_playlists = sp.next(popey_playlists)
        else:
            popey_playlists = None

    user_id = sp.me()['id']


if __name__ == "__main__":
    main()
