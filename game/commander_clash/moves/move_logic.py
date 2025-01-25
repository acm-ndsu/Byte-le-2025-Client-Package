import math

from game.commander_clash.character.character import Character
from game.commander_clash.character.stats import Stat
from game.commander_clash.moves.moves import *
from game.common.enums import MoveType
from game.common.map.game_board import GameBoard
from game.common.team_manager import TeamManager
from game.config import MINIMUM_DAMAGE, SPECIAL_POINT_LIMIT


def calculate_damage(user: Character, target: Character, current_move: AbstractAttack) -> int:
    """
    Calculates the damage done by using the following formula:

        ceiling((character attack value + move damage value) * (1 - target defense value / 100))

    This method can be used to plan for the competition and give competitors a way to adapt to battles.
    """
    ...


def calculate_healing(target: Character, current_move: AbstractHeal) -> int:
    """
    Calculates the healing done to the target by determining the smallest amount of healing possible. The numbers
    compared are the heal_points and the difference between the target's max health and current health.

    Example:
        Target health: 10/10
        heal_points: 5

        If target health = 4/10, return 5 since healing more than 5 isn't possible
        If target health = 5/10, return 5
        If target health = 6/10, return 4 since healing 5 isn't possible
    """
    ...
