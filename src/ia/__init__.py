"""
AI module for chess game artificial intelligence.

This module contains the AI components:
- BaseChessAI: Abstract base class for all AI implementations
- EasyAI: Simple Minimax AI
- MediumAI: Medium difficulty AI with Alpha-Beta pruning
- StockfishAI: Integration with Stockfish engine (to be implemented)
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

# # Export main classes
from .ai_base import BaseChessAI
from .easy_ai import EasyAI
from .medium_ai import MediumAI
# from .stockfish_ai import StockfishAI  # quando implementado

__all__ = [
    "BaseChessAI",
    "EasyAI",
    "MediumAI",
    # "StockfishAI"
] 