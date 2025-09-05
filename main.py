import pygame
import sys
import chess
import json
import os
from src.ui.board_renderer import BoardRenderer
from src.ui.asset_manager import AssetManager
from src.ui.audio_manager import AudioManager
from src.ia.easy_ai import EasyAI
from src.ia.medium_ai import MediumAI
from src.ia.stockfish_ai import StockfishAI
from src.data.Save_Manager import SaveManager
from src.core.chess_game import ChessGame
from src.ui.Game_modes import GameModes 
import ctypes


CONFIG_PATH = "config.json"
DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" # Initial FEN for a standard board

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {"selected_ai": "stockfish", "skill_level": 8, "thinking_time": 1.5}

def save_config(selected_ai, skill_level, thinking_time):
    with open(CONFIG_PATH, "w") as f:
        json.dump({
            "selected_ai": selected_ai,
            "skill_level": skill_level,
            "thinking_time": thinking_time
        }, f)

def run_main():
    # Initialize Pygame and the audio mixer once here
    pygame.init()
    pygame.mixer.init()

    # Get screen dimensions
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    # Create the main Pygame screen (window)
    screen = pygame.display.set_mode((screen_w, screen_h - 10), pygame.RESIZABLE)
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
    pygame.display.set_caption("AI Chess Game")

    # Instance of SaveManager to be used in the menu
    save_manager_instance = SaveManager()
    asset_manager = AssetManager()

    # Start the main loop of the game modes menu
    # We pass the 'screen' surface and the 'save_manager_instance' instance
    # to the GameModes class, which will now manage the main menu.
    GameModes(screen, save_manager_instance, asset_manager) 

    # Quit Pygame only when the main program finishes completely
    pygame.quit() 
    sys.exit() # Ensures the program is terminated

if __name__ == "__main__":
    run_main()