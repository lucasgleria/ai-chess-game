"""
Core module for chess game logic.

This module contains the main game logic classes:
- ChessGame: Main game state management
- GameManager: Game flow control
- MoveValidator: Move validation logic
"""

# Core module for chess game logic
# Expondo as principais classes do core
from .chess_game import ChessGame
from .game_manager import GameManager
from .move_validator import MoveValidator

__version__ = "1.0.0"
__author__ = "Chess Game Team: Insert your name here"

__all__ = [
    "ChessGame",
    "GameManager",
    "MoveValidator"
]