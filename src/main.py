# import pygame
# import sys
# import chess
# import json
# import os
# from src.ui.board_renderer import BoardRenderer
# from src.ui.asset_manager import AssetManager
# from src.ui.audio_manager import AudioManager
# from src.ia.easy_ai import EasyAI
# from src.ia.medium_ai import MediumAI
# from src.ia.stockfish_ai import StockfishAI
# from src.data.save_manager import SaveManager
# from src.core.chess_game import ChessGame
# import ctypes

# CONFIG_PATH = "config.json"
# BOARD_SIZE = 8
# MENU_HEIGHT = 80
# SQUARE_SIZE = 75  # Fixed square size for board (8 * 75 = 600)
# BOARD_WIDTH = SQUARE_SIZE * BOARD_SIZE
# BOARD_HEIGHT = BOARD_WIDTH + MENU_HEIGHT

# def load_config():
#     if os.path.exists(CONFIG_PATH):
#         with open(CONFIG_PATH, "r") as f:
#             return json.load(f)
#     return {"selected_ai": "stockfish", "skill_level": 8, "thinking_time": 1.5}

# def save_config(selected_ai, skill_level, thinking_time):
#     with open(CONFIG_PATH, "w") as f:
#         json.dump({
#             "selected_ai": selected_ai,
#             "skill_level": skill_level,
#             "thinking_time": thinking_time
#         }, f)

# def main(FEN, local):
#     pygame.init()
#     pygame.mixer.init()

#     info = pygame.display.Info()
#     screen_w, screen_h = info.current_w, info.current_h

#     # Create a resizable window the size of the screen
#     screen = pygame.display.set_mode((screen_w, screen_h - 10), pygame.RESIZABLE)
#     ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
#     pygame.display.set_caption("AI Chess Game")

#     font = pygame.font.SysFont(None, 24)
#     clock = pygame.time.Clock()

#     audio_manager = AudioManager()
#     asset_manager = AssetManager(square_size=SQUARE_SIZE)
#     board_renderer = BoardRenderer(screen, SQUARE_SIZE, FEN, local, asset_manager, audio_manager)
#     save_manager = SaveManager()
#     chess_game = ChessGame(FEN)

#     config = load_config()
#     selected_ai = config["selected_ai"]
#     skill_level = config["skill_level"]
#     thinking_time = config["thinking_time"]

#     ai = StockfishAI(skill_level=skill_level, thinking_time=thinking_time)
#     ai_thinking = False

#     def update_ai():
#         nonlocal ai
#         if selected_ai == "easy":
#             ai = EasyAI(depth=1)
#         elif selected_ai == "medium":
#             ai = MediumAI(depth=2)
#         elif selected_ai == "stockfish":
#             ai = StockfishAI(skill_level=skill_level, thinking_time=thinking_time)

#     def on_ai_move(best_move):
#         nonlocal ai_thinking
#         if best_move:
#             move_uci = best_move.uci()
#             board_renderer.from_chess_square(move_uci)
#             piece = board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai]
#             if piece and board_renderer.turn == True:
#                 ai_piece = piece
#                 board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai] = None
#             captured_piece = board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai]
#             board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai] = ai_piece
#             board_renderer.chess_game.make_move(move_uci)
#             board_renderer.turn = False
#             board_renderer.last_move = move_uci

#             if board_renderer.audio_manager:
#                 if captured_piece:
#                     board_renderer.audio_manager.play("capture")
#                 else:
#                     board_renderer.audio_manager.play("move")
#                 if board_renderer.chess_game.is_checkmate():
#                     board_renderer.audio_manager.play("checkmate")

#         ai_thinking = False

#     def draw_button(rect, text, selected=False):
#         pygame.draw.rect(screen, (100, 100, 100) if selected else (60, 60, 60), rect)
#         label = font.render(text, True, (255, 255, 255))
#         screen.blit(label, (rect.x + 10, rect.y + 8))

#     def draw_slider(x, y, label_text, value, min_val, max_val, step, width=150):
#         pygame.draw.rect(screen, (90, 90, 90), (x, y + 25, width, 6))
#         knob_x = x + int((value - min_val) / (max_val - min_val) * width)
#         pygame.draw.circle(screen, (200, 200, 200), (knob_x, y + 28), 8)
#         label = font.render(f"{label_text}: {value}", True, (255, 255, 255))
#         screen.blit(label, (x, y))
#         return pygame.Rect(x, y + 25, width, 16)

#     update_ai()
#     running = True

#     while running:
#         screen.fill((30, 30, 30))
#         window_width, window_height = screen.get_size()

#         # Centering X
#         board_x = (window_width - BOARD_WIDTH) // 2
#         board_y = (window_height - BOARD_HEIGHT) // 2

#         board_surface = pygame.Surface((BOARD_WIDTH, BOARD_WIDTH))
#         board_renderer.screen = board_surface
#         board_renderer.draw_board()
#         screen.blit(board_surface, (board_x, board_y))

#         # Draw menu
#         pygame.draw.rect(screen, (40, 40, 40), (board_x, board_y + BOARD_WIDTH, BOARD_WIDTH, MENU_HEIGHT))

#         # Button Positions
#         buttons = {
#             "easy": pygame.Rect(board_x + 10, board_y + BOARD_WIDTH + 10, 80, 30),
#             "medium": pygame.Rect(board_x + 100, board_y + BOARD_WIDTH + 10, 90, 30),
#             "stockfish": pygame.Rect(board_x + 200, board_y + BOARD_WIDTH + 10, 100, 30),
#         }

#         for ai_key, rect in buttons.items():
#             draw_button(rect, ai_key.capitalize(), selected_ai == ai_key)

#         # Sliders
#         skill_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 5, "Skill", skill_level, 0, 20, 1)
#         time_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 35, "Time", round(thinking_time, 1), 0.5, 5.0, 0.5)

#         # Save_Game button
#         button_width2 = 140 
#         button_height2 = 70

#         screen_width = screen.get_width()
#         screen_height = screen.get_height()

#         button_x2 = (screen_width) // 20
#         button_y2 = (screen_height) // 20

#         #colors
#         DARK_BLUE = (40, 100, 160)
#         BLUE = (70, 130, 180)
#         color = BLUE
#         button_rect2 = pygame.Rect(button_x2 , button_y2, button_width2, button_height2)
        
#         mouse_pos = pygame.mouse.get_pos()
#         if button_rect2.collidepoint(mouse_pos):
#             color = DARK_BLUE
#         else:
#             color = BLUE

#         pygame.draw.rect(screen, color, button_rect2, border_radius=12)
#         text_surface2 = font.render("Save Game", True, (255, 255, 255))
#         text_rect2 = text_surface2.get_rect(center=button_rect2.center)
#         screen.blit(text_surface2, text_rect2)

#         if board_renderer.turn and not ai_thinking:
#             ai_thinking = True
#             pygame.display.flip()
#             pygame.time.delay(1000)

#             if isinstance(ai, StockfishAI):
#                 ai.get_best_move(board_renderer.chess_game.board, callback=on_ai_move)
#             else:
#                 best_move = ai.get_best_move(board_renderer.chess_game.board)
#                 on_ai_move(best_move)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 save_config(selected_ai, skill_level, thinking_time)
#                 running = False

#             elif event.type == pygame.VIDEORESIZE:
#                 screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 for ai_key, rect in buttons.items():
#                     if rect.collidepoint(event.pos):
#                         selected_ai = ai_key
#                         update_ai()
#                 if skill_rect.collidepoint(event.pos):
#                     rel_x = max(0, min(skill_rect.width, event.pos[0] - skill_rect.x))
#                     skill_level = int((rel_x / skill_rect.width) * 20)
#                     update_ai()
#                 if time_rect.collidepoint(event.pos):
#                     rel_x = max(0, min(time_rect.width, event.pos[0] - time_rect.x))
#                     thinking_time = round((rel_x / time_rect.width) * 4.5 + 0.5, 1)
#                     update_ai()
#                 if board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
#                     board_renderer.handle_click((event.pos[0] - board_x, event.pos[1] - board_y))
#                     board_renderer.start_drag((event.pos[0] - board_x, event.pos[1] - board_y))

#                 if button_rect2.collidepoint(event.pos):
#                     save_manager.save_game(board_renderer.chess_game.board.fen())

#             elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 if board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
#                     board_renderer.end_drag((event.pos[0] - board_x, event.pos[1] - board_y))

#             elif event.type == pygame.MOUSEMOTION:
#                 board_renderer.update_mouse_pos((event.pos[0] - board_x, event.pos[1] - board_y))

        

#         pygame.display.flip()
#         clock.tick(60)

#     pygame.quit()
#     sys.exit()

# if __name__ == "__main__":
#     main()

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
import ctypes

# Import the GameModes class
from src.ui.game_modes import GameModes

CONFIG_PATH = "config.json"
BOARD_SIZE = 8
MENU_HEIGHT = 80
SQUARE_SIZE = 75  # Fixed square size for board (8 * 75 = 600)
BOARD_WIDTH = SQUARE_SIZE * BOARD_SIZE
BOARD_HEIGHT = BOARD_WIDTH + MENU_HEIGHT

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

def main(FEN, local):
    pygame.init()
    pygame.mixer.init()

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    # Create a resizable window the size of the screen
    screen = pygame.display.set_mode((screen_w, screen_h - 10), pygame.RESIZABLE)
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
    pygame.display.set_caption("AI Chess Game")

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    audio_manager = AudioManager()
    asset_manager = AssetManager(square_size=SQUARE_SIZE)
    board_renderer = BoardRenderer(screen, SQUARE_SIZE, FEN, local, asset_manager, audio_manager)
    save_manager = SaveManager()
    chess_game = ChessGame(FEN)

    config = load_config()
    selected_ai = config["selected_ai"]
    skill_level = config["skill_level"]
    thinking_time = config["thinking_time"]

    ai = StockfishAI(skill_level=skill_level, thinking_time=thinking_time)
    ai_thinking = False

    def update_ai():
        nonlocal ai
        if selected_ai == "easy":
            ai = EasyAI(depth=1)
        elif selected_ai == "medium":
            ai = MediumAI(depth=2)
        elif selected_ai == "stockfish":
            ai = StockfishAI(skill_level=skill_level, thinking_time=thinking_time)

    def on_ai_move(best_move):
        nonlocal ai_thinking
        if best_move:
            move_uci = best_move.uci()
            board_renderer.from_chess_square(move_uci)
            piece = board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai]
            if piece and board_renderer.turn == True:
                ai_piece = piece
                board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai] = None
            captured_piece = board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai]
            board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai] = ai_piece
            board_renderer.chess_game.make_move(move_uci)
            board_renderer.turn = False
            board_renderer.last_move = move_uci

            if board_renderer.audio_manager:
                if captured_piece:
                    board_renderer.audio_manager.play("capture")
                else:
                    board_renderer.audio_manager.play("move")
                if board_renderer.chess_game.is_checkmate():
                    board_renderer.audio_manager.play("checkmate")

        ai_thinking = False

    def draw_button(rect, text, selected=False):
        pygame.draw.rect(screen, (100, 100, 100) if selected else (60, 60, 60), rect)
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (rect.x + 10, rect.y + 8))

    def draw_slider(x, y, label_text, value, min_val, max_val, step, width=150):
        pygame.draw.rect(screen, (90, 90, 90), (x, y + 25, width, 6))
        knob_x = x + int((value - min_val) / (max_val - min_val) * width)
        pygame.draw.circle(screen, (200, 200, 200), (knob_x, y + 28), 8)
        label = font.render(f"{label_text}: {value}", True, (255, 255, 255))
        screen.blit(label, (x, y))
        return pygame.Rect(x, y + 25, width, 16)

    update_ai()
    running = True

    while running:
        screen.fill((30, 30, 30))
        window_width, window_height = screen.get_size()

        # Centering X
        board_x = (window_width - BOARD_WIDTH) // 2
        board_y = (window_height - BOARD_HEIGHT) // 2

        board_surface = pygame.Surface((BOARD_WIDTH, BOARD_WIDTH))
        board_renderer.screen = board_surface
        board_renderer.draw_board()
        screen.blit(board_surface, (board_x, board_y))

        # Draw menu
        pygame.draw.rect(screen, (40, 40, 40), (board_x, board_y + BOARD_WIDTH, BOARD_WIDTH, MENU_HEIGHT))

        # Button Positions
        buttons = {
            "easy": pygame.Rect(board_x + 10, board_y + BOARD_WIDTH + 10, 80, 30),
            "medium": pygame.Rect(board_x + 100, board_y + BOARD_WIDTH + 10, 90, 30),
            "stockfish": pygame.Rect(board_x + 200, board_y + BOARD_WIDTH + 10, 100, 30),
        }

        for ai_key, rect in buttons.items():
            draw_button(rect, ai_key.capitalize(), selected_ai == ai_key)

        # Sliders
        skill_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 5, "Skill", skill_level, 0, 20, 1)
        time_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 35, "Time", round(thinking_time, 1), 0.5, 5.0, 0.5)

        # Save_Game button
        button_width2 = 140
        button_height2 = 70

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        button_x2 = (screen_width) // 20
        button_y2 = (screen_height) // 20

        #colors
        DARK_BLUE = (40, 100, 160)
        BLUE = (70, 130, 180)
        color = BLUE
        button_rect2 = pygame.Rect(button_x2 , button_y2, button_width2, button_height2)

        mouse_pos = pygame.mouse.get_pos()
        if button_rect2.collidepoint(mouse_pos):
            color = DARK_BLUE
        else:
            color = BLUE

        pygame.draw.rect(screen, color, button_rect2, border_radius=12)
        text_surface2 = font.render("Save Game", True, (255, 255, 255))
        text_rect2 = text_surface2.get_rect(center=button_rect2.center)
        screen.blit(text_surface2, text_rect2)

        if board_renderer.turn and not ai_thinking:
            ai_thinking = True
            pygame.display.flip()
            pygame.time.delay(1000)

            if isinstance(ai, StockfishAI):
                ai.get_best_move(board_renderer.chess_game.board, callback=on_ai_move)
            else:
                best_move = ai.get_best_move(board_renderer.chess_game.board)
                on_ai_move(best_move)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_config(selected_ai, skill_level, thinking_time)
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for ai_key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        selected_ai = ai_key
                        update_ai()
                if skill_rect.collidepoint(event.pos):
                    rel_x = max(0, min(skill_rect.width, event.pos[0] - skill_rect.x))
                    skill_level = int((rel_x / skill_rect.width) * 20)
                    update_ai()
                if time_rect.collidepoint(event.pos):
                    rel_x = max(0, min(time_rect.width, event.pos[0] - time_rect.x))
                    thinking_time = round((rel_x / time_rect.width) * 4.5 + 0.5, 1)
                    update_ai()
                if board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
                    board_renderer.handle_click((event.pos[0] - board_x, event.pos[1] - board_y))
                    board_renderer.start_drag((event.pos[0] - board_x, event.pos[1] - board_y))

                if button_rect2.collidepoint(event.pos):
                    save_manager.save_game(board_renderer.chess_game.board.fen())

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
                    board_renderer.end_drag((event.pos[0] - board_x, event.pos[1] - board_y))

            elif event.type == pygame.MOUSEMOTION:
                board_renderer.update_mouse_pos((event.pos[0] - board_x, event.pos[1] - board_y))


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def run_main():
    # Create an instance of GameModes
    game_modes_instance = GameModes()
    # Call the GameModes_windows method on the instance
    game_modes_instance.GameModes_windows()

if __name__ == "__main__":
    run_main()
