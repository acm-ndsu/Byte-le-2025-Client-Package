from __future__ import annotations

from game.commander_clash.moves.moves import *
from game.common.game_object import GameObject


class Moveset(GameObject):
    """
    A container class to represent every character's moveset. Helps with storing a character's moves in the JSON
    by removing that heavier logic from the Character class. Also prevents "mutable default value" warnings
    from other classes, making the code more robust.
    """

    def __init__(self, moves: tuple[Move, Move, Move] = (Attack(), Buff(), Debuff())):
        super().__init__()
        self.object_type: ObjectType = ObjectType.MOVESET
        self.moves: dict[str, Move] = self.__tuple_to_dict(moves)

    # override the equals method to simplify testing
    def __eq__(self, other: Moveset) -> bool:
        # return false if `other` isn't a Moveset
        if not isinstance(other, Moveset):
            return False

        # it's harder to check every property of every move, so check that every move's object type and effect match
        for move, other_move in zip(self.moves.values(), other.moves.values()):
            # return true if both effects are None
            if move.effect is None and other_move.effect is None:
                return True

            if move.object_type != other_move.object_type:
                return False

            # return false if neither effect's object type matches
            if move.effect.object_type != other_move.effect.object_type:
                return False

        # return true as a base case
        return True

    @property
    def moves(self) -> dict[str, Move]:
        return self.__moves

    @moves.setter
    def moves(self, moves: dict[str, Move]) -> None:
        if moves is None or not isinstance(moves, dict):
            raise ValueError(
                f'{self.__class__.__name__}.moveset must be a dict. It is a(n) {moves.__class__.__name__} '
                f'and has the value of {moves}')

        # check if any of the keys in the dict are not a string
        if any([not isinstance(key, str) for key in moves.keys()]):
            raise ValueError(f'{self.__class__.__name__}.moveset must be a dict with strings as the keys.')

        # check if any of the values in the dict are not a Move object
        if any([not isinstance(value, Move) for value in moves.values()]):
            raise ValueError(f'{self.__class__.__name__}.moveset must be a dict with Move objects as the values.')

        # set the new dictionary
        self.__moves = moves

    def get_nm(self) -> Move:
        ...

    def get_s1(self) -> Move:
        ...

    def get_s2(self) -> Move:
        ...

    def as_dict(self) -> dict[str, Move]:
        ...
