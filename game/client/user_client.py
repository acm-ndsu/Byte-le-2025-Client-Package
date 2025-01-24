from game.common.enums import *
from game.config import Debug
import logging


class UserClient:
    def __init__(self):
        self.debug_level = DebugLevel.CLIENT
        self.debug = True

    def debug(self, *args):
        if self.debug and Debug.level >= self.debug_level:
            logging.basicConfig(level=logging.DEBUG)
            for arg in args:
                logging.debug(f'{self.__class__.__name__}: {arg}')

    def team_data(self) -> tuple[str, tuple[SelectLeader, SelectGeneric, SelectGeneric]]:
        """
        Returns a tuple representing the desired leader and generic characters.
        """
        return 'No_Team_Name_Available', (SelectLeader.ANAHITA, SelectGeneric.GEN_ATTACKER, SelectGeneric.GEN_ATTACKER)

    def take_turn(self, turn, actions, world, avatar):
        raise NotImplementedError("Implement this in subclass")
