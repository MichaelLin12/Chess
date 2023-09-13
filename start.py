from abc import ABC, abstractmethod
import pygame
import utility


class Pieces(ABC):
    def __init__(self, x,y, image,color,direction, identity) -> None:
        super().__init__()
        self.identity = identity
        self.x = x
        self.y = y
        self.image = image
        self.color = color
        self.direction = direction
        self.captured = False
    
    @abstractmethod
    def getMoves(self,board):
        pass

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getImage(self):
        return self.image
    
    def getColor(self):
        return self.color
    
    def getDirection(self):
        return self.direction
    
    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setImage(self, image):
        self.image = image

    def setColor(self, color):
        self.color = color

    def setDirection(self, direction):
        self.direction = direction

    def isCaptured(self):
        return self.captured
    
    def setCaptured(self, captured):
        self.captured = captured
    
    def getIdentity(self):
        return self.identity


class Pawn(Pieces):
    def __init__(self, x,y, image,color,direction) -> None:
        super().__init__(x,y, image,color,direction, 'pawn')
        self.move = 0 # number of moves made by the pawn
        self.en_passant = True # en passant flag
    
    def getMoves(self,board):
        moves_list = []
        y_val = self.x - self.direction[0][1]
        x_val = self.y - self.direction[0][0]
        offset = 1
        opponent = 'black'
        if self.color == 'black':
            offset = -1
            opponent = 'white'


        if self.move == 0:
            if 0 <= y_val < 8 and 0 <= x_val < 8 and board[y_val][x_val] == None: # check if the pawn can move one square forward
                moves_list.append((y_val, x_val))
            if 0 <= y_val-offset < 8 and 0 <= x_val < 8 and board[y_val - offset][x_val] == None: # check if the pawn can move two squares forward
                moves_list.append((y_val - offset, x_val))
            if 0 <= y_val < 8 and 0 <= x_val+offset < 8 and board[y_val][x_val + offset] != None and board[y_val][x_val + offset].getIdentity() == opponent: # check if the pawn can capture a piece to the right
                moves_list.append((y_val, x_val + offset))
            if 0 <= y_val < 8 and 0 <= x_val-offset < 8 and board[y_val][x_val - offset] != None and board[y_val][x_val + offset].getIdentity() == opponent: # check if the pawn can capture a piece to the left
                moves_list.append((y_val, x_val - offset))
        return moves_list
    def getEnPassant(self):
        return self.en_passant
    
    def setEnPassant(self, en_passant):
        self.en_passant = en_passant

    def getMove(self):
        return self.move
    
    def setMove(self, move):
        self.move = move

class Rook(Pieces):
    def __init__(self, x,y, image,color) -> None:
        super().__init__(x,y, image,color,[(1,0), (-1,0), (0,1), (0,-1)], 'rook')
        self.move = 0 # number of moves made by the rook
    
    def getMoves(self,board):
        pass

    def getMove(self):
        return self.move
    
    def setMove(self, move):
        self.move = move

class Knight(Pieces):
    def __init__(self, x,y, image,color) -> None:
        super().__init__(x,y, image,color,[(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (-1,2), (1,-2), (-1,-2)],'knight')
    
    def getMoves(self,board):
        pass

class Bishop(Pieces):
    def __init__(self, x,y, image,color) -> None:
        super().__init__(x,y, image,color,[(1,1), (1,-1), (-1,1), (-1,-1)], 'bishop')
    
    def getMoves(self,board):
        pass

class King(Pieces):
    def __init__(self, x,y, image,color) -> None:
        super().__init__(x,y, image,color,[(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)],'king')
        self.move = 0 # number of moves made by the king
    
    def getMoves(self,board):
        pass

    def getMove(self,board):
        return self.move
    
    def setMove(self, move):
        self.move = move

class Queen(Pieces):
    def __init__(self, x,y, image,color) -> None:
        super().__init__(x,y, image,color,[(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)],'queen')
    
    def getMoves(self,board):
        pass

class Player:
    pass

class Game_Over:
    pass

class Game_History:
    pass

class Timer:
    pass

class Board:
    def __init__(self, square_length) -> None:
        self.board = [[None for i in range(8)] for j in range(8)] # 2d array of pieces
        self.white_moves = [] # all possible white moves
        self.black_moves = [] # all possible black moves
        self.square_length = square_length # length of a square in pixels
        self.history = Game_History() # game history object ; keeps track of moves
        self.done = Game_Over() # game over object ; keeps track of game over
        self.selection = utility.Pieces.No_Piece # keeps track of current piece selection
        self.selected_moves = [] # list of possible moves for the selected piece
        self.game_pieces = {} # dictionary of (locations:pieces) on the board
        self.board_length = len(self.board) # length of the board
        self.populate_board()
        self.set_piece_mapping() # mapping of utility pieces to actual pieces on game board
        self.selected_moves = []

    def draw_selection(self, screen):
        if self.selection != utility.Pieces.No_Piece:
            x = self.piece_mapping[self.selection].getX()
            y = self.piece_mapping[self.selection].getY()
            pygame.draw.rect(screen, 'red', [y * self.square_length + 1, x * self.square_length + 50 + 1, self.square_length, self.square_length], 2)
            for move in self.selected_moves:
                pygame.draw.circle(screen, 'red', (move[1] * 75 + 37.5, move[0] * 75 + 37.5 + 50), 5)

    # sets the possible selected moves based on the game piece, coordinates, and turn
    def set_selection(self, coords, turn):
        if coords in self.game_pieces and self.game_pieces[coords] != utility.Pieces.No_Piece:
            piece = self.game_pieces[coords]
            if turn == utility.Turn_Step.White_Turn_No_Selection and self.piece_mapping[piece].getColor() == 'white':
                self.selection = piece
                self.selected_moves = self.piece_mapping[self.selection].getMoves(self.board)
                if self.selected_moves == None:
                    self.selected_moves = []
            elif turn == utility.Turn_Step.Black_Turn_No_Selection and self.piece_mapping[piece].getColor() == 'black':
                self.selection = piece
                self.selected_moves = self.piece_mapping[self.selection].getMoves(self.board)
                if self.selected_moves == None:
                    self.selected_moves = []
            else:
                self.selection = utility.Pieces.No_Piece
                self.selected_moves = []
        else:
            self.selection = utility.Pieces.No_Piece
            self.selected_moves = []

    def get_selection(self):
        return self.selection
    
    def get_selected_moves(self):
        return self.selected_moves


    def set_piece_mapping(self):
        self.piece_mapping = {utility.Pieces.White_Pawn_1: Pawn(6,0, pygame.transform.scale(pygame.image.load('assets/images/white pawn.png'), (60, 60)), 'white', [(0,1)]), 
        utility.Pieces.White_Pawn_2: Pawn(6,1, pygame.transform.scale(pygame.image.load('assets/images/white pawn.png'), (60, 60)), 'white', [(0,1)]),
        utility.Pieces.White_Pawn_3: Pawn(6,2, pygame.transform.scale(pygame.image.load('assets/images/white pawn.png'), (60, 60)), 'white', [(0,1)]),
        utility.Pieces.White_Pawn_4: Pawn(6,3, pygame.transform.scale(pygame.image.load('assets/images/white pawn.png'), (60, 60)), 'white', [(0,1)]),
        utility.Pieces.White_Pawn_5: Pawn(6,4, pygame.transform.scale(pygame.image.load('assets/images/white pawn.png'), (60, 60)), 'white', [(0,1)]),
        utility.Pieces.White_Pawn_6: Pawn(6,5, pygame.transform.scale(pygame.image.load('assets/images/white pawn.png'), (60, 60)), 'white', [(0,1)]),
        utility.Pieces.White_Pawn_7: Pawn(6,6, pygame.transform.scale(pygame.image.load('assets/images/white pawn.png'), (60, 60)), 'white', [(0,1)]),
        utility.Pieces.White_Pawn_8: Pawn(6,7, pygame.transform.scale(pygame.image.load('assets/images/white pawn.png'), (60, 60)), 'white', [(0,1)]),
        utility.Pieces.White_Rook_1: Rook(7,0, pygame.transform.scale(pygame.image.load('assets/images/white rook.png'), (60, 60)), 'white'),
        utility.Pieces.White_Rook_2: Rook(7,7, pygame.transform.scale(pygame.image.load('assets/images/white rook.png'), (60, 60)), 'white'),
        utility.Pieces.White_Queen: Queen(7,3, pygame.transform.scale(pygame.image.load('assets/images/white queen.png'), (60, 60)), 'white'),
        utility.Pieces.White_King: King(7,4, pygame.transform.scale(pygame.image.load('assets/images/white king.png'), (60, 60)), 'white'),
        utility.Pieces.White_Bishop_1: Bishop(7,2, pygame.transform.scale(pygame.image.load('assets/images/white bishop.png'), (60, 60)), 'white'),
        utility.Pieces.White_Bishop_2: Bishop(7,5, pygame.transform.scale(pygame.image.load('assets/images/white bishop.png'), (60, 60)), 'white'),
        utility.Pieces.White_Knight_1: Knight(7,1, pygame.transform.scale(pygame.image.load('assets/images/white knight.png'), (60, 60)), 'white'),
        utility.Pieces.White_Knight_2: Knight(7,6, pygame.transform.scale(pygame.image.load('assets/images/white knight.png'), (60, 60)), 'white'),
        utility.Pieces.Black_Pawn_1: Pawn(1,0, pygame.transform.scale(pygame.image.load('assets/images/black pawn.png'), (60, 60)), 'black', [(0,-1)]),
        utility.Pieces.Black_Pawn_2: Pawn(1,1, pygame.transform.scale(pygame.image.load('assets/images/black pawn.png'), (60, 60)), 'black', [(0,-1)]),
        utility.Pieces.Black_Pawn_3: Pawn(1,2, pygame.transform.scale(pygame.image.load('assets/images/black pawn.png'), (60, 60)), 'black', [(0,-1)]),
        utility.Pieces.Black_Pawn_4: Pawn(1,3, pygame.transform.scale(pygame.image.load('assets/images/black pawn.png'), (60, 60)), 'black', [(0,-1)]),
        utility.Pieces.Black_Pawn_5: Pawn(1,4, pygame.transform.scale(pygame.image.load('assets/images/black pawn.png'), (60, 60)), 'black', [(0,-1)]),
        utility.Pieces.Black_Pawn_6: Pawn(1,5, pygame.transform.scale(pygame.image.load('assets/images/black pawn.png'), (60, 60)), 'black', [(0,-1)]),
        utility.Pieces.Black_Pawn_7: Pawn(1,6, pygame.transform.scale(pygame.image.load('assets/images/black pawn.png'), (60, 60)), 'black', [(0,-1)]),
        utility.Pieces.Black_Pawn_8: Pawn(1,7, pygame.transform.scale(pygame.image.load('assets/images/black pawn.png'), (60, 60)), 'black', [(0,-1)]),
        utility.Pieces.Black_Rook_1: Rook(0,0, pygame.transform.scale(pygame.image.load('assets/images/black rook.png'), (60, 60)), 'black'),
        utility.Pieces.Black_Rook_2: Rook(0,7, pygame.transform.scale(pygame.image.load('assets/images/black rook.png'), (60, 60)), 'black'),
        utility.Pieces.Black_Queen: Queen(0,3, pygame.transform.scale(pygame.image.load('assets/images/black queen.png'), (60, 60)), 'black'),
        utility.Pieces.Black_King: King(0,4, pygame.transform.scale(pygame.image.load('assets/images/black king.png'), (60, 60)), 'black'),
        utility.Pieces.Black_Bishop_1: Bishop(0,2, pygame.transform.scale(pygame.image.load('assets/images/black bishop.png'), (60, 60)), 'black'),
        utility.Pieces.Black_Bishop_2: Bishop(0,5, pygame.transform.scale(pygame.image.load('assets/images/black bishop.png'), (60, 60)), 'black'),
        utility.Pieces.Black_Knight_1: Knight(0,1, pygame.transform.scale(pygame.image.load('assets/images/black knight.png'), (60, 60)), 'black'),
        utility.Pieces.Black_Knight_2: Knight(0,6, pygame.transform.scale(pygame.image.load('assets/images/black knight.png'), (60, 60)), 'black')}

        # add each piece to the board
        for key in self.piece_mapping:
            piece = self.piece_mapping[key]
            self.board[piece.getX()][piece.getY()] = piece

    def populate_board(self):
        # add each utility.Piece piece to game pieces dictionary
        self.game_pieces[(0,0)] = utility.Pieces.Black_Rook_1
        self.game_pieces[(0,1)] = utility.Pieces.Black_Knight_1
        self.game_pieces[(0,2)] = utility.Pieces.Black_Bishop_1
        self.game_pieces[(0,3)] = utility.Pieces.Black_Queen
        self.game_pieces[(0,4)] = utility.Pieces.Black_King
        self.game_pieces[(0,5)] = utility.Pieces.Black_Bishop_2
        self.game_pieces[(0,6)] = utility.Pieces.Black_Knight_2
        self.game_pieces[(0,7)] = utility.Pieces.Black_Rook_2
        self.game_pieces[(1,0)] = utility.Pieces.Black_Pawn_1
        self.game_pieces[(1,1)] = utility.Pieces.Black_Pawn_2
        self.game_pieces[(1,2)] = utility.Pieces.Black_Pawn_3
        self.game_pieces[(1,3)] = utility.Pieces.Black_Pawn_4
        self.game_pieces[(1,4)] = utility.Pieces.Black_Pawn_5
        self.game_pieces[(1,5)] = utility.Pieces.Black_Pawn_6
        self.game_pieces[(1,6)] = utility.Pieces.Black_Pawn_7
        self.game_pieces[(1,7)] = utility.Pieces.Black_Pawn_8
        self.game_pieces[(6,0)] = utility.Pieces.White_Pawn_1
        self.game_pieces[(6,1)] = utility.Pieces.White_Pawn_2
        self.game_pieces[(6,2)] = utility.Pieces.White_Pawn_3
        self.game_pieces[(6,3)] = utility.Pieces.White_Pawn_4
        self.game_pieces[(6,4)] = utility.Pieces.White_Pawn_5
        self.game_pieces[(6,5)] = utility.Pieces.White_Pawn_6
        self.game_pieces[(6,6)] = utility.Pieces.White_Pawn_7
        self.game_pieces[(6,7)] = utility.Pieces.White_Pawn_8
        self.game_pieces[(7,0)] = utility.Pieces.White_Rook_1
        self.game_pieces[(7,1)] = utility.Pieces.White_Knight_1
        self.game_pieces[(7,2)] = utility.Pieces.White_Bishop_1
        self.game_pieces[(7,3)] = utility.Pieces.White_Queen
        self.game_pieces[(7,4)] = utility.Pieces.White_King
        self.game_pieces[(7,5)] = utility.Pieces.White_Bishop_2
        self.game_pieces[(7,6)] = utility.Pieces.White_Knight_2
        self.game_pieces[(7,7)] = utility.Pieces.White_Rook_2

    def draw_board(self, screen):
        y_offset = 50
        for i in range(32):
            column = i % 4
            row = i // 4
            # Draw rectangles
            if row % 2 == 0:
                pygame.draw.rect(screen, 'light gray', [450 - (column * self.square_length * 2) , row * self.square_length + y_offset, self.square_length, self.square_length])
            else:
                pygame.draw.rect(screen, 'light gray', [525 - (column * self.square_length * 2), row * self.square_length + y_offset, self.square_length, self.square_length])
            # Draw lines around rectangles
            for j in range(9):
                pygame.draw.line(screen, 'black', (0,self.square_length * j + y_offset) , (600, self.square_length * j + y_offset), 2)
                pygame.draw.line(screen, 'black', (self.square_length * j, 0 + y_offset), (self.square_length * j, 600 + y_offset), 2)
    def draw_pieces(self, screen):
        for location in self.game_pieces:
            piece = self.piece_mapping[self.game_pieces[location]]
            x = location[0] * self.square_length
            y = location[1] * self.square_length
            if piece.getIdentity() == 'pawn':
                screen.blit(piece.getImage(), (y + 5, x + 56))
            else:
                screen.blit(piece.getImage(), (y, x + 50))
    
    def is_valid_move(self, coords):
        if coords in self.selected_moves:
            return True
        return False

    def move_piece(self, coords):
        # coords are the cordinates we want to move to
        # we want to get the coordinates we want to move from
        print('Move piece', self.selection)
        piece = self.piece_mapping[self.selection] # the current selected location
        fr_coords = (piece.getY(), piece.getX()) # from coords
        # now we just have to update the piece and the board along with in game_pieces
        # we should update the game_board
        pass
    # populate white_moves and black_mvoes list with all possible moves of their respective color in the current board state
    def populate_all_moves(self):
        for key in self.piece_mapping:
            piece = self.piece_mapping[key]
            if piece.getColor() == 'white':
                self.white_moves.extend(piece.getMoves(self.board))
            else:
                self.black_moves.extend(piece.getMoves(self.board))


class Game:
    # constructor initializes a chess game
    def __init__(self, fps,  width, height, display_name) -> None:
        pygame.init()
        self.fps = fps
        self.font = pygame.font.Font('freesansbold.ttf',40)
        self.big_font = pygame.font.Font('freesansbold.ttf',20)
        self.Timer = Timer() # chess clock
        self.Board = Board(square_length=75)
        self.width = width # height of screen
        self.height = height # width of screen
        self.screen = pygame.display.set_mode([width, height])
        self.display_name = display_name
        pygame.display.set_caption(display_name)
        self.turn = utility.Turn_Step.White_Turn_No_Selection # current turn
        self.timer = pygame.time.Clock() # in game clock for redrawing window window
        self.counter = 0 # counter for fps
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
        

    def run_game_loop(self):
        running = True
        self.timer.tick(self.fps)
        while running:
            self.screen.fill((64, 64, 64))  # RGB value for dark gray
            self.Board.draw_board(self.screen)
            self.Board.draw_pieces(self.screen)
            self.Board.draw_selection(self.screen)
            if self.counter < 30:
                self.counter += 1
            else:
                self.counter = 0
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x_coord = event.pos[0] // self.Board.square_length
                    y_coord = ((event.pos[1]+25) // self.Board.square_length)-1
                    self.left_click(y_coord, x_coord)
                    break


            
            pygame.display.flip()
        pygame.quit()
    
    # Method is here to make the necessary action on a left click by the user
    # The right action depends on the user selection as well as the state of self.turn
    def left_click(self, y_coord, x_coord):
        validity = False # flag for checking if the move is valid
        if self.turn == utility.Turn_Step.White_Turn_No_Selection or self.turn == utility.Turn_Step.Black_Turn_No_Selection:
            self.Board.set_selection((y_coord,x_coord), self.turn)
        else: # a piece is selected already
            validity = self.Board.is_valid_move((y_coord,x_coord))
            print(validity)
            if not validity: # the move the player selected for the piece is not valid
                if self.turn == utility.Turn_Step.White_Turn_Selection:
                    self.turn = utility.Turn_Step.White_Turn_No_Selection
                elif self.turn == utility.Turn_Step.Black_Turn_Selection:
                    self.turn = utility.Turn_Step.Black_Turn_No_Selection
                self.Board.set_selection((y_coord,x_coord), self.turn)
            else: # the move the player selected for the piece is valid so move the piece there
                print('Valid Move', y_coord, x_coord)
                self.Board.move_piece((y_coord,x_coord))
        # update the players turn based on the current turn and validity of the move along with updating the board state
        if self.turn == utility.Turn_Step.White_Turn_No_Selection and self.Board.get_selection() != utility.Pieces.No_Piece:
            self.turn = utility.Turn_Step.White_Turn_Selection
        elif self.turn == utility.Turn_Step.White_Turn_Selection and validity:
            self.turn = utility.Turn_Step.Black_Turn_No_Selection
            validity = False
        elif self.turn == utility.Turn_Step.Black_Turn_No_Selection and self.Board.get_selection() != utility.Pieces.No_Piece:
            self.turn = utility.Turn_Step.Black_Turn_Selection
        elif self.turn == utility.Turn_Step.Black_Turn_Selection and validity:
            self.turn = utility.Turn_Step.White_Turn_No_Selection
            validity = False




if __name__ == '__main__':
    WIDTH = 800
    HEIGHT = 700
    FPS = 30
    display_name = 'Chess'
    game = Game(fps=FPS, width=WIDTH, height=HEIGHT,display_name=display_name)
    game.run_game_loop()