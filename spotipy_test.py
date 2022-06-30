import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def main():
    auth_manager = SpotifyClientCredentials(client_id=os.environ.get("SPOTIPY_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"))
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlists = sp.user_playlists('sirpopey')
    playlist_dict = {}
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(playlist['name']) # TEMP
            print(playlist['uri'])
            pattern_1 = r"(?<=(:\s))[a-zA-Z0-9]{1,5}" # This regex pattern captures 5 alphanumeric characters after a colon and space
            pattern_2 = r"(?<!^)(?<!(:\s))(?<=(\s))[a-zA-Z]{1}" # This regex pattern captures capital letters after a space but not after a colon and space, and not at the beginning of a string
            playname_raw = re.search(pattern_1, playlist['name']) # Capturing the word(s) after the colon
            if playname_raw:
                playname_short = playname_raw.group()
                playname_short = playname_short.lower()
                playname_short_end = re.search(pattern_2, playlist['name'])
                if playname_short_end:
                    playname_short_end = playname_short_end.group()
                    playname_short_end = playname_short_end.lower()
                    playname_short = playname_short + playname_short_end
                    playlist_dict[playlist['uri']] = playname_short
                else:
                    playlist_dict[playlist['uri']] = playname_short
                print(playname_short) #
            else: #
                print("N/A") #
            print("\n") #
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = sp.user_playlists('sirpopey')
            break
    # Listing all D&D playlists with their URIs
    # Also listing their shortened versions in playlist_dict

    #user_input = input("Input a playlist name: ")
    user_input = "Location: Town/Village" #TEMP

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if user_input == playlist['name']: # TEMP
                print(f'"{user_input}" is a playlist! Nice!') #
                print(playlist_dict.values()) #TEMP
                return
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            print(f'"{user_input}" is not a playlist!') #
            playlists = None
    



if __name__ == "__main__":
    main()
    