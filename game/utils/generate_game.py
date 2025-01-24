import random

from game.commander_clash.generation.character_generation import *
from game.common.game_object import GameObject
from game.common.team_manager import TeamManager
from game.utils.vector import Vector
from game.config import *
from game.utils.helpers import write_json_file
from game.utils.pre_generate_game import pre_generate
from game.common.map.game_board import GameBoard


def generate(seed: int = random.randint(0, 1000000000)):
    """
    This method is what generates the game_map. This method is slow, so be mindful when using it. A seed can be set as
    the parameter; otherwise, a random one will be generated. Then, the method checks to make sure the location for
    storing logs exists. Lastly, the game map is written to the game file.
    :param seed:
    :return: None
    """

    print(f'Generating game map... seed: {seed}')

    # get the locations of the characters necessary from the pre_generation method
    info: tuple[dict[Vector, list[GameObject]], list[TeamManager]] = pre_generate()

    uroda_team_manager: TeamManager
    turpis_team_manager: TeamManager

    # determine which team manager is which
    for team_manager in info[1]:
        if team_manager.country_type == CountryType.URODA:
            uroda_team_manager = team_manager
        else:
            turpis_team_manager = team_manager

    # create the gameboard with the team managers so the ordered_teams list can be populated immediately
    temp: GameBoard = GameBoard(seed, Vector(2, 3), info[0], False,
                                uroda_team_manager, turpis_team_manager)
    temp.generate_map()
    data: dict = {'game_board': temp.to_json()}

    # for every created team manager, write them to the json
    data['game_board']['uroda_team_manager'] = uroda_team_manager.to_json()
    data['game_board']['turpis_team_manager'] = turpis_team_manager.to_json()

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    write_json_file(data, GAME_MAP_FILE)
