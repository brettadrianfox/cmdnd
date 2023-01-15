import re
import spotipy
import os
import json
from spotipy.oauth2 import SpotifyOAuth

"""
This Python script creates a .json file with name 'file_name' (defined in the main function) of the format:

{
    "RPG: Town/Village": {
        "name": "RPG: Town/Village", 
        "short name": "town", 
        "id": "spotify:playlist:4QZGUCPcIZebHnmHdtnzs6"
        }, 
    "RPG: Tavern - Upbeat": {
        "name": "RPG: Tavern - Upbeat", 
        "short name": "taveru", 
        "id": "spotify:playlist:552Vvc7fBFHKiBO5hXXSIF"
        },

        ...

}

All playlists added to this .json file have the

The script playlist_switcher.py converts this .json file to a Python dictionary to be used by it.
"""

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

def init_playlist_dict(sp: spotipy.Spotify, playlists: spotipy.Spotify.user_playlists, file_name: str):
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
            playlists = sp.user_playlists(os.environ.get("SPOTIFY_USERNAME")) # TEMP
            with open(file_name, "w") as outfile: # TEMP
                json.dump(playlist_dict, outfile) # TEMP
            return playlist_dict
    # Listing all D&D playlists with their URIs
    # Also listing their shortened versions in playlist_dict

def main():
    token = SpotifyOAuth(client_id=os.environ.get("SPOTIPY_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"), redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"), scope="streaming,user-read-playback-state", username=os.environ.get("SPOTIFY_USERNAME"))
    sp = spotipy.Spotify(auth_manager=token)

    file_name = "rpgdict.json"

    playlists = sp.user_playlists(os.environ.get("SPOTIFY_USERNAME"))
    playlist_dict = init_playlist_dict(sp, playlists, file_name)
    return playlist_dict

if __name__ == "__main__":
    main()