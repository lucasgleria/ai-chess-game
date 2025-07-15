# src/ui/board_renderer.py

import pygame

class BoardRenderer:
    def __init__(self, screen, square_size, asset_manager=None, audio_manager=None):

        self.screen = screen # screen: surface where the board will be drawn
        self.square_size = square_size # square_size: size (in pixels/px) of each square on the board
        self.asset_manager = asset_manager # asset_manager: instance of AssetManager to load and manage piece images
        self.audio_manager = audio_manager  # AudioManager instance for sound effects, if needed

        # Chessboard colors
        self.light_color = (240, 217, 181)  # light color
        self.dark_color = (181, 136, 99)    # dark color
        
        # Select and drag state variables
        self.selected_square = None
        self.dragging_piece = None
        self.dragging_offset = (0, 0)
        self.mouse_pos = (0, 0)

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
            
    def start_drag(self, mouse_pos):
        row = mouse_pos[1] // self.square_size
        col = mouse_pos[0] // self.square_size

        piece = self.test_board[row][col]
        if piece:
            self.selected_square = (row, col)
            self.dragging_piece = piece
            self.test_board[row][col] = None  # temporarily remove the piece from the board
            self.dragging_offset = (mouse_pos[0] % self.square_size, mouse_pos[1] % self.square_size)

    def end_drag(self, mouse_pos):
        if self.dragging_piece:
            new_row = mouse_pos[1] // self.square_size
            new_col = mouse_pos[0] // self.square_size

            # Update the board with the new position of the piece
            self.test_board[new_row][new_col] = self.dragging_piece

            # Clear the dragging state
            self.dragging_piece = None
            self.selected_square = None
        
        if self.audio_manager:
            self.audio_manager.play("move")


    def update_mouse_pos(self, pos):
        self.mouse_pos = pos