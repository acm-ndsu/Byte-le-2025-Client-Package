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
        ...

    def generate_map(self) -> None:
        # Dictionary Init
        ...

    def get(self, coords: Vector) -> GameObjectContainer | None:
        """
        A GameObjectContainer object returned given the coordinates. If the coordinates are valid but are not in the
        game_map yet, a new GameObjectContainer is created and is stored in a new entry in the game_map dictionary.

        :param coords:
        :return: GameObjectContainer or None
        """
        ...

    def place(self, coords: Vector, game_obj: GameObject | None) -> bool:
        """
        Places the given object at the given coordinates if they are valid. A boolean is returned to represent a
        successful placement
        :param coords:
        :param game_obj:
        :return: True or False for a successful placement of the given object
        """
        ...

    def get_objects_from(self, coords: Vector, object_type: ObjectType | None = None) -> list[GameObject]:
        """
        Returns a list of GameObjects from the given, valid coordinates. If an ObjectType is specified, only that
        ObjectType will be returned. If an ObjectType is not specified, the entire list of GameObjects will be
        returned. If nothing is found, an empty list is given.
        :param coords:
        :param object_type:
        :return: a list of GameObjects
        """
        ...

    def remove(self, coords: Vector, object_type: ObjectType) -> GameObject | None:
        """
        Removes the first instance of the given object type from the coordinates if they are valid. Returns None if
        invalid coordinates are given.
        :param coords:
        :param object_type:
        :return: GameObject or None
        """
        ...

    def replace(self, coords: Vector, to_place: GameObject) -> None:
        """
        Replaces the GameObjectContainer at the given coordinate with a new GameObjectContainer. The new one will
        contain the `to_place` object instead. No coordinates are removed in this way
        """
        ...

    def remove_coordinate(self, coords: Vector) -> None:
        """
        Removes the given coordinate from the game map.
        """
        ...

    def get_top(self, coords: Vector) -> GameObject | None:
        """
        Returns the last object in the GameObjectContainer (i.e, the top-most object in the stack). Returns None if
        invalid coordinates are given.
        :param coords:
        :return: GameObject or None
        """
        ...

    def object_is_found_at(self, coords: Vector, object_type: ObjectType) -> bool:
        """
        Searches for an object with the given object type at the given coordinate. If no object is found, or if the
        coordinate is invalid, return False.
        :param coords:
        :param object_type:
        :return: True or False to determine if the object is at that location
        """
        ...

    def is_valid_coords(self, coords: Vector) -> bool:
        """
        Check if the given coordinates are valid. In order to do so, the following criteria must be met:
            - The given coordinates must be in the self.game_map dictionary keys first
            - Otherwise, the coordinates must be within the size of the game map

        :param coords:
        :return: True if the coordinates are already in the map or are within the map size
        """
        ...

    def is_occupiable(self, coords: Vector) -> bool:
        ...

    # Returns the Vector and a list of GameObject for whatever objects you are trying to get
    # CHANGE RETURN TYPE TO BE A DICT NOT A LIST OF TUPLES
    def get_objects(self, look_for: ObjectType) -> list[tuple[Vector, list[GameObject]]]:
        """
        Zips together the game map's keys and values. A nested for loop then iterates through the zipped lists, and
        looks for any objects that have the same object type that was passed in. A list of tuples containing the
        coordinates and the objects found is returned. If the given object type isn't found on the map, then an empty
        list is returned
        """
        ...

    def get_active_pair(self) -> tuple[Character | None, Character | None]:
        ...

    def get_characters(self, country: CountryType | None = None) -> dict[Vector, Character]:
        """
        Returns a dictionary of Vector: Character pair.
        """
        ...

    def update_character_on_map(self, character: Character) -> None:
        ...

    def clean_up_dead_characters(self, uroda_team_manager, turpis_team_manager) -> None:
        """
        Using the `recently_died` list, this will remove every character from the list off the game map and also move
        them from their respective team manager's `team` list to its `dead_team` list.
        """
        ...

    def get_character_from(self, coords: Vector) -> Character | None:
        """
        Returns a Character object from the given coordinate. If no character is at the coordinate, return None. If
        a different object is at the current location, this will also return None since it only looks for Character
        objects.

        Example:
            * A Wall object is at the given coordinate of (0, 1). This would return None
            * A Character object is at the given coordinate of (1, 0) and would be returned
        """
        ...

    def get_in_bound_coords(self) -> list[Vector]:
        """
        Returns list of all vector positions available on the game board (everything in bounds).
        """
        ...

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
        ...

    def get_char_from_ordered_teams(self, char_name: str) -> Character | None:
        """
        Searches for the character by the given name in the `ordered_teams` list. If the character is not found, None
        is returned.
        """
        ...

    def generate_event(self, start: int, end: int) -> None:
        ...
