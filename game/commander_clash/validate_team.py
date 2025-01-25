from game.commander_clash.character.character import Character
from game.commander_clash.generation.character_generation import *
from game.common.enums import SelectLeader, SelectGeneric, ClassType


def validate_team_selection(
        enums: tuple[SelectGeneric, SelectLeader, SelectGeneric]) -> list[Character]:
    """
    Checks if the given tuple has SelectLeader, SelectGeneric, SelectGeneric. If any of the characters are not the class
    they should be, it will be replaced with a Generic Attacker
    """
    ...
