from enum import Enum, auto

"""
**NOTE:** The use of the enum structure is to make is easier to execute certain tasks. It also helps with
identifying types of Objects throughout the project.

When developing the game, add any extra enums as necessary.
"""


class DebugLevel(Enum):
    NONE = 1
    CLIENT = 2
    CONTROLLER = 3
    ENGINE = 4


class ObjectType(Enum):
    NONE = 1
    ACTION = 2
    PLAYER = 3
    TEAMMANAGER = 4
    GAMEBOARD = 5
    VECTOR = 6
    TILE = 7
    WALL = 8
    OCCUPIABLE = 9
    GAME_OBJECT_CONTAINER = 10
    CHARACTER = 11
    URODA_GENERIC_ATTACKER = 12
    URODA_GENERIC_HEALER = 13
    URODA_GENERIC_TANK = 14
    TURPIS_GENERIC_ATTACKER = 15
    TURPIS_GENERIC_HEALER = 16
    TURPIS_GENERIC_TANK = 17
    GENERIC_TRASH = 18
    ANAHITA = 19
    BERRY = 20
    FULTRA = 21
    NINLIL = 22
    CALMUS = 23
    IRWIN = 24
    LEADER = 25
    MOVESET = 26
    STAT = 27
    ATTACK_STAT = 28
    DEFENSE_STAT = 29
    SPEED_STAT = 30
    MOVE = 31
    ATTACK_MOVE = 32
    HEAL_MOVE = 33
    BUFF_MOVE = 34
    DEBUFF_MOVE = 35
    EFFECT = 36
    ATTACK_EFFECT = 37
    HEAL_EFFECT = 38
    BUFF_EFFECT = 39
    DEBUFF_EFFECT = 40


class CountryType(Enum):
    URODA = 1
    TURPIS = 2


class SelectLeader(Enum):
    ANAHITA = 1
    BERRY = 2
    FULTRA = 3
    NINLIL = 4
    CALMUS = 5
    IRWIN = 6


class SelectGeneric(Enum):
    GEN_ATTACKER = 1
    GEN_HEALER = 2
    GEN_TANK = 3
    GEN_TRASH = 4


class MoveType(Enum):
    MOVE = 1
    ATTACK = 2
    HEAL = 3
    BUFF = 4
    DEBUFF = 5


class TargetType(Enum):
    SELF = 1
    ADJACENT_ALLIES = 2
    ENTIRE_TEAM = 3
    SINGLE_OPP = 4
    ALL_OPPS = 5


class ClassType(Enum):
    ATTACKER = 1
    HEALER = 2
    TANK = 3


class RankType(Enum):
    GENERIC = 1
    LEADER = 2


class ActionType(Enum):
    NONE = 1
    USE_NM = 2
    USE_S1 = 3
    USE_S2 = 4
    SWAP_UP = 5
    SWAP_DOWN = 6
