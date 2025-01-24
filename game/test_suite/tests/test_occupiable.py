import unittest

from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector
from game.common.enums import *


class TestOccupiable(unittest.TestCase):
    def setUp(self) -> None:
        # TEST WHEN OCCUPIABLE REDONE

        self.game_board = GameBoard(0, Vector(4, 4), self.locations, True)  # create 4x4 gameboard
        self.game_board.generate_map()

    # def test_if_occupiable(self):
    #     self.assertEqual(self.game_board.get_objects_from(Vector(2, 2))[0].object_type, ObjectType.OCCUPIABLE_STATION)
    #
    # def test_if_not_occupiable(self):
    #     self.assertEqual(self.game_board.get_objects_from(Vector(1, 1))[0].object_type, ObjectType.STATION)