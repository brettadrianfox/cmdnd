import os
import re
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth

def format_playname(playname_raw, playlist, pattern_2: str):
    playname = playname_raw.group()
    playname_short = playname.lower()
    playname_short_end = re.search(pattern_2, playlist['name'])
    playname_tuple = (playname_short, playname_short_end)
    return playname_tuple

def reformat_playname(playlist_dict: dict, playlist, playname_tuple: tuple):
    if playname_tuple[1]:
        playname_short_end = playname_tuple[1].group()
        playname_short_end = playname_short_end.lower()
        playname_short = playname_tuple[0] + playname_short_end
    else:
        playname_short = playname_tuple[0]
    dict_element = {"name": playlist['name'], "short name": playname_short, "id": playlist['uri']}
    playlist_dict[playlist['name']] = dict_element
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

def find_playlist(playlist_dict: dict, user_input: str, sp: spotipy.Spotify):
    for playlist in playlist_dict:
        if user_input == playlist_dict[playlist]["short name"]: # TEMP
            print(f'\n"{playlist_dict[playlist]["name"]}" is a playlist!\n') #
            sp.shuffle(True)
            sp.start_playback(context_uri=playlist_dict[playlist]["id"])
            # print(playlist_dict.values()) #TEMP
            break
    else:
        print(f'\n"{user_input}" is not a playlist in the included dictionary!\n') #
        return

def driver(playlist_dict: dict, sp: spotipy.Spotify, playlists, on = bool):
    user_input = input("Input a playlist name (type q to quit): ") #TEMP
    # user_input = "p" #TEMP
    if user_input == "q" or user_input == "quit":
        on = False
        return on
    elif user_input == "p" or user_input == "pause" or user_input == "play": # TODO: IMPLEMENT PAUSE FUNCTIONALITY -> NEED TO CHECK IF SPOTIFY IS PLAYING TO AVOID ERROR
        playback_info = sp.current_playback() #TEMP
        if not playback_info['is_playing']:
            sp.start_playback()
        else:
            sp.pause_playback()
    elif user_input == "n" or user_input == "next":
        playback_info = sp.current_playback()
        if playback_info['is_playing']:
            sp.next_track()
        else:
            print(f'\nPlayback is paused!\n')
    elif user_input == "ls" or user_input == "list":
        pprint.pprint(playlist_dict) # TODO: REFORMAT THE DICT THAT CONTAINS THE PLAYLIST NAMES. MAYBE ADD IT TO THE OLD PLAYLIST DICT THAT SPOTIPY GIVES US?
    else:
        find_playlist(playlist_dict, user_input, sp) # Implement is_paused functionality -- don't play playlist if the status is set to paused
    return on
    

def main():
    token = SpotifyOAuth(client_id=os.environ.get("SPOTIPY_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"), redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"), scope="streaming,user-read-playback-state", username=os.environ.get("SPOTIFY_USERNAME"))
    sp = spotipy.Spotify(auth_manager=token)

    playlists = sp.user_playlists(os.environ.get("SPOTIFY_USERNAME"))
    playlist_dict = init_playlist_dict(sp, playlists)

    on = True
    while on: # TODO: Implement switcher_driver function
        on = driver(playlist_dict, sp, playlists, on)

if __name__ == "__main__":
    main()
    
