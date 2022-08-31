"""
This is the model in a model-view-controller framework for the RPG battlemap grid.
"""

class BattleMap:

    def __init__(self, x_squares: int, y_squares: int):
        self._max_x = x_squares
        self._max_y = y_squares
        self._being_list = [] # A list of all entities on the battle map
        self._grid = [] # A list of lists that represents the battle map. Each tile represents 5 square feet.
        self._round = 0
        self._initiative_order = []
        self._current_turn = None # TODO: Try deleting this when you have "update" function enabled


        for i in range(self._max_y):
            row = []
            for i in range(self._max_x):
                row.append(None)
            self._grid.append(row)

    def __repr__(self):
        grid_list = []
        for count_y, row in enumerate(self._grid):
            row_list = []
            for count_x, element in enumerate(row):
                if element == None:
                    coord_tuple = (count_x + 1, self._max_y - count_y)
                    row_list.append(coord_tuple) # The pound sign represents an empty tile
                else:
                    row_list.append(element[:4]) # TODO: Append the object/entity's representation
            row_repr = str(row_list).strip("[]")
            grid_list.append(row_repr)
        grid_repr = "\n".join(grid_list)
        grid_repr += "\n"
        return grid_repr

    def add_being(self, to_add: "Being"):
        self._being_list.append(to_add)
        self._grid[self._max_y - to_add._y_position][to_add._x_position - 1] = to_add._name # TODO: Make sure no two beings have the same name
        # The grid is 1-indexed, so we subtract 1 from the positions
        # We subtract to_add._y_position from self._max_y because we are converting Cartesian y-coordinates (0 on bottom) to row-major y-coordinates (0 on top)

    def remove_being(self, to_remove: "Being"):
        self._being_list.remove(to_remove)
        self._grid[self._max_y - to_remove._y_position][to_remove._x_position - 1] = None
        # The grid is 1-indexed, so we subtract 1 from the positions
        # We subtract to_add._y_position from self._max_y because we are converting Cartesian y-coordinates (0 on bottom) to row-major y-coordinates (0 on top)

    def move_being(self, to_move: "Being", direction, magnitude):
        self.remove_being(to_move)
        to_move.move(direction, magnitude, self, direction_dict=to_move.base_direction_dict)
        self._grid[self._max_y - to_move._y_position][to_move._x_position - 1] = to_move._name
        # The grid is 1-indexed, so we subtract 1 from the x-position
        # We subtract to_add._y_position from self._max_y because we are converting Cartesian y-coordinates (0 on bottom) to row-major y-coordinates (0 on top)


class Being:

    def __init__(self, name, x_position, y_position, speed, swimming_speed = None, flying_speed = None):
        self._name = name
        self._x_position = x_position # 1-indexed, using Cartesian coordinates
        self._y_position = y_position # 1-indexed, using Cartesian coordinates
        self._speed = speed
        self._swimming_speed = swimming_speed
        self._flying_speed = flying_speed

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def right_movement(self, magnitude, battle_map: BattleMap):
        if self._x_position + int(magnitude/5) < self._x_position: # Checking for list wrap arounds (collision detection)
            self._x_position = battle_map._max_x
        else:
            self._x_position += int(magnitude/5)

    def up_right_movement(self, magnitude, battle_map: BattleMap):
        no_x_collision = self._x_position + int(magnitude/5) >= self._x_position
        no_y_collision = self._y_position + int(magnitude/5) >= self._y_position
        collision_list = [no_x_collision, no_y_collision]

        if all(collision_list): # Checking for no collisions in either direction
            self._x_position += int((0.7071*magnitude)/5)
            self._y_position += int((0.7071*magnitude)/5)
        elif not no_x_collision and no_y_collision: # Checking if there is an x-collision but no y-collison
            self._x_position = battle_map._max_x
            self._y_position += int((0.7071*magnitude)/5)
        elif not no_y_collision and no_x_collision: # Checking if there is a y-collision but no x-collision
            self._y_position = battle_map._max_y
            self._x_position += int((0.7071*magnitude)/5)
        else: # Only true if there are collisions in both directions
            self._x_position = battle_map._max_x
            self._y_position = battle_map._max_y

    def up_movement(self, magnitude, battle_map: BattleMap):
        if self._y_position + int(magnitude/5) < self._y_position: # Checking for list wrap arounds (collision detection)
            self._y_position = battle_map._max_y
        else:
            self._y_position += int(magnitude/5)

    def up_left_movement(self, magnitude, battle_map: BattleMap):
        no_x_collision = self._x_position - int(magnitude/5) <= self._x_position
        no_y_collision = self._y_position + int(magnitude/5) >= self._y_position
        collision_list = [no_x_collision, no_y_collision]

        if all(collision_list): # Checking for no collisions in either direction
            self._x_position -= int((0.7071*magnitude)/5)
            self._y_position += int((0.7071*magnitude)/5)
        elif not no_x_collision and no_y_collision: # Checking if there is an x-collision but no y-collison
            self._x_position = 1 # Minimum value of x-position for all beings
            self._y_position += int((0.7071*magnitude)/5)
        elif not no_y_collision and no_x_collision: # Checking if there is a y-collision but no x-collision
            self._y_position = battle_map._max_y # Minimum value of y-position for all beings
            self._x_position -= int((0.7071*magnitude)/5)
        else: # Only true if there are collisions in both directions
            self._x_position = 1 # Minimum value of x-position for all beings
            self._y_position = battle_map._max_y

    def left_movement(self, magnitude, battle_map: BattleMap):
        if self._x_position - int(magnitude/5) > self._x_position: # Checking for list wrap arounds (collision detection)
            self._x_position = 1 # Minimum value of x-position for all beings
        else:
            self._x_position -= int(magnitude/5)

    def down_left_movement(self, magnitude, battle_map: BattleMap):
        no_x_collision = self._x_position - int(magnitude/5) <= self._x_position
        no_y_collision = self._y_position + int(magnitude/5) >= self._y_position
        collision_list = [no_x_collision, no_y_collision]

        if all(collision_list): # Checking for no collisions in either direction
            self._x_position -= int((0.7071*magnitude)/5)
            self._y_position -= int((0.7071*magnitude)/5)
        elif not no_x_collision and no_y_collision: # Checking if there is an x-collision but no y-collison
            self._x_position = 1 # Minimum value of x-position for all beings
            self._y_position -= int((0.7071*magnitude)/5)
        elif not no_y_collision and no_x_collision: # Checking if there is a y-collision but no x-collision
            self._y_position = 1 # Minimum value of y-position for all beings
            self._x_position -= int((0.7071*magnitude)/5)
        else: # Only true if there are collisions in both directions
            self._x_position = 1 # Minimum value of x-position for all beings
            self._y_position = 1 # Minimum value of y-position for all beings

    def down_movement(self, magnitude, battle_map: BattleMap):
        if self._y_position - int(magnitude/5) < self._y_position: # Checking for list wrap arounds (collision detection)
            self._y_position = 1 # Minimum value of x-position for all beings
        else:
            self._y_position -= int(magnitude/5)

    def down_right_movement(self, magnitude, battle_map: BattleMap):
        no_x_collision = self._x_position + int(magnitude/5) >= self._x_position
        no_y_collision = self._y_position - int(magnitude/5) <= self._y_position
        collision_list = [no_x_collision, no_y_collision]

        if all(collision_list): # Checking for no collisions in either direction
            self._x_position += int((0.7071*magnitude)/5)
            self._y_position -= int((0.7071*magnitude)/5)
        elif not no_x_collision and no_y_collision: # Checking if there is an x-collision but no y-collison
            self._x_position = battle_map._max_x
            self._y_position -= int((0.7071*magnitude)/5)
        elif not no_y_collision and no_x_collision: # Checking if there is a y-collision but no x-collision
            self._y_position = 1 # Minimum value of y-position for all beings
            self._x_position += int((0.7071*magnitude)/5)
        else: # Only true if there are collisions in both directions
            self._x_position = battle_map._max_x 
            self._y_position = 1 # Minimum value of y-position for all beings

    base_direction_dict = { # TODO: Refactor direction into a class of its own
        "r": right_movement,
        "ur": up_right_movement,
        "u": up_movement,
        "ul": up_left_movement,
        "l": left_movement,
        "dl": down_left_movement,
        "d": down_movement,
        "dr": down_right_movement
    }

    def move(self, direction, magnitude, battle_map: BattleMap, direction_dict=base_direction_dict): # Magnitude is in feet
        try:
            direction_dict[direction](self, magnitude, battle_map) # TODO: Add try-except for error handling here # TEMP
        except KeyError:
            print("Input not a valid direction")


def main(): #
    test_map = BattleMap(10, 10)

    test_being = Being("test_being", 2, 2, 30)

    test_map.add_being(test_being)

    print(repr(test_map))

    test_map.move_being(test_being, "u", 0) # TEMP
 
    print(repr(test_map))

if __name__ == "__main__":
    main()

"""
SCAFFOLDING:

BattleMap:
    * __max_x
    * __max_y
    * __being_list
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
        * __x_position
        * __y_position
        * __sizeof
        * __ambient_effect # THE EFFECT AN ENTITY HAS SIMPLY BY EXISTING ON THE BATTLE MAP
        * __current_hp
        * __hp_max
        * __temporary_hp
        * __armor_class
        * __languages
        * __skills
        * __attributes
        * __saving throws
        * __damage_resistances
        * __damage_immunities
        * __senses
        * __challenge_rating
        * __experience points
        * __spells_known
        * __effects
        * __speed
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