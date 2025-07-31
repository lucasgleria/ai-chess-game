"""
Main class for managing the chess game state.
Encapsulates a chess.Board object and methods for game manipulation.
"""
import chess

class ChessGame():
    """
    Manages the chessboard state and main game operations.
    """
    def __init__(self, FEN):
        self.board = chess.Board(FEN)
        self.result = None

    def new_game(self):
        """
        Resets the board for a new game.
        """
        self.board.reset()
        self.result = None

    def make_move(self, move_str):
        """
        Applies a move in UCI format (e.g., 'e2e4'). Returns True if the move is legal and applied.
        """
        move = chess.Move.from_uci(move_str)
        if move:
            self.board.push(move)

        return False

    def undo_move(self):
        """
        Undoes the last move, if possible.
        """
        if self.board.move_stack:
            self.board.pop()
            return True
        return False

    def is_legal_move(self, move_str):
        """
        Checks if the move in UCI format is legal in the current position.
        """
        move = self.uci_to_move(move_str)
        return move in self.board.legal_moves if move else False

    def is_checkmate(self):
        return self.board.is_checkmate()

    def is_stalemate(self):
        return self.board.is_stalemate()

    def is_game_over(self):
        return self.board.is_game_over()

    def outcome(self):
        return self.board.outcome()

    def get_legal_moves(self):
        """
        Returns a list of legal moves in UCI format.
        """
        return [move.uci() for move in self.board.legal_moves]
    
    def get_legal_moves_from(self, square_str):
        """
        Returns a list of destination squares (as (row, col)) for legal moves starting from the given square.
        Example: 'e2' -> [(5, 2), (4, 2)] (if those are legal)
        """
        moves = []
        from_square = chess.parse_square(square_str)
        
        for move in self.board.legal_moves:
            if move.from_square == from_square:
                to_row, to_col = divmod(move.to_square, 8)
                to_row = 7 - to_row  # <--- Inverted Row
                moves.append((to_row, to_col))
        
        return moves

    def uci_to_move(self, move_str):
        """
        Converts a UCI string to a python-chess Move object.
        """
        try:
            return chess.Move.from_uci(move_str)
        except Exception:
            return None

    def move_to_uci(self, move_obj):
        """
        Converts a python-chess Move object to a UCI string.
        """
        return move_obj.uci() if move_obj else None

    def end_game(self, result: str):
        """
        Ends the game and stores the result.
        """
        self.result = result
        print(f"\n🛑 Game Over: {self.result}") 