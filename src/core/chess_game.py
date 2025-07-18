"""
Main class for managing the chess game state.
Encapsulates a chess.Board object and methods for game manipulation.
"""

try:
    import chess
except ImportError:
    print("Warning: python-chess not installed. Please install with: pip install python-chess")

class ChessGame:
    """
    Manages the chessboard state and main game operations.
    """
    def __init__(self):
        self.board = chess.Board()
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
            return True
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