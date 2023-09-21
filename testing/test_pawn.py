import unittest
import pygame
from start import Pawn


class Test_Pawn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = [[None for i in range(8)] for j in range(8)] # 2d array of pieces
        cls.white_pawn = Pawn(0,0, None, 'white', [(0,1)])
    @classmethod
    def tearDownClass(cls):
        cls.board = None
        cls.white_pawn = None
    def setUp(self) -> None:
        pass
    def tearDown(self) -> None:
        pass
    def test_white_initial_move_generation(self):
        # Arrange
        self.white_pawn.setX(6)
        self.white_pawn.setY(3)
        self.white_pawn.setMove(0)
        self.board[self.white_pawn.getX()][self.white_pawn.getY()] = self.white_pawn
        expected = {(4,3),(5,3)}
        # Act
        moves = self.white_pawn.getMoves(self.board)
        moves = set(moves)
        # Assert
        self.assertEqual(expected,moves,f"Initial moves aren't correct: expected {[(4,3),(5,3)]} but got {moves}")