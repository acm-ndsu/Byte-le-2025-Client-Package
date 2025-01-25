import json

from game.commander_clash.character.character import Leader, Generic, Character, GenericTrash
from game.common.enums import CountryType, RankType, ObjectType, ClassType
from game.common.team_manager import TeamManager
from game.utils.vector import Vector


def generate_locations_dict(team_managers: list[TeamManager]) -> dict:
    ...


def update_character_info(team_managers: list[TeamManager]):
    """
    Gives all characters in the team managers their country affiliation and positions.
    """
    ...


def __assign_generic_object_type(char: Character):
    """
    Gives a Generic character their ObjectType based on their country and their ClassType.
    """
    ...
