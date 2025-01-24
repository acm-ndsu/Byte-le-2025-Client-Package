from __future__ import annotations
from typing import Self
from game.common.game_object import GameObject
from game.common.team_manager import TeamManager
from game.common.enums import *
from game.client.user_client import UserClient


class Player(GameObject):
    """
    `Player Class Notes:`

    -----

        The Player class is what represents the team that's competing. The player can contain a list of Actions to
        execute each turn. The team_manager is what's used to execute actions (e.g., interacting with stations, picking up
        items, etc.). For more details on the difference between the Player and team_manager classes, refer to the README
        document.
    """

    def __init__(self, code: object | None = None, team_name: str | None = None, actions: list[ActionType] = [],
                 team_manager: TeamManager | None = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.PLAYER
        self.functional: bool = True
        self.error: str | None = None
        self.file_name: str | None = None
        self.team_name: str | None = team_name
        self.code: UserClient | None = code
        self.actions: list[ActionType] = actions
        self.team_manager: TeamManager | None = team_manager

    @property
    def error(self) -> str | None:
        return self.__error

    @error.setter
    def error(self, error: str | None) -> None:
        if error is not None and not isinstance(error, str):
            raise ValueError(f'{self.__class__.__name__}.error must be either a string or None.')
        self.__error = error

    @property
    def actions(self) -> list[ActionType] | list:  # change to Action if you want to use the action object
        return self.__actions

    @actions.setter
    def actions(self, actions: list[ActionType] | list) -> None:  # showing it returns nothing(like void in java)
        # if it's (not none = and) if its (none = or)
        # going across all action types and making it a boolean, if any are true this will be true\/
        if actions is None or not isinstance(actions, list) \
                or (len(actions) > 0
                    and any(map(lambda action_type: not isinstance(action_type, ActionType), actions))):
            raise ValueError(
                f'{self.__class__.__name__}.action must be an empty list or a list of action types. It is a(n) {actions.__class__.__name__} and has the value of {actions}.')
            # ^if it's not either throw an error
        self.__actions = actions

    @property
    def functional(self) -> bool:
        return self.__functional

    @functional.setter  # do this for all the setters
    def functional(self, functional: bool) -> None:  # this enforces the type hinting
        if functional is None or not isinstance(functional, bool):  # if this statement is true throw an error
            raise ValueError(
                f'{self.__class__.__name__}.functional must be a boolean. It is a(n) {functional.__class__.__name__} and has the value of {functional}.')
        self.__functional = functional

    @property
    def team_name(self) -> str | None:
        return self.__team_name

    @team_name.setter
    def team_name(self, team_name: str | None) -> None:
        if team_name is not None and not isinstance(team_name, str):
            raise ValueError(
                f'{self.__class__.__name__}.team_name must be a String or None. It is a(n) {team_name.__class__.__name__} and has the value of {team_name}.')
        self.__team_name = team_name

    @property
    def file_name(self) -> str | None:
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name: str | None) -> None:
        if file_name is not None and not isinstance(file_name, str):
            raise ValueError(f'{self.__class__.__name__}.file_name must be a String or None')
        self.__file_name = file_name

    @property
    def team_manager(self) -> TeamManager:
        return self.__team_manager

    @team_manager.setter
    def team_manager(self, team_manager: TeamManager) -> None:
        if team_manager is not None and not isinstance(team_manager, TeamManager):
            raise ValueError(
                f'{self.__class__.__name__}.team_manager must be team_manager or None. It is a(n) {team_manager.__class__.__name__} and has the value of {team_manager}.')
        self.__team_manager = team_manager

    @property
    def object_type(self) -> ObjectType:
        return self.__object_type

    @object_type.setter
    def object_type(self, object_type: ObjectType) -> None:
        if object_type is None or not isinstance(object_type, ObjectType):
            raise ValueError(
                f'{self.__class__.__name__}.object_type must be ObjectType. It is a(n) {object_type.__class__.__name__} and has the value of {object_type}.')
        self.__object_type = object_type

    def to_json(self) -> dict:
        data = super().to_json()

        data['functional'] = self.functional
        data['error'] = self.error
        data['team_name'] = self.team_name
        data['file_name'] = self.file_name
        data['actions'] = [act.value for act in self.actions]
        data['team_manager'] = self.team_manager.to_json() if self.team_manager is not None else None

        return data

    def from_json(self, data) -> Self:
        super().from_json(data)

        self.functional = data['functional']
        self.error = data['error']
        self.team_name = data['team_name']
        self.file_name = data['file_name']

        self.actions: list[ActionType] = [ActionType(action) for action in data['actions']]
        team_manager: dict | None = data['team_manager']
        if team_manager is None:
            self.team_manager = None
            return self

        # match case for team_manager
        match ObjectType(team_manager['object_type']):
            case ObjectType.TEAMMANAGER:
                self.team_manager = TeamManager().from_json(data['team_manager'])
            case None:
                self.team_manager = None
            case _:
                raise Exception(f'Could not parse team_manager: {self.team_manager}')
        return self

    # to String
    def __str__(self):
        p = f"""ID: {self.id}
            Team name: {self.team_name}
            Actions: 
            """
        # This concatenates every action from the list of actions to the string 
        [p := p + action for action in self.actions]
        return p
