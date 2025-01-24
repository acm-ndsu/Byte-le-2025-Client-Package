import unittest

from game.commander_clash.character.stats import *
from game.config import STAT_MINIMUM, ATTACK_MAXIMUM, DEFENSE_MAXIMUM, SPEED_MAXIMUM


class TestStat(unittest.TestCase):
    def setUp(self):
        self.stat = Stat(5)
        self.other_stat = Stat(1)
        self.attack_stat = AttackStat(5)
        self.defense_stat = DefenseStat(5)
        self.speed_stat = SpeedStat(5)
        self.string: str = 'hi'

    def test_overridden_hash_methods(self) -> None:
        self.assertNotEqual(self.stat, self.other_stat)
        self.assertGreater(self.stat, self.other_stat)
        self.assertLess(self.other_stat, self.stat)

        self.other_stat.value = 5
        self.other_stat.base_value = 5

        self.assertGreaterEqual(self.stat, self.other_stat)
        self.assertLessEqual(self.stat, self.other_stat)
        self.assertTrue(self.stat == self.other_stat)

        # test failing cases for the hashable methods
        self.assertFalse(self.stat == self.string)
        self.assertFalse(self.stat < self.string)
        self.assertFalse(self.stat > self.string)
        self.assertFalse(self.stat <= self.string)
        self.assertFalse(self.stat >= self.string)
        self.assertFalse(self.stat != self.string)

    def test_properties(self) -> None:
        self.assertEqual(self.stat.base_value, 5)
        self.assertEqual(self.stat.value, 5)

        # testing base_value
        with self.assertRaises(ValueError) as e:
            self.stat.base_value = self.string
        self.assertEqual(str(e.exception),
                         f'{self.stat.__class__.__name__}.base_value must be an int or float. It is a(n) '
                         f'{self.string.__class__.__name__} and has a value of {self.string}')

        with self.assertRaises(ValueError) as e:
            self.stat.base_value = -1
        self.assertEqual(str(e.exception), f'{self.stat.__class__.__name__}.base_value must be greater than 0')

        # testing value
        with self.assertRaises(ValueError) as e:
            self.stat.value = self.string
        self.assertEqual(str(e.exception), f'{self.stat.__class__.__name__}.value must be an int or float. It is a(n) '
                                           f'{self.string.__class__.__name__} and has a value of {self.string}')

        with self.assertRaises(ValueError) as e:
            self.stat.value = -1
        self.assertEqual(str(e.exception), f'{self.stat.__class__.__name__}.value must be a positive int or float')

    def test_is_maxed(self) -> None:
        self.assertFalse(self.attack_stat.is_maxed())
        self.attack_stat.value = ATTACK_MAXIMUM
        self.assertTrue(self.attack_stat.is_maxed())

        self.assertFalse(self.defense_stat.is_maxed())
        self.defense_stat.value = DEFENSE_MAXIMUM
        self.assertTrue(self.defense_stat.is_maxed())

        self.assertFalse(self.speed_stat.is_maxed())
        self.speed_stat.value = SPEED_MAXIMUM
        self.assertTrue(self.speed_stat.is_maxed())

    def test_is_minimized(self) -> None:
        self.assertFalse(self.attack_stat.is_minimized())
        self.attack_stat.value = STAT_MINIMUM
        self.assertTrue(self.attack_stat.is_minimized())

        self.assertFalse(self.defense_stat.is_minimized())
        self.defense_stat.value = STAT_MINIMUM
        self.assertTrue(self.defense_stat.is_minimized())

        self.assertFalse(self.speed_stat.is_minimized())
        self.speed_stat.value = STAT_MINIMUM
        self.assertTrue(self.speed_stat.is_minimized())

    def test_buffing(self) -> None:
        self.attack_stat.apply_modification(10)
        self.assertEqual(self.attack_stat.value, 15)

    def test_buffing_over_maximum(self) -> None:
        self.attack_stat.apply_modification(1000)
        self.assertEqual(self.attack_stat.value, ATTACK_MAXIMUM)

        self.defense_stat.apply_modification(1000)
        self.assertEqual(self.defense_stat.value, DEFENSE_MAXIMUM)

        self.speed_stat.apply_modification(1000)
        self.assertEqual(self.speed_stat.value, SPEED_MAXIMUM)

    def test_debuffing(self) -> None:
        self.attack_stat.apply_modification(-2)
        self.assertEqual(self.attack_stat.value, 3)

    def test_debuffing_under_minimum(self) -> None:
        self.attack_stat.apply_modification(-1000)
        self.assertEqual(self.attack_stat.value, 1)

    def test_stats_equal(self) -> None:
        # even if it's a new reference, a stat should be equal if they're the same class
        self.assertTrue(self.attack_stat == AttackStat(5))
        self.assertTrue(self.defense_stat == DefenseStat(5))
        self.assertTrue(self.speed_stat == SpeedStat(5))

    def test_stats_not_equal(self) -> None:
        # different values should mean the stats are not equal
        self.assertFalse(self.attack_stat == AttackStat(10))
        self.assertFalse(self.defense_stat == DefenseStat(10))
        self.assertFalse(self.speed_stat == SpeedStat(10))

        # test equalling two different stats
        self.assertTrue(self.attack_stat == DefenseStat(5))
        self.assertTrue(self.attack_stat == SpeedStat(5))

        self.assertTrue(self.defense_stat == AttackStat(5))
        self.assertTrue(self.defense_stat == SpeedStat(5))

        self.assertTrue(self.speed_stat == AttackStat(5))
        self.assertTrue(self.speed_stat == DefenseStat(5))

    def test_json(self) -> None:
        data: dict = self.stat.to_json()
        stat: Stat = Stat().from_json(data)
        self.assertEqual(stat.object_type, self.stat.object_type)
        self.assertEqual(stat.base_value, self.stat.base_value)
        self.assertEqual(stat.value, self.stat.value)

        data = self.attack_stat.to_json()
        attack_stat: AttackStat = AttackStat().from_json(data)
        self.assertEqual(attack_stat.object_type, self.attack_stat.object_type)
        self.assertEqual(attack_stat.base_value, self.attack_stat.base_value)
        self.assertEqual(attack_stat.value, self.attack_stat.value)

        data = self.defense_stat.to_json()
        defense_stat: DefenseStat = DefenseStat().from_json(data)
        self.assertEqual(defense_stat.object_type, self.defense_stat.object_type)
        self.assertEqual(defense_stat.base_value, self.defense_stat.base_value)
        self.assertEqual(defense_stat.value, self.defense_stat.value)

        data = self.speed_stat.to_json()
        speed_stat: SpeedStat = SpeedStat().from_json(data)
        self.assertEqual(speed_stat.object_type, self.speed_stat.object_type)
        self.assertEqual(speed_stat.base_value, self.speed_stat.base_value)
        self.assertEqual(speed_stat.value, self.speed_stat.value)
