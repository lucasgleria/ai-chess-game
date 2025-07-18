# src/ui/board_renderer.py

import pygame
from src.core.chess_game import ChessGame
from src.core.move_validator import MoveValidator


class BoardRenderer:
    def __init__(self, screen, square_size, asset_manager=None, audio_manager=None):

        self.screen = screen # screen: surface where the board will be drawn
        self.square_size = square_size # square_size: size (in pixels/px) of each square on the board
        self.asset_manager = asset_manager # asset_manager: instance of AssetManager to load and manage piece images
        self.audio_manager = audio_manager  # AudioManager instance for sound effects, if needed
        self.chess_game = ChessGame()  # Instance of ChessGame to manage game state
        self.move_val = MoveValidator(self.chess_game)


        # Chessboard colors
        self.light_color = (240, 217, 181)  # light color
        self.dark_color = (181, 136, 99)    # dark color
        
        # Select and drag state variables
        self.selected_square = None
        self.dragging_piece = None
        self.dragging_offset = (0, 0)
        self.mouse_pos = (0, 0)
        self.row = None
        self.col = None
        self.row_ai = None
        self.col_ai = None
        self.new_row = None
        self.new_col = None
        self.new_row_ai = None
        self.new_col_ai = None
        self.pos = None
        self.turn = False  # Placeholder for boolean state, if needed

        # Chessboard test with pieces (AssetManager)
        self.test_board = [
            ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop", "black_knight", "black_rook"],
            ["black_pawn"] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ["white_pawn"] * 8,
            ["white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_bishop", "white_knight", "white_rook"]
        ]
        
        self.selected_square = None  # No piece selected initially

    def draw_board(self):
        
        # Draws the board (8x8) by alternating colors between light and dark squares
        
        for row in range(8):
            for col in range(8):
                # Alternates colors for the squares
                color = self.light_color if (row + col) % 2 == 0 else self.dark_color

                # Sets the position and size of the square
                rect = pygame.Rect(
                    col * self.square_size,
                    row * self.square_size,
                    self.square_size,
                    self.square_size
                )
                pygame.draw.rect(self.screen, color, rect)
                
                # Draws the piece if it exists in the test board
                piece = self.test_board[row][col]
                if piece and self.asset_manager:
                    image = self.asset_manager.get_piece(piece)
                    if image:
                        image_rect = image.get_rect(center=rect.center)
                        self.screen.blit(image, image_rect.topleft)
                        
                # Draws selected square highlight
                if self.selected_square == (row, col):
                    pygame.draw.rect(self.screen, (255, 255, 0), rect, 4)  # yellow, 4px border
                    
        # If dragging a piece, draw it at the current mouse position
        if self.dragging_piece and self.asset_manager:
            image = self.asset_manager.get_piece(self.dragging_piece)
            if image:
                pos = (self.mouse_pos[0] - self.dragging_offset[0], self.mouse_pos[1] - self.dragging_offset[1])
                self.screen.blit(image, pos)



    def handle_click(self, mouse_pos):
        
        # Detects which square was clicked and stores it as selected
        col = mouse_pos[0] // self.square_size
        row = mouse_pos[1] // self.square_size

        # Selection Toggle: select or unmark the square
        if self.selected_square == (row, col):
            self.selected_square = None
        else:
            self.selected_square = (row, col)

    def to_chess_square(self, row, col):
        self.files = 'abcdefgh'  # columns
        self.ranks = '87654321'  # rows (0 is rank 8)
        return self.files[col] + self.ranks[row]

    def from_chess_square(self, square):
        files = 'abcdefgh'  # columns (file)
        ranks = '87654321'  # rows (rank from top to bottom)

        self.col_ai = files.index(square[0])   # 'a' → 0, 'b' → 1, ..., 'h' → 7
        self.row_ai = ranks.index(square[1])   # '8' → 0, '7' → 1, ..., '1' → 7
        self.new_row_ai = ranks.index(square[3])
        self.new_col_ai = files.index(square[2])

        return self.row_ai, self.col_ai, self.new_row_ai, self.new_col_ai

                
    def start_drag(self, mouse_pos):
        self.row = mouse_pos[1] // self.square_size
        self.col = mouse_pos[0] // self.square_size

        piece = self.test_board[self.row][self.col]
        if piece:
            self.selected_square = (self.row, self.col)
            self.dragging_piece = piece
            self.test_board[self.row][self.col] = None  # temporarily remove the piece from the board
            self.dragging_offset = (mouse_pos[0] % self.square_size, mouse_pos[1] % self.square_size)

    def deteremaine_drag(self):
        # Determines the new position of the piece being dragged
        self.pos = str(self.to_chess_square(self.row, self.col) + self.to_chess_square(self.new_row, self.new_col))

    def deterimine_ai(self):

        self.from_chess_square(self.row_ai), self.from_chess_square(self.col_ai),self.from_chess_square(self.new_row_ai), self.from_chess_square(self.new_col_ai)

    def end_drag(self, mouse_pos):
        if self.dragging_piece:
            self.new_row = mouse_pos[1] // self.square_size
            self.new_col = mouse_pos[0] // self.square_size
            self.deteremaine_drag()

            # If the move is legal, update the board
            if self.chess_game.is_legal_move(self.pos) and self.turn == False:
                self.test_board[self.new_row][self.new_col] = self.dragging_piece
                self.chess_game.make_move(self.pos)
                self.turn = True
                if self.audio_manager:
                    self.audio_manager.play("move")

            # If the move is illegal, put the piece back to its original position
            else:
                self.test_board[self.row][self.col] = self.dragging_piece

            # If the move is checkmate, stalemate, ect.
            self.move_val.validate_move()
                
            # Clear the dragging state
            self.dragging_piece = None
            self.selected_square = None
        
        

    def update_mouse_pos(self, pos):
        self.mouse_pos = pos