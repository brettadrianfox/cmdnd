import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# TODO: Mask the name of the user you are copying playlists from using an environment variable!

token = SpotifyOAuth(client_id=os.environ.get("SPOTIPY_SWITCHER_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_SWITCHER_CLIENT_SECRET"), redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"), scope="playlist-modify-public", username=os.environ.get("SPOTIFY_USERNAME"))
sp = spotipy.Spotify(auth_manager=token)

def main():
    user_id = sp.me()['id']
    other_user_playlists = sp.user_playlists('OTHER_SPOTIFY_USERNAME')

    while other_user_playlists:
        for playlist in other_user_playlists['items']:
            line_split = playlist['name'].split()
            line_joined = " ".join(line_split[1:])
            line_edited = "RPG: " + line_joined
            print(line_edited)
            new_playlist = sp.user_playlist_create(user_id, line_edited)
            song_dict = sp.playlist_items(playlist['id'], fields='items')
            songs = []
            for song in song_dict['items']:
                if song['track']['id'] is not None:
                    songs.extend(song['track']['id']) # TODO: Check if this works instead of the list comprehension!
            # songs = [song['track']['id'] for song in song_dict['items'] if song['track']['id'] is not None]
            sp.playlist_add_items(new_playlist['id'], songs)
        if other_user_playlists['next']:
            other_user_playlists = sp.next(other_user_playlists)
        else:
            other_user_playlists = None

    user_id = sp.me()['id']


if __name__ == "__main__":
    main()
