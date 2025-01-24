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
        uroda_team_manager: TeamManager = clients[0].team_manager \
            if clients[0].team_manager.country_type == CountryType.URODA else clients[1].team_manager
        turpis_team_manager: TeamManager = clients[0].team_manager \
            if clients[0].team_manager.country_type == CountryType.TURPIS else clients[1].team_manager

        # get the active pair for the turn, but only get character references; that is, filter None values
        active_chars: list[Character] = [char for char in world.get_active_pair() if char is not None]

        # explicitly filter to only characters that have not acted yet (i.e., didn't swap)
        # active_chars: list[Character] = [char for char in active_chars if not char.took_action]

        # if all active characters are None, nothing can happen; return
        if all([obj is None for obj in active_chars]):
            return

        # sort the list so that the fastest character is listed first
        active_chars = sorted(active_chars, key=lambda character: character.speed, reverse=True)

        is_speed_tie: bool = active_chars[0].speed == active_chars[1].speed if len(active_chars) == 2 else False

        # indicate it's a speed tie in the gameboard's turn info string
        if is_speed_tie:
            world.turn_info += f'\nIt\'s a speed tie between {active_chars[0].name} and {active_chars[1].name}!\n'

            # if both active characters have a selected move and a speed tie, organize by selected move priority
            if active_chars[0].selected_move is not None and active_chars[1].selected_move is not None:
                # reorganize the two characters based on their selected move priority instead of speed for speed ties
                active_chars = sorted(active_chars, key=lambda character: character.selected_move.priority, reverse=True)

        # for every character, execute the logic for their move if applicable
        for user in active_chars:
            # if the client's character died before their turn AND it is not a speed tie, continue to next iteration
            # if it is a speed tie and the character died before their turn, they can still act to simulate them
            # attacking at the same time
            if user.is_dead and not is_speed_tie:
                world.turn_info += f'\n{user.name} died before they could take their turn!\n'
                continue

            # move to next iteration if no move was selected
            if user.selected_move is None:
                world.turn_info += f'\n{user.name} didn\'t execute a Move because they didn\'t have one selected!\n'
                continue

            world.turn_info += f'\n{user.name} wants to execute a Move!\n'

            current_move: Move = user.selected_move
            is_normal_move: bool = user.selected_move == user.get_nm()
            user.took_action = True

            # if the character cannot use the desired move, continue to next iteration
            if user.special_points < current_move.cost:
                world.turn_info += (f'\n{user.name} could not use {current_move.name} due to not having enough Special '
                                    f'Points!\n'
                                    f'{user.name}\'s Special Points: {user.special_points}. '
                                    f'Needed Special Points: {current_move.cost}\n')
                continue

            # get the possible targets based on the target type
            primary_targets: list[Character] | list = self.__get_targets(user, current_move.target_type, world)

            # don't do anything if there are no available targets
            if len(primary_targets) == 0:
                world.turn_info += f'\n{user.name} has no initial targets for {current_move.name}!\n'
                continue

            # call the move_logic file's method to handle the rest of the logic
            handle_move_logic(user, primary_targets, current_move, is_normal_move, world,
                              uroda_team_manager, turpis_team_manager)

            defeated_characters: list[Character] = []

            # add the defeated characters to the collection
            defeated_characters += [target for target in primary_targets if target.current_health == 0]

            effect_targets: list[Character] | list = []

            # if the current move has an effect, get the targets for it and apply the same logic
            if current_move.effect is not None:
                # get the possible targets based on the effect's target type
                effect_targets = self.__get_targets(user, current_move.effect.target_type, world)

                if len(effect_targets) != 0:
                    handle_effect_logic(user, effect_targets, current_move.effect, world)
                else:
                    # add to the turn info there were no targets for the secondary effect of the move
                    world.turn_info += (f'\n{user.name} has no targets for the secondary effect of '
                                        f'{current_move.name}!\n')

                # add any additional characters to defeated_characters
                defeated_characters += [target for target in effect_targets if
                                        target not in defeated_characters and target.current_health == 0]

            for char in defeated_characters:
                world.turn_info += f'\n{user.name} defeated {char.name}!\n'

            # perform the logic of defeating a character(s)
            self.__defeated_char_logic(clients, user, defeated_characters, world)

            # sync the primary and effect targets
            self.__sync_targeted_characters(primary_targets, uroda_team_manager, turpis_team_manager, world)
            self.__sync_targeted_characters(effect_targets, uroda_team_manager, turpis_team_manager, world)

            # sync the users that took their action
            self.__sync_active_characters(active_chars, uroda_team_manager, turpis_team_manager, world)

    def __defeated_char_logic(self, clients: list[Player], user: Character,
                              defeated_characters: list[Character], world: GameBoard) -> None:

        # don't do anything if there are no defeated characters
        if len(defeated_characters) == 0:
            return

        client_to_use: Player = Player()

        # find the client the user character belongs to
        for client in clients:
            if client.team_manager.country_type == user.country_type:
                client_to_use = client

        # for all defeated characters, set their state to 'defeated;' remove them at start of next turn
        for defeated_char in defeated_characters:
            defeated_char.is_dead = True
            defeated_char.state = 'defeated'
            client_to_use.team_manager.score += DEFEATED_SCORE

            # add the defeated character to the recently died list of the game board
            world.recently_died.append(defeated_char)

    def __get_targets(self, user: Character, target_type: TargetType, world: GameBoard) -> list[Character] | list:
        """
        Helper method that determines the necessary targets for a character. Will return a list of Character objects
        or an empty list. If an empty list is returned, the character's won't perform anything during their turn.
        """

        match target_type:
            case TargetType.SELF:
                return [user]
            case TargetType.ADJACENT_ALLIES:
                result: list = []

                # get the position that is above the character
                above_pos: Vector = user.position.add_to_vector(Vector(0, -1))
                below_pos: Vector = user.position.add_to_vector(Vector(0, 1))

                # get the actual targets
                above_target: GameObject = world.get_character_from(above_pos)
                below_target: GameObject = world.get_character_from(below_pos)

                # if neither character is None, add them to the list
                if above_target is not None:
                    result.append(above_target)

                if below_target is not None:
                    result.append(below_target)

                return result
            case TargetType.ENTIRE_TEAM:
                # get_characters() returns a dict; receives the characters by getting the dict's values as a list
                return list(world.get_characters(user.country_type).values())
            case TargetType.SINGLE_OPP:

                # adjusts the vector value based on who is attacking, so it attacks across from the user
                adjustment_vector: Vector = Vector(1, 0) if user.country_type is CountryType.URODA else Vector(-1, 0)

                # get the position that is across the character
                across_pos: Vector = user.position.add_to_vector(adjustment_vector)
                target: Character | None = world.get_character_from(across_pos)

                return [target] if target is not None else []
            case TargetType.ALL_OPPS:
                return list(world.get_characters(user.get_opposing_country()).values())
            case _:
                return []

    def __sync_targeted_characters(self, targets: list[Character], uroda_team_manager: TeamManager,
                                   turpis_team_manager: TeamManager, world: GameBoard) -> None:
        """
        Takes the list of targets that were affected and applies all changes to the team manager references of that
        character. This is because the targets originally come from the game map, so the team manager references must be
        updated.

        The team manager reference receives the differences from the game map.
        Game Map Reference -> Team Manager Reference
        """

        # for every game map reference of a character, sync it with the team manager and ordered_teams references
        for gm_character in targets:
            tm_to_use: TeamManager = uroda_team_manager \
                if gm_character.country_type == CountryType.URODA else turpis_team_manager

            tm_character: Character = tm_to_use.get_character(gm_character.name)

            # sync these attributes specifically to maintain the correct info
            tm_character.current_health = gm_character.current_health
            tm_character.attack = gm_character.attack
            tm_character.defense = gm_character.defense
            tm_character.speed = gm_character.speed
            tm_character.is_dead = gm_character.is_dead
            tm_character.state = gm_character.state

            # sync the ordered_teams reference
            ot_char: Character = world.get_char_from_ordered_teams(gm_character.name)

            # the ordered_team reference might be None if the target was in active_chars
            if ot_char is not None:
                ot_char.current_health = gm_character.current_health
                ot_char.attack = gm_character.attack
                ot_char.defense = gm_character.defense
                ot_char.speed = gm_character.speed
                ot_char.is_dead = gm_character.is_dead
                ot_char.state = gm_character.state

    def __sync_active_characters(self, active_chars: list[Character], uroda_team_manager: TeamManager,
                                 turpis_team_manager: TeamManager, world: GameBoard) -> None:
        # for every active character from the ordered_teams list, sync with the team manager and game map references
        for active_char in active_chars:
            tm_to_use: TeamManager = uroda_team_manager \
                if active_char.country_type == CountryType.URODA else turpis_team_manager

            # sync the client's team manager reference of the character
            tm_character: Character = tm_to_use.get_character(active_char.name)

            tm_character.attack = active_char.attack
            tm_character.defense = active_char.defense
            tm_character.speed = active_char.speed
            tm_character.selected_move = active_char.selected_move
            tm_character.took_action = active_char.took_action
            tm_character.is_dead = active_char.is_dead
            tm_character.special_points = active_char.special_points
            tm_character.state = active_char.state

            # sync the game map's reference of the character
            gm_character: Character = world.get_character_from(active_char.position)

            gm_character.attack = active_char.attack
            gm_character.defense = active_char.defense
            gm_character.speed = active_char.speed
            gm_character.selected_move = active_char.selected_move
            gm_character.took_action = active_char.took_action
            gm_character.is_dead = active_char.is_dead
            gm_character.special_points = active_char.special_points
            gm_character.state = active_char.state
