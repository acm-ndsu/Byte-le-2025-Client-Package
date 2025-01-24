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

        active_chars: tuple[Character | None, Character | None] = world.get_active_pair()

        # index will be 0 if Uroda, 1 if Turpis
        tuple_index_to_use: int = client.team_manager.country_type.value - 1

        user: Character | None = active_chars[tuple_index_to_use]

        if user is None:
            world.turn_info += f'\n{client.team_name} doesn\'t have an active character'
            return

        # if the user took action already, don't do anything
        # if user.took_action:
        #     world.turn_info += f'\n{user.name} already took their action when getting to the select move controller'
        #     return

        current_move: Move

        match action:
            case ActionType.USE_NM:
                user.selected_move = user.get_nm()
            case ActionType.USE_S1:
                user.selected_move = user.get_s1()
            case ActionType.USE_S2:
                user.selected_move = user.get_s2()
            case _:
                return

        # sync the team manager reference
        tm_char: Character | None = client.team_manager.get_character(user.name)

        if tm_char is not None:
            tm_char.selected_move = user.selected_move

        # give the reference in the ordered_teams and game map the same selected move
        ot_char: Character | None = world.get_char_from_ordered_teams(user.name)

        # giving the ordered_teams reference the selected move
        if ot_char is not None:
            ot_char.selected_move = user.selected_move

        gm_char: Character | None = world.get_character_from(user.position)

        # giving the game map reference the selected move
        if gm_char is not None:
            gm_char.selected_move = user.selected_move
