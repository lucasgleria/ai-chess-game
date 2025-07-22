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
        
        # Fonte para mensagens de status | Font for status messages
        self.status_font = pygame.font.SysFont("Arial", 28, bold=True)

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
        
        self.valid_moves = []  # List to store valid moves for the selected piece
        self.last_move = None
    
    # Desenha uma mensagem centralizada no topo do tabuleiro | Draws a centered message at the top of the board
    def draw_status_message(self, message, color=(255, 255, 255)):
        text_surface = self.status_font.render(message, True, color)
        screen_width = self.screen.get_width()  # Pega a largura total da tela | Get screen width
        text_rect = text_surface.get_rect(center=(screen_width // 2, 30))  # Centraliza na tela inteira
        self.screen.blit(text_surface, text_rect)

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
                    # Adjust the piece scale
                    scaled_image = pygame.transform.smoothscale(image, (int(self.square_size * 0.8), int(self.square_size * 0.8)))
                    image_rect = scaled_image.get_rect(center=rect.center)
                    self.screen.blit(scaled_image, image_rect.topleft)
                
                # Mostra mensagens de status na parte superior | Show status messages at the top
                if self.chess_game.board.is_checkmate():
                    message = "Checkmate!"
                elif self.chess_game.board.is_stalemate() or self.chess_game.board.is_insufficient_material():
                    message = "Draw!"
                elif self.chess_game.board.is_check():
                    message = "Check!"
                else:
                    message = "Black's Turn" if self.turn else "White's Turn"

                self.draw_status_message(message)

                # Draws selected square highlight
                if self.selected_square == (row, col):
                    pygame.draw.rect(self.screen, (255, 255, 0), rect, 4)  # yellow, 4px border
                    
        # If dragging a piece, draw it at the current mouse position
        if self.dragging_piece and self.asset_manager:
            image = self.asset_manager.get_piece(self.dragging_piece)
            if image:
                scaled_image = pygame.transform.smoothscale(image, (int(self.square_size * 0.8), int(self.square_size * 0.8)))
                pos = (self.mouse_pos[0] - self.dragging_offset[0], self.mouse_pos[1] - self.dragging_offset[1])
                self.screen.blit(scaled_image, pos)
                
        # Higlight valid moves for the selected piece
        for move_row, move_col in self.valid_moves:
            center = (
                move_col * self.square_size + self.square_size // 2,
                move_row * self.square_size + self.square_size // 2,
            )
            radius = self.square_size // 6
            pygame.draw.circle(self.screen, (0, 255, 0), center, radius)

        # Destaca o último movimento (se houver)
        if self.last_move:
            from_sq = self.last_move[:2]
            to_sq = self.last_move[2:]

            for sq in [from_sq, to_sq]:
                col = 'abcdefgh'.index(sq[0])
                row = '87654321'.index(sq[1])
                rect = pygame.Rect(
                    col * self.square_size,
                    row * self.square_size,
                    self.square_size,
                    self.square_size
                )
                pygame.draw.rect(self.screen, (255, 165, 0, 0.5), rect, 4)
    
    def handle_click(self, mouse_pos):
        
        # Detects which square was clicked and stores it as selected
        col = mouse_pos[0] // self.square_size
        row = mouse_pos[1] // self.square_size

        # Selection Toggle: select or unmark the square
        if self.selected_square == (row, col):
            self.selected_square = None
            self.valid_moves = []  # Clear valid moves if unselecting
        else:
            self.selected_square = (row, col)
            square_str = self.to_chess_square(row, col)
            self.valid_moves = self.chess_game.get_legal_moves_from(square_str)

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
    
    # Toca som se o audio_manager estiver disponível
    def play_sound(self, sound_type):  # sound_type: "move", "capture", etc.
        if self.audio_manager:
            self.audio_manager.play(sound_type)
  
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
            if self.chess_game.is_legal_move(self.pos) and self.turn == False:  # noqa: E712
                captured_piece = self.test_board[self.new_row][self.new_col]
                self.test_board[self.new_row][self.new_col] = self.dragging_piece
                self.chess_game.make_move(self.pos)
                self.turn = True
                self.last_move = self.pos  # armazena o último movimento
                if self.audio_manager:
                    # Verifica se foi captura
                    if captured_piece:
                        self.audio_manager.play("capture")
                    else:
                        self.audio_manager.play("move")
                    if self.chess_game.is_checkmate():
                        self.audio_manager.play("checkmate")
    
            # If the move is illegal, put the piece back to its original position
            else:
                self.test_board[self.row][self.col] = self.dragging_piece

            # If the move is checkmate, stalemate, ect.
            self.move_val.validate_move()
                
            # Clear the dragging state
            self.dragging_piece = None
            self.selected_square = None   
            self.valid_moves = []  # Clear valid moves after dragging

    def update_mouse_pos(self, pos):
        self.mouse_pos = pos
        
    def animate_piece_movement(self, piece, start_pos, end_pos, duration=300):
        """
        Anima o movimento suave de uma peça no tabuleiro | Animate smooth movement of a piece
        > piece: peça a ser animada | piece to animate
        > start_pos: posição inicial (linha, coluna) | starting position (row, col)
        > end_pos: posição final (linha, coluna) | ending position (row, col)
        > duration: duração da animação em ms | animation duration in milliseconds
        """
        start_x = start_pos[1] * self.square_size
        start_y = start_pos[0] * self.square_size
        end_x = end_pos[1] * self.square_size
        end_y = end_pos[0] * self.square_size

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while True:
            elapsed = pygame.time.get_ticks() - start_time
            progress = min(1, elapsed / duration)

            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress

            self.draw_board()
            if piece:
                piece_img = self.asset_manager.piece_images.get(piece, self.default_piece)
                if piece_img:
                    piece_img = pygame.transform.scale(piece_img, (self.square_size, self.square_size))
                    self.screen.blit(piece_img, (current_x, current_y))
                
            pygame.display.flip()
            clock.tick(60)

            if progress >= 1:
                break