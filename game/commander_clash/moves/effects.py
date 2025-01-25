from __future__ import annotations

from game.commander_clash.moves.abstract_moves import *
from game.common.enums import TargetType


class Effect(AbstractMove):
    """
    The Effect class - and any of its subclasses - behave as a secondary effect that occurs when a move is used. This
    can include inflicting damage to the user, giving a buff, providing additional healing, inflicting a debuff, and
    more. These inherit from AbstractMove since they have common attributes.
    """

    def __init__(self, target_type: TargetType = TargetType.SELF):
        super().__init__(target_type)
        self.object_type = ObjectType.EFFECT


class AttackEffect(AbstractAttack, Effect):
    def __init__(self, target_type: TargetType = TargetType.SELF, damage_points: int = 1):
        super().__init__(target_type, damage_points)
        self.object_type = ObjectType.ATTACK_EFFECT

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two effects
        return (self.object_type == other.object_type and self.target_type == other.target_type
                and self.damage_points == other.damage_points)


class HealEffect(AbstractHeal, Effect):
    def __init__(self, target_type: TargetType = TargetType.SELF, heal_points: int = 0):
        super().__init__(target_type, heal_points)
        self.object_type = ObjectType.HEAL_EFFECT

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two effects
        return (self.object_type == other.object_type and self.target_type == other.target_type
                and self.heal_points == other.heal_points)


class BuffEffect(AbstractBuff, Effect):
    def __init__(self, target_type: TargetType = TargetType.SELF, buff_amount: int = 1,
                 stat_to_affect: ObjectType = ObjectType.ATTACK_STAT):
        super().__init__(target_type, buff_amount, stat_to_affect)
        self.object_type = ObjectType.BUFF_EFFECT

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two effects
        return (self.object_type == other.object_type and self.target_type == other.target_type
                and self.buff_amount == other.buff_amount)


class DebuffEffect(AbstractDebuff, Effect):
    def __init__(self, target_type: TargetType = TargetType.SELF, debuff_amount: int = -1,
                 stat_to_affect: ObjectType = ObjectType.ATTACK_STAT):
        super().__init__(target_type, debuff_amount, stat_to_affect)
        self.object_type = ObjectType.DEBUFF_EFFECT

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two effects
        return (self.object_type == other.object_type and self.target_type == other.target_type
                and self.debuff_amount == other.debuff_amount)
