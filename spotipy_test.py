import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

def main():
    auth_manager = SpotifyClientCredentials(client_id=os.environ.get("SPOTIPY_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"))
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlists = sp.user_playlists('sirpopey')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(playlist['name'], playlist['uri']) # TEMP
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = sp.user_playlists('sirpopey')
            break

    # Listing all D&D playlists with their URIs

    #user_input = input("Input a command: ")
    user_input = "Atmosphere: Creepy Fast" #TEMP

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if user_input == playlist['name']: # TEMP
                print(f'"{user_input}" is a playlist! Nice!') #
                return
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                print(f'"{user_input}" is not a playlist!') #
                playlists = None




if __name__ == "__main__":
    main()
    print("git works on my main system!")