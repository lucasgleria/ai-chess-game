"""
Validates chess moves and game rules.
"""
from src.core.chess_game import ChessGame

class MoveValidator:
    """
    Responsible for validating moves and chess game rules.
    """
    def __init__(self, current_game: ChessGame):
        self.current_game = current_game
        self.move = None

    def validate_move(self):
        
        if self.current_game.board.is_checkmate():
            print("Checkmate!")
            winner = "Black" if self.current_game.board.turn else "White"
            self.current_game.end_game(f"{winner} wins by checkmate")
            return True
        elif self.current_game.board.is_seventyfive_moves():
            self.current_game.end_game("draw (75-move rule)")
            return True
        elif self.current_game.board.is_fivefold_repetition():
            self.current_game.end_game("draw (5-time repetition)")
            return True
        elif self.current_game.board.can_claim_fifty_moves():
            self.current_game.end_game("draw (50-move rule)")
            return True
        elif self.current_game.board.can_claim_threefold_repetition():
            self.current_game.end_game("draw (3-fold repetition)")
            return True
        elif self.current_game.board.is_stalemate():
            self.current_game.end_game("draw (stalemate)")
            return True
        elif self.current_game.board.is_insufficient_material():
            self.current_game.end_game("draw (insufficient material)")
            return True
        elif self.current_game.board.is_variant_draw():
            self.current_game.end_game("draw (variant-specific rule)")
            return True
        """else:
            move = input("Enter your move in UCI format (e.g., e2e4): ")
            if move == "undo":
                if self.current_game.board.move_stack:
                    self.current_game.board.pop()
                    print("Last move undone.")
                else:
                    print("No moves to undo.")
            else:
                user_move = self._parse_move(move)
                if user_move and user_move in self.current_game.board.legal_moves:
                    self.current_game.board.push(user_move)
                else:
                    print("Illegal move, try again.")"""
        return False

    def _parse_move(self, move_str):
        """
        Converts a UCI string into a python-chess Move object.
        """
        import chess
        try:
            return chess.Move.from_uci(move_str)
        except Exception:
            print("Invalid move format.")
            return None 