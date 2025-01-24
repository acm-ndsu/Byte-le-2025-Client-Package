from typing import Self

from game.common.enums import *


class Action:
    """
    `Action Class:`

        This class encapsulates the different actions a player can execute while playing the game.

        **NOTE**: This is not currently implemented in this version of the Byte Engine. If you want more complex
        actions, you can use this class for Objects instead of the enums.
    """

    def __init__(self):
        self.object_type: ObjectType = ObjectType.ACTION
        self._example_action = None

    def set_action(self, action):
        self._example_action = action

    def to_json(self) -> dict:
        data: dict = dict()
        data['object_type'] = self.object_type
        data['example_action'] = self._example_action

        return data

    def from_json(self, data) -> Self:
        self.object_type: ObjectType = data['object_type']
        self._example_action = data['example_action']

        return self

    def __str__(self) -> str:
        outstring: str = ''
        outstring += f'Example Action: {self._example_action}\n'

        return outstring
