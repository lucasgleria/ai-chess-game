"""
AI module for chess game artificial intelligence.

This module contains the AI components:
- BaseChessAI: Abstract base class for all AI implementations
- EasyAI: Simple Minimax AI
- MediumAI: Medium difficulty AI with Alpha-Beta pruning
- StockfishAI: Integration with Stockfish engine
"""

# AI imports
try:
    import chess
    import chess.engine
except ImportError:
    print("Warning: python-chess not installed. Please install with: pip install python-chess")

# Version info
__version__ = "1.0.0"
__author__ = "Chess Game Team: Insert your name here"

# Export main classes (to be implemented)
__all__ = [
    "BaseChessAI",
    "EasyAI",
    "MediumAI", 
    "StockfishAI"
]

# Placeholder classes (to be implemented)
class BaseChessAI:
    """Abstract base class for all chess AI implementations."""
    
    def get_best_move(self, board):
        """Get the best move for the given board position."""
        raise NotImplementedError("Subclasses must implement get_best_move")

class EasyAI(BaseChessAI):
    """Simple AI using basic Minimax algorithm."""
    pass

class MediumAI(BaseChessAI):
    """Medium difficulty AI using Minimax with Alpha-Beta pruning."""
    pass

class StockfishAI(BaseChessAI):
    """AI using Stockfish chess engine."""
    pass 