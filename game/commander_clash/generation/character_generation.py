from game.commander_clash.character.character import Leader, GenericAttacker, GenericTank, GenericHealer, GenericTrash
from game.commander_clash.character.stats import AttackStat, DefenseStat, SpeedStat
from game.commander_clash.moves.effects import AttackEffect, BuffEffect, DebuffEffect, HealEffect
from game.commander_clash.moves.moves import Attack, Buff, Debuff, Heal
from game.commander_clash.moves.moveset import Moveset
from game.common.enums import ObjectType, ClassType, TargetType

"""
This file is used to create the different leaders and generic characters. In this file, all attributes of a character 
(stats, movesets, etc.) will be set here.
"""


def generate_anahita() -> Leader:
    ...


def generate_berry() -> Leader:
    ...


def generate_fultra() -> Leader:
    ...


def generate_ninlil() -> Leader:
    ...


def generate_calmus() -> Leader:
    ...


def generate_irwin() -> Leader:
    ...


def generate_generic_attacker(name: str = 'Attacker') -> GenericAttacker:
    ...


def generate_generic_healer(name: str = 'Healer') -> GenericHealer:
    ...


def generate_generic_tank(name: str = 'Tank') -> GenericTank:
    ...


def generate_generic_trash() -> GenericTrash:
    ...
