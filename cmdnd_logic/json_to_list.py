"""
This throwaway script generates a python list out of the json file for the SRD for DND 5e monsters
"""

import json

with open("srd_5e_monsters.json", encoding="utf-8") as srd_list:
    # TODO: Check if srd_5e_monsters.json is really utf-8 on both Windows and Linux
    srd_list = json.load(srd_list)
