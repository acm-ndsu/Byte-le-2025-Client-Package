import unittest

from game.commander_clash.moves.effects import *
from game.common.enums import *


class TestEffects(unittest.TestCase):
    """
    `Test Move Notes:`

    This class tests the different classes of the effects module.
    This class tests the constructors, getters, setters, and json methods.
    """
    # TEST THE USE METHOD ONCE IMPLEMENTED
    def setUp(self):
        self.effect: Effect = Effect()
        self.attack_effect: AttackEffect = AttackEffect(target_type=TargetType.SINGLE_OPP, damage_points=10)
        self.heal_effect: HealEffect = HealEffect(target_type=TargetType.ENTIRE_TEAM, heal_points=5)
        self.buff_effect: BuffEffect = BuffEffect(target_type=TargetType.ENTIRE_TEAM, buff_amount=1)
        self.debuff_effect: DebuffEffect = DebuffEffect(target_type=TargetType.SINGLE_OPP, debuff_amount=-1)

    def test_base_init(self) -> None:
        self.assertEqual(self.effect.object_type, ObjectType.EFFECT)
        self.assertEqual(self.effect.move_type, MoveType.MOVE)
        self.assertEqual(self.effect.target_type, TargetType.SELF)

    def test_attack_effect_equals_method(self) -> None:
        # test both are equal
        other_effect: AttackEffect = AttackEffect(target_type=TargetType.SINGLE_OPP, damage_points=10)
        self.assertTrue(other_effect == self.attack_effect)

        # test that the different damage points makes them different
        other_effect = AttackEffect(target_type=TargetType.SINGLE_OPP, damage_points=11)
        self.assertFalse(other_effect == self.attack_effect)

        # test a different target type makes it different
        other_effect = AttackEffect(target_type=TargetType.ALL_OPPS, damage_points=10)
        self.assertFalse(other_effect == self.attack_effect)

    def test_heal_effect_equals_method(self) -> None:
        # test both heal effects are equal
        other_effect: HealEffect = HealEffect(target_type=TargetType.ENTIRE_TEAM, heal_points=5)
        self.assertTrue(other_effect == self.heal_effect)

        # test that the different heal points makes them different
        other_effect = HealEffect(target_type=TargetType.ENTIRE_TEAM, heal_points=6)
        self.assertFalse(other_effect == self.heal_effect)

        # test a different target type makes it different
        other_effect = HealEffect(target_type=TargetType.ADJACENT_ALLIES, heal_points=5)
        self.assertFalse(other_effect == self.heal_effect)

    def test_buff_effect_equals_method(self) -> None:
        # test both buff effects are equal
        other_effect: BuffEffect = BuffEffect(target_type=TargetType.ENTIRE_TEAM, buff_amount=1)
        self.assertTrue(other_effect == self.buff_effect)

        # test that the different buff amounts makes them different
        other_effect = BuffEffect(target_type=TargetType.ENTIRE_TEAM, buff_amount=2)
        self.assertFalse(other_effect == self.buff_effect)

        # test a different target type makes it different
        other_effect = BuffEffect(target_type=TargetType.ADJACENT_ALLIES, buff_amount=1)
        self.assertFalse(other_effect == self.buff_effect)

    def test_debuff_effect_equals_method(self) -> None:
        # test both heal effects are equal
        other_effect: DebuffEffect = DebuffEffect(target_type=TargetType.SINGLE_OPP, debuff_amount=-1)
        self.assertTrue(other_effect == self.debuff_effect)

        # test that the different heal points makes them different
        other_effect = DebuffEffect(target_type=TargetType.SINGLE_OPP, debuff_amount=-2)
        self.assertFalse(other_effect == self.debuff_effect)

        # test a different target type makes it different
        other_effect = DebuffEffect(target_type=TargetType.ALL_OPPS, debuff_amount=-1)
        self.assertFalse(other_effect == self.debuff_effect)

    def test_base_json(self) -> None:
        data: dict = self.effect.to_json()
        effect: Effect = Effect().from_json(data)
        self.assertEqual(effect.object_type, self.effect.object_type)

    def test_attack_effect_json(self) -> None:
        data: dict = self.attack_effect.to_json()
        attack_effect: AttackEffect = AttackEffect().from_json(data)
        self.assertEqual(attack_effect.object_type, self.attack_effect.object_type)
        self.assertEqual(attack_effect.damage_points, self.attack_effect.damage_points)

    def test_heal_effect_json(self) -> None:
        data: dict = self.heal_effect.to_json()
        heal_effect: HealEffect = HealEffect().from_json(data)
        self.assertEqual(heal_effect.object_type, self.heal_effect.object_type)
        self.assertEqual(heal_effect.heal_points, self.heal_effect.heal_points)

    def test_buff_effect_json(self) -> None:
        data: dict = self.buff_effect.to_json()
        buff_effect: BuffEffect = BuffEffect().from_json(data)
        self.assertEqual(buff_effect.object_type, self.buff_effect.object_type)
        self.assertEqual(buff_effect.buff_amount, self.buff_effect.buff_amount)

    def test_debuff_effect_json(self) -> None:
        data: dict = self.debuff_effect.to_json()
        debuff_effect: DebuffEffect = DebuffEffect().from_json(data)
        self.assertEqual(debuff_effect.object_type, self.debuff_effect.object_type)
        self.assertEqual(debuff_effect.debuff_amount, self.debuff_effect.debuff_amount)
