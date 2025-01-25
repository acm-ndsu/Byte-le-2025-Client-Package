from __future__ import annotations

from typing import Self

from game.common.enums import MoveType, TargetType, ObjectType
from game.common.game_object import GameObject


class AbstractMove(GameObject):
    def __init__(self, target_type: TargetType = TargetType.SELF):
        super().__init__()
        self.move_type = MoveType.MOVE
        self.target_type = target_type

    @property
    def move_type(self) -> MoveType:
        return self.__move_type

    @move_type.setter
    def move_type(self, move_type: MoveType) -> None:
        if move_type is None or not isinstance(move_type, MoveType):
            raise ValueError(f'{self.__class__.__name__}.move_type must be a MoveType. It is a(n) '
                             f'{move_type.__class__.__name__} and has the value of {move_type}.')
        self.__move_type: MoveType = move_type

    @property
    def target_type(self) -> TargetType:
        return self.__target_type

    @target_type.setter
    def target_type(self, target_type: TargetType) -> None:
        if target_type is None or not isinstance(target_type, TargetType):
            raise ValueError(f'{self.__class__.__name__}.target_type must be a TargetType. It is a(n) '
                             f'{target_type.__class__.__name__} and has the value of {target_type}.')
        self.__target_type: TargetType = target_type


class AbstractAttack(AbstractMove):
    def __init__(self, target_type: TargetType = TargetType.SELF, damage_points: int = 0):
        super().__init__(target_type)
        self.damage_points: int = damage_points
        self.move_type = MoveType.ATTACK

    @property
    def damage_points(self) -> int:
        return self.__damage_points

    @damage_points.setter
    def damage_points(self, damage_points: int) -> None:
        if damage_points is None or not isinstance(damage_points, int):
            raise ValueError(f'{self.__class__.__name__}.damage_points must be an int. It is a(n) '
                             f'{damage_points.__class__.__name__} and has the value of {damage_points}.')
        self.__damage_points: int = damage_points


class AbstractHeal(AbstractMove):
    def __init__(self, target_type: TargetType = TargetType.SELF, heal_points: int = 0):
        super().__init__(target_type)
        self.heal_points: int = heal_points
        self.move_type: MoveType = MoveType.HEAL

    @property
    def heal_points(self) -> int:
        return self.__heal_points

    @heal_points.setter
    def heal_points(self, heal_points: int) -> None:
        if heal_points is None or not isinstance(heal_points, int):
            raise ValueError(f'{self.__class__.__name__}.heal_points must be an int. It is a(n) '
                             f'{heal_points.__class__.__name__} and has the value of {heal_points}.')
        self.__heal_points: int = heal_points


class AbstractBuff(AbstractMove):
    def __init__(self, target_type: TargetType = TargetType.SELF, buff_amount: int = 1,
                 stat_to_affect: ObjectType = ObjectType.ATTACK_STAT):
        super().__init__(target_type)
        self.buff_amount: int = buff_amount
        self.move_type: MoveType = MoveType.BUFF
        self.stat_to_affect: ObjectType = stat_to_affect

    @property
    def buff_amount(self) -> int:
        return self.__buff_amount

    @buff_amount.setter
    def buff_amount(self, buff_amount: int) -> None:
        if buff_amount is None or not isinstance(buff_amount, int):
            raise ValueError(f'{self.__class__.__name__}.buff_amount must be an int. It is a(n) '
                             f'{buff_amount.__class__.__name__} and has the value of {buff_amount}.')

        if buff_amount <= 0:
            raise ValueError(f'{self.__class__.__name__}.buff_amount must be >= 0. The value '
                             f'{buff_amount} was given')

        self.__buff_amount: int = buff_amount

    @property
    def stat_to_affect(self) -> ObjectType:
        return self.__stat_to_affect

    @stat_to_affect.setter
    def stat_to_affect(self, stat_to_affect: ObjectType) -> None:
        if stat_to_affect is None or not isinstance(stat_to_affect, ObjectType):
            raise ValueError(f'{self.__class__.__name__}.stat_to_affect must be a ObjectType. It is a(n) '
                             f'{stat_to_affect.__class__.__name__} and has the value of {stat_to_affect}.')

        self.__stat_to_affect: ObjectType = stat_to_affect


class AbstractDebuff(AbstractMove):
    def __init__(self, target_type: TargetType = TargetType.SELF, debuff_amount: int = -1,
                 stat_to_affect: ObjectType = ObjectType.ATTACK_STAT):
        super().__init__(target_type)
        self.debuff_amount: int = debuff_amount
        self.move_type: MoveType = MoveType.DEBUFF
        self.stat_to_affect: ObjectType = stat_to_affect

    @property
    def debuff_amount(self) -> int:
        return self.__debuff_amount

    @debuff_amount.setter
    def debuff_amount(self, debuff_amount: int) -> None:
        if debuff_amount is None or not isinstance(debuff_amount, int):
            raise ValueError(f'{self.__class__.__name__}.debuff_amount must be an int. It is a(n) '
                             f'{debuff_amount.__class__.__name__} and has the value of {debuff_amount}.')

        if debuff_amount > -1:
            raise ValueError(f'{self.__class__.__name__}.debuff_amount must be < 0 . The value '
                             f'{debuff_amount} was given')

        self.__debuff_amount: int = debuff_amount
        
    @property
    def stat_to_affect(self) -> ObjectType:
        return self.__stat_to_affect

    @stat_to_affect.setter
    def stat_to_affect(self, stat_to_affect: ObjectType) -> None:
        if stat_to_affect is None or not isinstance(stat_to_affect, ObjectType):
            raise ValueError(f'{self.__class__.__name__}.stat_to_affect must be a ObjectType. It is a(n) '
                             f'{stat_to_affect.__class__.__name__} and has the value of {stat_to_affect}.')

        self.__stat_to_affect: ObjectType = stat_to_affect
