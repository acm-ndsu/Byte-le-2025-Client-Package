from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.team_manager import *
from game.controllers.controller import Controller


class SwapController(Controller):
    """
    `Swap Controller Notes:`

        The Swap Controller manages the swap actions the player tries to execute. Players can move up and down to swap placed.
        If the player tries to move into a space that's impassable, they don't move.

        For example, if the player attempts to move into an Occupiable Station (something the player can be on) that is
        occupied by a Wall object (something the player can't be on), the player doesn't move; that is, if the player
        tries to move into anything that can't be occupied by something, they won't move.
    """

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard) -> None:
        ...