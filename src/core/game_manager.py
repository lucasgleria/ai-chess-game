"""
Manages the chess game flow and state transitions.
"""
from .chess_game import ChessGame
from .move_validator import MoveValidator

class GameManager:
    """
    Controls the main game flow, initialization, and execution loop.
    """
    def __init__(self):
        self.current_game = ChessGame()
        self.move_validator = MoveValidator(self.current_game)

    def start_game(self):
        while not self.current_game.board.is_game_over():
            should_end = self.move_validator.validate_move()
            if should_end:
                break 