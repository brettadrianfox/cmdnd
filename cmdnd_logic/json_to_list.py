"""
This throwaway script generates a python list out of the json file for the SRD for DND 5e monsters
"""

import json

with open("srd_5e_monsters.json") as srd_list:
    srd_list = json.load(srd_list)
