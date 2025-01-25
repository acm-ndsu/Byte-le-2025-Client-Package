from game.commander_clash.moves.move_logic import handle_move_logic, handle_effect_logic
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.team_manager import *
from game.config import DEFEATED_SCORE
from game.controllers.controller import Controller


class MoveController(Controller):
    """
    A controller that allows for characters to use a move from their moveset. If given the correct enum,
    it will access that move and call its `use()` method to attempt to activate it.
    """

    def handle_logic(self, clients: list[Player], world: GameBoard, turn: int = 1) -> None:
        ...