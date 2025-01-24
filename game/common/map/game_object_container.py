from game.commander_clash.character.character import *
from game.common.team_manager import TeamManager
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType
from game.common.map.wall import Wall
from typing import Self


class GameObjectContainer(GameObject):
    """
    This class encapsulates all objects that are to be stored at a coordinate in the GameBoard.
    """

    def __init__(self, objects: list[GameObject] | None = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.GAME_OBJECT_CONTAINER
        self.__sublist: list[GameObject] = []
        self.place_all(objects)

    def place_all(self, game_objs: list[GameObject] | None) -> bool:
        if game_objs is None:
            return False

        return all([self.place(x) for x in game_objs])

    def place(self, game_obj: GameObject | None) -> bool:
        """
        Attempts to place the given GameObject on the given coordinate if the coordinate is valid. If the top-most
        object inherits from Occupiable, the given object will be placed. If the top-most object *doesn't* inherit
        from Occupiable, but the given object does, it will be placed below the unoccupiable object. If the neither
        the top-most object nor the given object inherit from Occupiable, it will not be placed. If the top-most object
        is a wall, nothing will be placed at all.

        Examples

        1:
            - Top of stack object: OccupiableStation1
            - Given: OcccupiableStation2
            - Result: OccupiableStation1 -> OccupiableStation2
                Success
        2:
            - Top of stack object: Avatar
            - Given: OccupiableStation
            - Result: OccupiableStation, Avatar
                Success
        3:
            - Top of stack object: Station
            - Given: Avatar
            - Result: Station
                Failure
        4:
            - Top of stack object: Wall
            - Given: Avatar
            - Result: Wall
                Failure

        NOTE: True and False are returned instead of raising an error to prevent misuse of these methods during the
        competition; if a competitor uses them and the game crashes, the game would end abruptly.

        :param game_obj:
        :return: True to represent a success, False to represent a failure
        """

        # If the passed in object is not a game object, return False
        if game_obj is None:
            return False

        # If placing an unoccupiable object on an unoccupiable object, return False
        if not isinstance(game_obj, Occupiable) and not isinstance(self.get_top(), Occupiable | None):
            return False

        # get the top-most object from the list; assign to be None if list doesn't exist or is empty
        top_of_stack: GameObject | None = self.get_top()

        if self.__sublist is None:
            self.__sublist = []

        # if the top object is Occupiable, add the given object to the end of the list
        # otherwise, it's placed below the top (the insert method handles this while using the -1 index)
        self.__sublist.append(game_obj) if isinstance(top_of_stack, Occupiable) or top_of_stack is None \
            else self.__sublist.insert(-1, game_obj)

        return True

    def remove(self, object_type: ObjectType) -> GameObject | None:
        """
        Removes the first instance of the given ObjectType from the valid coordinate. The removed object is returned if
        applicable.
        :param object_type:
        :return: removed GameObject or None
        """

        for obj in self.__sublist:
            if obj.object_type == object_type:
                self.__sublist.remove(obj)
                return obj

        return None

    def get_top(self) -> GameObject | None:
        """
        Returns the last object in the sublist.
        """
        return self.__sublist[-1] if self.__sublist is not None and len(self.__sublist) > 0 else None

    def contains_character(self, character: Character) -> bool:
        """
        Checks if the given character is in the sublist.
        """
        return isinstance(character, Character) and character in self.__sublist

    def get_objects(self, object_type: ObjectType | None = None) -> list[GameObject]:
        """
        Gets all GameObjects of a specified type. If no parameter is provided, all objects are returned.
        :param object_type:
        :return: a list of GameObjects
        """
        if object_type is None or object_type is ObjectType.NONE:
            return self.__sublist

        return [obj for obj in self.__sublist if obj.object_type == object_type]

    def to_json(self) -> dict:
        data: dict[str, object] = super().to_json()
        data['sublist'] = [obj.to_json() for obj in self.__sublist] if self.__sublist is not None else []
        return data

    def __from_json_helper(self, data: dict) -> GameObject:
        temp: ObjectType = ObjectType(data['object_type'])
        match temp:
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
                    f'The object type of the object is not handled properly. The object type passed in is {temp}.')

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        temp_sublist: [GameObject] = [self.__from_json_helper(obj) for obj in data['sublist']] \
            if data['sublist'] is not None else []
        self.__sublist = []
        self.place_all(temp_sublist)
        return self
