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
        characters_pos: dict[Vector, Character] = world.get_characters(client.team_manager.country_type)

        active_chars: tuple[Character | None, Character | None] = world.get_active_pair()

        # index will be 0 if Uroda, 1 if Turpis
        tuple_index_to_use: int = client.team_manager.country_type.value - 1

        active_character: Character | None = active_chars[tuple_index_to_use]

        # if the active character from the ordered_teams list is None, it's not its turn to do anything yet
        if active_character is None:
            return

        # active_character: Character = client.team_manager.get_active_character()

        pos_mod: Vector

        # used for describing what the character did in the gameboard's turn_info string
        swapping_direction: str

        # Determine pos_mod based on swapping up or down
        match action:
            case ActionType.SWAP_UP:
                pos_mod = Vector(x=0, y=-1)
                swapping_direction = 'up'
            case ActionType.SWAP_DOWN:
                pos_mod = Vector(x=0, y=1)
                swapping_direction = 'down'
            case _:  # default case
                return

        # Set active_character's took_action to True as their turn has started
        # active_character.took_action = True

        # used in the turn_info string
        position_before: Vector = active_character.position

        # since the active character is swapping, set its selected move to be none
        active_character.selected_move = None

        new_vector: Vector = Vector.add_vectors(active_character.position, pos_mod)

        # If character is attempting to leave the gameboard, prevent it (there is no escape)
        if not world.is_valid_coords(new_vector):
            world.turn_info += (f'\n{active_character.name} tried to swap to coordinate {new_vector} '
                                f'but couldn\'t be moved off the map!\n')

            # sync the active character if they can't move
            self.__sync_character_references(active_character, None, client, world)
            return

        # Get character to swap to if there is one
        swapped_character: Character | None = characters_pos.get(new_vector)

        # First remove the acting character from the board
        # Then, if there is a swapped character, move them to the acting characters former position
        # Then finish moving the acting character to the new position
        world.remove_coordinate(active_character.position)

        if swapped_character is not None:
            world.remove_coordinate(swapped_character.position)
            swapped_character.position = active_character.position
            world.place(active_character.position, swapped_character)

        active_character.position = new_vector
        world.place(new_vector, active_character)

        self.__sync_character_references(active_character, swapped_character, client, world)

        world.turn_info += (f'\nStarting {active_character.name}\'s turn!'
                            f'\n{active_character.name} swapped {swapping_direction} on the map!'
                            f'\n{active_character.name}\'s position before: {position_before} -> '
                            f'{active_character.name}\'s position after: {active_character.position}\n')

        if swapped_character is not None:
            world.turn_info += (f'\n{active_character.name} swapped with {swapped_character.name}!'
                                f'\n{swapped_character.name}\'s position before: {new_vector} -> '
                                f'{swapped_character.name}\'s position after: {swapped_character.position}\n')

    def __sync_character_references(self, active_character: Character, swapped_character: Character | None,
                                    client: Player, world: GameBoard) -> None:
        """
        A helper method to ensure that all character references are synchronized. The controller ensures the
        character's position is updated and that the game map is updated too, but the same update needs to happen with
        the gameboard's `ordered_teams` list.

        Then, the swapped character references also need to be synchronized. This is done by finding its
        `ordered_teams` reference and its TeamManager reference.
        """

        # updated references for the active character and set that reference's took_action bool to true
        ot_active_char: Character = world.get_char_from_ordered_teams(active_character.name)

        if ot_active_char is not None:
            ot_active_char.position = active_character.position
            ot_active_char.took_action = active_character.took_action
            ot_active_char.selected_move = active_character.selected_move

            # update the team manager reference of the character
            tm_active_char: Character = client.team_manager.get_character(active_character.name)
            tm_active_char.position = active_character.position
            tm_active_char.took_action = active_character.took_action
            tm_active_char.selected_move = active_character.selected_move

        # after all swapping is done, update references for the swapped character if applicable
        if swapped_character is not None:
            # syncing the ordered_teams reference of the swapped character
            ot_swapped_char: Character | None = world.get_char_from_ordered_teams(swapped_character.name)

            # if there is no ordered_team character reference, do nothing
            if ot_swapped_char is None:
                return

            ot_swapped_char.position = swapped_character.position

            # now sync the team manager's reference of the swapped character
            tm_swapped_char: Character = client.team_manager.get_character(swapped_character.name)
            tm_swapped_char.position = swapped_character.position
