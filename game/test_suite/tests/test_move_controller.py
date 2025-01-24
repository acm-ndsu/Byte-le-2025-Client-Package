import unittest
from unittest.mock import Mock

from game.commander_clash.generation.character_generation import *
from game.commander_clash.moves import move_logic
from game.commander_clash.moves.moves import *
from game.common.enums import CountryType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.team_manager import TeamManager
from game.controllers.move_controller import MoveController
from game.utils.vector import Vector


class TestMoveController(unittest.TestCase):
    """
    This is the test file for both the MoveController and the move_logic.py file since they work in tandem.
    """

    def setUp(self):
        self.move_controller: MoveController = MoveController()

        self.uroda_attacker: GenericAttacker = generate_generic_attacker('Uroda Attacker')
        self.uroda_attacker.selected_move = self.uroda_attacker.get_nm()
        self.uroda_attacker.country_type = CountryType.URODA

        self.uroda_healer: GenericHealer = generate_generic_healer('Uroda Healer')
        self.uroda_healer.selected_move = self.uroda_healer.get_nm()
        self.uroda_healer.country_type = CountryType.URODA

        self.uroda_tank: GenericTank = generate_generic_tank('Uroda Tank')
        self.uroda_tank.selected_move = self.uroda_tank.get_nm()
        self.uroda_tank.country_type = CountryType.URODA

        self.turpis_attacker: GenericAttacker = generate_generic_attacker('Turpis Attacker')
        self.turpis_attacker.selected_move = self.turpis_attacker.get_nm()
        self.turpis_attacker.country_type = CountryType.TURPIS

        self.turpis_tank: GenericTank = generate_generic_tank('Turpis Tank')
        self.turpis_tank.selected_move = self.turpis_tank.get_nm()
        self.turpis_tank.country_type = CountryType.TURPIS

        self.turpis_tank2: GenericTank = generate_generic_tank('Turpis Tank 2')
        self.turpis_tank2.selected_move = self.turpis_tank2.get_nm()
        self.turpis_tank2.country_type = CountryType.TURPIS

        # Uroda on the left, Turpis on the right;
        # Left side from top to bottom: Urodan attack, healer, tank
        # Right side from top to bottom: Turpisian attack, tank, tank2
        self.locations: dict[Vector, list[GameObject]] = {Vector(0, 0): [self.uroda_attacker],
                                                          Vector(0, 1): [self.uroda_healer],
                                                          Vector(0, 2): [self.uroda_tank],
                                                          Vector(1, 0): [self.turpis_attacker],
                                                          Vector(1, 1): [self.turpis_tank],
                                                          Vector(1, 2): [self.turpis_tank2]}

        # create a Player object with a TeamManager
        self.uroda_team_manager: TeamManager = TeamManager([self.uroda_attacker, self.uroda_healer, self.uroda_tank],
                                                           CountryType.URODA)
        self.turpis_team_manager: TeamManager = TeamManager(
            [self.turpis_attacker, self.turpis_tank, self.turpis_tank2],
            CountryType.TURPIS)

        self.uroda_client: Player = Player(team_manager=self.uroda_team_manager)
        self.turpis_client: Player = Player(team_manager=self.turpis_team_manager)
        self.clients: list[Player] = [self.uroda_client, self.turpis_client]

        self.gameboard: GameBoard = GameBoard(locations=self.locations, map_size=Vector(2, 3),
                                              uroda_team_manager=self.uroda_team_manager,
                                              turpis_team_manager=self.turpis_team_manager)

        self.gameboard.generate_map()

        # instantiate another gameboard and teams for ease of testing--------------------------------------------------

        self.attack_effect: AttackEffect = AttackEffect(TargetType.SELF, 10)
        self.heal_effect: HealEffect = HealEffect(TargetType.ADJACENT_ALLIES, 10)
        self.buff_effect: BuffEffect = BuffEffect(TargetType.ALL_OPPS, 1, ObjectType.SPEED_STAT)
        self.debuff_effect: DebuffEffect = DebuffEffect(TargetType.ENTIRE_TEAM, -1, ObjectType.SPEED_STAT)

        self.attacker_moveset: Moveset = Moveset(
            (Attack('Baja Blast', TargetType.SINGLE_OPP, 0, HealEffect(TargetType.ENTIRE_TEAM, 10), 5),
             Buff('Baja Slurp', TargetType.SELF, 2, HealEffect(heal_points=10), 1),
             Debuff('Baja Dump', TargetType.ALL_OPPS, 3, None, -1,
                    ObjectType.SPEED_STAT)))

        self.healer_moveset: Moveset = Moveset(
            (Heal('Water Halo', TargetType.ADJACENT_ALLIES, 0, self.attack_effect, 15),
             Attack('Inferno', TargetType.ALL_OPPS, 0, self.debuff_effect, 15),
             Debuff('Potion of Weakness', TargetType.SINGLE_OPP, 0, self.buff_effect, -1,
                    stat_to_affect=ObjectType.DEFENSE_STAT)))

        self.tank_moveset: Moveset = Moveset((Buff('Baja Barrier', TargetType.SELF, 0, None, 10),
                                              Attack('Break Bone', TargetType.SINGLE_OPP, 0, None, 15),
                                              Heal('Healing Potion', TargetType.ADJACENT_ALLIES, 0, None, 15)))

        # create uroda team
        self.other_uroda_attacker: GenericAttacker = GenericAttacker(health=20, attack=AttackStat(15),
                                                                     defense=DefenseStat(5),
                                                                     speed=SpeedStat(15), position=Vector(0, 0),
                                                                     country_type=CountryType.URODA,
                                                                     moveset=self.attacker_moveset,
                                                                     name='Other Uroda Attacker')
        self.other_uroda_attacker.special_points = 4

        self.other_uroda_healer: GenericHealer = GenericHealer(health=20, attack=AttackStat(5), defense=DefenseStat(5),
                                                               speed=SpeedStat(10), position=Vector(0, 1),
                                                               country_type=CountryType.URODA,
                                                               moveset=self.healer_moveset,
                                                               name='Other Uroda Healer')
        self.other_uroda_healer.selected_move = self.other_uroda_healer.get_nm()

        self.other_uroda_tank: GenericTank = GenericTank(health=20, attack=AttackStat(10), defense=DefenseStat(10),
                                                         speed=SpeedStat(5), position=Vector(0, 2),
                                                         country_type=CountryType.URODA, moveset=self.tank_moveset,
                                                         name='Other Uroda Tank')

        # create turpis team
        self.other_turpis_attacker: GenericAttacker = GenericAttacker(health=20, attack=AttackStat(15),
                                                                      defense=DefenseStat(5),
                                                                      speed=SpeedStat(15), position=Vector(1, 1),
                                                                      country_type=CountryType.TURPIS,
                                                                      moveset=self.attacker_moveset,
                                                                      name='Other Turpis Attacker')
        self.other_turpis_tank: GenericTank = GenericTank(health=20, attack=AttackStat(10), defense=DefenseStat(10),
                                                          speed=SpeedStat(5), position=Vector(1, 0),
                                                          country_type=CountryType.TURPIS, moveset=self.tank_moveset,
                                                          name='Other Turpis Tank')
        self.other_turpis_healer: GenericHealer = GenericHealer(health=20, attack=AttackStat(5), defense=DefenseStat(5),
                                                                speed=SpeedStat(10), position=Vector(1, 2),
                                                                country_type=CountryType.TURPIS,
                                                                moveset=self.healer_moveset,
                                                                name='Other Turpis Healer')

        # Uroda on the left, Turpis on the right;
        # Left side from top to bottom: Urodan healer, attacker, tank
        # Right side from top to bottom: Turpisian attack, tank, healer
        self.other_locations: dict[Vector, list[GameObject]] = {Vector(0, 0): [self.other_uroda_attacker],
                                                                Vector(0, 1): [self.other_uroda_healer],
                                                                Vector(0, 2): [self.other_uroda_tank],
                                                                Vector(1, 0): [self.other_turpis_tank],
                                                                Vector(1, 1): [self.other_turpis_attacker],
                                                                Vector(1, 2): [self.other_turpis_healer]}

        # create a Player object with a TeamManager
        self.other_uroda_team_manager: TeamManager = TeamManager(
            [self.other_uroda_attacker, self.other_uroda_healer, self.other_uroda_tank],
            CountryType.URODA)
        self.other_turpis_team_manager: TeamManager = TeamManager(
            [self.other_turpis_attacker, self.other_turpis_healer, self.other_turpis_tank],
            CountryType.TURPIS)

        self.other_uroda_client: Player = Player(team_manager=self.other_uroda_team_manager)
        self.other_turpis_client: Player = Player(team_manager=self.other_turpis_team_manager)

        self.other_clients: list[Player] = [self.other_uroda_client, self.other_turpis_client]

        self.other_gameboard: GameBoard = GameBoard(locations=self.other_locations, map_size=Vector(2, 3),
                                                    uroda_team_manager=self.other_uroda_team_manager,
                                                    turpis_team_manager=self.other_turpis_team_manager)

        self.other_gameboard.generate_map()

    def test_given_invalid_enum(self) -> None:
        # mock the handle_move_logic method to later check if it was ever called
        mock: Mock = Mock()
        move_logic.handle_move_logic = mock

        # set the uroda healer to not have a selected move
        self.uroda_healer.selected_move = None

        self.move_controller.handle_logic(self.clients, self.gameboard)

        # check that the Generic Tank wasn't affected at all
        self.assertEqual(self.turpis_tank.current_health, self.turpis_tank.max_health)

        # test passes if the handle_move_logic method was never called
        mock.assert_not_called()

    def test_speed_tie(self) -> None:
        # set the game board's active_pair_index to 2 (teams aren't ordered by speed currently)
        self.gameboard.active_pair_index = 2

        # uroda attacker and turpis attacker should be attacking each other at the same time
        self.move_controller.handle_logic(self.clients, self.gameboard)

        # expected damage: ceil((45 + 5) * (1 - 30 / 100)) = 35
        self.assertTrue(self.uroda_attacker.current_health == self.turpis_attacker.current_health
                        == self.uroda_attacker.max_health - 35)

        # both attackers should have +1 special points
        self.assertEqual(self.uroda_attacker.special_points, 1)
        self.assertEqual(self.turpis_attacker.special_points, 1)

        self.assertTrue(self.uroda_attacker.took_action)
        self.assertTrue(self.turpis_attacker.took_action)

        # test that the game map's instance of the characters are the same
        self.assertTrue(self.uroda_attacker == self.gameboard.get_character_from(self.uroda_attacker.position))
        self.assertTrue(self.turpis_attacker == self.gameboard.get_character_from(self.turpis_attacker.position))

        # the attacker references cannot be compared in ordered_teams since their instances were popped off the list

    def test_speed_tie_both_defeated(self) -> None:
        # set the game board's active_pair_index to 2 for both attackers
        self.gameboard.active_pair_index = 2

        # set the health of both attackers to be 1
        self.uroda_attacker.current_health = 1
        self.turpis_attacker.current_health = 1

        self.move_controller.handle_logic(self.clients, self.gameboard)

        # both should be dead and have 0 health
        self.assertTrue(self.uroda_attacker.current_health == self.turpis_attacker.current_health == 0)
        self.assertTrue(self.uroda_attacker.is_dead and self.turpis_attacker.is_dead)
        self.assertTrue(self.uroda_attacker.took_action)
        self.assertTrue(self.turpis_attacker.took_action)

        # test that the game map's instance of the characters are the same
        self.assertTrue(self.uroda_attacker == self.gameboard.get_character_from(self.uroda_attacker.position))
        self.assertTrue(self.turpis_attacker == self.gameboard.get_character_from(self.turpis_attacker.position))

        # the attacker references cannot be compared in ordered_teams since their instances were popped off the list

    def test_defeated_before_taking_turn(self) -> None:
        # set the game board's active_pair_index to 0
        self.gameboard.active_pair_index = 0

        # set turpis tank health to 1
        self.turpis_tank.current_health = 1

        # uroda healer and turpis tank fight; healer is faster and should kill tank before it attacks
        self.move_controller.handle_logic(self.clients, self.gameboard)

        # ensure the tank is dead and that the healer took no damage
        self.assertTrue(self.turpis_tank.current_health == 0 and self.turpis_tank.is_dead)
        self.assertFalse(self.turpis_tank.took_action)

        self.assertEqual(self.uroda_healer.current_health, self.uroda_healer.max_health)
        self.assertEqual(self.uroda_healer.special_points, 1)
        self.assertTrue(self.uroda_healer.took_action)

        # test that the game map's instance of the characters are the same
        self.assertTrue(self.uroda_healer == self.gameboard.get_character_from(self.uroda_healer.position))
        self.assertTrue(self.turpis_tank == self.gameboard.get_character_from(self.turpis_tank.position))

    def test_both_teams_are_defeated_with_speed_tie(self) -> None:
        # set the game board's active_pair_index to 2
        self.gameboard.active_pair_index = 2

        # set the special points so the attackers can use their aoe
        self.uroda_attacker.special_points = 5
        self.uroda_attacker.selected_move = self.uroda_attacker.get_s2()

        self.turpis_attacker.special_points = 5
        self.turpis_attacker.selected_move = self.turpis_attacker.get_s2()

        # set all characters to have 1 hp
        self.uroda_attacker.current_health = 1
        self.uroda_healer.current_health = 1
        self.uroda_tank.current_health = 1

        self.turpis_attacker.current_health = 1
        self.turpis_tank.current_health = 1
        self.turpis_tank2.current_health = 1

        self.move_controller.handle_logic(self.clients, self.gameboard)

        # check that the special points were reduced appropriately
        self.assertTrue(self.uroda_attacker.special_points == 3)
        self.assertTrue(self.turpis_attacker.special_points == 3)

        # ensure all characters died (cannot iterate through team manager since the updates aren't there)
        self.assertTrue(self.uroda_attacker.is_dead)
        self.assertTrue(self.uroda_healer.is_dead)
        self.assertTrue(self.uroda_tank.is_dead)

        self.assertTrue(self.turpis_attacker.is_dead)
        self.assertTrue(self.turpis_tank.is_dead)
        self.assertTrue(self.turpis_tank2.is_dead)

        # test that the game map's instance of the characters are the same
        self.assertTrue(self.uroda_attacker == self.gameboard.get_character_from(self.uroda_attacker.position))
        self.assertTrue(self.uroda_healer == self.gameboard.get_character_from(self.uroda_healer.position))
        self.assertTrue(self.uroda_tank == self.gameboard.get_character_from(self.uroda_tank.position))
        self.assertTrue(self.turpis_attacker == self.gameboard.get_character_from(self.turpis_attacker.position))
        self.assertTrue(self.turpis_tank == self.gameboard.get_character_from(self.turpis_tank.position))
        self.assertTrue(self.turpis_tank2 == self.gameboard.get_character_from(self.turpis_tank2.position))

    def test_speed_ties_with_move_priorities(self) -> None:
        self.other_locations: dict[Vector, list[GameObject]] = {Vector(0, 0): [self.other_uroda_attacker],
                                                                Vector(0, 1): [self.other_uroda_healer],
                                                                Vector(0, 2): [self.other_uroda_tank],
                                                                Vector(1, 0): [self.other_turpis_attacker],
                                                                Vector(1, 1): [self.other_turpis_healer],
                                                                Vector(1, 2): [self.other_turpis_tank]}

        self.other_gameboard: GameBoard = GameBoard(locations=self.other_locations, map_size=Vector(2, 3),
                                                    uroda_team_manager=self.other_uroda_team_manager,
                                                    turpis_team_manager=self.other_turpis_team_manager)

        self.other_gameboard.generate_map()
        self.other_gameboard.active_pair_index = 1

        # uroda healer attacks entire opposing team, turpis healer heals adjacent allies
        self.other_uroda_healer.selected_move = self.other_uroda_healer.get_s1()
        self.other_turpis_healer.selected_move = self.other_turpis_healer.get_nm()

        # offset the health a little bit for the turpis team. these chars should be at full health & THEN receive damage
        self.other_turpis_attacker.current_health = self.other_turpis_attacker.max_health - 1
        self.other_turpis_tank.current_health = self.other_turpis_tank.max_health - 1

        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # assert that the turpis attacker and tank took damage from full health specifically
        self.assertEqual(self.other_turpis_attacker.current_health, 101)
        self.assertEqual(self.other_turpis_tank.current_health, 102)

    def test_no_special_point_increase(self) -> None:
        # set the game board's active_pair_index to 0
        self.gameboard.active_pair_index = 0

        # remove the turpis attacker from the game map so the uroda attack has no target
        self.gameboard.remove_coordinate(self.turpis_attacker.position)

        # remove the turpis attacker from the turpis team manager
        # this is done so that the turpis attack isn't contained in the ordered_teams list
        for index in range(len(self.turpis_team_manager.team)):
            if self.turpis_team_manager.team[index].name == self.turpis_attacker.name:
                self.turpis_team_manager.team.pop(index)
                break

        # reorganize the teams to reflect the missing turpis attacker
        self.gameboard.order_teams(self.uroda_team_manager, self.turpis_team_manager)

        self.move_controller.handle_logic(self.clients, self.gameboard)

        self.assertTrue(self.uroda_attacker.special_points == 0)

        # test that the game map's instance of the characters are the same
        self.assertTrue(self.uroda_attacker == self.gameboard.get_character_from(self.uroda_attacker.position))

    def test_no_special_point_decrease(self) -> None:
        # set the game board's active_pair_index to 0
        self.gameboard.active_pair_index = 0

        # set the special points to 5 to show the uroda attacker has enough points to use the special
        self.uroda_attacker.special_points = 4

        self.gameboard.remove_coordinate(self.turpis_attacker.position)

        # remove the turpis attacker from the turpis team manager
        # this is done so that the turpis attack isn't contained in the ordered_teams list
        for index in range(len(self.turpis_team_manager.team)):
            if self.turpis_team_manager.team[index].name == self.turpis_attacker.name:
                self.turpis_team_manager.team.pop(index)
                break

        # reorganize the teams to reflect the missing turpis attacker
        self.gameboard.order_teams(self.uroda_team_manager, self.turpis_team_manager)

        self.move_controller.handle_logic(self.clients, self.gameboard)

        self.assertEqual(self.uroda_attacker.special_points, 4)

        # test that the game map's instance of the characters are the same
        self.assertTrue(self.uroda_attacker == self.gameboard.get_character_from(self.uroda_attacker.position))

    def test_user_heals_entire_team(self) -> None:
        # set the game board's active_pair_index to 0
        self.gameboard.active_pair_index = 0

        # set the uroda team to be on low health and allow the healer to take its turn
        self.uroda_attacker.current_health = 1
        self.uroda_healer.current_health = 1
        self.uroda_tank.current_health = 1

        self.uroda_healer.special_points = 5
        self.uroda_healer.selected_move = self.uroda_healer.get_s2()

        # don't want the turpis tank to take its turn since that will deal damage
        self.turpis_tank.selected_move = None

        self.move_controller.handle_logic(self.clients, self.gameboard)

        self.assertEqual(self.uroda_attacker.current_health, 71)
        self.assertEqual(self.uroda_healer.current_health, 71)
        self.assertEqual(self.uroda_tank.current_health, 71)

        # test that the game map's instance of the characters are the same
        self.assertTrue(self.uroda_attacker == self.gameboard.get_character_from(self.uroda_attacker.position))
        self.assertTrue(self.uroda_healer == self.gameboard.get_character_from(self.uroda_healer.position))
        self.assertTrue(self.uroda_tank == self.gameboard.get_character_from(self.uroda_tank.position))

    def test_user_heals_over_max_health(self) -> None:
        # set the game board's active_pair_index to 0
        self.gameboard.active_pair_index = 0

        # set the uroda team to be on low health and allow the healer to take its turn
        self.uroda_attacker.current_health = self.uroda_attacker.max_health - 1
        self.uroda_healer.current_health = self.uroda_healer.max_health - 1
        self.uroda_tank.current_health = self.uroda_tank.max_health - 1

        self.uroda_healer.special_points = 5
        self.uroda_healer.selected_move = self.uroda_healer.get_s2()

        # don't want the turpis tank to take its turn since that will deal damage
        self.turpis_tank.selected_move = None

        self.move_controller.handle_logic(self.clients, self.gameboard)

        self.assertEqual(self.uroda_attacker.current_health, self.uroda_attacker.max_health)
        self.assertEqual(self.uroda_healer.current_health, self.uroda_healer.max_health)
        self.assertEqual(self.uroda_tank.current_health, self.uroda_tank.max_health)

    def test_gameboard_logs_turn_info(self) -> None:
        self.move_controller.handle_logic(self.clients, self.gameboard)

        # simply need to check that the string is not empty
        self.assertTrue(self.gameboard.turn_info != '')

    # -------------------------------------------------------------------------------------------------------

    # the methods below are the same from the original test move controller; it was easier to paste them here
    def test_self_buffing(self) -> None:
        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        self.other_uroda_attacker.selected_move = self.other_uroda_attacker.get_s1()

        # test that a character buffing itself works while the target is themselves
        # uroda attacker buffs themselves
        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # check the stat was buffed properly
        self.assertEqual(self.other_uroda_attacker.attack.value, 16)

        # ensure the special points decreased
        self.assertEqual(self.other_uroda_attacker.special_points, 2)

        # test that the game map's instance of the characters are the same
        self.assertTrue(
            self.other_uroda_attacker == self.other_gameboard.get_character_from(self.other_uroda_attacker.position))

    def test_heal_ally_up(self) -> None:
        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        # set urodan attacker health to be at 1 HP and to have already taken their turn
        self.other_uroda_attacker.current_health = 1

        # allow the healer to take its turn
        self.other_gameboard.ordered_teams.pop(0)

        # don't want the turpis healer to do anything
        self.other_turpis_healer.selected_move = None

        # let the healer use their normal to heal the injured ally
        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # 1 + 15 = 16 HP
        self.assertEqual(self.other_uroda_attacker.current_health, 16)

        # ensure the special points increased; this is the healer, so it's special points start at 0
        self.assertEqual(self.other_uroda_healer.special_points, 1)

        # test that the game map's instance of the characters are the same
        self.assertTrue(
            self.other_uroda_attacker == self.other_gameboard.get_character_from(self.other_uroda_attacker.position))
        self.assertTrue(
            self.other_uroda_healer == self.other_gameboard.get_character_from(self.other_uroda_healer.position))

    def test_heal_adjacent_allies(self) -> None:
        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        # set urodan attacker health to be on 1 HP
        self.other_uroda_attacker.current_health = 1

        # set urodan tank health to be at 1 HP
        self.other_uroda_tank.current_health = 1

        # allow the healer to take its turn
        self.other_gameboard.ordered_teams.pop(0)

        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # Tank's health: 1 + 15 = 16 HP
        self.assertEqual(self.other_uroda_tank.current_health, 16)

        # attacker's health: 1 + 15 = 16 HP
        self.assertEqual(self.other_uroda_tank.current_health, 16)

        # test that the game map's instance of the characters are the same
        self.assertTrue(
            self.other_uroda_attacker == self.other_gameboard.get_character_from(self.other_uroda_attacker.position))
        self.assertTrue(
            self.other_uroda_tank == self.other_gameboard.get_character_from(self.other_uroda_tank.position))

    def test_no_ally_target_available(self) -> None:
        mock: Mock = Mock()
        move_logic.handle_move_logic = mock

        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        # remove all urodan characters except the healer who is in the middle
        self.other_gameboard.remove_coordinate(self.other_uroda_attacker.position)
        self.other_gameboard.remove_coordinate(self.other_uroda_tank.position)
        self.other_uroda_team_manager.team.remove(self.other_uroda_tank)
        self.other_uroda_team_manager.team.remove(self.other_uroda_attacker)

        # allow the healer to take its turn
        self.other_gameboard.ordered_teams.pop(0)

        # attempt to use moves that target an ally above and below, and ensure the `handle_actions` method wasn't called
        # checks if using the normal attack worked (heal ally up)
        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)
        mock.assert_not_called()

        # checks if using s2 works (heal ally down)
        self.other_gameboard.order_teams(self.uroda_team_manager, self.turpis_team_manager)
        self.other_gameboard.ordered_teams.pop(0)

        # the healer is the character that tried to act
        self.assertEqual(self.other_uroda_healer.special_points, 0)
        self.assertEqual(self.other_uroda_healer.took_action, True)

        # test that the game map's instance of the characters are the same
        self.assertTrue(self.other_uroda_healer == self.other_gameboard.get_character_from(self.other_uroda_healer.position))

    # explicit move_logic tests below ---------------------------------------------------------------------

    def test_debuff_modifier_is_applied(self) -> None:
        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        # testing to ensure a debuff is applied properly from move_logic.py
        self.other_gameboard.ordered_teams.pop(0)

        self.other_uroda_healer.selected_move = self.other_uroda_healer.get_s2()
        self.other_uroda_healer.special_points = 5

        # using the healer's debuff attack
        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # check that the turpis attacker's defense decreased by -1
        self.assertEqual(self.other_turpis_attacker.defense.value, 4)

        # test that the game map's instance of the characters are the same
        self.assertTrue(
            self.other_uroda_healer == self.other_gameboard.get_character_from(self.other_uroda_healer.position))
        self.assertTrue(
            self.other_uroda_attacker == self.other_gameboard.get_character_from(self.other_uroda_attacker.position))

    def test_attack_effect(self) -> None:
        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        # the uroda healer has the effects to test, so let it be its turn
        self.other_gameboard.ordered_teams.pop(0)

        self.other_uroda_healer.selected_move = self.other_uroda_healer.get_nm()

        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # the attack effect damages the user. health - 10 damage = remaining health
        self.assertEqual(self.other_uroda_healer.current_health, 110)

        self.assertTrue(
            self.other_uroda_healer == self.other_gameboard.get_character_from(self.other_uroda_healer.position))

    def test_healing_effect(self) -> None:
        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        # the uroda attacker has the effects to test
        # set the allies' health to be 1 to test healing effect
        self.other_uroda_healer.current_health = 1
        self.other_uroda_tank.current_health = 1

        self.other_uroda_attacker.selected_move = self.other_uroda_attacker.get_nm()

        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # the healing effect heals 10 health
        self.assertEqual(self.other_uroda_healer.current_health, 11)
        self.assertEqual(self.other_uroda_tank.current_health, 11)

        self.assertTrue(
            self.other_uroda_healer == self.other_gameboard.get_character_from(self.other_uroda_healer.position))
        self.assertTrue(
            self.other_uroda_tank == self.other_gameboard.get_character_from(self.other_uroda_tank.position))

    def test_buff_effect(self) -> None:
        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        # the uroda healer has the effects to test, so let it be its turn
        self.other_gameboard.ordered_teams.pop(0)

        self.other_uroda_healer.special_points = 5
        self.other_uroda_healer.selected_move = self.other_uroda_healer.get_s2()

        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # the buff effect boosts all opponents' speed stats by 1 stage
        self.assertEqual(self.other_turpis_attacker.speed.value, 16)
        self.assertEqual(self.other_turpis_healer.speed.value, 11)
        self.assertEqual(self.other_turpis_tank.speed.value, 6)

        # test that the game map's instance of the characters are the same
        self.assertTrue(
            self.other_uroda_healer == self.other_gameboard.get_character_from(self.other_uroda_healer.position))
        self.assertTrue(
            self.other_turpis_attacker == self.other_gameboard.get_character_from(self.other_turpis_attacker.position))
        self.assertTrue(
            self.other_turpis_healer == self.other_gameboard.get_character_from(self.other_turpis_healer.position))
        self.assertTrue(
            self.other_turpis_tank == self.other_gameboard.get_character_from(self.other_turpis_tank.position))

    def test_debuff_effect(self) -> None:
        # set the other game board's active_pair_index to 0
        self.other_gameboard.active_pair_index = 0

        # the uroda healer has the effects to test, so let it be its turn
        self.other_gameboard.ordered_teams.pop(0)

        self.other_uroda_healer.special_points = 5
        self.other_uroda_healer.selected_move = self.other_uroda_healer.get_s1()

        self.move_controller.handle_logic(self.other_clients, self.other_gameboard)

        # the debuff effect decreases all allies' speed stats by -1
        self.assertEqual(self.other_uroda_attacker.speed.value, 14)
        self.assertEqual(self.other_uroda_healer.speed.value, 9)
        self.assertEqual(self.other_uroda_tank.speed.value, 4)

        # test that the game map's instance of the characters are the same
        self.assertTrue(
            self.other_uroda_healer == self.other_gameboard.get_character_from(self.other_uroda_healer.position))
        self.assertTrue(
            self.other_uroda_attacker == self.other_gameboard.get_character_from(self.other_uroda_attacker.position))
        self.assertTrue(
            self.other_uroda_tank == self.other_gameboard.get_character_from(self.other_uroda_tank.position))
