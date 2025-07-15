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

# Export main classes 

from .board_renderer import BoardRenderer
from .asset_manager import AssetManager
from .audio_manager import AudioManager

__all__ = [
    "BoardRenderer",
    "AssetManager",
    "AudioManager"
]
