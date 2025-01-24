import unittest

from game.commander_clash.character.character import Character
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.controllers.swap_controller import SwapController
from game.utils.vector import Vector
from game.common.player import Player
from game.common.team_manager import TeamManager
from game.common.enums import ActionType, CountryType


class TestSwapController(unittest.TestCase):
    """
    `Test Swap Controller:`

        This class tests the Swap Controller for swapping up and down. It tests:
        - Swapping with other characters
        - Swapping with nothing
        - Not moving due to trying to leave the boundaries of the game

        The tests follow a format of:
        - Set the took_turn booleans of the characters to determine the active character
        - Call the swap controller on the active character, moving up or down
        - Check if the characters position/s changed or not
        - Check if the game_board has placed the character/s in the correct position or not
    """

    def setUp(self) -> None:
        self.swap_controller: SwapController = SwapController()
        self.team_manager: TeamManager = TeamManager([Character(name='Reginald', position=Vector(0, 0)),
                                                      Character(name='Count Leopold Von Liechtenstein III',
                                                                position=Vector(0, 1)),
                                                      Character(name='Bob', position=Vector(0, 2))])
        self.client: Player = Player(None, None, [], self.team_manager)
        self.locations: dict[Vector, list[GameObject]] = {Vector(0, 0): [self.client.team_manager.team[0]],
                                                          Vector(0, 1): [self.client.team_manager.team[1]],
                                                          Vector(0, 2): [self.client.team_manager.team[2]]}
        self.game_board: GameBoard = GameBoard(0, Vector(2, 3), self.locations,
                                               False, self.client.team_manager, TeamManager())
        self.game_board.generate_map()

    # tests for swap up
    def test_swap_up_character(self) -> None:
        # set the active pair index
        self.game_board.active_pair_index = 2

        self.client.team_manager.team[0].took_action = True
        self.client.team_manager.team[1].took_action = True
        self.client.team_manager.team[2].took_action = False

        self.swap_controller.handle_actions(ActionType.SWAP_UP, self.client, self.game_board)

        self.assertEqual(self.client.team_manager.team[2].position, Vector(0, 1))
        self.assertEqual(self.client.team_manager.team[1].position, Vector(0, 2))
        self.assertEqual(self.game_board.get_characters(CountryType.URODA)[Vector(0, 1)].name, 'Bob')
        self.assertEqual(self.game_board.get_characters(CountryType.URODA)[Vector(0, 2)].name,
                         'Count Leopold Von Liechtenstein III')

        # ensure the team manager references for all affected characters are synchronized
        self.assertEqual(self.team_manager.get_character('Bob').position, Vector(0, 1))
        self.assertEqual(self.team_manager.get_character(
            'Count Leopold Von Liechtenstein III').position, Vector(0, 2))

        # now ensure the ordered_teams references of the characters are synced
        self.assertEqual(self.game_board.get_char_from_ordered_teams('Bob').position, Vector(0, 1))
        self.assertEqual(self.game_board.get_char_from_ordered_teams('Count Leopold Von Liechtenstein III').position,
                         Vector(0, 2))

    def test_swap_up_none(self) -> None:
        # set the active pair index
        self.game_board.active_pair_index = 2

        self.game_board.remove_coordinate(self.client.team_manager.team.pop(1).position)
        self.client.team_manager.team[0].took_action = True
        self.client.team_manager.team[1].took_action = False

        self.swap_controller.handle_actions(ActionType.SWAP_UP, self.client, self.game_board)

        self.assertEqual(self.client.team_manager.team[1].position, Vector(0, 1))
        self.assertEqual(self.game_board.get_characters(CountryType.URODA)[Vector(0, 1)].name, 'Bob')
        with self.assertRaises(KeyError):
            self.game_board.get_characters(CountryType.URODA)[Vector(0, 2)].name

        # ensure the team manager and ordered_teams references didn't change
        self.assertEqual(self.team_manager.get_character('Bob').position, Vector(0, 1))
        self.assertEqual(self.game_board.get_char_from_ordered_teams('Bob').position, Vector(0, 1))

    def test_swap_up_fail(self) -> None:
        # set the active pair index
        self.game_board.active_pair_index = 0

        self.client.team_manager.team[0].took_action = False
        self.client.team_manager.team[1].took_action = True
        self.client.team_manager.team[2].took_action = True

        self.swap_controller.handle_actions(ActionType.SWAP_UP, self.client, self.game_board)

        self.assertEqual(self.client.team_manager.team[0].position, Vector(0, 0))
        self.assertEqual(self.game_board.get_characters(CountryType.URODA)[Vector(0, 0)].name, 'Reginald')

        # ensure the team manager and ordered_teams references didn't change
        self.assertEqual(self.team_manager.get_character('Reginald').position, Vector(0, 0))
        self.assertEqual(self.game_board.get_char_from_ordered_teams('Reginald').position, Vector(0, 0))

    # tests for swap down
    def test_swap_down_character(self) -> None:
        # set the active pair index
        self.game_board.active_pair_index = 1

        self.client.team_manager.team[0].took_action = True
        self.client.team_manager.team[1].took_action = False
        self.client.team_manager.team[2].took_action = True

        self.swap_controller.handle_actions(ActionType.SWAP_DOWN, self.client, self.game_board)

        self.assertEqual(self.client.team_manager.team[1].position, Vector(0, 2))
        self.assertEqual(self.client.team_manager.team[2].position, Vector(0, 1))
        self.assertEqual(self.game_board.get_characters(CountryType.URODA)[Vector(0, 1)].name, 'Bob')
        self.assertEqual(self.game_board.get_characters(CountryType.URODA)[Vector(0, 2)].name,
                         'Count Leopold Von Liechtenstein III')

        # ensure the team manager references for all affected characters are synchronized
        self.assertEqual(self.team_manager.get_character('Bob').position, Vector(0, 1))
        self.assertEqual(self.team_manager.get_character(
            'Count Leopold Von Liechtenstein III').position, Vector(0, 2))

        # now ensure the ordered_teams references of the characters are synced
        self.assertEqual(self.game_board.get_char_from_ordered_teams('Bob').position, Vector(0, 1))
        self.assertEqual(self.game_board.get_char_from_ordered_teams('Count Leopold Von Liechtenstein III').position,
                         Vector(0, 2))

    def test_swap_down_none(self) -> None:
        # set the active pair index
        self.game_board.active_pair_index = 0

        self.game_board.remove_coordinate(self.client.team_manager.team.pop(1).position)
        self.client.team_manager.team[0].took_action = False
        self.client.team_manager.team[1].took_action = True

        self.swap_controller.handle_actions(ActionType.SWAP_DOWN, self.client, self.game_board)

        self.assertEqual(self.client.team_manager.team[0].position, Vector(0, 1))
        self.assertEqual(self.game_board.get_characters(CountryType.URODA)[Vector(0, 1)].name, 'Reginald')
        with self.assertRaises(KeyError):
            self.game_board.get_characters(CountryType.URODA)[Vector(0, 0)].name

        # ensure the team manager references for all affected characters are synchronized
        self.assertEqual(self.team_manager.get_character('Reginald').position, Vector(0, 1))
        self.assertTrue(self.team_manager.get_character('Count Leopold Von Liechtenstein III') is None)

        # now ensure the ordered_teams references of the character is synced
        self.assertEqual(self.game_board.get_char_from_ordered_teams('Reginald').position, Vector(0, 1))

    def test_swap_down_fail(self) -> None:
        # set the active pair index
        self.game_board.active_pair_index = 2

        self.client.team_manager.team[0].took_action = True
        self.client.team_manager.team[1].took_action = True
        self.client.team_manager.team[2].took_action = False

        self.swap_controller.handle_actions(ActionType.SWAP_DOWN, self.client, self.game_board)

        self.assertEqual(self.client.team_manager.team[2].position, Vector(0, 2))
        self.assertEqual(self.game_board.get_characters(CountryType.URODA)[Vector(0, 2)].name, 'Bob')

        # ensure the team manager and ordered_teams references didn't change
        self.assertEqual(self.team_manager.get_character('Bob').position, Vector(0, 2))
        self.assertEqual(self.game_board.get_char_from_ordered_teams('Bob').position, Vector(0, 2))
