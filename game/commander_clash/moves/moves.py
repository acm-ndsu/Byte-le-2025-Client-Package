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

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['name'] = self.name
        data['cost'] = self.cost
        data['effect'] = self.effect.to_json() if self.effect is not None else None
        data['priority'] = self.priority

        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.name: str = data['name']
        self.cost: int = data['cost']

        if data['effect'] is None:
            self.effect: Effect | None = None
        else:
            # convert the int from the JSON to the proper MoveType enum
            move_type: MoveType = MoveType(data['effect']['move_type'])

            if move_type == MoveType.MOVE:
                self.effect: Effect | None = Effect().from_json(data['effect'])
            elif move_type == MoveType.ATTACK:
                self.effect: AttackEffect | None = AttackEffect().from_json(data['effect'])
            elif move_type == MoveType.HEAL:
                self.effect: HealEffect | None = HealEffect().from_json(data['effect'])
            elif move_type == MoveType.BUFF:
                self.effect: BuffEffect | None = BuffEffect().from_json(data['effect'])
            elif move_type == MoveType.DEBUFF:
                self.effect: DebuffEffect | None = DebuffEffect().from_json(data['effect'])

        self.priority = data['priority']

        return self


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
