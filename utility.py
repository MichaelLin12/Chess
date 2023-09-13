from enum import Enum

class Turn_Step(Enum):
    White_Turn_No_Selection = 0
    White_Turn_Selection = 1
    Black_Turn_No_Selection = 2
    Black_Turn_Selection = 3

class Pieces(Enum):
    No_Piece = 100
    White_Pawn_1 = 0
    White_Pawn_2 = 1
    White_Pawn_3 = 2
    White_Pawn_4 = 3
    White_Pawn_5 = 4
    White_Pawn_6 = 5
    White_Pawn_7 = 6
    White_Pawn_8 = 7
    White_Rook_1 = 8
    White_Rook_2 = 9
    White_Queen = 10
    White_King = 11
    White_Bishop_1 = 12
    White_Bishop_2 = 13
    White_Knight_1 = 14
    White_Knight_2 = 15
    Black_Pawn_1 = 16
    Black_Pawn_2 = 17
    Black_Pawn_3 = 18
    Black_Pawn_4 = 19
    Black_Pawn_5 = 20
    Black_Pawn_6 = 21
    Black_Pawn_7 = 22
    Black_Pawn_8 = 23
    Black_Rook_1 = 24
    Black_Rook_2 = 25
    Black_Queen = 26
    Black_King = 27
    Black_Bishop_1 = 28
    Black_Bishop_2 = 29
    Black_Knight_1 = 30
    Black_Knight_2 = 31
    