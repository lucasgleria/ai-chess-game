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
class ChessGame:
    """Main chess game class that manages game state."""
    pass

class GameManager:
    """Manages game flow and state transitions."""
    pass

class MoveValidator:
    """Validates chess moves and game rules."""
    pass 