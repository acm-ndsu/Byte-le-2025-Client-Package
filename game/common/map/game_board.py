import ast
import random

from game.commander_clash.character.character import *
from game.common.enums import *
from game.common.game_object import GameObject
from game.common.map.game_object_container import GameObjectContainer
from game.common.map.occupiable import Occupiable
from game.common.map.tile import Tile
from game.common.map.wall import Wall
from game.common.team_manager import TeamManager
from game.utils.vector import Vector


class GameBoard(GameObject):
    """
    `GameBoard Class Notes:`

    Map Size:
    ---------
        map_size is a Vector object, allowing you to specify the size of the (x, y) plane of the game board.
        For example, a Vector object with an 'x' of 5 and a 'y' of 7 will create a board 5 tiles wide and
        7 tiles long.

        Example:
        ::
            _ _ _ _ _  y = 0
            |       |
            |       |
            |       |
            |       |
            |       |
            |       |
            _ _ _ _ _  y = 6

    -----

    Locations:
    ----------
        This is the bulkiest part of the generation.

        The locations field is a dictionary with a key of a tuple of Vectors, and the value being a list of
        GameObjects (the key **must** be a tuple instead of a list because Python requires dictionary keys to be
        immutable).

        This is used to assign the given GameObjects the given coordinates via the Vectors. This is done in two ways:

        Statically:
            If you want a GameObject to be at a specific coordinate, ensure that the key-value pair is
            *ONE* Vector and *ONE* GameObject.
            An example of this would be the following:
            ::
                locations = { (vector_2_4) : [station_0] }

            In this example, vector_2_4 contains the coordinates (2, 4). (Note that this naming convention
            isn't necessary, but was used to help with the concept). Furthermore, station_0 is the
            GameObject that will be at coordinates (2, 4).

        Dynamically:
            If you want to assign multiple GameObjects to different coordinates, use a key-value
            pair of any length.

            **NOTE**: The length of the tuple and list *MUST* be equal, otherwise it will not
            work. In this case, the assignments will be random. An example of this would be the following:
            ::
                locations =
                {
                    (vector_0_0, vector_1_1, vector_2_2) : [station_0, station_1, station_2]
                }

            (Note that the tuple and list both have a length of 3).

            When this is passed in, the three different vectors containing coordinates (0, 0), (1, 1), or
            (2, 2) will be randomly assigned station_0, station_1, or station_2.

            If station_0 is randomly assigned at (1, 1), station_1 could be at (2, 2), then station_2 will be at (0, 0).
            This is just one case of what could happen.

        Lastly, another example will be shown to explain that you can combine both static and
        dynamic assignments in the same dictionary:
        ::
            locations =
                {
                    (vector_0_0) : [station_0],
                    (vector_0_1) : [station_1],
                    (vector_1_1, vector_1_2, vector_1_3) : [station_2, station_3, station_4]
                }

        In this example, station_0 will be at vector_0_0 without interference. The same applies to
        station_1 and vector_0_1. However, for vector_1_1, vector_1_2, and vector_1_3, they will randomly
        be assigned station_2, station_3, and station_4.

    -----

    Walled:
    -------
        This is simply a bool value that will create a wall barrier on the boundary of the game_board. If
        walled is True, the wall will be created for you.

        For example, let the dimensions of the map be (5, 7). There will be wall Objects horizontally across
        x = 0 and x = 4. There will also be wall Objects vertically at y = 0 and y = 6

        Below is a visual example of this, with 'x' being where the wall Objects are.

        Example:
        ::
            x x x x x   y = 0
            x       x
            x       x
            x       x
            x       x
            x       x
            x x x x x   y = 6
    """

    def __init__(self, seed: int | None = None, map_size: Vector = Vector(),
                 locations: dict[Vector, list[GameObject]] | None = None, walled: bool = False,
                 uroda_team_manager: TeamManager | None = None, turpis_team_manager: TeamManager | None = None):

        super().__init__()
        # game_map is initially going to be None. Since generation is slow, call generate_map() as needed
        self.game_map: dict[Vector, GameObjectContainer] | None = None
        self.seed: int | None = seed
        random.seed(seed)
        self.object_type: ObjectType = ObjectType.GAMEBOARD
        self.event_active: int | None = None
        self.map_size: Vector = map_size
        # when passing Vectors as a tuple, end the tuple of Vectors with a comma, so it is recognized as a tuple
        self.locations: dict | None = locations
        self.walled: bool = walled

        self.ordered_teams: list[tuple[Character | None, Character | None]] = []

        # call order teams to order them immediately when the gameboard is created
        self.order_teams(uroda_team_manager, turpis_team_manager)

        self.recently_died: list[Character] = []

        self.turn_info: str = ''

        self.active_pair_index: int = 0

    @property
    def seed(self) -> int:
        return self.__seed

    @seed.setter
    def seed(self, seed: int | None) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if seed is not None and not isinstance(seed, int):
            raise ValueError(
                f'{self.__class__.__name__}.seed must be an int. '
                f'It is a(n) {seed.__class__.__name__} with the value of {seed}.')
        self.__seed = seed

    @property
    def game_map(self) -> dict[Vector, GameObjectContainer] | None:
        return self.__game_map

    @game_map.setter
    def game_map(self, game_map: dict[Vector, GameObjectContainer] | None) -> None:
        if game_map is not None and not isinstance(game_map, dict) \
                and any([not isinstance(vec, Vector) or not isinstance(go_container, GameObjectContainer)
                         for vec, go_container in game_map.items()]):
            raise ValueError(
                f'{self.__class__.__name__}.game_map must be a dict[Vector, GameObjectContainer].'
                f'It has a value of {game_map}.'
            )

        self.__game_map = game_map

    @property
    def map_size(self) -> Vector:
        return self.__map_size

    @map_size.setter
    def map_size(self, map_size: Vector) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if map_size is None or not isinstance(map_size, Vector):
            raise ValueError(
                f'{self.__class__.__name__}.map_size must be a Vector. '
                f'It is a(n) {map_size.__class__.__name__} with the value of {map_size}.')
        self.__map_size = map_size

    @property
    def locations(self) -> dict:
        return self.__locations

    @locations.setter
    def locations(self, locations: dict[Vector, list[GameObject]] | None) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if locations is not None and not isinstance(locations, dict):
            raise ValueError(
                f'Locations must be a dict. The key must be a tuple of Vector Objects, '
                f'and the value a list of GameObject. '
                f'It is a(n) {locations.__class__.__name__} with the value of {locations}.')

        self.__locations = locations

    @property
    def walled(self) -> bool:
        return self.__walled

    @walled.setter
    def walled(self, walled: bool) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if walled is None or not isinstance(walled, bool):
            raise ValueError(
                f'{self.__class__.__name__}.walled must be a bool. '
                f'It is a(n) {walled.__class__.__name__} with the value of {walled}.')

        self.__walled = walled

    def get_ordered_teams_as_list(self) -> list[Character]:
        """
        Returns a list that will have the exact order every character will take their turn in. Returns a list
        to easily loop through.
        """
        result: list[Character] = []

        # separate every tuple into it's individual characters
        for pair in self.ordered_teams:
            result.append(pair[0]) if pair[0] is not None else None
            result.append(pair[1]) if pair[1] is not None else None

        result = sorted(result, key=lambda character: character.speed, reverse=True)

        # return a final list that only contains the current, alive characters
        return [character for character in result if character is not None]

    def generate_map(self) -> None:
        # Dictionary Init
        self.game_map = self.__map_init()

    def __map_init(self) -> dict[Vector, GameObjectContainer]:
        output: dict[Vector, GameObjectContainer] = dict()

        # Update all Character positions if they are to be placed on the map
        for vec, objs in self.locations.items():
            for obj in objs:
                if isinstance(obj, Character):
                    obj.position = vec

        if self.walled:
            # Generate the walls
            output.update({Vector(x=x, y=0): GameObjectContainer([Wall(), ]) for x in range(self.map_size.x)})
            output.update({Vector(x=x, y=self.map_size.y - 1): GameObjectContainer([Wall(), ])
                           for x in range(self.map_size.x)})
            output.update({Vector(x=0, y=y): GameObjectContainer([Wall(), ]) for y in range(1, self.map_size.y - 1)})
            output.update({Vector(x=self.map_size.x - 1, y=y): GameObjectContainer([Wall(), ])
                           for y in range(1, self.map_size.y - 1)})

        # convert locations dict to go_container
        output.update({vec: GameObjectContainer(objs) for vec, objs in self.locations.items()})

        return output

    def get(self, coords: Vector) -> GameObjectContainer | None:
        """
        A GameObjectContainer object returned given the coordinates. If the coordinates are valid but are not in the
        game_map yet, a new GameObjectContainer is created and is stored in a new entry in the game_map dictionary.

        :param coords:
        :return: GameObjectContainer or None
        """
        if self.is_valid_coords(coords) and self.game_map.get(coords, None) is None:
            self.game_map[coords] = GameObjectContainer()

        return self.game_map.get(coords)

    def place(self, coords: Vector, game_obj: GameObject | None) -> bool:
        """
        Places the given object at the given coordinates if they are valid. A boolean is returned to represent a
        successful placement
        :param coords:
        :param game_obj:
        :return: True or False for a successful placement of the given object
        """
        return self.get(coords).place(game_obj) if self.is_valid_coords(coords) else False

    def get_objects_from(self, coords: Vector, object_type: ObjectType | None = None) -> list[GameObject]:
        """
        Returns a list of GameObjects from the given, valid coordinates. If an ObjectType is specified, only that
        ObjectType will be returned. If an ObjectType is not specified, the entire list of GameObjects will be
        returned. If nothing is found, an empty list is given.
        :param coords:
        :param object_type:
        :return: a list of GameObjects
        """
        return self.game_map[coords].get_objects(object_type) if coords in self.game_map else []

    def remove(self, coords: Vector, object_type: ObjectType) -> GameObject | None:
        """
        Removes the first instance of the given object type from the coordinates if they are valid. Returns None if
        invalid coordinates are given.
        :param coords:
        :param object_type:
        :return: GameObject or None
        """
        to_return: GameObject | None = self.game_map[coords].remove(object_type) if coords in self.game_map else None

        # if there is a None value paired with the coordinate key after removal, delete that entry from the dict
        if self.is_valid_coords(coords) and self.get(coords).get_top() is None:
            self.game_map.pop(coords, None)

        return to_return

    def replace(self, coords: Vector, to_place: GameObject) -> None:
        """
        Replaces the GameObjectContainer at the given coordinate with a new GameObjectContainer. The new one will
        contain the `to_place` object instead. No coordinates are removed in this way
        """
        goc: GameObjectContainer = GameObjectContainer([to_place])
        self.game_map[coords] = goc

    def remove_coordinate(self, coords: Vector) -> None:
        """
        Removes the given coordinate from the game map.
        """

        if self.is_valid_coords(coords):
            self.game_map.pop(coords, None)

    def get_top(self, coords: Vector) -> GameObject | None:
        """
        Returns the last object in the GameObjectContainer (i.e, the top-most object in the stack). Returns None if
        invalid coordinates are given.
        :param coords:
        :return: GameObject or None
        """
        return self.game_map[coords].get_top() if coords in self.game_map else None

    def object_is_found_at(self, coords: Vector, object_type: ObjectType) -> bool:
        """
        Searches for an object with the given object type at the given coordinate. If no object is found, or if the
        coordinate is invalid, return False.
        :param coords:
        :param object_type:
        :return: True or False to determine if the object is at that location
        """

        if not self.is_valid_coords(coords):
            return False

        result: list[GameObject] | None = self.game_map[coords].get_objects(object_type)
        return result is not None and len(result) > 0

    def is_valid_coords(self, coords: Vector) -> bool:
        """
        Check if the given coordinates are valid. In order to do so, the following criteria must be met:
            - The given coordinates must be in the self.game_map dictionary keys first
            - Otherwise, the coordinates must be within the size of the game map

        :param coords:
        :return: True if the coordinates are already in the map or are within the map size
        """

        return (0 <= coords.x < self.map_size.x) and (0 <= coords.y < self.map_size.y)

    def is_occupiable(self, coords: Vector) -> bool:
        return self.is_valid_coords(coords) and (self.get(coords).get_top() is None or
                                                 isinstance(self.get(coords).get_top(), Occupiable))

    # Returns the Vector and a list of GameObject for whatever objects you are trying to get
    # CHANGE RETURN TYPE TO BE A DICT NOT A LIST OF TUPLES
    def get_objects(self, look_for: ObjectType) -> list[tuple[Vector, list[GameObject]]]:
        """
        Zips together the game map's keys and values. A nested for loop then iterates through the zipped lists, and
        looks for any objects that have the same object type that was passed in. A list of tuples containing the
        coordinates and the objects found is returned. If the given object type isn't found on the map, then an empty
        list is returned
        """

        results: list[tuple[Vector, list[GameObject]]] = []

        # Loops through the zipped list
        # DICTIONARY COMPREHENSION HERE PLEASE
        for vec, go_container in self.game_map.items():
            found: list[GameObject] = go_container.get_objects(look_for)  # add the matching object to the found list

            # add values to result if something was found
            if len(found) > 0:
                results.append((vec, found))  # Add tuple pairings and objects found

        return results

    def get_active_pair(self) -> tuple[Character | None, Character | None]:
        return self.ordered_teams[self.active_pair_index]

    def get_characters(self, country: CountryType | None = None) -> dict[Vector, Character]:
        """
        Returns a dictionary of Vector: Character pair.
        """

        # all values are GameObjectContainers (GOC), so this gets all the characters from each GOC
        # Ignore the warning; Character objects will always be at the top of an existing GOC
        objects: list[GameObject] = [game_object_container.get_top() for game_object_container in
                                     self.game_map.values()]

        if country is None:
            # create a dictionary by combining all coordinates with the characters
            return {coords: character for coords, character in zip(self.game_map.keys(), objects)
                    if self.game_map[coords].contains_character(character)}

        # filter out any objects that aren't characters and doesn't have the matching country_type
        # the warning can be ignored since that if statement is only reached if the object is a Character
        return {coords: character for coords, character in zip(self.game_map.keys(), objects) if
                isinstance(self.game_map[coords].get_top(), Character) and
                self.game_map[coords].get_top().country_type == country}

    def update_character_on_map(self, character: Character) -> None:
        # remove the old instance of the character from the map
        self.replace(character.position, character)

    def clean_up_dead_characters(self, uroda_team_manager, turpis_team_manager) -> None:
        """
        Using the `recently_died` list, this will remove every character from the list off the game map and also move
        them from their respective team manager's `team` list to its `dead_team` list.
        """

        while len(self.recently_died) > 0:
            dead_char: Character = self.recently_died.pop(0)
            team_manager: TeamManager = uroda_team_manager \
                if dead_char.country_type == CountryType.URODA else turpis_team_manager

            # remove the character from the game map
            self.remove_coordinate(dead_char.position)

            # add the character to the dead_team list and remove it from the team list
            team_manager.organize_dead_characters()

            # find the character in the ordered_teams list and remove it from there
            for index in range(len(self.ordered_teams)):
                obj1: Character | None = self.ordered_teams[index][0]
                obj2: Character | None = self.ordered_teams[index][1]

                # if an object is not none and has the same name, create a new tuple and replace the object with None
                if obj1 is not None and obj1.name == dead_char.name:
                    self.ordered_teams[index] = (None, obj2)

                if obj2 is not None and obj2.name == dead_char.name:
                    self.ordered_teams[index] = (obj1, None)

            # reset all characters' took_action bool after a character is removed
            if team_manager.everyone_took_action():
                for char in team_manager.team:
                    char.took_action = False

                team_manager.speed_sort()

    def get_character_from(self, coords: Vector) -> Character | None:
        """
        Returns a Character object from the given coordinate. If no character is at the coordinate, return None. If
        a different object is at the current location, this will also return None since it only looks for Character
        objects.

        Example:
            * A Wall object is at the given coordinate of (0, 1). This would return None
            * A Character object is at the given coordinate of (1, 0) and would be returned
        """
        # return None if the coordinates are not in the map
        if coords not in self.game_map:
            return

        obj: GameObject = self.game_map[coords].get_top()

        # return the object if it's an instance of Character, else return None
        return obj if isinstance(obj, Character) else None

    def get_in_bound_coords(self) -> list[Vector]:
        """
        Returns list of all vector positions available on the game board (everything in bounds).
        """
        return [Vector(x, y) for x in range(self.map_size.x) for y in range(self.map_size.y)]

    def order_teams(self, uroda_team_manager: TeamManager, turpis_team_manager: TeamManager) -> None:
        """
        Each turn, at most two characters will take action. It will be each team's next fastest character, assuming
        it hasn't died or taken its action yet.

        Assume that the Uroda team has speeds of the following: [15, 17, 16]. They would be ordered as [17, 16, 15]
        instead.

        An example of fully ordered teams is below.

        Example:
            Uroda team speeds: [17, 16, 15]
            Turpis team speeds: [20, 18, 14]

        Now, each character needs to be paired by how fast they are. The pairs will be coupled together in a tuple. This
        tuple will specifically be ordered as the following: (Uroda character, Turpis character). Having a structured
        tuple creates a good structure for organization.

        Each tuple will be added to a list. The result of pairing the example Uroda and Turpis teams is below.

        Example:
            [(17, 20), (16, 18), (15, 14)]

        If each pair is not already in order, when it is time execute each character's action, it will take the fastest
        of the two characters and have it act first.
        """

        if uroda_team_manager is None or turpis_team_manager is None:
            return

        uroda_team_manager.speed_sort()
        turpis_team_manager.speed_sort()

        # contains the pairs of characters for each team; tuples will contain Character or None values
        result: list[tuple[Character | None, Character | None]] = []

        # easy access to both teams
        uroda_team: list[Character] = [char for char in uroda_team_manager.team]  # if not char.took_action]
        turpis_team: list[Character] = [char for char in turpis_team_manager.team]  # if not char.took_action]

        # pair the characters; the ordered pair matters, so uroda will be first in the tuples
        for index in range(max(len(uroda_team), len(turpis_team))):
            if index >= min(len(uroda_team), len(turpis_team)):
                if len(uroda_team) > len(turpis_team):
                    result.append((uroda_team[index], None))
                else:
                    result.append((None, turpis_team[index]))
            else:
                result.append((uroda_team[index], turpis_team[index]))

        self.ordered_teams = result

    def get_char_from_ordered_teams(self, char_name: str) -> Character | None:
        """
        Searches for the character by the given name in the `ordered_teams` list. If the character is not found, None
        is returned.
        """
        for pair in self.ordered_teams:
            for char in pair:
                if char is not None and char.name == char_name:
                    return char

    def to_json(self) -> dict:
        data: dict[str, object] = super().to_json()
        temp: dict[Vector, GameObjectContainer] | None = {str(vec.to_json()): go_container.to_json() for
                                                          vec, go_container in
                                                          self.game_map.items()} if self.game_map is not None else None
        data['game_map'] = temp
        data['seed'] = self.seed
        data['map_size'] = self.map_size.to_json()
        data['location_vectors'] = [vec.to_json() for vec in self.locations.keys()] if self.locations is not None \
            else None
        data['location_objects'] = [[obj.to_json() for obj in v] for v in
                                    self.locations.values()] if self.locations is not None else None
        data['walled'] = self.walled
        data['event_active'] = self.event_active

        # since json doesn't have tuples, convert the list of tuples to a list of lists and convert later
        data['ordered_teams'] = [
            [pair[0].to_json() if pair[0] is not None else None,
             pair[1].to_json() if pair[1] is not None else None]
            for pair in self.ordered_teams]

        data['recently_died'] = [char.to_json() for char in self.recently_died]

        data['turn_info'] = self.turn_info

        data['active_pair_index'] = self.active_pair_index

        return data

    def generate_event(self, start: int, end: int) -> None:
        self.event_active = random.randint(start, end)

    def __from_json_helper(self, data: dict) -> GameObject:
        temp: ObjectType = ObjectType(data['object_type'])

        match temp:
            case ObjectType.TILE:
                return Tile().from_json(data)
            case ObjectType.WALL:
                return Wall().from_json(data)
            case (ObjectType.ANAHITA | ObjectType.BERRY | ObjectType.FULTRA |
                  ObjectType.NINLIL | ObjectType.CALMUS | ObjectType.IRWIN):
                return Leader().from_json(data)
            case ObjectType.URODA_GENERIC_ATTACKER | ObjectType.TURPIS_GENERIC_ATTACKER:
                return GenericAttacker().from_json(data)
            case ObjectType.URODA_GENERIC_HEALER | ObjectType.TURPIS_GENERIC_HEALER:
                return GenericHealer().from_json(data)
            case ObjectType.URODA_GENERIC_TANK | ObjectType.TURPIS_GENERIC_TANK:
                return GenericTank().from_json(data)
            case ObjectType.GENERIC_TRASH:
                return GenericTrash().from_json(data)
            case _:
                raise ValueError(
                    f'The object type of the object is not handled properly. The object type passed in is {temp}. The '
                    f'data passed in is:\n{data}')

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.seed: int | None = data['seed']
        self.map_size: Vector = Vector().from_json(data['map_size'])

        self.locations: dict[Vector, list[GameObject]] = {
            Vector().from_json(k): [self.__from_json_helper(obj) for obj in v] for k, v in
            zip(data['location_vectors'], data['location_objects'])} if data['location_vectors'] is not None else None

        self.walled: bool = data['walled']
        self.event_active: int = data['event_active']

        # json.ast.literal_eval is `abstract syntax tree`
        # the vector objects were stored as a dictionary in a string format
        # json.ast.literal_eval takes in the string, converts it to a dict, and uses that for the from_json()

        self.game_map: dict[Vector, GameObjectContainer] = {
            Vector().from_json(ast.literal_eval(k)): GameObjectContainer().from_json(v)
            for k, v in data['game_map'].items()} if data['game_map'] is not None else None

        # this converts the list of lists into a list of tuples while handling none values
        self.ordered_teams: list[tuple[Character | None, Character | None]] = [
            (self.__from_json_helper(pair[0]) if pair[0] is not None else None,
             self.__from_json_helper(pair[1]) if pair[1] is not None else None)
            for pair in data['ordered_teams']
        ]

        self.recently_died: list[Character] = [self.__from_json_helper(info) for info in data['recently_died']]

        self.turn_info: str = data['turn_info']

        self.active_pair_index: int = data['active_pair_index']

        return self
