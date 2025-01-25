from game.commander_clash.character.character import Character
from game.commander_clash.moves.moves import Move
from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller


class SelectMoveController(Controller):
    """
    A controller that sets the `selected_move` variable for a client's active character.
    """

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard) -> None:
        """
        Given the correct ActionType enum, the client's active character's `selected_move` variable will be set. This
        will be used in another controller that will execute a move's logic.
        """
        ...