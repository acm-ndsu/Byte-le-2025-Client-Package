import unittest

from game.commander_clash.character.character import *
from game.common.action import *
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.team_manager import TeamManager
from game.controllers.swap_controller import SwapController


class TestTeamManager(unittest.TestCase):
    """
    Test for Team Manager class
    """

    def setUp(self):
        self.leader: Leader = Leader('Agles', ClassType.TANK, 100, AttackStat(), DefenseStat(10),
                                     SpeedStat(5))
        self.attacker: GenericAttacker = GenericAttacker('Grog', health=50, attack=AttackStat(), defense=DefenseStat(5),
                                                         speed=SpeedStat(15))
        self.healer: GenericHealer = GenericHealer('Eden', health=60, attack=AttackStat(), defense=DefenseStat(15),
                                                   speed=SpeedStat(10))
        self.team_manager: TeamManager = TeamManager()
        self.team_manager2: TeamManager = TeamManager([self.leader, self.attacker, self.healer],
                                                      CountryType.URODA)
        self.team_manager2.speed_sort()

        # set the object types
        self.leader.object_type = ObjectType.IRWIN
        self.attacker.object_type = ObjectType.URODA_GENERIC_ATTACKER
        self.healer.object_type = ObjectType.URODA_GENERIC_HEALER

        self.swap_controller: SwapController = SwapController()

        self.client: Player = Player(None, None, [], self.team_manager2)

        self.locations: dict[Vector, list[GameObject]] = {Vector(0, 0): [self.client.team_manager.team[0]],
                                                          Vector(0, 1): [self.client.team_manager.team[1]],
                                                          Vector(0, 2): [self.client.team_manager.team[2]]}
        self.game_board: GameBoard = GameBoard(0, Vector(2, 3), self.locations,
                                               False, self.client.team_manager, TeamManager())
        self.game_board.generate_map()

    def test_init_default(self) -> None:
        self.assertEqual(self.team_manager.object_type, ObjectType.TEAMMANAGER)
        self.assertEqual(self.team_manager.team, TeamManager().team)
        self.assertEqual(self.team_manager.score, 0)

    def test_init_unique(self) -> None:
        self.assertEqual(self.team_manager2.object_type, ObjectType.TEAMMANAGER)

        # order is like this since speed sort was used in the init method
        self.assertEqual(self.team_manager2.team, [self.attacker, self.healer, self.leader])
        self.assertEqual(self.team_manager2.score, 0)

    def test_setters(self) -> None:
        with self.assertRaises(ValueError) as e:
            self.team_manager.object_type = 2
        self.assertEqual(str(e.exception), f'{self.team_manager.__class__.__name__}.object_type must be an '
                                           f'ObjectType. It is a(n) {int.__name__} '
                                           f'and has the value of 2.')
        with self.assertRaises(ValueError) as e:
            self.team_manager.team = 1
        self.assertEqual(str(e.exception), f'{self.team_manager.__class__.__name__}.team must be a list[Character]. '
                                           f'It is a(n) {int.__name__} '
                                           f'and has the value of 1.')
        with self.assertRaises(ValueError) as e:
            self.team_manager.team = [self.leader, self.attacker, 3]
        self.assertEqual(str(e.exception), f'{self.team_manager.__class__.__name__}.team must be a list[Character]. '
                                           f'It contains a(n) {int.__name__} with the value 3.')
        with self.assertRaises(ValueError) as e:
            self.team_manager.team = [self.leader, self.attacker, self.healer, self.leader]
        self.assertEqual(str(e.exception), f'{self.team_manager.__class__.__name__}.team must be a list[Character] '
                                           f'with a length of three or less. It has a length of 4.')
        with self.assertRaises(ValueError) as e:
            self.team_manager.score = 'hi'
        self.assertEqual(str(e.exception), f'{self.team_manager.__class__.__name__}.score must be an int. '
                                           f'It is a(n) {str.__name__} and has the value of hi.')

    def test_speed_sort(self) -> None:
        self.team_manager2.speed_sort()
        self.assertEqual(self.team_manager2.team, [self.attacker, self.healer, self.leader])

    def test_filter_by_type(self) -> None:
        self.assertEqual(self.team_manager.filter_by_type(ClassType.ATTACKER), TeamManager().team)
        self.assertEqual(self.team_manager.filter_by_type(ClassType.TANK), [])
        self.assertEqual(self.team_manager2.filter_by_type(ClassType.TANK), [self.leader])
        self.assertEqual(self.team_manager2.filter_by_type(ClassType.ATTACKER), [self.attacker])
        self.assertEqual(self.team_manager2.filter_by_type(ClassType.HEALER), [self.healer])

    # test ensuring the correct character is returned to represent the team manager's active character for a turn
    def test_get_active_character(self) -> None:
        # set the active pair index for the sake of testing
        self.game_board.active_pair_index = 0

        self.assertEqual(self.team_manager2.get_active_character(self.game_board.ordered_teams,
                                                                 self.game_board.active_pair_index), self.attacker)
        self.game_board.active_pair_index += 1

        self.assertEqual(self.team_manager2.get_active_character(self.game_board.ordered_teams,
                                                                 self.game_board.active_pair_index), self.healer)
        self.game_board.active_pair_index += 1

        self.assertEqual(self.team_manager2.get_active_character(self.game_board.ordered_teams,
                                                                 self.game_board.active_pair_index), self.leader)

    def test_json_default(self) -> None:
        data: dict = self.team_manager.to_json()
        team_manager: TeamManager = TeamManager().from_json(data)
        self.assertEqual(team_manager.object_type, self.team_manager.object_type)
        self.assertEqual(team_manager.country_type, self.team_manager.country_type)
        self.assertEqual(team_manager.score, self.team_manager.score)

        [self.assertTrue(team_manager.team[x] == self.team_manager.team[x]) for
         x in range(len(self.team_manager.team))]

    def test_json_unique(self) -> None:
        data: dict = self.team_manager2.to_json()
        team_manager2: TeamManager = TeamManager().from_json(data)
        self.assertEqual(team_manager2.object_type, self.team_manager2.object_type)
        self.assertEqual(team_manager2.country_type, self.team_manager2.country_type)
        self.assertEqual(team_manager2.score, self.team_manager2.score)

        [self.assertTrue(team_manager2.team[x] == self.team_manager2.team[x]) for
         x in range(len(self.team_manager2.team))]
