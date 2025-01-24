import math

from game.commander_clash.character.character import Character
from game.commander_clash.character.stats import Stat
from game.commander_clash.moves.moves import *
from game.common.enums import MoveType
from game.common.map.game_board import GameBoard
from game.common.team_manager import TeamManager
from game.config import MINIMUM_DAMAGE, SPECIAL_POINT_LIMIT


def handle_move_logic(user: Character, targets: list[Character], current_move: Move, is_normal_move: bool,
                      world: GameBoard, uroda_team_manager: TeamManager, turpis_team_manager: TeamManager) -> None:
    """
    Handles the logic for every move type. That is, damage is applied for attacks, health is increased for healing,
    and stats are modified based on the buff/debuff
    """
    match current_move.move_type:
        case MoveType.ATTACK:
            user.state = 'attacking'
            __assign_target_states(targets, 'attacked')
            current_move: Attack
            __calc_and_apply_damage(user, targets, current_move, world)
        case MoveType.HEAL:
            __assign_target_states(targets, 'healing')
            current_move: Heal
            __apply_heal_points(targets, current_move, world)
        case MoveType.BUFF:
            __assign_target_states(targets, 'buffing')
            current_move: Buff
            __handle_stat_modification(targets, current_move, world)
        case MoveType.DEBUFF:
            __assign_target_states(targets, 'debuffing')
            current_move: Debuff
            __handle_stat_modification(targets, current_move, world)
        case _:
            return

    if is_normal_move:
        next_sp: int = user.special_points + 1

        # prevent the special points from going over the cap
        user.special_points = next_sp if next_sp <= SPECIAL_POINT_LIMIT else user.special_points

    # subtract the cost of using the move from the character's total special points if there were targets
    user.special_points -= current_move.cost


def handle_effect_logic(user: Character, targets: list[Character], current_effect: Effect, world: GameBoard) -> None:
    match current_effect.move_type:
        case MoveType.ATTACK:
            current_effect: AttackEffect
            __calc_and_apply_damage(user, targets, current_effect, world)
        case MoveType.HEAL:
            current_effect: HealEffect
            __apply_heal_points(targets, current_effect, world)
        case MoveType.BUFF:
            current_effect: BuffEffect
            __handle_stat_modification(targets, current_effect, world)
        case MoveType.DEBUFF:
            current_effect: DebuffEffect
            __handle_stat_modification(targets, current_effect, world)
        case _:
            return


def calculate_damage(user: Character, target: Character, current_move: AbstractAttack) -> int:
    """
    Calculates the damage done by using the following formula:

        ceiling((character attack value + move damage value) * (1 - target defense value / 100))

    This method can be used to plan for the competition and give competitors a way to adapt to battles.
    """

    # If it's an AttackEffect, the base damage should be applied and nothing else; no damage calculation needed for this
    if isinstance(current_move, AttackEffect):
        return current_move.damage_points

    damage: int = math.ceil((user.attack.value + current_move.damage_points) * (1 - target.defense.value / 100))

    # if damage amount is less than 1, return 1 as the minimum damage; otherwise, return the damage
    return MINIMUM_DAMAGE if damage < MINIMUM_DAMAGE else damage


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

    return min(current_move.heal_points, target.max_health - target.current_health)


def __calc_and_apply_damage(user: Character, targets: list[Character], current_move: AbstractAttack, world: GameBoard):
    """
    Calculates the damage to deal for every target and applies it to the target's health.
    """

    for target in targets:
        # get the damage to be dealt
        damage_to_deal: int = calculate_damage(user, target, current_move)

        target_hp_before: int = target.current_health

        # reduces the target's health while preventing it from going below 0 (the setter will throw an error if < 0)
        if target.current_health - damage_to_deal < 0:
            target.current_health = 0
        else:
            target.current_health -= damage_to_deal

        # change the message depending on if the current move is a Move or Effect
        if isinstance(current_move, Attack):
            world.turn_info += (f'{user.name} used {current_move.name} and dealt {damage_to_deal} damage to '
                                f'{target.name}!\n'
                                f'{target.name} health before: {target_hp_before} -> '
                                f'{target.name} health after: {target.current_health}\n')
        else:
            world.turn_info += (f'The secondary effect activated and dealt {damage_to_deal} damage to '
                                f'{target.name}!\n'
                                f'{target.name} health before: {target_hp_before} -> '
                                f'{target.name} health after: {target.current_health}\n')


def __apply_heal_points(targets: list[Character], current_move: AbstractHeal, world: GameBoard) -> None:
    """
    For every target in the list of targets, apply the heal amount to their current health. If the addition
    causes the current health to become larger than the character's max health, set it to be the max health.
    """

    # cannot reassign heal_amount, so make a new int that will store the new value calculated
    adjusted_healing_amount: int

    for target in targets:
        # calculate the healing amount
        adjusted_healing_amount = calculate_healing(target, current_move)

        target_hp_before: int = target.current_health

        target.current_health = target.current_health + adjusted_healing_amount

        # change the message depending on if the current move is a Move or Effect
        if isinstance(current_move, Heal):
            world.turn_info += (f'{current_move.name} healed {target.name} {adjusted_healing_amount} HP!\n'
                                f'{target.name} health before: {target_hp_before} -> '
                                f'{target.name} health after: {target.current_health}\n')
        else:
            world.turn_info += (f'The secondary effect activated and healed {target.name} '
                                f'{adjusted_healing_amount} HP!\n'
                                f'{target.name} health before: {target_hp_before} -> '
                                f'{target.name} health after: {target.current_health}\n')


def __handle_stat_modification(targets: list[Character], current_move: AbstractBuff | AbstractDebuff,
                               world: GameBoard) -> None:
    """
    Gets the modification needed from the current_move and applies it to every target's corresponding stat.
    """

    stat: Stat

    for target in targets:
        stat = __get_stat_object_to_affect(target, current_move)

        before_val: int = stat.value

        stat.apply_modification(current_move.buff_amount) if isinstance(current_move, AbstractBuff) else \
            stat.apply_modification(current_move.debuff_amount)

        after_val: int = stat.value

        # change the message depending on if the current move is a Move or Effect
        if isinstance(current_move, Buff) or isinstance(current_move, Debuff):
            world.turn_info += (f'{current_move.name} changed {target.name}\'s {stat.__class__.__name__.lower()} by '
                                f'{after_val - before_val}!\n'
                                f'{target.name}\'s {stat.__class__.__name__.lower()} before: {before_val} -> '
                                f'{target.name}\'s {stat.__class__.__name__.lower()} after: {after_val}\n')
        elif isinstance(current_move, Effect):
            world.turn_info += (f'The secondary effect activated and changed '
                                f'{target.name}\'s {stat.__class__.__name__.lower()} by '
                                f'{after_val - before_val}!\n'
                                f'{target.name}\'s {stat.__class__.__name__.lower()} before: {before_val} -> '
                                f'{target.name}\'s {stat.__class__.__name__.lower()} after: {after_val}\n')


def __get_stat_object_to_affect(target: Character, current_move: AbstractBuff | AbstractDebuff) -> Stat:
    """
    A helper method that returns the Stat object to buff/debuff based on the current_move's stat_to_affect.
    """

    match current_move.stat_to_affect:
        case ObjectType.ATTACK_STAT:
            return target.attack
        case ObjectType.DEFENSE_STAT:
            return target.defense
        case ObjectType.SPEED_STAT:
            return target.speed


def __assign_target_states(targets: list[Character], state: str) -> None:
    for target in targets:
        target.state = state
