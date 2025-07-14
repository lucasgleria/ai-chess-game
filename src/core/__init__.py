"""
Core module for chess game logic.

This module contains the main game logic classes:
- ChessGame: Main game state management
- GameManager: Game flow control
- MoveValidator: Move validation logic
"""

# Core game logic imports
try:
    import chess
except ImportError:
    print("Warning: python-chess not installed. Please install with: pip install python-chess")

# Version info
__version__ = "1.0.0"
__author__ = "Chess Game Team: Insert your name here"

# Export main classes (to be implemented)
__all__ = [
    "ChessGame",
    "GameManager", 
    "MoveValidator"
]

# Placeholder classes (to be implemented)
#Initialize the chess game state.
class ChessGame:

    def __init__(self):
        self.board = chess.Board()

    def end_game(self, result: str):
        self.result = result
        print(f"\n🛑 Game Over: {self.result}")
        


#Manages game flow and state transitions.
class GameManager:

    def __init__(self):
        self.current_game = ChessGame()
        self.move_validator = MoveValidator()

    def start_game(self):
        while not self.current_game.board.is_game_over():
            should_end = self.move_validator.validate_move()
            if should_end:
                break

#Validates chess moves and game rules.
class MoveValidator:
    
    def __init__(self):
        self.current_game = ChessGame()
        self.move = None

    def validate_move(self):
        print(self.current_game.board)
        if self.current_game.board.is_checkmate():
            print("Checkmate!")
            self.winner = "Black" if self.current_game.board.turn == chess.WHITE else "White"
            self.current_game.end_game(f"{self.winner} wins by checkmate")
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
        
        else:
            self.move = input("Enter your move in UCI format (e.g., e2e4): ")
            if self.move == "undo":
                if self.current_game.board.move_stack:
                    self.current_game.board.pop()
                    print("Last move undone.")

                else:
                    print("No moves to undo.")
            self.user_move = chess.Move.from_uci(self.move)
            # Check if the move is legal
            if self.user_move in self.current_game.board.legal_moves:
                self.current_game.board.push(self.user_move)
            else:
                print("Illegal move, try again.")
        
        return False
        

GameManager().start_game()  # Start the game loop