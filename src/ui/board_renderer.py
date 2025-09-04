import pygame
import chess
import re 
from src.core.move_validator import MoveValidator 

class PromotionDialog:
    """
    Pop-up dialog for pawn promotion piece selection.
    """
    def __init__(self, screen, square_size, asset_manager, is_white_pawn):
        self.screen = screen
        self.square_size = square_size
        self.asset_manager = asset_manager
        
        # Chess-themed colors
        self.CHESS_BROWN = (139, 69, 19)
        self.CHESS_CREAM = (245, 245, 220)
        self.CHESS_DARK = (47, 79, 79)
        self.CHESS_GOLD = (255, 215, 0)
        self.CHESS_SILVER = (192, 192, 192)
        self.CHESS_LIGHT = (240, 248, 255)
        
        # Piece options for promotion
        self.pieces = ['queen', 'rook', 'bishop', 'knight']
        
        # Calculate dialog dimensions and position
        dialog_width = 400
        dialog_height = 150
        dialog_x = (screen.get_width() - dialog_width) // 2
        dialog_y = (screen.get_height() - dialog_height) // 2
        
        # Create piece selection buttons with improved positioning
        button_width = 60
        button_height = 60
        spacing = 20
        start_x = dialog_x + (dialog_width - (len(self.pieces) * (button_width + spacing) - spacing)) // 2
        
        self.piece_buttons = []
        for i, piece in enumerate(self.pieces):
            x = start_x + i * (button_width + spacing)
            y = dialog_y + 60
            self.piece_buttons.append({
                'rect': pygame.Rect(x, y, button_width, button_height),
                'piece': piece,
                'asset_name': f"{'white' if is_white_pawn else 'black'}_{piece}"
            })
    
    def draw(self):
        """Draw the promotion dialog with improved chess theme and positioning."""
        # Create semi-transparent overlay with chess pattern
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        
        # Add chess board pattern to overlay
        pattern_size = 40
        for y in range(0, self.screen.get_height(), pattern_size):
            for x in range(0, self.screen.get_width(), pattern_size):
                color = self.CHESS_BROWN if (x + y) // pattern_size % 2 == 0 else self.CHESS_CREAM
                pattern_surface = pygame.Surface((pattern_size, pattern_size), pygame.SRCALPHA)
                pattern_surface.fill((*color, 30))
                overlay.blit(pattern_surface, (x, y))
        
        self.screen.blit(overlay, (0, 0))
        
        # Draw main dialog box with improved positioning
        dialog_width = 400
        dialog_height = 150
        dialog_x = (self.screen.get_width() - dialog_width) // 2
        dialog_y = (self.screen.get_height() - dialog_height) // 2
        
        # Draw dialog background with chess theme
        pygame.draw.rect(self.screen, self.CHESS_DARK, (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=15)
        pygame.draw.rect(self.screen, self.CHESS_GOLD, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=15)
        
        # Draw title
        title_font = pygame.font.SysFont(None, 36, bold=True)
        title_text = title_font.render("Choose Promotion Piece", True, self.CHESS_GOLD)
        title_rect = title_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 25))
        self.screen.blit(title_text, title_rect)
        
        # Draw piece selection buttons with improved spacing
        button_width = 60
        button_height = 60
        spacing = 20
        start_x = dialog_x + (dialog_width - (len(self.pieces) * (button_width + spacing) - spacing)) // 2
        
        for i, button in enumerate(self.pieces):
            x = start_x + i * (button_width + spacing)
            y = dialog_y + 60
            
            # Draw button background
            pygame.draw.rect(self.screen, self.CHESS_SILVER, button['rect'], border_radius=8)
            pygame.draw.rect(self.screen, self.CHESS_GOLD, button['rect'], 2, border_radius=8)
            
            # Draw piece image
            if hasattr(self.asset_manager, 'get_piece'):
                piece_image = self.asset_manager.get_piece(button['asset_name'])
                if piece_image:
                    # Scale image to fit button
                    scaled_image = pygame.transform.scale(piece_image, (button_width - 10, button_height - 10))
                    image_rect = scaled_image.get_rect(center=button['rect'].center)
                    self.screen.blit(scaled_image, image_rect)
    
    def handle_click(self, pos):
        """Handle mouse click on the dialog."""
        # Adjust position for dialog surface
        adjusted_pos = (pos[0] - self.dialog_x, pos[1] - self.dialog_y)
        
        for button in self.piece_buttons:
            if button['rect'].collidepoint(adjusted_pos):
                self.selected_piece = button['piece']
                return True  # Dialog should close
        
        return False  # Dialog should stay open
    
    def get_selected_piece(self):
        """Return the selected piece for promotion."""
        return self.selected_piece

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
        
        # Promotion dialog state
        self.promotion_dialog = None
        self.pending_promotion_move = None

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

    # Draws a centered message at the top of the board with chess theme
    def draw_status_message(self, message):
        """Draw status message with improved positioning and styling"""
        # Create a semi-transparent background for better readability
        font = pygame.font.SysFont(None, 32, bold=True)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        
        # Position at the top center of the board
        board_offset_x = (self.screen.get_width() - 8 * self.square_size) // 2
        board_offset_y = (self.screen.get_height() - 8 * self.square_size) // 2
        
        # Create background rectangle for better visibility
        padding = 10
        bg_rect = pygame.Rect(
            board_offset_x + (8 * self.square_size - text_rect.width) // 2 - padding,
            board_offset_y - 50,  # Position above the board
            text_rect.width + 2 * padding,
            text_rect.height + 2 * padding
        )
        
        # Draw semi-transparent background
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(bg_surface, bg_rect)
        
        # Draw border
        pygame.draw.rect(self.screen, (255, 215, 0), bg_rect, 2, border_radius=8)
        
        # Draw text
        text_rect.center = bg_rect.center
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

                    highlight_color = (255, 215, 0, 120) # Semi-transparent gold
                    s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                    s.fill(highlight_color)

                    if r == from_row_last and c == from_col_last:
                        self.screen.blit(s, (c * self.square_size, r * self.square_size))
                    if r == to_row_last and c == to_col_last:
                        self.screen.blit(s, (c * self.square_size, r * self.square_size))

                # Highlight selected square
                if self.selected_square and self.selected_square == (r, c):
                    pygame.draw.rect(self.screen, (255, 215, 0), rect, 4) # Gold border

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
                pygame.draw.circle(self.screen, (34, 139, 34, 150), center, radius) # Semi-transparent forest green

        # Displays status messages at the top - Improved positioning
        if self.chess_game.board.is_checkmate():
            message = "Checkmate!"
        elif self.chess_game.board.is_stalemate() or self.chess_game.board.is_insufficient_material():
            message = "Draw!"
        elif self.chess_game.board.is_check():
            message = "Check!"
        else:
            message = "Black's Turn" if self.chess_game.board.turn == chess.BLACK else "White's Turn"

        self.draw_status_message(message)
        
        # Note: Promotion dialog is now drawn on the main screen in main.py

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

            # Check if this is a pawn promotion move
            piece = self.chess_game.board.piece_at(chess.parse_square(from_uci))
            is_promotion = False
            if piece and piece.piece_type == chess.PAWN:
                if (piece.color == chess.WHITE and target_row == 0) or \
                   (piece.color == chess.BLACK and target_row == 7):
                    is_promotion = True

            if is_promotion:
                # Store the pending promotion move and show dialog
                self.pending_promotion_move = move_uci
                self.promotion_dialog = PromotionDialog(
                    self.screen, 
                    self.square_size, 
                    self.asset_manager, 
                    piece.color == chess.WHITE
                )
            else:
                # Regular move processing
                self._process_move(move_uci)

        # Clears drag and selection state
        self.selected_square = None
        self.dragging_piece = None
        self.dragging_piece_original_pos = None

    def _process_move(self, move_uci):
        """Process a move and apply it to the board."""
        if self.chess_game.is_legal_move(move_uci):
            # Checks if a capture occurred before making the move
            captured_piece_before_move = self.chess_game.board.piece_at(chess.parse_square(move_uci[2:4]))

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

    def handle_promotion_click(self, pos):
        """Handle clicks when promotion dialog is active."""
        if self.promotion_dialog:
            if self.promotion_dialog.handle_click(pos):
                # User selected a piece, complete the promotion
                selected_piece = self.promotion_dialog.get_selected_piece()
                promotion_move = self.pending_promotion_move + selected_piece[0]  # Add piece letter
                
                self._process_move(promotion_move)
                
                # Clear promotion state
                self.promotion_dialog = None
                self.pending_promotion_move = None
                return True  # Indicate that the click was handled
        return False  # Indicate that the click was not handled

    def is_promotion_active(self):
        """Check if promotion dialog is currently active."""
        return self.promotion_dialog is not None

    def draw_promotion_dialog(self):
        """Draw the promotion dialog if active."""
        if self.promotion_dialog:
            self.promotion_dialog.draw()

    def update_mouse_pos(self, pos):
        self.mouse_pos = pos
        
    def to_chess_square(self, row, col):
        # This function was moved inside the BoardRenderer class
        # to resolve the AttributeError
        files = 'abcdefgh'  # columns
        ranks = '87654321'  # rows (0 is rank 8)
        return files[col] + ranks[row]