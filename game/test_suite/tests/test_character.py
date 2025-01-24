import unittest

from game.commander_clash.character.character import *
from game.commander_clash.moves.effects import HealEffect
from game.common.enums import ClassType
from game.test_suite.utils import spell_check
from game.utils.vector import Vector


class TestCharacter(unittest.TestCase):
    def setUp(self) -> None:
        self.character: Character = Character('name', ClassType.TANK, country_type=CountryType.TURPIS)
        self.gen_attacker: GenericAttacker = GenericAttacker('Billy', ClassType.ATTACKER)
        self.gen_healer: GenericHealer = GenericHealer('Steve', ClassType.HEALER)
        self.gen_tank: GenericTank = GenericTank('Bertha', ClassType.TANK)
        self.leader: Leader = Leader('Phil', ClassType.TANK)
        self.special: Character = Character('Special', ClassType.TANK, 10, AttackStat(), DefenseStat(20),
                                            SpeedStat(10), Vector(0, 0))

        self.sync_leader: Leader = Leader('Phil', ClassType.TANK)
        self.sync_leader.is_dead = True
        self.sync_leader.took_action = True
        self.sync_leader.current_health = 5
        self.sync_leader.max_health = 5
        self.sync_leader.selected_move = Attack('Synced Attack')
        self.sync_leader.position = Vector(1, 1)
        self.sync_leader.attack = AttackStat(5)
        self.sync_leader.defense = DefenseStat(5)
        self.sync_leader.speed = SpeedStat(5)
        self.sync_leader.special_points = 5

        # set the selected move for two characters to test the json
        self.gen_tank.selected_move = Buff('Ultimate Buff')
        self.leader.selected_move = Attack('Ultimate Attack')

        self.num: int = 100
        self.neg_num: int = -1
        self.none: None = None

        self.moves = (Attack('Baja Blast', TargetType.ALL_OPPS, 0, None, 5),
                      Buff('Baja Slurp', TargetType.SELF, 1, HealEffect(heal_points=10), 1),
                      Debuff('Baja Dump', TargetType.ALL_OPPS, 2, None, -1))

        self.moveset: Moveset = Moveset(self.moves)

        self.gen_tank.moveset = self.moveset

    # Test that passing in valid inputs for all the constructor parameters is correct
    def test_initialization(self) -> None:
        self.gen_tank.health = self.num
        self.gen_tank.defense.base_value = self.num
        self.gen_tank.defense.value = self.num
        self.gen_tank.speed.base_value = self.num
        self.gen_tank.speed.value = self.num
        # test passive ability later
        self.gen_tank.guardian = self.gen_attacker
        self.gen_tank.moveset = self.moveset
        self.gen_tank.special_points = self.num
        self.gen_tank.position = Vector(0, 0)

        # ensure the values are stored properly
        self.assertEqual(self.gen_tank.health, self.num)
        self.assertEqual(self.gen_tank.defense.base_value, self.num)
        self.assertEqual(self.gen_tank.defense.value, self.num)
        self.assertEqual(self.gen_tank.speed.base_value, self.num)
        self.assertEqual(self.gen_tank.speed.value, self.num)
        self.assertEqual(self.gen_tank.guardian, self.gen_attacker)
        self.assertEqual(self.gen_tank.special_points, self.num)
        self.assertEqual(self.gen_tank.position, Vector(0, 0))

        # test that all the parameters are set properly with the constructor
        self.assertEqual(self.special.name, 'Special')
        self.assertEqual(self.special.class_type, ClassType.TANK)

        # health is 10 * HEALTH_MODIFIER from config
        self.assertEqual(self.special.current_health, 60)
        self.assertEqual(self.special.defense.base_value, 20)
        self.assertEqual(self.special.defense.value, 20)
        self.assertEqual(self.special.speed.base_value, 10)
        self.assertEqual(self.special.speed.value, 10)
        self.assertEqual(self.special.position, Vector(0, 0))

    # Test that passing in bad inputs (a string instead of an int, a None value where it's not needed, etc)
    def test_initialization_fail(self) -> None:
        with self.assertRaises(ValueError) as e:
            self.character.name = 123
        self.assertTrue(str(e.exception), f'{self.character.__class__.name}.name must be a string. It is a(n) int'
                                          f'and has the value 1')

        with self.assertRaises(ValueError) as e:
            self.character.class_type = 1
        self.assertTrue(str(e.exception), f'{self.character.__class__.name}.name must be a ClassType. It is '
                                          f'a(n) int and has the value 1')

        # check that a negative int fails for CURRENT health
        with self.assertRaises(ValueError) as e:
            self.gen_tank.current_health = self.neg_num
        self.assertTrue(spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.current_health must be a'
                                                      f' positive int.', True))

        # check that a None value fails for CURRENT health
        with self.assertRaises(ValueError) as e:
            self.gen_tank.current_health = self.none
        self.assertTrue(spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.current_health must be '
                                                      f'an int. It is a(n) {self.none.__class__.__name__} '
                                                      f'and has the value of {self.none}', True))

        # check that a negative int fails for MAX health
        with self.assertRaises(ValueError) as e:
            self.gen_tank.max_health = self.neg_num
        self.assertTrue(spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.max_health must be a'
                                                      f' positive int.', True))

        # check that a None value fails for MAX health
        with self.assertRaises(ValueError) as e:
            self.gen_tank.max_health = self.none
        self.assertTrue(spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.max_health must be '
                                                      f'an int. It is a(n) {self.none.__class__.__name__} '
                                                      f'and has the value of {self.none}', True))

        # check that a None value fails for attack
        with self.assertRaises(ValueError) as e:
            self.gen_tank.attack = self.none
        self.assertTrue(
            spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.attack must be an AttackStat. It '
                                          f'is a(n) {self.none.__class__.__name__} '
                                          f'and has the value of {self.none}', True))

        # check that a None value fails for defense
        with self.assertRaises(ValueError) as e:
            self.gen_tank.defense = self.none
        self.assertTrue(
            spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.defense must be a DefenseStat. It '
                                          f'is a(n) {self.none.__class__.__name__} '
                                          f'and has the value of {self.none}', True))

        # check that a None value fails for speed
        with self.assertRaises(ValueError) as e:
            self.gen_tank.speed = self.none
        self.assertTrue(
            spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.speed must be a SpeedStat. It '
                                          f'is a(n) {self.none.__class__.__name__} '
                                          f'and has the value of {self.none}', True))

        # check that a negative int fails for special_points
        with self.assertRaises(ValueError) as e:
            self.gen_tank.special_points = self.neg_num
        self.assertTrue(
            spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.special_points must be a positive '
                                          f'int.', True))

        # check that a None value fails for special_points
        with self.assertRaises(ValueError) as e:
            self.gen_tank.special_points = self.none
        self.assertTrue(
            spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.special_points must be an int. It '
                                          f'is a(n) {self.none.__class__.__name__} '
                                          f'and has the value of {self.none}', True))

        # check that the Character position has to be a Vector
        value: int = 10
        with self.assertRaises(ValueError) as e:
            self.gen_tank.position = value
        self.assertTrue(spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.position must be a Vector '
                                                      f'or None. It is a(n) {value.__class__.__name__} and has the '
                                                      f'value of {value}', False))

        # check that a None fails for a moveset
        with self.assertRaises(ValueError) as e:
            self.gen_tank.moveset = self.none
        self.assertTrue(spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.moveset must be a '
                                                      f'Moveset. It is a(n) {self.none.__class__.__name__} and has the '
                                                      f'value of {self.none}', True))

        # check that took_action has error handling
        with self.assertRaises(ValueError) as e:
            self.gen_tank.took_action = 1
        self.assertTrue(
            spell_check(str(e.exception), f'{self.gen_tank.__class__.__name__}.took_action must be a bool. It '
                                          f'is a(n) int and has the value of 1', True))

        # ensure passing None as the guarding works since there's currently a warning
        self.special.guardian = None
        self.assertEqual(self.special.guardian, None)

    def test_generics(self) -> None:
        self.assertTrue(isinstance(self.gen_tank, Generic))
        self.assertTrue(isinstance(self.gen_attacker, Generic))
        self.assertTrue(isinstance(self.gen_healer, Generic))

    def test_get_move_methods(self) -> None:
        self.assertEqual(self.gen_tank.get_nm(), self.moveset.get_nm())
        self.assertEqual(self.gen_tank.get_s1(), self.moveset.get_s1())
        self.assertEqual(self.gen_tank.get_s2(), self.moveset.get_s2())

    def test_get_opposing_country(self) -> None:
        # character is Turpis; gen_attacker is Uroda
        self.assertEqual(self.character.get_opposing_country(), CountryType.URODA)
        self.assertEqual(self.gen_attacker.get_opposing_country(), CountryType.TURPIS)

    def test_to_json_character(self) -> None:
        data: dict = self.character.to_json()
        char: Character = Character().from_json(data)
        self.assertEqual(char.name, self.character.name)
        self.assertEqual(char.object_type, self.character.object_type)
        self.assertEqual(char.class_type, self.character.class_type)
        self.assertEqual(char.current_health, self.character.current_health)
        self.assertEqual(char.max_health, self.character.max_health)
        self.assertEqual(char.attack, self.character.attack)
        self.assertEqual(char.defense.value, self.character.defense.value)
        self.assertEqual(char.speed.value, self.character.speed.value)
        self.assertEqual(char.rank_type, self.character.rank_type)
        self.assertEqual(char.special_points, self.character.special_points)
        self.assertEqual(char.position, None)
        self.assertTrue(char.moveset == self.character.moveset)
        self.assertEqual(char.took_action, self.character.took_action)
        self.assertEqual(char.country_type, self.character.country_type)
        self.assertEqual(char.is_dead, self.character.is_dead)
        self.assertTrue(char.selected_move is None and self.character.selected_move is None)

    def test_to_json_gen_atk(self) -> None:
        data: dict = self.gen_attacker.to_json()
        char: GenericAttacker = GenericAttacker().from_json(data)
        self.assertEqual(char.name, self.gen_attacker.name)
        self.assertEqual(char.object_type, self.gen_attacker.object_type)
        self.assertEqual(char.class_type, self.gen_attacker.class_type)
        self.assertEqual(char.current_health, self.gen_attacker.current_health)
        self.assertEqual(char.max_health, self.gen_attacker.max_health)
        self.assertEqual(char.attack, self.gen_attacker.attack)
        self.assertEqual(char.defense.value, self.gen_attacker.defense.value)
        self.assertEqual(char.speed.value, self.gen_attacker.speed.value)
        self.assertEqual(char.rank_type, self.gen_attacker.rank_type)
        self.assertEqual(char.special_points, self.gen_attacker.special_points)
        self.assertEqual(char.position, None)
        self.assertTrue(char.moveset == self.gen_attacker.moveset)
        self.assertEqual(char.took_action, self.gen_attacker.took_action)
        self.assertEqual(char.country_type, self.gen_attacker.country_type)
        self.assertEqual(char.is_dead, self.gen_attacker.is_dead)
        self.assertTrue(char.selected_move is None and self.gen_attacker.selected_move is None)

    def test_to_json_gen_heal(self) -> None:
        data: dict = self.gen_healer.to_json()
        char: GenericHealer = GenericHealer().from_json(data)
        self.assertEqual(char.name, self.gen_healer.name)
        self.assertEqual(char.object_type, self.gen_healer.object_type)
        self.assertEqual(char.class_type, self.gen_healer.class_type)
        self.assertEqual(char.current_health, self.gen_healer.current_health)
        self.assertEqual(char.max_health, self.gen_healer.max_health)
        self.assertEqual(char.attack, self.gen_healer.attack)
        self.assertEqual(char.defense.value, self.gen_healer.defense.value)
        self.assertEqual(char.speed.value, self.gen_healer.speed.value)
        self.assertEqual(char.rank_type, self.gen_healer.rank_type)
        self.assertEqual(char.special_points, self.gen_healer.special_points)
        self.assertEqual(char.position, None)
        self.assertTrue(char.moveset == self.gen_healer.moveset)
        self.assertEqual(char.took_action, self.gen_healer.took_action)
        self.assertEqual(char.country_type, self.gen_healer.country_type)
        self.assertEqual(char.is_dead, self.gen_healer.is_dead)
        self.assertTrue(char.selected_move is None and self.gen_healer.selected_move is None)

    def test_to_json_gen_tank(self) -> None:
        data: dict = self.gen_tank.to_json()
        char: GenericTank = GenericTank().from_json(data)
        self.assertEqual(char.name, self.gen_tank.name)
        self.assertEqual(char.object_type, self.gen_tank.object_type)
        self.assertEqual(char.class_type, self.gen_tank.class_type)
        self.assertEqual(char.current_health, self.gen_tank.current_health)
        self.assertEqual(char.max_health, self.gen_tank.max_health)
        self.assertEqual(char.attack, self.gen_tank.attack)
        self.assertEqual(char.defense.value, self.gen_tank.defense.value)
        self.assertEqual(char.speed.value, self.gen_tank.speed.value)
        self.assertEqual(char.rank_type, self.gen_tank.rank_type)
        self.assertEqual(char.special_points, self.gen_tank.special_points)
        self.assertEqual(char.position, None)
        self.assertEqual(char.took_action, self.gen_tank.took_action)
        self.assertEqual(char.country_type, self.gen_tank.country_type)
        self.assertEqual(char.is_dead, self.gen_tank.is_dead)
        self.assertTrue(char.moveset == self.gen_tank.moveset)
        self.assertTrue(char.selected_move.name == self.gen_tank.selected_move.name == 'Ultimate Buff')

    def test_to_json_leader(self) -> None:
        data: dict = self.leader.to_json()
        char: Leader = Leader().from_json(data)
        self.assertEqual(char.name, self.leader.name)
        self.assertEqual(char.object_type, self.leader.object_type)
        self.assertEqual(char.class_type, self.leader.class_type)
        self.assertEqual(char.current_health, self.leader.current_health)
        self.assertEqual(char.max_health, self.leader.max_health)
        self.assertEqual(char.attack, self.leader.attack)
        self.assertEqual(char.defense.value, self.leader.defense.value)
        self.assertEqual(char.speed.value, self.leader.speed.value)
        self.assertEqual(char.rank_type, self.leader.rank_type)
        self.assertEqual(char.special_points, self.leader.special_points)
        self.assertEqual(char.position, None)
        self.assertEqual(char.moveset, self.leader.moveset)
        self.assertEqual(char.took_action, self.leader.took_action)
        self.assertEqual(char.country_type, self.leader.country_type)
        self.assertEqual(char.is_dead, self.leader.is_dead)
        self.assertTrue(char.selected_move.name == self.leader.selected_move.name == 'Ultimate Attack')
