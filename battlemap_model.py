from json_to_list import srd_list
from random import randint
import numpy as np
import numpy.ma as ma
import json
import re
import sys

"""
This is the model in a model-view-controller framework for the RPG battlemap grid.
"""

class BattleMap:

    def __init__(self, x_squares: int, y_squares: int):
        self._max_x = x_squares
        self._max_y = y_squares
        self._being_list = [] # A list of the names of all entities on the battle map. NAMES MUST BE UNIQUE
        self._grid = np.empty((self._max_x, self._max_y), dtype=object) # A list of lists that represents the battle map. Each tile represents 5 square feet.
        self._round = 0
        self._initiative_order = []
        self._current_turn = None # TODO: Try deleting this when you have "update" function enabled
        self._creature_dict = srd_list # TODO: Refactor this into another function?
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

    def remove_being(self, to_remove: "Being"):
        self._being_list.remove(to_remove)
        self._grid[self._max_y - to_remove._y_position, to_remove._x_position - 1] = None
        # The grid is 1-indexed, so we subtract 1 from the positions
        # We subtract to_add._y_position from self._max_y because we are converting Cartesian y-coordinates (0 on bottom) to row-major y-coordinates (0 on top)

    def move_being(self, to_move: "Being", direction, magnitude): # TODO: Make moving "through" corners impossible
        if magnitude < 0:
            print("Magnitude cannot be negative!")
            sys.exit(0)
        else:
            try:
                self.remove_being(to_move)
                to_move.move(direction, magnitude)
                self.add_being(to_move)
            except IndexError:
                print("List wrap-around is invalid for movement!")
                sys.exit(0)
        # TODO: Print a more specific error message here [number of feet/squares you are actually allowed to move]
        # TODO: If there is a list wrap-around, replace it with moving to the edge of the board (collision detection)
        # The grid is 1-indexed, so we subtract 1 from the x-position
        # We subtract to_add._y_position from self._max_y because we are converting Cartesian y-coordinates (0 on bottom) to row-major y-coordinates (0 on top)


class Being:

    def __init__(self, name, category, x_position, y_position, battle_map: BattleMap): # TODO: Add being "categories" to be loaded into this class, i.e. Adult Red Dragon, Lizardfolk Shaman, etc.
        # TODO: Distinguish between being category (Ancient Red Dragon) and being name (Smaug)
        self._name = name # TODO: Make sure name is less than 256 characters!

        for element in battle_map._creature_dict:
            if category.lower() == element["name"].lower(): # TEMP
                self._category = element["name"].lower() # TODO: Add error handling for inputted category not contained within battle map creature dict
                self._category_dict_element = element
                
        self._x_position = x_position # 1-indexed, using Cartesian coordinates
        self._y_position = y_position # 1-indexed, using Cartesian coordinates
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


def main():

    test_map = BattleMap(10, 10)

    test_being = Being("test_being", "commoner", 2, 2, test_map)

    test_map.add_being(test_being)

    print(repr(test_map))

    test_map.move_being(test_being, "u", 40) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "r", 40) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "d", 45) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "l", 45) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "u", 45) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "r", 45) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "d", 45) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "ul", 70) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "d", 45) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "ur", 70) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "dl", 36) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "dl", 35) # TEMP

    print(repr(test_map))

    test_map.move_being(test_being, "ur", 8) # TEMP

    print(repr(test_map))

    # TODO: Test diagonal movement!
 
    print(repr(test_map))

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
    * add_being
    * remove_being
    * add_env
    * remove_env
    * empty_location
    * look_at_location

    Environment: (A thing that remains constant on the battle map)

        Tile: (Something that can be moved over)

        Object: (Something that impedes progress)

    Being: (A thing that moves on the battle map that can be killed)
        * __x_position v/
        * __y_position v/
        * __size_of
        * __ambient_effect # THE EFFECT AN ENTITY HAS SIMPLY BY EXISTING ON THE BATTLE MAP
        * __current_hp
        * __hp_max v/
        * __temporary_hp
        * __armor_class v/
        * __languages
        * __skills
        * __attributes v/
        * __saving throws
        * __damage_resistances
        * __damage_immunities
        * __senses
        * __challenge_rating
        * __experience points
        * __spells_known
        * __effects
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