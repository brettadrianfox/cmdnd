import os
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

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
    playlist_dict[playname_short] = playlist['uri']
    return playlist_dict

def init_playlist_dict(sp: spotipy.Spotify, playlists: spotipy.Spotify.user_playlists):
    playlist_dict = {}
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            # print(playlist['name']) # TEMP
            pattern_1 = r"(?<=(RPG:\s))[a-zA-Z0-9]{1,5}" # This regex pattern captures 5 alphanumeric characters after a colon and space
            pattern_2 = r"(?<!^)(?<!(:\s))(?<=(\s))[a-zA-Z]{1}" # This regex pattern captures capital letters after a space but not after a colon and space, and not at the beginning of a string
            playname_raw = re.search(pattern_1, playlist['name']) # Capturing the word(s) after the colon
            if playname_raw:
                playname_tuple = format_playname(playname_raw, playlist, pattern_2)
                playlist_dict = reformat_playname(playlist_dict, playlist, playname_tuple) # TODO: INQUIRE INTO "nomadc". IT SHOULD BE "nomad"
                # print(playlist['name']) #
                # print(list(playlist_dict)[-1]) #
                # print("\n") #
            # else: #
                # print("N/A") #
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            # print(playlist_dict.values()) #
            playlists = sp.user_playlists(os.environ.get("SPOTIFY_USERNAME"))
            return playlist_dict
    # Listing all D&D playlists with their URIs
    # Also listing their shortened versions in playlist_dict    


def main():
    token = SpotifyOAuth(client_id=os.environ.get("SPOTIPY_SWITCHER_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_SWITCHER_CLIENT_SECRET"), redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"), scope="streaming,user-read-playback-state", username=os.environ.get("SPOTIFY_USERNAME"))
    sp = spotipy.Spotify(auth_manager=token)

    playlists = sp.user_playlists(os.environ.get("SPOTIFY_USERNAME"))
    playlist_dict = init_playlist_dict(sp, playlists)

    on = True
    while on:
        user_input = input("Input a playlist name (type q to quit): ")
        # user_input = "p" #TEMP
        if user_input == "q" or user_input == "quit":
            on = False
            return
        # elif user_input == "p" or user_input == "pause": # TODO: IMPLEMENT PAUSE FUNCTIONALITY -> NEED TO CHECK IF SPOTIFY IS PLAYING TO AVOID ERROR
            # sp.pause_playback()
        elif user_input == "ls" or user_input == "list":
            pprint(playlist_dict) # TODO: REFORMAT THE DICT THAT CONTAINS THE PLAYLIST NAMES. MAYBE ADD IT TO THE OLD PLAYLIST DICT THAT SPOTIPY GIVES US?
        else:
            while playlists: # TODO: REFORMAT THIS BLOCK
                found_playlist = False # Variable that checks if we have found our variable
                for key, val in playlist_dict.items():
                    if user_input == key: # TEMP
                        print(f'\n"{user_input}" is a playlist!\n') #
                        sp.shuffle(True)
                        sp.start_playback(context_uri=val)
                        # print(playlist_dict.values()) #TEMP
                        found_playlist = True
                        break
                if found_playlist == True:
                    break
                elif playlists['next']:
                    playlists = sp.next(playlists)
                else:
                    print(f'\n"{user_input}" is not a playlist!\n') #
                    break
    



if __name__ == "__main__":
    main()
    
