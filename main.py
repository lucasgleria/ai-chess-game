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
from src.data.save_manager import SaveManager
from src.core.chess_game import ChessGame
from src.ui import game_modes # Importa o módulo game_modes
import ctypes

# --- Configurações globais ---
CONFIG_PATH = "config.json"
DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" # FEN inicial de um tabuleiro padrão

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
    # Inicializa o Pygame e o mixer de áudio uma única vez aqui
    pygame.init()
    pygame.mixer.init()

    # Obtém as dimensões da tela
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    # Cria a tela principal do Pygame (janela)
    screen = pygame.display.set_mode((screen_w, screen_h - 10), pygame.RESIZABLE)
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
    pygame.display.set_caption("AI Chess Game")

    # Instância do SaveManager para ser usada no menu
    save_manager_instance = SaveManager()

    # Inicia o loop principal do menu de modos de jogo
    # Passamos a superfície 'screen' e a instância de 'save_manager_instance'
    # para a classe GameModes, que agora gerenciará o menu principal.
    game_modes.GameModes(screen, save_manager_instance) # CORRIGIDO: Era game_modes.GameModes_windows

    # Encerra o Pygame apenas quando o programa principal finalizar completamente
    pygame.quit() 
    sys.exit() # Garante que o programa seja encerrado

if __name__ == "__main__":
    run_main()
