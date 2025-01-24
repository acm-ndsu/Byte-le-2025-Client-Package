import importlib
import sys
import traceback

from game.client.user_client import UserClient
from game.commander_clash.generation.char_position_generation import generate_locations_dict
from game.commander_clash.validate_team import validate_team_selection as validate
from game.common.game_object import GameObject
from game.common.player import Player
from game.common.team_manager import TeamManager
from game.config import *
from game.utils.thread import CommunicationThread
from game.utils.vector import Vector


def pre_generate() -> tuple[dict[Vector, list[GameObject]], list[TeamManager]]:
    """
    This method will be used to handle any logic that needs to occur BEFORE the actual generation of the game map. An
    example of this would be if the user needs to choose a character to use before the map is generated. This is done to
    honor the control flow of the engine, to create some abstraction from the engine file, and to also ensure the
    `generate()` method in the `generate_game.py` file is only called once.

    This method *must* be called in the `generate()` method in the `generate_game.py` file before any other logic
    specified in that method. This method can return or receive whatever information is necessary for the game created.

    The code used below is very similar to the engine file. This is executed here since it simplifies the engine's code
    and can be done separately for generation
    """

    # Insert path of where clients are expected to be inside where python will look
    current_dir = os.getcwd()
    sys.path.insert(0, current_dir)
    sys.path.insert(0, f'{current_dir}/{CLIENT_DIRECTORY}')

    # a list to contain all the team managers created
    team_managers: list[TeamManager] = []
    clients: list[Player] = []
    world = dict()

    # an int used to keep track of which client file is being used to assign country values
    client_files_found: int = 0

    # Find and load clients in
    for filename in os.listdir(CLIENT_DIRECTORY):
        # create a new team manager to use later
        team_manager: TeamManager = TeamManager()

        try:
            filename = filename.replace('.py', '')

            # Filter out files that do not contain CLIENT_KEYWORD in their filename (located in config)
            if CLIENT_KEYWORD.upper() not in filename.upper():
                continue

            # Filter out folders
            if os.path.isdir(os.path.join(CLIENT_DIRECTORY, filename)):
                continue

            # Otherwise, instantiate the player
            player = Player()
            clients.append(player)

            # Attempt creation of the client object
            obj: UserClient | None = None
            try:
                # Import client's code
                im = importlib.import_module(f'{filename}', CLIENT_DIRECTORY)
                obj = im.Client()
            except Exception:
                player.functional = False
                player.error = str(traceback.format_exc())
                continue

            player.code = obj
            thr = None

            try:
                # Retrieve team name
                thr = CommunicationThread(player.code.team_data, list(), tuple)
                thr.start()
                thr.join(0.01)  # Shouldn't take long to get a string

                if thr.is_alive():
                    player.functional = False
                    player.error = 'Client failed to provide a team name in time.'

                if thr.error is not None:
                    player.functional = False
                    player.error = str(thr.error)
            finally:
                # Note: I keep the above thread for both naming conventions to check for client errors
                try:
                    # get the team data from the thread's value
                    team_data = thr.retrieve_value()

                    # use index 0 to access the team name from `team_data`
                    player.team_name = team_data[0]

                    # use index 1 to access the tuple of character selection enums from `team_data`
                    team_manager.team = validate(team_data[1])

                    # assign countries to the team managers
                    if client_files_found == 0:
                        team_manager.country_type = CountryType.URODA
                        client_files_found += 1
                    else:
                        team_manager.country_type = CountryType.TURPIS

                    for char in team_manager.team:
                        char.country_type = team_manager.country_type

                    # give the team manager the player's team name for organization later in the engine.py file
                    team_manager.team_name = player.team_name

                    team_managers.append(team_manager)
                except Exception as e:
                    print(f"{str(e)}\n{traceback.print_exc()}")
        except Exception as e:
            print(f"Bad client for {filename}: exception: {e}")

    return generate_locations_dict(team_managers), team_managers
