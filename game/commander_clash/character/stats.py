from typing import Self

from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.config import STAT_MINIMUM, ATTACK_MAXIMUM, DEFENSE_MAXIMUM, SPEED_MAXIMUM


class Stat(GameObject):
    """
    The Stat class represents the different stats a character has: Attack, Defense, Speed.

    Each stat has a base value that is used as an initial value. The `value` property is the actual value that is used
    and modified for calculations.

    The `stage` property is used to help calculate the buff/debuff modifier that needs to be applied to a stat. The way
    this system works is similar to a slider or a number line. The bounds are from -4 to 4 inclusive. If the stage is
    at 0, that means the modifier is at x1. When the stage increases or decreases, the modifier is adjusted
    appropriately for the calculation.

    The AttackStat subclass will work a bit differently. The attack stat will simply be a modifier that is adjusted
    and affects the damage points of an attack Move when a character deals damage to an opponent. Therefore,
    the base value will always be 1 when initialized, and when the stage and modifier properties are calculated,
    the value will adjust appropriately as a modifier instead.

    Example:
        AttackStat value at stage +1 = 1.5
        AttackStat value at stage -1 = 0.667

    This is why the base_value and value properties are type hinted as int | float.
    """

    def __init__(self, base_value: int = 1):
        super().__init__()

        self.object_type = ObjectType.STAT
        self.base_value: int | float = base_value
        self.value: int | float = base_value

    # override the hashable methods to easily compare stats
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Stat):
            return False

        return self.value == other.value

    def __gt__(self, other: Self) -> bool:
        if not isinstance(other, Stat):
            return False

        return self.value > other.value

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, Stat):
            return False

        return self.value < other.value

    def __ge__(self, other: Self) -> bool:
        if not isinstance(other, Stat):
            return False

        return self.value >= other.value

    def __le__(self, other: Self) -> bool:
        if not isinstance(other, Stat | int):
            return False

        return self.value <= other.value

    def __ne__(self, other: Self) -> bool:
        if not isinstance(other, Stat):
            return False

        return self.value != other.value

    @property
    def base_value(self) -> int | float:
        return self.__base_value

    @base_value.setter
    def base_value(self, base_value: int | float) -> None:
        if base_value is None or not isinstance(base_value, int | float):
            raise ValueError(f'{self.__class__.__name__}.base_value must be an int or float. It is a(n) '
                             f'{base_value.__class__.__name__} and has a value of {base_value}')

        if not base_value > 0:
            raise ValueError(f'{self.__class__.__name__}.base_value must be greater than 0')

        self.__base_value = base_value

    @property
    def value(self) -> int | float:
        return self.__value

    @value.setter
    def value(self, value: int | float) -> None:
        if value is None or not isinstance(value, int | float):
            raise ValueError(f'{self.__class__.__name__}.value must be an int or float. It is a(n) '
                             f'{value.__class__.__name__} and has a value of {value}')

        if value < 0:
            raise ValueError(f'{self.__class__.__name__}.value must be a positive int or float')

        self.__value = value

    def is_maxed(self) -> None:
        """
        Returns true if the stat is maxed out. This is determined by the individual stat's max amount.
        """
        ...

    def is_minimized(self):
        ...

    def apply_modification(self, modification_amount: int) -> None:
        """
        This method will add the modification amount from either a buff or debuff. If it goes below the stat minimum,
        it will set it to that minimum. The same applies to the maximum.
        """
        ...


class AttackStat(Stat):
    def __init__(self, base_value: int = 1):
        super().__init__(base_value)
        self.object_type = ObjectType.ATTACK_STAT

    def is_maxed(self):
        ...

    def apply_modification(self, modification_amount: int) -> None:
        ...


class DefenseStat(Stat):
    def __init__(self, base_value: int = 1):
        super().__init__(base_value)
        self.object_type = ObjectType.DEFENSE_STAT

    def is_maxed(self):
        ...

    def apply_modification(self, modification_amount: int) -> None:
        ...


class SpeedStat(Stat):
    def __init__(self, base_value: int = 1):
        super().__init__(base_value)
        self.object_type = ObjectType.SPEED_STAT

    def is_maxed(self):
        ...

    def apply_modification(self, modification_amount: int) -> None:
        ...
