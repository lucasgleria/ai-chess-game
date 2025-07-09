"""
UI module for chess game interface.

This module contains the user interface components:
- BoardRenderer: Renders the chess board and pieces
- UIManager: Manages UI state and interactions
- Button: UI button components
- Menu: Menu system components
"""

# UI imports
try:
    import pygame
except ImportError:
    print("Warning: pygame not installed. Please install with: pip install pygame")

# Version info
__version__ = "1.0.0"
__author__ = "Chess Game Team: Insert your name here"

# Export main classes (to be implemented)
__all__ = [
    "BoardRenderer",
    "UIManager",
    "Button",
    "Menu"
]

# Placeholder classes (to be implemented)
class BoardRenderer:
    """Renders the chess board and pieces on screen."""
    pass

class UIManager:
    """Manages UI state and user interactions."""
    pass

class Button:
    """UI button component."""
    pass

class Menu:
    """Menu system for the game."""
    pass 