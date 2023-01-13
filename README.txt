The project name, "cmdnd" is a pun. Since its original purpose was a simple Python script to switch between Spotify
playlists in the cmd terminal for Dungeons and Dragons games. Yes, I know that PowerShell is the new Windows terminal,
but the pun was too good (bad) to pass up on.

For the Python code on this project, we use Pylint as our linter to catch and correct problems and errors

Guide to the files:

    playlist_switcher.py allows the user to switch between Spotify playlists in the rpgdict.json file in their terminal
    for a fast and smooth tabletop RPG experience.

    playlist_copier.py is the original script: it copies a collection of another user's Spotify playlists 
    (using the Spotipy library) and uses them as a base to generate playlists for the signed-in user. This 
    is used if you want to copy another user's playlists en masse.

    

    rpgdict.json is a json file of RPG Spotify playlists used in the playlist_switcher.py file