The project name, "cmdnd" is a pun. Since its original purpose was a simple Python script to switch between Spotify
playlists in the cmd terminal for Dungeons and Dragons games. Yes, I know that PowerShell is the new Windows terminal,
but the pun was too good (bad) to pass up on.

For the Python code on this project, we use Pylint as our linter to catch and correct problems and errors

Guide to the files:

    Spotify playlist switcher files:
    These files exist to switch between custom Spotify playlists in the terminal. Will eventually be integrated into the Cmdnd GUI.

        playlist_switcher.py allows the user to switch between Spotify playlists in the rpgdict.json file in their terminal
        for a fast and smooth tabletop RPG experience.

        playlist_copier.py is the original script: it copies a collection of another user's Spotify playlists 
        (using the Spotipy library) and uses them as a base to generate playlists for the signed-in user. This 
        is used if you want to copy another user's playlists in bulk

        playlist_dict_creator.py transforms a json file of Spotify playlists into a Python dictionary used by playlist_switcher.py

        rpgdict.json is a json file of RPG Spotify playlists used in the playlist_switcher.py file

    Battlemap files:
    These files exist to run the battlemap portion of the Cmdnd program. Here, we follow a model-view-controller framework.

        battlemap_model.py contains the backend logic for the battlemap. It generates a top-down battle map composed of squares, where each square
        represents a 5 foot by 5 foot plot of land. You can place Beings (mobile entities, such as monsters, NPCs, and player characters), Objects (immobile
        entities, such as trees, furniture, and walls), and Terrain (grass, floor, shrubs) on the map via the terminal

        battlemap_view does not exist yet, but will display the battlemap

        battlemap_controller does not exist yet, but will "interface" between battlemap_model and battlemap_view

        srd_5e_monsters.json consists of all the D&D 5e monsters from the System Reference Document (SRD) (released under the OGL),
        converted into a .json format. The battlemap_model parses this information and uses it in the battlemap. SRD converted to .json
        by tkfu on GitHub (https://gist.github.com/tkfu/9819e4ac6d529e225e9fc58b358c3479#file-srd_5e_monsters-json)

    Cmdnd files:
    These are the main files that integrate the various processes and produce the overall Cmdnd system

        [None yet]

    We plan on including in the overall Cmdnd screen a battlemap, a terminal where you can input commands to manipulate the map, 
    The Spotify playlist integration may not be part of the final program, depending on how hard it is to integrate into the web app.
    
    Similarly, we plan on setting this up as a web app, but we might do a standard program if a web app is too hard