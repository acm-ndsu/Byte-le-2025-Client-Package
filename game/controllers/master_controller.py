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
        # the clients and their team managers will match up, so assign the client their correct team manager
        for iteration, client in enumerate(clients):
            client.team_manager = team_managers[iteration]

            # sort the team manager by speed
            client.team_manager.speed_sort()

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate world information
    def game_loop_logic(self, start=1):
        self.turn = start

        # Basic loop from 1 to max turns
        while True:
            # Wait until the next call to give the number
            yield str(self.turn)
            # Increment the turn counter by 1
            self.turn += 1

    # Receives world data from the generated game log and is responsible for interpreting it
    def interpret_current_turn_data(self, clients: list[Player], world: dict, turn):
        self.current_world_data = world

        if turn == 1:
            random.seed(world['game_board']['seed'])
            # self.event_times = random.randrange(162, 172), random.randrange(329, 339)

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client: Player, turn):
        # turn_action: Action = Action()
        # client.action: Action = turn_action
        # ^if you want to use action as an object instead of an enum

        turn_actions: list[ActionType] = []
        client.actions = turn_actions

        # Create deep copies of all objects sent to the player
        current_world = GameBoard().from_json(self.current_world_data[
                                                  'game_board'])  # deepcopy(self.current_world_data["game_board"])  # what is current world and copy avatar
        copy_team_manager = TeamManager().from_json(client.team_manager.to_json())  # deepcopy(client.team_manager)
        # Obfuscate data in objects that that player should not be able to see
        # Currently world data isn't obfuscated at all

        args = (self.turn, turn_actions, current_world, copy_team_manager)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, clients: list[Player], turn):
        gameboard: GameBoard = GameBoard().from_json(self.current_world_data['game_board'])

        gameboard.turn_info = f'\nStarting turn {turn}'

        uroda_team_manager: TeamManager = clients[0].team_manager if (
                clients[0].team_manager.country_type == CountryType.URODA) else clients[1].team_manager

        turpis_team_manager: TeamManager = clients[0].team_manager if (
                clients[0].team_manager.country_type == CountryType.TURPIS) else clients[1].team_manager

        # # increment the active_pair_index for the next turn
        # gameboard.active_pair_index += 1

        # start by organizing the dead characters that died last turn if applicable
        gameboard.clean_up_dead_characters(uroda_team_manager, turpis_team_manager)

        # now that dead characters are organized, check if the game is over
        for client in clients:
            # the game is over if everyone is defeated
            if client.team_manager.everyone_is_defeated():
                self.game_over = True

        if self.game_over:
            # add the final scores and return if the game is over; perform no more logic
            self.add_final_client_scores(clients)
            return

        # reset the turn info string for new information
        gameboard.turn_info += (f'\nUnordered active pair for turn {turn}: {[
            char.name if char is not None else None for char in gameboard.get_active_pair()
        ]}\n')

        # set each character's state to 'idle' in the gameboard's ordered_teams list
        for pair in gameboard.ordered_teams:
            for char in pair:
                if char is not None:
                    char.state = 'idle'

        # set each character's state to 'idle' in the game map
        # do this by getting all characters by country and making the dict values a list
        for char in list(gameboard.get_characters(CountryType.URODA).values()) + list(
                gameboard.get_characters(CountryType.TURPIS).values()):
            char.state = 'idle'

        for client in clients:
            # set each character's state to 'idle' in the client's team manager
            for character in client.team_manager.team:
                character.state = 'idle'

            # if the team is defeated, move on
            if client.team_manager.everyone_is_defeated():
                continue

            # attempt to perform the action for the given ActionType
            for i in range(MAX_NUMBER_OF_ACTIONS_PER_TURN):
                try:
                    self.swap_controller.handle_actions(client.actions[i], client, gameboard)
                    self.select_move_controller.handle_actions(client.actions[i], client, gameboard)
                except IndexError:
                    pass

        self.move_controller.handle_logic(clients, gameboard, turn)

        # NOTE: when there are 6 characters alive, every json file whose turn is a multiple of 3 will show
        # all characters as not taken a turn yet. This is fine unless the visualizer needs it for something!
        for client in clients:
            # if everyone took their action in the given team manager, set their took_action bool to False
            if client.team_manager.everyone_took_action():
                for character in client.team_manager.team:
                    character.took_action = False

                # ensure the team is ordered by speed after everyone took their turn
                client.team_manager.speed_sort()

        # increment the active_pair_index for the next turn
        gameboard.active_pair_index += 1

        # repopulate the ordered_teams property if the active_pair_index is the length of the list and reset that value
        if gameboard.active_pair_index == len(gameboard.ordered_teams):
            gameboard.order_teams(uroda_team_manager, turpis_team_manager)
            gameboard.active_pair_index = 0

        # update the current world json by setting it to the game board's updated state
        self.current_world_data['game_board'] = gameboard.to_json()

        print(f'{gameboard.turn_info}')

    def add_final_client_scores(self, clients: list[Player]) -> None:
        client1: Player = clients[0]
        client2: Player = clients[1]

        # add the differential bonus to both teams (150 * # of alive characters)
        client1.team_manager.score += DIFFERENTIAL_BONUS * len(client1.team_manager.team)

        client2.team_manager.score += DIFFERENTIAL_BONUS * len(client2.team_manager.team)

        # client1 is the winner if client2's team is all dead
        winner: Player | None = client1 if client2.team_manager.everyone_is_defeated() else \
            client2 if client1.team_manager.everyone_is_defeated() else None

        # if there is a clear winner (one team was defeated), add the winning score to the winner
        if winner is not None:
            winner.team_manager.score += WIN_SCORE

    # Return serialized version of game
    def create_turn_log(self, clients: list[Player], turn: int):
        data = dict()
        data['tick'] = turn
        data['clients'] = [client.to_json() for client in clients]

        # Add things that should be thrown into the turn logs here
        data['game_board'] = self.current_world_data['game_board']

        return data

    # Gather necessary data together in results file
    def return_final_results(self, clients: list[Player], turn):
        data = dict()

        data['players'] = list()

        # Determine results
        for client in clients:
            data['players'].append(client.to_json())

        return data
