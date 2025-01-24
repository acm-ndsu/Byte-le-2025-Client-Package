import unittest

from game.commander_clash.moves.moves import *
from game.commander_clash.moves.moveset import Moveset


class TestMoveset(unittest.TestCase):
    def setUp(self):
        self.na: Attack = Attack('Normal Attack')
        self.na1: Attack = Attack('Normal Attack Extra')
        self.s1: Buff = Buff('Special 1')
        self.s2: Debuff = Debuff('Special 2')
        self.s3: Heal = Heal('Special 3')
        self.none: None = None
        self.moveset = Moveset((self.na, self.s1, self.s2))
        self.other_moveset = Moveset((self.na1, self.s1, self.s2))

    def test_get_nm(self) -> None:
        self.assertEqual(self.moveset.get_nm(), self.na)

    def test_get_s1(self) -> None:
        self.assertEqual(self.moveset.get_s1(), self.s1)

    def test_get_s2(self) -> None:
        self.assertEqual(self.moveset.get_s2(), self.s2)

    def test_equals_method(self) -> None:
        self.assertTrue(self.moveset == self.other_moveset)

    def test_equals_method_fails_not_given_moveset_object(self) -> None:
        self.assertFalse(self.moveset == 5)

    def test_equals_method_given_none_values(self) -> None:
        self.moveset = None
        self.assertTrue(self.moveset == self.none)

    def test_equals_method_with_mismatching_effects(self) -> None:
        self.moveset.get_nm().effect = DebuffEffect()
        self.other_moveset.get_nm().effect = BuffEffect()
        self.assertFalse(self.moveset == self.other_moveset)

    def test_json(self) -> None:
        data: dict = self.moveset.to_json()
        other_moveset: Moveset = Moveset().from_json(data)

        self.assertEqual(['NA', 'S1', 'S2'], list(self.moveset.moves.keys()))

        for move, other_move in zip(self.moveset.moves.values(), other_moveset.moves.values()):
            self.assertEqual(move.object_type, other_move.object_type)
            self.assertEqual(move.name, other_move.name)
            self.assertEqual(move.target_type, other_move.target_type)
            self.assertEqual(move.move_type, other_move.move_type)
            self.assertEqual(move.cost, other_move.cost)
            self.assertEqual(move.effect, other_move.effect)

