from json_to_list import srd_list
from random import randint
import numpy as np
import numpy.ma as ma
import json
import re
import sys
from fractions import Fraction

"""
This is the model in a model-view-controller framework for the RPG battlemap grid.
"""

class BattleMap:
    """ A representation of a battle map consisting of squares.

    Consists of squares, a list of beings contained by the battle
    map, the combat round, the order of initiative, the current turn, and a
    dictionary that contains all monsters that can be included on the battlemap.

    Attributes:
        _max_x = x_squares (int): The x-distance in 5-foot intervals
        _max_y = y_squares (int): The y-distance in 5-foot intervals
        _being_list (list): A list of the names of all entities on the battlemap.
        _grid (numpy array): A 2-dimensional numpy array whose entries represent
        the tiles of the battle map and their contents.

    
    """

    def __init__(self, x_squares: int, y_squares: int):
        self._max_x = x_squares
        self._max_y = y_squares
        self._being_list = [] # A list of the names of all entities on the battle map. NAMES MUST BE UNIQUE
        self._grid = np.empty((self._max_x, self._max_y), dtype=object) # A list of lists that represents the battle map. Each tile represents 5 square feet.
        self._round = 0
        self._initiative_order = []
        self._current_turn = None # TODO: Try deleting this when you have "update" function enabled
        self._monster_dict = srd_list # TODO: Refactor this into another function?
        # TODO: Add a list of names to be used on the battle map

    def __repr__(self):
        grid_list = []
        for count_y, row in enumerate(self._grid):
            row_list = []
            for count_x, element in enumerate(row):
                if type(element) is tuple: # All entities must be tuples
                    row_list.append(element) # TODO: Append the object/entity's representation
                else:
                    coord_tuple = (count_x + 1, self._max_y - count_y)
                    row_list.append(coord_tuple) # The pound sign represents an empty tile
            row_repr = str(row_list).strip("[]")
            grid_list.append(row_repr)
        grid_repr = "\n".join(grid_list)
        grid_repr += "\n"
        return grid_repr

    def add_being(self, to_add: "Being"):
        self._being_list.append(to_add)
        name_category_tuple = (to_add._name, f"({to_add._category})") # TODO: Remove quotes from name_type_tuple in repr of battle_map
        self._grid[self._max_y - to_add._y_position, to_add._x_position - 1] = name_category_tuple # TODO: Make sure no two beings have the same name
        # The grid is 1-indexed, so we subtract 1 from the positions
        # We subtract to_add._y_position from self._max_y because we are converting Cartesian y-coordinates (0 on bottom) to row-major y-coordinates (0 on top)

    def remove_being(self, to_remove):
        if type(to_remove) is not Being:
            for being in self._being_list: # TODO: Add error handling for being not found in self._being list!
                if being._name == to_remove:
                    being_obj = being
        else:
            being_obj = to_remove
        self._being_list.remove(being_obj)
        self._grid[self._max_y - being_obj._y_position, being_obj._x_position - 1] = None
        # The grid is 1-indexed, so we subtract 1 from the positions
        # We subtract to_add._y_position from self._max_y because we are converting Cartesian y-coordinates (0 on bottom) to row-major y-coordinates (0 on top)

    def move_being(self, to_move: str, direction, magnitude): # TODO: Make moving "through" corners impossible
        magnitude = float(magnitude)
        for being in self._being_list: # TODO: Add error handling for being not found in self._being list!
            if being._name == to_move:
                being_obj = being
        if magnitude < 0:
            print("Magnitude cannot be negative!")
            sys.exit(0)
        else:
            try:
                self.remove_being(being_obj)
                being_obj.move(direction, magnitude)
                self.add_being(being_obj)
            except IndexError:
                print("List wrap-around is invalid for movement!")
                sys.exit(0)
        # TODO: Print a more specific error message here [number of feet/squares you are actually allowed to move]
        # TODO: If there is a list wrap-around, replace it with moving to the edge of the board (collision detection)
        # The grid is 1-indexed, so we subtract 1 from the x-position
        # We subtract to_add._y_position from self._max_y because we are converting Cartesian y-coordinates (0 on bottom) to row-major y-coordinates (0 on top)


class Being:
    """ All unmarked distances are in feet"""

    def __init__(self, category, name, x_pos, y_pos, battle_map: BattleMap): # TODO: Add being "categories" to be loaded into this class, i.e. Adult Red Dragon, Lizardfolk Shaman, etc.
        # TODO: Distinguish between being category (Ancient Red Dragon) and being name (Smaug)
        self._name = name # TODO: Make sure name is less than 256 characters!

        for element in battle_map._monster_dict:
            if category.lower() == element["name"].lower(): # TEMP
                self._category = element["name"].lower() # TODO: Add error handling for inputted category not contained within battle map creature dict
                self._category_dict_element = element
                
        self._x_position = int(x_pos) # 1-indexed, using Cartesian coordinates
        self._y_position = int(y_pos) # 1-indexed, using Cartesian coordinates
        self._speed = int(re.search(r"^[0-9]{1,4}", self._category_dict_element["Speed"]).group()) # Capturing the first 1-4 numbers at the beginning of the str

        swimming_speed = re.search(r"(?<=swim )[0-9]{1,4}", self._category_dict_element["Speed"])
        if swimming_speed is not None:
            self._swimming_speed = swimming_speed.group()

        flying_speed = re.search(r"(?<=fly )[0-9]{1,4}", self._category_dict_element["Speed"])
        if flying_speed is not None:
            self._flying_speed = flying_speed.group()

        burrowing_speed = re.search(r"(?<=burrow )[0-9]{1,4}", self._category_dict_element["Speed"])
        if burrowing_speed is not None:
            self._burrowing_speed = burrowing_speed.group()

        strength = int(self._category_dict_element["STR"])
        dexterity = int(self._category_dict_element["DEX"])
        constitution = int(self._category_dict_element["CON"])
        wisdom = int(self._category_dict_element["WIS"])
        intelligence = int(self._category_dict_element["INT"])
        charisma = int(self._category_dict_element["CHA"])

        self._ability_scores = {
            "STR": strength,
            "DEX": dexterity,
            "CON": constitution,
            "WIS": wisdom,
            "INT": intelligence,
            "CHA": charisma
        }

        strength_modifier = int(re.search(r"[0-9,-]{1,2}", self._category_dict_element["STR_mod"]).group())
        dexterity_modifier = int(re.search(r"[0-9,-]{1,2}", self._category_dict_element["DEX_mod"]).group())
        constitution_modifier = int(re.search(r"[0-9,-]{1,2}", self._category_dict_element["CON_mod"]).group())
        wisdom_modifier = int(re.search(r"[0-9,-]{1,2}", self._category_dict_element["WIS_mod"]).group())
        intelligence_modifier = int(re.search(r"[0-9,-]{1,2}", self._category_dict_element["INT_mod"]).group())
        charisma_modifier = int(re.search(r"[0-9,-]{1,2}", self._category_dict_element["CHA_mod"]).group())

        self._ability_modifiers = {
            "STR": strength_modifier,
            "DEX": dexterity_modifier,
            "CON": constitution_modifier,
            "WIS": wisdom_modifier,
            "INT": intelligence_modifier,
            "CHA": charisma_modifier
        }

        self._hp_max_static = int(re.search(r"^[0-9]{1,4}", self._category_dict_element["Hit Points"]).group()) # TODO: Add a global setting where you can choose between static and dynamic hp maxes

        self._num_hit_dice = int(re.search(r"(?<=\()[0-9]{1,4}", self._category_dict_element["Hit Points"]).group()) # TODO: Make this a self._ variable?

        self._hit_dice_type = "d" + str(re.search(r"(?<=d)[0-9]{1,3}", self._category_dict_element["Hit Points"]).group()) # TODO: Make this a self._ variable?

        hp_modifier = re.search(r"(?<= )[\-,0-9]", self._category_dict_element["Hit Points"]) # TODO: Make this a self._ variable?
        if hp_modifier is not None:
            self._hp_modifier = int(hp_modifier.group())
        else:
            self._hp_modifier = 0

        self._hp_max_dynamic = self._num_hit_dice*randint(1, int(self._hit_dice_type[1])) + self._hp_modifier

        # TODO: Implement current_hp (choice between static and dynamic hp)

        self._armor_class = int(re.search(r"^[0-9]{1,2}", self._category_dict_element["Armor Class"]).group())
        
        self._type = re.search(r"(?<= )[a-zA-Z,(,) ]+(?=,)", self._category_dict_element["meta"]).group() # i.e. humanoid, abberation, etc.

        self._alignment = re.search(r"(?<=, )[a-zA-Z, ]+$", self._category_dict_element["meta"]).group()

        self._size = re.search(r"^[a-zA-Z]+", self._category_dict_element["meta"]).group().lower()

        if "Languages" in self._category_dict_element.keys():
            self._languages = re.findall(r"([A-Z][^\,\n]+)", self._category_dict_element["Languages"])
        else:
            self._languages = None # NoneType represents no element present

        if "Skills" in self._category_dict_element.keys():
            skills_temp = re.findall(r"([A-Z][^\,\n]+)", self._category_dict_element["Skills"])
            skills_dict = {}
            for element in skills_temp:
                skill_name = re.search(r"([A-Z][^\s]+)", element).group()
                skill_modifier = re.search(r"(?<=[\s\+])[0-9\-]+", element).group()
                skills_dict[skill_name] = int(skill_modifier) # Skill name is key, skill modifier is val
            self._skills = skills_dict
        else:
            self._skills = None # NoneType represents no element present

        if "Saving Throws" in self._category_dict_element.keys():
            saving_throws_temp = re.findall(r"([A-Z][^\,\n]+)", self._category_dict_element["Saving Throws"])
            saving_throws_dict = {}
            for element in saving_throws_temp:
                saving_throw_type = re.search(r"([A-Z][^\s]+)", element).group()
                saving_throw_modifier = re.search(r"(?<=[\s\+])[0-9\-]+", element).group()
                saving_throws_dict[saving_throw_type] = int(saving_throw_modifier) # Skill name is key, skill modifier is val
            self._saving_throws = saving_throws_dict
        else:
            self._saving_throws = None # NoneType represents no element present

        if "Damage Resistances" in self._category_dict_element.keys():
            self._damage_resistances = re.findall(r"([A-Z][^\,\;\n]+)", self._category_dict_element["Damage Resistances"])
        else:
            self._damage_resistances = None # NoneType represents no element present

        if "Damage Immunities" in self._category_dict_element.keys():
            self._damage_immunities = re.findall(r"([A-Z][^\,\;\n]+)", self._category_dict_element["Damage Immunities"])
        else:
            self._damage_immunities = None # NoneType represents no element present

        if "Condition Immunities" in self._category_dict_element.keys():
            self._condition_immunities = re.findall(r"([A-Z][^\,\;\n]+)", self._category_dict_element["Condition Immunities"])
        else:
            self._condition_immunities = None # NoneType represents no element present

        if "Senses" in self._category_dict_element.keys():
            senses_temp = re.findall(r"([A-Z][^\,\n]+)", self._category_dict_element["Senses"])
            senses_dict = {}
            for element in senses_temp:
                sense_name = re.search(r".+(?=\s\d)", element).group()
                sense_modifier = re.search(r"(?<=[\s\+])[0-9\-]+", element).group()
                senses_dict[sense_name] = int(sense_modifier) # Skill name is key, skill modifier is val
            self._senses = senses_dict
        else:
            self._senses = None # NoneType represents no element present

        if "Challenge" in self._category_dict_element.keys():
            challenge_rating = re.search((r"^[0-9\/]+"), self._category_dict_element["Challenge"]).group()
            challenge_xp = re.search((r"(?<=\()[0-9\,]+"), self._category_dict_element["Challenge"]).group()
            challenge_xp = challenge_xp.replace(",", "")
            self._challenge_rating = Fraction(challenge_rating)
            self._xp = int(challenge_xp)
        else:
            self._challenge = None # NoneType represents no element present

        # TODO: Determine if key not present in monster json dict means it does not exist in "Being" object, or it exists, but equals None






        # self._hp_max_variable = # TEMP

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def right_movement(self, magnitude):
        self._x_position += int(magnitude/5)

    def up_right_movement(self, magnitude):
        self._x_position += int((0.7071*magnitude)/5) # Decomposing a unit vector in 2-D into its orthogonal components
        self._y_position += int((0.7071*magnitude)/5)

    def up_movement(self, magnitude):
        self._y_position += int(magnitude/5)

    def up_left_movement(self, magnitude):
        self._x_position -= int((0.7071*magnitude)/5)
        self._y_position += int((0.7071*magnitude)/5)

    def left_movement(self, magnitude):
        self._x_position -= int(magnitude/5)

    def down_left_movement(self, magnitude):
        self._x_position -= int((0.7071*magnitude)/5)
        self._y_position -= int((0.7071*magnitude)/5)

    def down_movement(self, magnitude):
        self._y_position -= int(magnitude/5)

    def down_right_movement(self, magnitude):
        self._x_position += int((0.7071*magnitude)/5)
        self._y_position -= int((0.7071*magnitude)/5)

    _base_direction_dict = { # TODO: Refactor direction into a class of its own
        "r": right_movement,
        "ur": up_right_movement,
        "u": up_movement,
        "ul": up_left_movement,
        "l": left_movement,
        "dl": down_left_movement,
        "d": down_movement,
        "dr": down_right_movement
    }

    def move(self, direction, magnitude): # Magnitude is in feet
        try:
            if magnitude > self._speed: # TODO: Add functionality for swimming, climbing, burrowing, etc.
                self._base_direction_dict[direction](self, self._speed)
            else:
                self._base_direction_dict[direction](self, magnitude) # TODO: Add try-except for error handling here # TEMP
        except KeyError:
            print("Input not a valid direction!")
            sys.exit(0)

def driver(on: bool = True): # TODO: Add index/guide for commands
    print('Input size of battle map (press "q" to quit):')
    x_input = input("Input desired size of x-axis (in feet): ")
    if x_input == "q" or x_input == "quit":
        on = False
        return
    y_input = input("Input desired size of y-axis (in feet): ")
    if y_input == "q" or x_input == "quit":
        on = False
        return
    my_battlemap = BattleMap(int(x_input) // 5, int(y_input) // 5) # Everything is rounded to 5-foot "squares"

    command_dict = {
        "add being": my_battlemap.add_being,
        "remove being": my_battlemap.remove_being,
        "move being": my_battlemap.move_being
    }

    while on:
        user_input =  input('Input a battlemap command (type "h" to get help): ') #TEMP
        # user_input = "p" #TEMP
        user_input = user_input.lower()

        if user_input == "q" or user_input == "quit":
            on = False
            return

        elif user_input == "h" or user_input == "help":
            print('To add a being to the map: type "add being, [being type], [being name], [x-tile], [y-tile]"')
            print('To move a being around the map: type "move being, [being name], [direction], [distance in feet]')
            print('To remove a being from the map: type "remove being, [being name]')
            print('Being names must be unique')

        else:
            input_split = user_input.split(", ")
            # TODO: Refactor this parser into a new function

            command = input_split[0]

            if command == "add being":
                new_being = Being(*input_split[1:], my_battlemap)
                command_input = new_being
                command_dict[command](command_input)
            else:
                command_input = input_split[1:]
                command_dict[command](*command_input)

            print("\n") # TEMP
            print(repr(my_battlemap)) # TEMP

        # TODO: Add a "h / help command that displays formatting about the command line prompt"

        print("\n")

def main():
    driver()

if __name__ == "__main__":
    main()

"""
SCAFFOLDING:

BattleMap:
    * __max_x v/
    * __max_y v/
    * __being_list v/
    * __round
    * __initiative_order
    * __current_turn # Who's turn is it?
    * draw
    * update # Change turns/rounds
    * add_being v/
    * remove_being v/
    * add_object
    * remove_object
    * empty_location
    * look_at_location

    Environment: (A thing that remains constant on the battle map)

        Tile: (Something that can be moved over)

        Object: (Something that impedes progress)

    Being: (A thing that moves on the battle map that can be killed)
        * __x_position v/
        * __y_position v/
        * __size_of v/
        * __ambient_effect # THE EFFECT AN ENTITY HAS SIMPLY BY EXISTING ON THE BATTLE MAP
        * __current_hp
        * __hp_max v/
        * __temporary_hp
        * __armor_class v/
        * __languages v/
        * __skills v/
        * __attributes v/
        * __saving throws v/
        * __damage_resistances v/
        * __damage_immunities v/
        *   condition_immunities v/
        * __senses v/
        * __challenge_rating v/
        * __experience points v/
        * __spells_known
        * __effects
        * __traits
        * __actions
        * __speed v/
        * move
        * 

        Player Character:
            * __name
            * __race
            * __alignment
            * __background
            * __level
            * __experience_points
            * __class
            * __proficiencies
            * __hit_dice
            * __class_features
            * __spell_slots
            * __carrying_capacity
            * __death_saves
            * __initiative
            * __character_information
            *attack
            *cast_spell
            *dash
            *disengage
            *dodge
            *escape
            *guard
            *harry
            *help
            *hide
            *sunder
            *ready
            *search
            *use_object

        NPC:
            * __special_traits
            * __innate_spellcasting
            * __actions
            * __legendary_actions
            * run_ai_turn

        Natural Phenomenon:
"""