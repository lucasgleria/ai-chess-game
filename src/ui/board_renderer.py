import pygame
import chess
import re 
from src.core.move_validator import MoveValidator 

class BoardRenderer():
    def __init__(self, screen, square_size, chess_game_instance, local, asset_manager=None, audio_manager=None):
        self.screen = screen
        self.square_size = square_size
        self.asset_manager = asset_manager
        self.audio_manager = audio_manager
        self.local = local # Indicates if it's a local game (Player vs Player)

        # NOW, self.chess_game RECEIVES THE ALREADY CREATED INSTANCE FROM main.py
        self.chess_game = chess_game_instance
        # Instance of MoveValidator using the same ChessGame instance
        self.move_val = MoveValidator(self.chess_game)

        # Font for status messages
        self.status_font = pygame.font.SysFont("Arial", 28, bold=True)

        # Chessboard colors
        self.light_color = (240, 217, 181)  # light color
        self.dark_color = (181, 136, 99)    # dark color

        self.selected_square = None # (row, col) of the selected piece
        self.dragging_piece = None  # Symbol of the piece being dragged
        self.dragging_piece_original_pos = None # (row, col) original of the dragged piece
        self.drag_offset_x = 0      # X offset of the mouse relative to the top-left corner of the piece
        self.drag_offset_y = 0      # Y offset of the mouse relative to the top-left corner of the piece
        self.mouse_pos = (0, 0)     # Current mouse position on the screen

        self.last_move = None # To highlight the last move

        # Mapping of FEN symbols to asset names
        self.piece_map = {
            'r': "black_rook", 'n': "black_knight", 'b': "black_bishop",
            'q': "black_queen", 'k': "black_king", 'p': "black_pawn",
            
            'R': "white_rook", 'N': "white_knight", 'B': "white_bishop",
            'Q': "white_queen", 'K': "white_king", 'P': "white_pawn"
        }

        # Loads pieces based on the current FEN of chess_game
        self.load_pieces()

    def load_pieces(self):
        # Creates a 2D representation of the board for rendering in Pygame.
        # This is different from chess.Board, it's just for the visual state.
        self.test_board = [[None for _ in range(8)] for _ in range(8)]
        # Gets the FEN of the actual board from chess_game
        current_fen = self.chess_game.board.fen()
        # Splits the FEN to get the piece part
        fen_parts = current_fen.split(' ')[0]
        
        row_idx = 0
        col_idx = 0
        for char in fen_parts:
            if char == '/':
                row_idx += 1
                col_idx = 0
            elif char.isdigit():
                col_idx += int(char)
            else:
                # Uses self.piece_map to get the asset name
                self.test_board[row_idx][col_idx] = self.piece_map.get(char)
                col_idx += 1

    # Draws a centered message at the top of the board
    def draw_status_message(self, message, color=(255, 255, 255)):
        text_surface = self.status_font.render(message, True, color)
        screen_width = self.screen.get_width()
        text_rect = text_surface.get_rect(center=(screen_width // 2, 30))
        self.screen.blit(text_surface, text_rect)

    def draw_board(self):
        # Draws the board (8x8) alternating square colors
        for r in range(8):
            for c in range(8):
                color = self.light_color if (r + c) % 2 == 0 else self.dark_color
                rect = pygame.Rect(c * self.square_size, r * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, color, rect)

                # Highlight the last move
                if self.last_move:
                    from_square_uci = self.last_move[:2]
                    to_square_uci = self.last_move[2:4]
                    
                    # Converts UCI to Pygame row/column coordinates
                    from_col_last = chess.parse_square(from_square_uci) % 8
                    from_row_last = 7 - (chess.parse_square(from_square_uci) // 8)
                    to_col_last = chess.parse_square(to_square_uci) % 8
                    to_row_last = 7 - (chess.parse_square(to_square_uci) // 8)

                    highlight_color = (200, 200, 0, 100) # Semi-transparent yellow
                    s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                    s.fill(highlight_color)

                    if r == from_row_last and c == from_col_last:
                        self.screen.blit(s, (c * self.square_size, r * self.square_size))
                    if r == to_row_last and c == to_col_last:
                        self.screen.blit(s, (c * self.square_size, r * self.square_size))

                # Highlight selected square
                if self.selected_square and self.selected_square == (r, c):
                    pygame.draw.rect(self.screen, (255, 255, 0), rect, 3) # Yellow, 3px border

                # Draw pieces
                piece_symbol = self.test_board[r][c]
                # Does not draw the piece being dragged in its original position
                if piece_symbol and (r, c) != self.dragging_piece_original_pos:
                    piece_image = self.asset_manager.get_piece(piece_symbol)
                    if piece_image:
                        self.screen.blit(piece_image, (c * self.square_size, r * self.square_size))

        # Draw the dragged piece last, on top of everything
        if self.dragging_piece:
            x, y = pygame.mouse.get_pos()
            # Adjusts the dragged piece's position to the board surface
            # Considers the board's offset on the main screen
            board_offset_x = (self.screen.get_width() - 8 * self.square_size) // 2
            board_offset_y = (self.screen.get_height() - 8 * self.square_size) // 2 # Might be different if the menu is at the top

            piece_image = self.asset_manager.get_piece(self.dragging_piece)
            if piece_image:
                # The position of the dragged piece is the mouse position minus the drag offset,
                # minus the board's offset on the screen so it stays within the board area.
                self.screen.blit(piece_image, (x - self.drag_offset_x - board_offset_x, y - self.drag_offset_y - board_offset_y))

        # Highlight valid moves for the selected piece
        if self.selected_square:
            for move_row, move_col in self.chess_game.get_legal_moves_from(self.to_chess_square(self.selected_square[0], self.selected_square[1])):
                center = (
                    move_col * self.square_size + self.square_size // 2,
                    move_row * self.square_size + self.square_size // 2,
                )
                radius = self.square_size // 6
                pygame.draw.circle(self.screen, (0, 255, 0, 100), center, radius) # Semi-transparent green

        # Displays status messages at the top
        if self.chess_game.board.is_checkmate():
            message = "Checkmate!"
        elif self.chess_game.board.is_stalemate() or self.chess_game.board.is_insufficient_material():
            message = "Draw!"
        elif self.chess_game.board.is_check():
            message = "Check!"
        else:
            message = "Black's Turn" if self.chess_game.board.turn == chess.BLACK else "White's Turn"

        self.draw_status_message(message)

    def handle_click(self, pos):
        col = pos[0] // self.square_size
        row = pos[1] // self.square_size
        
        # Converts to python-chess notation
        chess_square = chess.square(col, 7 - row)
        
        # Checks if the clicked square has a piece of the current turn's color
        piece = self.chess_game.board.piece_at(chess_square)
        if piece and piece.color == self.chess_game.board.turn:
            self.selected_square = (row, col)
            self.dragging_piece = self.test_board[row][col]
            self.dragging_piece_original_pos = (row, col) # Stores the original position of the dragged piece
            
            # Adjusts the offset for the mouse position relative to the piece
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # We need to consider the board's offset on the main screen for correct calculation
            board_offset_x = (self.screen.get_width() - 8 * self.square_size) // 2
            board_offset_y = (self.screen.get_height() - 8 * self.square_size) // 2

            self.drag_offset_x = (mouse_x - board_offset_x) - (col * self.square_size)
            self.drag_offset_y = (mouse_y - board_offset_y) - (row * self.square_size)
        else:
            self.selected_square = None
            self.dragging_piece = None
            self.dragging_piece_original_pos = None


    def start_drag(self, pos):
        # The drag start logic is already in handle_click
        pass

    def end_drag(self, pos):
        if self.selected_square:
            target_col = pos[0] // self.square_size
            target_row = pos[1] // self.square_size

            from_row, from_col = self.selected_square
            from_uci = chess.square_name(chess.square(from_col, 7 - from_row))
            to_uci = chess.square_name(chess.square(target_col, 7 - target_row))

            move_uci = from_uci + to_uci

            # Promotion logic (simple example: always queen)
            # Checks if the piece is a pawn and is on the last rank
            piece = self.chess_game.board.piece_at(chess.parse_square(from_uci))
            if piece and piece.piece_type == chess.PAWN:
                if (piece.color == chess.WHITE and target_row == 0) or \
                   (piece.color == chess.BLACK and target_row == 7):
                    move_uci += 'q' # Promotes to queen by default

            if self.chess_game.is_legal_move(move_uci):
                # Checks if a capture occurred before making the move
                captured_piece_before_move = self.chess_game.board.piece_at(chess.parse_square(to_uci))

                self.chess_game.make_move(move_uci) # Applies the move to the main board
                self.last_move = move_uci # Stores the last move for highlighting
                self.load_pieces() # Reloads pieces to reflect the new state

                # Plays move or capture sound
                if self.audio_manager:
                    if captured_piece_before_move:
                        self.audio_manager.play("capture")
                    else:
                        self.audio_manager.play("move")
                
                # Calls MoveValidator to check game state
                self.move_val.validate_move() # THIS IS THE CRITICAL LINE!
            else:
                # Illegal move, the piece will be redrawn in the original position
                pass

        # Clears drag and selection state
        self.selected_square = None
        self.dragging_piece = None
        self.dragging_piece_original_pos = None
        # self.valid_moves = [] # No need to clear here, it's cleared in handle_click if selection changes

    def update_mouse_pos(self, pos):
        self.mouse_pos = pos
        
    def to_chess_square(self, row, col):
        # This function was moved inside the BoardRenderer class
        # to resolve the AttributeError
        files = 'abcdefgh'  # columns
        ranks = '87654321'  # rows (0 is rank 8)
        return files[col] + ranks[row]