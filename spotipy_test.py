import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def format_playname(playname_raw, playlist, pattern_2):
    playname_short = playname_raw.group()
    playname_short = playname_short.lower()
    playname_short_end = re.search(pattern_2, playlist['name'])
    playname_tuple = (playname_short, playname_short_end)
    return playname_tuple

def reformat_playname(playlist_dict, playlist, playname_tuple):
    if playname_tuple[1]:
        playname_short_end = playname_tuple[1].group()
        playname_short_end = playname_short_end.lower()
        playname_short = playname_tuple[0] + playname_short_end
    else:
        playname_short = playname_tuple[0]
    playlist_dict[playlist['uri']] = playname_short
    return playlist_dict

def main():
    auth_manager = SpotifyClientCredentials(client_id=os.environ.get("SPOTIPY_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"))
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlists = sp.user_playlists(os.environ.get("SPOTIFY_USERNAME"))
    playlist_dict = {}
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            # print(playlist['name']) # TEMP
            pattern_1 = r"(?<=(RPG:\s))[a-zA-Z0-9]{1,5}" # This regex pattern captures 5 alphanumeric characters after a colon and space
            pattern_2 = r"(?<!^)(?<!(:\s))(?<=(\s))[a-zA-Z]{1}" # This regex pattern captures capital letters after a space but not after a colon and space, and not at the beginning of a string
            playname_raw = re.search(pattern_1, playlist['name']) # Capturing the word(s) after the colon
            if playname_raw:
                playname_tuple = format_playname(playname_raw, playlist, pattern_2)
                playlist_dict = reformat_playname(playlist_dict, playlist, playname_tuple)
                print(playlist['name']) #
                print(list(playlist_dict)[-1]) #
                # print("\n") #
            # else: #
                # print("N/A") #
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            print(playlist_dict.values()) #
            playlists = sp.user_playlists(os.environ.get("SPOTIFY_USERNAME"))
            break
    # Listing all D&D playlists with their URIs
    # Also listing their shortened versions in playlist_dict

    on = True
    while on:
        user_input = input("Input a playlist name (type q to quit): ")
        #user_input = "Location: Town/Village" #TEMP
        if user_input == "q":
            on = False
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
    