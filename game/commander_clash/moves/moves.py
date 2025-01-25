from __future__ import annotations

from game.commander_clash.moves.effects import *
from game.common.enums import MoveType, ObjectType


class Move(AbstractMove):
    def __init__(self, name: str = '', target_type: TargetType = TargetType.SINGLE_OPP, cost: int = 0,
                 effect: Effect | None = None):
        super().__init__(target_type)
        self.name: str = name
        self.object_type = ObjectType.MOVE
        self.cost: int = cost
        self.effect: Effect | None = effect
        self.priority: int = 0

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if name is None or not isinstance(name, str):
            raise ValueError(f'{self.__class__.__name__}.name must be a string. It is a(n) {name.__class__.__name__} '
                             f'and has the value of {name}.')
        self.__name: str = name

    @property
    def cost(self) -> int:
        return self.__cost

    @cost.setter
    def cost(self, cost: int) -> None:
        if cost is None or not isinstance(cost, int):
            raise ValueError(f'{self.__class__.__name__}.cost must be an int. It is a(n) {cost.__class__.__name__} '
                             f'and has the value of {cost}.')
        self.__cost: int = cost

    @property
    def effect(self) -> Effect | None:
        return self.__effect

    @effect.setter
    def effect(self, effect: Effect | None) -> None:
        if effect is not None and not isinstance(effect, Effect):
            raise ValueError(f'{self.__class__.__name__}.effect must be a Move or None. It is a(n) '
                             f'{effect.__class__.__name__} and has the value of {effect}.')
        self.__effect: Effect | None = effect


class Attack(Move, AbstractAttack):
    def __init__(self, name: str = '', target_type: TargetType = TargetType.SINGLE_OPP, cost: int = 0,
                 effect: Effect | None = None, damage_points: int = 0):
        super().__init__(name, target_type, cost, effect)

        self.damage_points: int = damage_points
        self.object_type = ObjectType.ATTACK_MOVE
        self.move_type = MoveType.ATTACK
        self.priority = 1

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two Moves
        return (self.name == other.name and self.object_type == other.object_type
                and self.damage_points == other.damage_points and self.cost == other.cost
                and self.effect == other.effect and self.move_type == other.move_type)


class Heal(Move, AbstractHeal):
    def __init__(self, name: str = '', target_type: TargetType = TargetType.ENTIRE_TEAM, cost: int = 0,
                 effect: Effect | None = None, heal_points: int = 0):
        super().__init__(name, target_type, cost, effect)

        self.heal_points: int = heal_points
        self.object_type = ObjectType.HEAL_MOVE
        self.move_type = MoveType.HEAL
        self.priority = 4

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two Moves
        return (self.name == other.name and self.object_type == other.object_type
                and self.heal_points == other.heal_points and self.cost == other.cost
                and self.effect == other.effect and self.move_type == other.move_type)


class Buff(Move, AbstractBuff):
    def __init__(self, name: str = '', target_type: TargetType = TargetType.ENTIRE_TEAM, cost: int = 0,
                 effect: Effect | None = None, buff_amount: int = 1,
                 stat_to_affect: ObjectType = ObjectType.ATTACK_STAT):
        super().__init__(name, target_type, cost, effect)

        self.object_type = ObjectType.BUFF_MOVE
        self.move_type = MoveType.BUFF
        self.buff_amount: int = buff_amount
        self.stat_to_affect: ObjectType = stat_to_affect
        self.priority = 3

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two Moves
        return (self.name == other.name and self.object_type == other.object_type
                and self.buff_amount == other.buff_amount and self.cost == other.cost
                and self.effect == other.effect and self.move_type == other.move_type
                and self.stat_to_affect == other.stat_to_affect)


class Debuff(Move, AbstractDebuff):
    def __init__(self, name: str = '', target_type: TargetType = TargetType.SINGLE_OPP, cost: int = 0,
                 effect: Effect | None = None, debuff_amount: int = -1,
                 stat_to_affect: ObjectType = ObjectType.ATTACK_STAT):
        super().__init__(name, target_type, cost, effect)

        self.object_type = ObjectType.DEBUFF_MOVE
        self.move_type = MoveType.DEBUFF
        self.debuff_amount: int = debuff_amount
        self.stat_to_affect: ObjectType = stat_to_affect
        self.priority = 2

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two Moves
        return (self.name == other.name and self.object_type == other.object_type
                and self.debuff_amount == other.debuff_amount and self.cost == other.cost
                and self.effect == other.effect and self.move_type == other.move_type
                and self.stat_to_affect == other.stat_to_affect)
