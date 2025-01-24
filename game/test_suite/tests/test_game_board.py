import unittest

from game.commander_clash.character.character import *
from game.common.enums import ObjectType, CountryType
from game.common.map.wall import Wall
from game.common.team_manager import TeamManager
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.test_suite.utils import spell_check


class TestGameBoard(unittest.TestCase):
    """
    `Test Gameboard Notes:`

        This class tests the different methods in the Gameboard class. This file is worthwhile to look at to understand
        the GameBoard class better if there is still confusion on it.

        *This class tests the Gameboard specifically when the map is generated.*
    """

    def setUp(self) -> None:
        self.wall: Wall = Wall()
        self.leader: Leader = Leader(position=Vector(1, 2), country_type=CountryType.TURPIS)
        self.attacker: GenericAttacker = GenericAttacker(position=Vector(1, 3))

        # self.avatar: TeamManager = TeamManager()
        self.locations: dict[Vector, list[GameObject]] = {
            Vector(1, 1): [self.wall],
            Vector(1, 2): [self.leader],
            Vector(1, 3): [self.attacker],
        }

        self.ga1: GenericAttacker = GenericAttacker(name='GA1', speed=SpeedStat(6), country_type=CountryType.URODA)
        self.gh1: GenericHealer = GenericHealer(name='GH1', speed=SpeedStat(3), country_type=CountryType.URODA)
        self.gt1: GenericTank = GenericTank(name='GT1', speed=SpeedStat(2), country_type=CountryType.URODA)

        self.ga2: GenericAttacker = GenericAttacker(name='GA2', speed=SpeedStat(5), country_type=CountryType.TURPIS)
        self.gh2: GenericHealer = GenericHealer(name='GH2', speed=SpeedStat(4), country_type=CountryType.TURPIS)
        self.gt2: GenericTank = GenericTank(name='GT2', speed=SpeedStat(1), country_type=CountryType.TURPIS)

        # set object types
        self.ga1.object_type = ObjectType.URODA_GENERIC_ATTACKER
        self.gh1.object_type = ObjectType.URODA_GENERIC_HEALER
        self.gt1.object_type = ObjectType.URODA_GENERIC_TANK

        self.ga2.object_type = ObjectType.URODA_GENERIC_ATTACKER
        self.gh2.object_type = ObjectType.URODA_GENERIC_HEALER
        self.gt2.object_type = ObjectType.URODA_GENERIC_TANK

        self.leader.object_type = ObjectType.ANAHITA
        self.attacker.object_type = ObjectType.URODA_GENERIC_ATTACKER

        self.uroda_team: list[Character] = [self.ga1, self.gh1, self.gt1]
        self.turpis_team: list[Character] = [self.ga2, self.gh2, self.gt2]

        self.uroda_manager: TeamManager = TeamManager(country_type=CountryType.URODA, team=self.uroda_team)
        self.turpis_manager: TeamManager = TeamManager(country_type=CountryType.TURPIS, team=self.turpis_team)

        self.game_board: GameBoard = GameBoard(1, Vector(3, 3), self.locations, False,
                                               uroda_team_manager=self.uroda_manager,
                                               turpis_team_manager=self.turpis_manager)

        self.game_board.recently_died = [self.ga1]

        self.game_board.generate_map()

    # test that seed cannot be set after generate_map
    def test_seed_fail(self) -> None:
        with self.assertRaises(RuntimeError) as e:
            self.game_board.seed = 20
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that map_size cannot be set after generate_map
    def test_map_size_fail(self) -> None:
        with self.assertRaises(RuntimeError) as e:
            self.game_board.map_size = Vector(1, 1)
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that locations cannot be set after generate_map
    def test_locations_fail(self) -> None:
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = self.locations
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that locations raises RuntimeError even with incorrect data type
    def test_locations_incorrect_fail(self) -> None:
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = Vector(1, 1)
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that walled cannot be set after generate_map
    def test_walled_fail(self) -> None:
        with self.assertRaises(RuntimeError) as e:
            self.game_board.walled = False
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that get_objects works correctly with walls
    def test_get_objects_wall(self) -> None:
        walls: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.WALL)
        self.assertTrue(all(map(lambda wall: isinstance(wall[1][0], Wall), walls)))
        self.assertEqual(len(walls), 1)

    def test_get_characters(self) -> None:
        characters: dict[Vector, Character] = self.game_board.get_characters()
        self.assertTrue(characters[Vector(1, 2)] == self.leader)
        self.assertTrue(characters[Vector(1, 3)] == self.attacker)
        self.assertEqual(len(characters), 2)

    def test_get_characters_by_country(self) -> None:
        characters: dict[Vector, Character] = self.game_board.get_characters(CountryType.TURPIS)
        self.assertEqual(characters[Vector(1, 2)], self.leader)
        self.assertEqual(len(characters), 1)

    # uroda has 3 characters, turpis has 3
    def test_order_characters_3x3(self) -> None:
        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2), (self.gh1, self.gh2),
                                                         (self.gt1, self.gt2)])

    # uroda has 3 characters, turpis has 2
    def test_order_characters_3x2(self) -> None:
        self.turpis_manager.team = self.turpis_manager.team[:2]

        # generate the game map again so the new turpis team is reflected
        self.game_board.generate_map()

        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2), (self.gh1, self.gh2),
                                                         (self.gt1, None)])

    # uroda has 3 characters, turpis has 1
    def test_order_character_3x1(self) -> None:
        self.turpis_manager.team = self.turpis_team[:1]

        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2), (self.gh1, None),
                                                         (self.gt1, None)])

    # uroda has 2 characters, turpis has 3
    def test_order_character_2x3(self) -> None:
        self.uroda_manager.team = self.uroda_team[:2]

        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2), (self.gh1, self.gh2),
                                                         (None, self.gt2)])

    # uroda has 2 characters, turpis has 3
    def test_order_character_1x3(self) -> None:
        self.uroda_manager.team = self.uroda_team[:1]

        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2), (None, self.gh2),
                                                         (None, self.gt2)])

    # uroda has 2 characters, turpis has 2
    def test_order_character_2x2(self) -> None:
        self.uroda_manager.team = self.uroda_team[:2]
        self.turpis_manager.team = self.turpis_team[:2]

        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2), (self.gh1, self.gh2)])

    # uroda has 2 characters, turpis has 1
    def test_order_character_2x1(self):
        self.uroda_manager.team = self.uroda_team[:2]
        self.turpis_manager.team = self.turpis_team[:1]

        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2), (self.gh1, None)])

    # uroda has 1 characters, turpis has 2
    def test_order_character_1x2(self) -> None:
        self.uroda_manager.team = self.uroda_team[:1]
        self.turpis_manager.team = self.turpis_team[:2]

        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2), (None, self.gh2)])

    # uroda has 1 characters, turpis has 1
    def test_order_character_1x1(self) -> None:
        self.uroda_manager.team = self.uroda_team[:1]
        self.turpis_manager.team = self.turpis_team[:1]

        self.game_board.order_teams(self.uroda_manager, self.turpis_manager)
        self.assertEqual(self.game_board.ordered_teams, [(self.ga1, self.ga2)])

    def test_get_ordered_teams_as_list(self) -> None:
        self.assertEqual(self.game_board.get_ordered_teams_as_list(),
                         [self.ga1, self.ga2, self.gh2, self.gh1, self.gt1, self.gt2])

    def test_get_char_from_ordered_teams(self) -> None:
        char: Character | None = self.game_board.get_char_from_ordered_teams(self.ga1.name)
        self.assertEqual(char.name, self.ga1.name)

        char: Character | None = self.game_board.get_char_from_ordered_teams(self.ga2.name)
        self.assertEqual(char.name, self.ga2.name)

        char: Character | None = self.game_board.get_char_from_ordered_teams(self.gh1.name)
        self.assertEqual(char.name, self.gh1.name)

        char: Character | None = self.game_board.get_char_from_ordered_teams(self.gh2.name)
        self.assertEqual(char.name, self.gh2.name)

        char: Character | None = self.game_board.get_char_from_ordered_teams(self.gt1.name)
        self.assertEqual(char.name, self.gt1.name)

        char: Character | None = self.game_board.get_char_from_ordered_teams(self.gt2.name)
        self.assertEqual(char.name, self.gt2.name)

        char = self.game_board.get_char_from_ordered_teams('Bob')
        self.assertTrue(char is None)

    def test_is_valid_coords(self) -> None:
        # test that the 9 coordinates are valid game board coordinates
        self.assertTrue(self.game_board.is_valid_coords(Vector(0, 0)))
        self.assertTrue(self.game_board.is_valid_coords(Vector(0, 1)))
        self.assertTrue(self.game_board.is_valid_coords(Vector(0, 2)))
        self.assertTrue(self.game_board.is_valid_coords(Vector(1, 0)))
        self.assertTrue(self.game_board.is_valid_coords(Vector(1, 1)))
        self.assertTrue(self.game_board.is_valid_coords(Vector(1, 2)))
        self.assertTrue(self.game_board.is_valid_coords(Vector(2, 0)))
        self.assertTrue(self.game_board.is_valid_coords(Vector(2, 1)))
        self.assertTrue(self.game_board.is_valid_coords(Vector(2, 2)))

    def test_is_valid_coords_fail(self) -> None:
        # test that the following coordinates are invalid for the game board
        self.assertFalse(self.game_board.is_valid_coords(Vector(-1, -1)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(-1, -2)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(-1, -3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(-1, 3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(-1, 4)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(-1, 5)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(0, -1)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(0, -2)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(0, -3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(0, 3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(0, 4)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(0, 5)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(1, -1)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(1, -2)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(1, -3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(1, 3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(1, 4)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(1, 5)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(2, -1)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(2, -2)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(2, -3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(2, 3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(2, 4)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(2, 5)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(3, -1)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(3, -2)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(3, -3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(3, 3)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(3, 4)))
        self.assertFalse(self.game_board.is_valid_coords(Vector(3, 5)))

    # test json method
    def test_game_board_json(self):
        data: dict = self.game_board.to_json()
        temp: GameBoard = GameBoard().from_json(data)

        self.assertEqual(self.game_board.seed, temp.seed)
        self.assertEqual(self.game_board.map_size, temp.map_size)
        self.assertEqual(self.game_board.walled, temp.walled)
        self.assertEqual(self.game_board.event_active, temp.event_active)

        self.assertEqual(self.game_board.game_map.keys(), temp.game_map.keys())
        self.assertTrue(self.game_board.game_map.values(), temp.game_map.values())

        # check that the ordered_teams property was stored properly
        self.assertEqual(len(self.game_board.ordered_teams), len(temp.ordered_teams))
        self.assertTrue(all([isinstance(pair, tuple) for pair in temp.ordered_teams]))

        # now check that every pair is in the same order as when the gameboard was instantiated
        # remember that it's a list of tuples (first indexing is the list, second indexing is the tuple)
        self.assertTrue(self.game_board.ordered_teams[0][0] == temp.ordered_teams[0][0])
        self.assertTrue(self.game_board.ordered_teams[0][1] == temp.ordered_teams[0][1])

        self.assertTrue(self.game_board.ordered_teams[1][0] == temp.ordered_teams[1][0])
        self.assertTrue(self.game_board.ordered_teams[1][1] == temp.ordered_teams[1][1])

        self.assertTrue(self.game_board.ordered_teams[2][0] == temp.ordered_teams[2][0])
        self.assertTrue(self.game_board.ordered_teams[2][1] == temp.ordered_teams[2][1])

        # test the recently_died list
        self.assertTrue(self.game_board.recently_died[0] == self.ga1)
        self.assertEqual(len(self.game_board.recently_died), 1)
