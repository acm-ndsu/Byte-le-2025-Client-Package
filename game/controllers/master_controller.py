import random

from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.team_manager import TeamManager
from game.config import MAX_NUMBER_OF_ACTIONS_PER_TURN, WIN_SCORE, DIFFERENTIAL_BONUS
from game.controllers.controller import Controller
from game.controllers.move_controller import MoveController
from game.controllers.select_move_controller import SelectMoveController
from game.controllers.swap_controller import SwapController


class MasterController(Controller):
    """
    `Master Controller Notes:`

        Give Client Objects:
            Takes a list of Player objects and places each one in the game world.

        Game Loop Logic:
            Increments the turn count as the game plays (look at the engine to see how it's controlled more).

        Interpret Current Turn Data:
            This accesses the gameboard in the first turn of the game and generates the game's seed.

        Client Turn Arguments:
            There are lines of code commented out that create Action Objects instead of using the enum. If your project
            needs Actions Objects instead of the enums, comment out the enums and use Objects as necessary.

        Turn Logic:
            This method executes every movement and interact behavior from every client in the game. This is done by
            using every other type of Controller object that was created in the project that needs to be managed
            here (InteractController, MovementController, other game-specific controllers, etc.).

        Create Turn Log:
            This method creates a dictionary that stores the turn, all client objects, and the gameboard's JSON file to
            be used as the turn log.

        Return Final Results:
            This method creates a dictionary that stores a list of the clients' JSON files. This represents the final
            results of the game.
    """

    def __init__(self):
        super().__init__()
        self.game_over: bool = False
        # self.event_timer = GameStats.event_timer   # anything related to events are commented it out until made
        # self.event_times: tuple[int, int] | None = None
        self.turn: int = 1
        self.current_world_data: dict = None
        self.swap_controller: SwapController = SwapController()
        self.select_move_controller: SelectMoveController = SelectMoveController()
        self.move_controller: MoveController = MoveController()

    # Receives all clients for the purpose of giving them the objects they will control
    def give_clients_objects(self, clients: list[Player], world: dict, team_managers: list[TeamManager]):
        ...

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate world information
    def game_loop_logic(self, start=1):
        ...

    # Receives world data from the generated game log and is responsible for interpreting it
    def interpret_current_turn_data(self, clients: list[Player], world: dict, turn):
        ...

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client: Player, turn):
        ...

    # Perform the main logic that happens per turn
    def turn_logic(self, clients: list[Player], turn):
        ...

    def add_final_client_scores(self, clients: list[Player]) -> None:
        ...

    # Return serialized version of game
    def create_turn_log(self, clients: list[Player], turn: int):
        ...

    # Gather necessary data together in results file
    def return_final_results(self, clients: list[Player], turn):
        ...
